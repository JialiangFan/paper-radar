from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Sequence

from .snippet_selector import Snippet
from .util import format_srt_time


_STOPWORDS = {
    "a","an","and","are","as","at","be","but","by","for","from","has","have","he","her","hers",
    "him","his","i","if","in","into","is","it","its","me","my","no","not","of","on","or","our",
    "ours","she","so","that","the","their","theirs","them","then","there","they","this","to","too","up",
    "us","was","we","were","what","when","where","who","why","with","you","your","yours","yeah","uh","um",
}

_COMMON_DEFS = {
    "gonna": "informal: going to",
    "wanna": "informal: want to",
    "kinda": "informal: kind of; somewhat",
    "gotta": "informal: have got to; must",
    "lemme": "informal: let me",
    "cuz": "informal: because",
    "okay": "used to agree or accept; all right",
    "alright": "all right; acceptable",
    "sorry": "used to apologize",
    "actually": "in fact; used to correct or emphasize",
    "maybe": "possibly",
    "probably": "very likely",
    "sure": "certain; also used to agree",
}


@dataclass(frozen=True)
class EmailContent:
    subject: str
    body: str


_WORD_RE = re.compile(r"[A-Za-z][A-Za-z']+")


def _estimate_chars_per_minute() -> int:
    # Rough proxy for spoken reading rate (English).
    # ~130–160 wpm; ~5 chars/word + spaces/punct => ~800–1000 chars/min.
    return 900


def _tokenize(lines: Iterable[str]) -> list[str]:
    tokens: list[str] = []
    for ln in lines:
        for w in _WORD_RE.findall(ln):
            w = w.lower().strip("'")
            if w:
                tokens.append(w)
    return tokens


def _select_vocab(lines: list[str], k: int = 5) -> list[str]:
    toks = _tokenize(lines)
    if not toks:
        return []

    counts: dict[str, int] = {}
    for t in toks:
        if t in _STOPWORDS:
            continue
        if len(t) < 4:
            continue
        counts[t] = counts.get(t, 0) + 1

    # bigrams (simple “phrases”)
    bigram_counts: dict[str, int] = {}
    for a, b in zip(toks, toks[1:]):
        if a in _STOPWORDS or b in _STOPWORDS:
            continue
        if len(a) < 3 or len(b) < 3:
            continue
        bg = f"{a} {b}"
        bigram_counts[bg] = bigram_counts.get(bg, 0) + 1

    candidates: list[tuple[float, str]] = []
    for w, c in counts.items():
        candidates.append((c * (1.0 + min(len(w), 10) / 10.0), w))
    for bg, c in bigram_counts.items():
        # slightly favor phrases if repeated
        candidates.append((c * 1.2, bg))

    candidates.sort(key=lambda t: (-t[0], t[1]))

    out: list[str] = []
    for _, item in candidates:
        if item in out:
            continue
        out.append(item)
        if len(out) >= k:
            break
    return out


def _define(term: str) -> str:
    if term in _COMMON_DEFS:
        return _COMMON_DEFS[term]
    if " " in term:
        return "a short phrase from the dialogue (focus on natural rhythm)"
    if term.endswith("n't"):
        return "a contraction meaning 'not' (e.g., don't/can't)"
    if term.endswith("'re"):
        return "a contraction meaning 'are'"
    if term.endswith("'ve"):
        return "a contraction meaning 'have'"
    if term.endswith("'ll"):
        return "a contraction meaning 'will'"
    if term.endswith("'d"):
        return "a contraction meaning 'would' or 'had'"
    if term.endswith("ing") and len(term) > 5:
        return "present-participle form; describes an ongoing action"
    if term.endswith("ed") and len(term) > 4:
        return "past-tense/past-participle form; describes a completed action"
    return "a key word from the dialogue; look up a dictionary definition after practice"


def build_email(
    *,
    show_title: str,
    season: int,
    episode: int,
    snippets: Sequence[Snippet],
    target_read_minutes: int = 10,
) -> EmailContent:
    subject = f"Daily 10-min Speaking Practice — {show_title} S{season:02}E{episode:02}"

    if not snippets:
        raise ValueError("snippets must be non-empty")

    # Dialogue pack
    pack_lines: list[str] = []
    for idx, sn in enumerate(snippets, start=1):
        start = format_srt_time(sn.time_range.start_ms)
        end = format_srt_time(sn.time_range.end_ms)
        pack_lines.append(f"[Snippet {idx}] ({start}–{end})")
        pack_lines.extend(f"- {ln}" for ln in sn.lines)
        pack_lines.append("")

    dialogue_pack = "\n".join(pack_lines).rstrip()

    # Estimate reading time by characters (dialogue only; routine excluded)
    dialogue_chars = sum(len(ln) for ln in dialogue_pack)
    est_min = max(1, int(round(dialogue_chars / float(_estimate_chars_per_minute()))))

    all_dialogue_lines: list[str] = []
    for sn in snippets:
        all_dialogue_lines.extend(sn.lines)

    vocab = _select_vocab(all_dialogue_lines, k=5)
    vocab_block = "\n".join(f"- {t}: {_define(t)}" for t in vocab) if vocab else "- (no vocabulary extracted)"

    body = (
        f"[Dialogue pack]\n"
        f"(Estimated by characters: ~{dialogue_chars} chars ≈ ~{est_min} min reading)\n"
        f"{dialogue_pack}\n\n"
        f"[10-min routine]\n"
        f"1) Warm-up (1 min): Read slowly once\n"
        f"2) Shadowing (3 min): Line-by-line repetition\n"
        f"3) Role-play (3 min): Act both roles\n"
        f"4) Retell (2 min): Summarize in your own words\n"
        f"5) Upgrade (1 min): Rewrite 2 lines more naturally\n\n"
        f"[Vocabulary]\n"
        f"{vocab_block}\n"
    )

    return EmailContent(subject=subject, body=body)
