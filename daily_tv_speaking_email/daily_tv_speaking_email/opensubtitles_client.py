from __future__ import annotations

import gzip
import io
import time
import zipfile
from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_BASE_URL = "https://api.opensubtitles.com/api/v1"


@dataclass(frozen=True)
class SubtitleChoice:
    file_id: int
    file_name: str | None
    score: float
    meta: dict[str, Any]


class OpenSubtitlesClient:
    def __init__(
        self,
        *,
        api_key: str,
        username: str | None = None,
        password: str | None = None,
        user_agent: str = "daily_tv_speaking_email/0.1",
        base_url: str = DEFAULT_BASE_URL,
        debug: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.username = username
        self.password = password
        self.debug = debug

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Api-Key": self.api_key,
                "User-Agent": user_agent,
                "Accept": "application/json",
            }
        )
        self._token: str | None = None

    def _log(self, msg: str) -> None:
        if self.debug:
            print(f"[opensubtitles] {msg}")

    def login_if_possible(self) -> None:
        if self._token:
            return
        if not (self.username and self.password):
            self._log("No username/password set; continuing without login token.")
            return

        payload = {"username": self.username, "password": self.password}
        data = self._request("POST", "/login", json=payload)
        token = (data or {}).get("token")
        if token:
            self._token = token
            self.session.headers["Authorization"] = f"Bearer {token}"
            self._log("Login succeeded; token stored.")
        else:
            self._log("Login response did not include token; continuing without token.")

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        max_attempts = 6
        backoff = 1.0
        for attempt in range(1, max_attempts + 1):
            try:
                resp = self.session.request(method, url, timeout=30, **kwargs)
            except requests.RequestException as e:
                if attempt == max_attempts:
                    raise
                self._log(f"Network error: {e}; retrying in {backoff:.1f}s")
                time.sleep(backoff)
                backoff = min(backoff * 2, 30)
                continue

            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                wait = backoff
                if retry_after:
                    try:
                        wait = max(wait, float(retry_after))
                    except ValueError:
                        pass
                self._log(f"HTTP 429 rate-limited; waiting {wait:.1f}s (attempt {attempt}/{max_attempts})")
                time.sleep(wait)
                backoff = min(backoff * 2, 60)
                continue

            if 500 <= resp.status_code <= 599:
                if attempt == max_attempts:
                    resp.raise_for_status()
                self._log(f"HTTP {resp.status_code}; retrying in {backoff:.1f}s")
                time.sleep(backoff)
                backoff = min(backoff * 2, 30)
                continue

            if resp.status_code >= 400:
                # Provide helpful context
                try:
                    j = resp.json()
                except Exception:
                    j = {"text": resp.text[:500]}
                raise requests.HTTPError(f"OpenSubtitles API error {resp.status_code}: {j}")

            if resp.content:
                return resp.json()
            return {}

        return {}

    def search_subtitles(self, *, title: str, season: int, episode: int, language: str = "en") -> list[dict[str, Any]]:
        self.login_if_possible()
        params = {
            "query": title,
            "season_number": season,
            "episode_number": episode,
            "languages": language,
        }
        data = self._request("GET", "/subtitles", params=params)
        items = data.get("data") or []
        if not isinstance(items, list):
            return []
        return items

    def choose_best(self, items: list[dict[str, Any]], *, season: int, episode: int, language: str = "en") -> SubtitleChoice | None:
        choices: list[SubtitleChoice] = []

        for it in items:
            attr = (it or {}).get("attributes") or {}

            lang = (attr.get("language") or attr.get("language_code") or "").lower()
            if lang and lang != language.lower():
                continue

            # Find file_id
            files = attr.get("files") or []
            file_id = None
            file_name = None
            if isinstance(files, list) and files:
                f0 = files[0] or {}
                file_id = f0.get("file_id") or f0.get("fileId")
                file_name = f0.get("file_name") or f0.get("fileName")
            if file_id is None:
                continue

            # Metadata-based scoring
            dl = attr.get("download_count") or 0
            rating = attr.get("ratings") or attr.get("rating") or 0
            try:
                dl = float(dl)
            except Exception:
                dl = 0.0
            try:
                rating = float(rating)
            except Exception:
                rating = 0.0

            # Prefer exact season/episode if feature_details exists
            feat = attr.get("feature_details") or attr.get("featureDetails") or {}
            s_ok = True
            e_ok = True
            try:
                s_ok = int(feat.get("season_number", season)) == int(season)
            except Exception:
                s_ok = True
            try:
                e_ok = int(feat.get("episode_number", episode)) == int(episode)
            except Exception:
                e_ok = True

            exact = 1.0 if (s_ok and e_ok) else 0.0

            # Prefer not machine/AI translated (if metadata exists)
            ai = attr.get("ai_translated")
            mt = attr.get("machine_translated")
            translated_penalty = 0.0
            if ai is True or mt is True:
                translated_penalty = 2.0

            score = exact * 10.0 + (rating * 2.0) + (dl / 1000.0) - translated_penalty

            choices.append(
                SubtitleChoice(
                    file_id=int(file_id),
                    file_name=file_name,
                    score=score,
                    meta={
                        "download_count": dl,
                        "rating": rating,
                        "ai_translated": ai,
                        "machine_translated": mt,
                        "feature_details": feat,
                    },
                )
            )

        if not choices:
            return None

        choices.sort(key=lambda c: c.score, reverse=True)
        return choices[0]

    def download_srt_text(self, *, file_id: int) -> str:
        self.login_if_possible()

        payload = {"file_id": int(file_id)}
        data = self._request("POST", "/download", json=payload)
        link = data.get("link")
        if not link:
            raise RuntimeError(f"Download response missing link: {data}")

        # The link is a direct download URL
        r = self.session.get(link, timeout=60)
        r.raise_for_status()

        # Usually plain SRT text, but sometimes ZIP/GZIP.
        content_type = (r.headers.get("Content-Type") or "").lower()
        raw = r.content

        # ZIP
        if raw[:2] == b"PK" or "zip" in content_type:
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                # Prefer .srt files; otherwise take the first file.
                names = [n for n in zf.namelist() if not n.endswith("/")]
                srt_names = [n for n in names if n.lower().endswith(".srt")]
                pick = (srt_names[0] if srt_names else (names[0] if names else None))
                if not pick:
                    raise RuntimeError("ZIP download contained no files")
                data_bytes = zf.read(pick)
                return data_bytes.decode("utf-8", errors="replace")

        # GZIP
        if raw[:2] == b"\x1f\x8b" or "gzip" in content_type:
            try:
                data_bytes = gzip.decompress(raw)
            except Exception:
                # Some servers double-wrap; fall back to GzipFile
                with gzip.GzipFile(fileobj=io.BytesIO(raw)) as gf:
                    data_bytes = gf.read()
            return data_bytes.decode("utf-8", errors="replace")

        # Plain text
        try:
            return raw.decode(r.encoding or "utf-8", errors="replace")
        except Exception:
            return r.text

    def fetch_best_srt(self, *, title: str, season: int, episode: int, language: str = "en") -> tuple[str, SubtitleChoice]:
        items = self.search_subtitles(title=title, season=season, episode=episode, language=language)
        best = self.choose_best(items, season=season, episode=episode, language=language)
        if not best:
            raise RuntimeError("No suitable subtitles found")

        # If the top result is weird (e.g. empty), try a couple alternatives
        ordered = sorted(
            [c for c in [best] if c is not None],
            key=lambda c: c.score,
            reverse=True,
        )

        # Also consider next-best few from items
        # Re-score quickly and sample top few
        rescored: list[SubtitleChoice] = []
        for it in items:
            c = self.choose_best([it], season=season, episode=episode, language=language)
            if c:
                rescored.append(c)
        rescored.sort(key=lambda c: c.score, reverse=True)
        for c in rescored[:5]:
            if c.file_id != best.file_id:
                ordered.append(c)

        # Try in order
        last_err: Exception | None = None
        for c in ordered[:6]:
            try:
                text = self.download_srt_text(file_id=c.file_id)
                if text and len(text) > 100:
                    return text, c
            except Exception as e:
                last_err = e
                continue

        if last_err:
            raise last_err
        raise RuntimeError("Failed to download SRT")
