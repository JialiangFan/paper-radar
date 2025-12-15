from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Iterable

from .srt_parser import Cue
from .util import TimeRange


_STAGE_RE = re.compile(
    r"^\s*(\(|\[|\*)\s*(?:"  # opening
    r"laughs?|sighs?|gasps?|groans?|coughs?|clears throat|music|applause|"  # common
    r"phone (?:rings?|ringing)|door (?:opens?|closes?)|"  # foley
    r"inaudible|unintelligible|whispering|"  # misc
    r".+"  # catch-all within brackets
    r")\s*(\)|\]|\*)\s*$",
    re.IGNORECASE,
)

_PURE_BRACKET_RE = re.compile(r"^\s*(\([^)]*\)|\[[^]]*\]|\*[^*]*\*)\s*$")


@dataclass(frozen=True)
class Snippet:
    time_range: TimeRange
    lines: list[str]

    def text(self) -> str:
        return "\n".join(self.lines).strip()


def _is_stage_direction(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if _PURE_BRACKET_RE.match(s):
        return True
    if "♪" in s:
        return True
    if _STAGE_RE.match(s):
        return True
    # All-caps short foley like "MUSIC" or "APPLAUSE"
    if len(s) <= 24 and s.isupper() and any(ch.isalpha() for ch in s):
        return True
    return False


def _clean_lines(cues: Iterable[Cue]) -> list[str]:
    lines: list[str] = []
    for cue in cues:
        for ln in cue.lines:
            ln = ln.strip()
            if not ln:
                continue
            if _is_stage_direction(ln):
                continue
            # Collapse multiple spaces
            ln = re.sub(r"\s+", " ", ln)
            lines.append(ln)
    return lines


def find_candidate_snippets(
    cues: list[Cue],
    duration_sec: int,
    min_duration_sec: int = 30,
    max_duration_sec: int = 60,
    min_lines: int = 6,
    max_lines: int = 12,
) -> list[Snippet]:
    if not cues:
        return []

    target_ms = int(duration_sec) * 1000
    min_ms = int(min_duration_sec) * 1000
    max_ms = int(max_duration_sec) * 1000

    out: list[Snippet] = []

    n = len(cues)
    for i in range(n):
        start = cues[i].start_ms
        # Expand j until we exceed max
        for j in range(i, n):
            end = cues[j].end_ms
            span = end - start
            if span < min_ms:
                continue
            if span > max_ms:
                break

            window = cues[i : j + 1]
            lines = _clean_lines(window)
            if not (min_lines <= len(lines) <= max_lines):
                continue

            # Prefer windows near target duration
            score = abs(span - target_ms)
            out.append((score, Snippet(time_range=TimeRange(start, end), lines=lines)))

    out.sort(key=lambda t: t[0])
    return [sn for _, sn in out]


def pick_snippet(
    candidates: list[Snippet],
    rng: random.Random | None = None,
    top_k: int = 25,
) -> Snippet | None:
    if not candidates:
        return None
    if rng is None:
        rng = random.Random()

    # Randomize among the best-scoring windows to avoid always sending the same early snippet.
    pool = candidates[: max(1, min(top_k, len(candidates)))]
    return rng.choice(pool)
