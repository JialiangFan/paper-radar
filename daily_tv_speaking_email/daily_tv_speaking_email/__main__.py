from __future__ import annotations

import argparse
import os
import random
from pathlib import Path

from .config import apply_env_overrides, load_config
from .email_builder import build_email
from .opensubtitles_client import OpenSubtitlesClient
from .srt_parser import parse_srt
from .snippet_selector import Snippet, find_candidate_snippets, pick_snippet
from .state_store import StateStore
from .util import sha256_text, utc_now


def _maybe_load_dotenv(debug: bool, config_path: str | None = None) -> None:
    try:
        from dotenv import load_dotenv  # type: ignore

        # 1) Current working directory
        load_dotenv(override=False)

        # 2) Optional explicit env file
        explicit = os.getenv("DTVSE_ENV_FILE")
        if explicit:
            load_dotenv(dotenv_path=explicit, override=False)

        # 3) Nearby to config: config dir and one parent up
        if config_path:
            cfg_p = Path(config_path).expanduser().resolve()
            for candidate in [cfg_p.parent / ".env", cfg_p.parent.parent / ".env"]:
                if candidate.exists():
                    load_dotenv(dotenv_path=candidate, override=False)

        if debug:
            print("[debug] Loaded .env files (if present)")
    except Exception:
        return


def _require(cfg: dict, path: str):
    cur = cfg
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise ValueError(f"Missing required config field: {path}")
        cur = cur[part]
    return cur


def _choose_show(cfg: dict, state: StateStore, debug: bool) -> tuple[dict, int]:
    shows = cfg.get("shows")
    if not isinstance(shows, list) or not shows:
        raise ValueError("Config must include non-empty 'shows' list")

    selection = (cfg.get("show_selection") or os.getenv("DTVSE_SHOW_SELECTION") or "round_robin").strip().lower()
    if selection == "random":
        idx = random.randrange(0, len(shows))
    else:
        idx = state.next_show_index(len(shows))

    show = shows[idx]
    if debug:
        print(f"[debug] show_selection={selection}, index={idx}")
    return show, idx


def run_once(config_path: str, dry_run: bool, debug: bool) -> int:
    _maybe_load_dotenv(debug, config_path=config_path)

    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)

    snippet_duration = int(cfg.get("snippet_duration_sec", 45))
    if not (30 <= snippet_duration <= 60):
        raise ValueError("snippet_duration_sec must be between 30 and 60")

    language = (cfg.get("language") or "en").lower()

    # State location
    state_path = cfg.get("state_path")
    if state_path:
        sp = Path(str(state_path)).expanduser().resolve()
    else:
        sp = (cfg_obj.path.parent / "state.json").resolve()

    state = StateStore.load(sp)
    now = utc_now()
    state.prune(keep_days=30, now=now)

    show, _idx = _choose_show(cfg, state, debug)

    title = show.get("title")
    season = int(show.get("season"))
    episode = int(show.get("episode"))
    if not title:
        raise ValueError("Show missing title")

    api_key = os.getenv("OS_API_KEY")
    if not api_key:
        raise ValueError("Missing OS_API_KEY environment variable")

    os_user = os.getenv("OS_USERNAME")
    os_pass = os.getenv("OS_PASSWORD")

    client = OpenSubtitlesClient(api_key=api_key, username=os_user, password=os_pass, debug=debug)

    if debug:
        print(f"[debug] Fetching subtitles for: {title} S{season:02}E{episode:02} lang={language}")

    srt_text, choice = client.fetch_best_srt(title=title, season=season, episode=episode, language=language)

    cues = parse_srt(srt_text)
    if debug:
        print(f"[debug] Parsed cues: {len(cues)} (file_id={choice.file_id}, score={choice.score:.2f})")

    candidates = find_candidate_snippets(cues, duration_sec=snippet_duration)
    if debug:
        print(f"[debug] Candidate snippets: {len(candidates)}")

    target_read_minutes = int(cfg.get("target_read_minutes", 10))
    if target_read_minutes < 3:
        target_read_minutes = 3
    if target_read_minutes > 30:
        target_read_minutes = 30

    target_chars = target_read_minutes * 900

    def overlaps(a: Snippet, b: Snippet, pad_ms: int = 2000) -> bool:
        return not (
            (a.time_range.end_ms + pad_ms) <= b.time_range.start_ms
            or (b.time_range.end_ms + pad_ms) <= a.time_range.start_ms
        )

    # Build a dialogue pack: multiple distinct snippets until we reach target_chars.
    rng = random.Random()
    picked: list[Snippet] = []
    picked_hashes: list[str] = []
    seen_hashes: set[str] = set()

    # Prefer better-scoring candidates but randomize to avoid always picking the same.
    pool = candidates[:]
    max_snippets = min(60, max(10, len(pool)))

    for _ in range(max_snippets * 3):
        if len(picked) >= max_snippets:
            break
        sn = pick_snippet(pool, rng=rng, top_k=50)
        if not sn:
            break

        h = sha256_text(sn.text())
        if h in seen_hashes or state.seen_recently(h, keep_days=30, now=now):
            # Drop this candidate and continue.
            pool = [c for c in pool if sha256_text(c.text()) != h]
            continue

        if any(overlaps(sn, existing) for existing in picked):
            # Drop overlapping snippets to keep the pack spread out.
            pool = [c for c in pool if not overlaps(c, sn)]
            continue

        picked.append(sn)
        picked_hashes.append(h)
        seen_hashes.add(h)

        approx_chars = sum(len(s.text()) for s in picked)
        if approx_chars >= target_chars and len(picked) >= 3:
            break

    if not picked:
        raise RuntimeError("Could not find any new (non-recent) snippets that meet requirements")

    # Sort by time so the pack reads naturally.
    picked.sort(key=lambda s: (s.time_range.start_ms, s.time_range.end_ms))

    email = build_email(show_title=title, season=season, episode=episode, snippets=picked, target_read_minutes=target_read_minutes)

    if dry_run:
        print(f"Subject: {email.subject}\n")
        print(email.body)
    else:
        from_addr = _require(cfg, "email.from")
        to_addrs = _require(cfg, "email.to")
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]

        from .mailer import send_email

        # Mailgun-first behavior is controlled by USE_MAILGUN_API (paper_agent compatible).
        # If Mailgun is enabled and fails, it will fall back to SMTP.
        smtp_host = cfg.get("email", {}).get("smtp_host")
        smtp_port = cfg.get("email", {}).get("smtp_port")
        smtp_user = cfg.get("email", {}).get("smtp_user")
        smtp_password = cfg.get("email", {}).get("smtp_password")

        send_email(
            smtp_host=str(smtp_host) if smtp_host else None,
            smtp_port=int(smtp_port) if smtp_port is not None else None,
            smtp_user=str(smtp_user) if smtp_user else None,
            smtp_password=str(smtp_password) if smtp_password else None,
            from_addr=str(from_addr),
            to_addrs=[str(t) for t in to_addrs],
            subject=email.subject,
            body=email.body,
            debug=debug,  # verbose logs, no secrets
        )

        # Update state only after successful send
        for h in picked_hashes:
            state.add_snippet(
                h,
                now=now,
                meta={
                    "show": title,
                    "season": season,
                    "episode": episode,
                    "os_file_id": choice.file_id,
                },
            )
        state.save()

    # Persist show index advances and pruning even on dry-run
    if dry_run:
        state.save()

    return 0


def send_test_email(config_path: str, debug: bool) -> int:
    _maybe_load_dotenv(debug, config_path=config_path)

    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)

    from_addr = _require(cfg, "email.from")
    to_addrs = _require(cfg, "email.to")
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]

    smtp_host = cfg.get("email", {}).get("smtp_host")
    smtp_port = cfg.get("email", {}).get("smtp_port")
    smtp_user = cfg.get("email", {}).get("smtp_user")
    smtp_password = cfg.get("email", {}).get("smtp_password")

    subject = "daily_tv_speaking_email test"
    body = (
        "This is a test email from daily_tv_speaking_email.\n\n"
        "If you received this, Mailgun/SMTP configuration works.\n"
    )

    from .mailer import send_email

    send_email(
        smtp_host=str(smtp_host) if smtp_host else None,
        smtp_port=int(smtp_port) if smtp_port is not None else None,
        smtp_user=str(smtp_user) if smtp_user else None,
        smtp_password=str(smtp_password) if smtp_password else None,
        from_addr=str(from_addr),
        to_addrs=[str(t) for t in to_addrs],
        subject=subject,
        body=body,
        debug=debug,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="daily_tv_speaking_email")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Fetch subtitle snippet and send email")
    run_p.add_argument("--config", required=True, help="Path to config.yaml or config.json")
    run_p.add_argument("--dry-run", action="store_true", help="Print email to stdout, do not send")
    run_p.add_argument("--debug", action="store_true", help="Verbose logs (no secrets)")

    test_p = sub.add_parser("test-email", help="Send a simple test email (Mailgun-first, SMTP fallback)")
    test_p.add_argument("--config", required=True, help="Path to config.yaml or config.json")
    test_p.add_argument("--debug", action="store_true", help="Verbose logs (no secrets)")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        return run_once(args.config, dry_run=bool(args.dry_run), debug=bool(args.debug))
    if args.cmd == "test-email":
        return send_test_email(args.config, debug=bool(args.debug))

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
