from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .util import strip_html


_TIME_RE = re.compile(
    r"^(?P<sh>\d{2}):(?P<sm>\d{2}):(?P<ss>\d{2}),(?P<sms>\d{3})\s*-->\s*"
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2}),(?P<ems>\d{3})\s*$"
)


@dataclass(frozen=True)
class Cue:
    start_ms: int
    end_ms: int
    lines: list[str]


def _time_to_ms(h: str, m: str, s: str, ms: str) -> int:
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)


def parse_srt(srt_text: str) -> list[Cue]:
    # Normalize newlines and split into blocks
    text = srt_text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = [b for b in text.split("\n\n") if b.strip()]

    cues: list[Cue] = []
    for block in blocks:
        lines = [ln.strip("\ufeff").rstrip() for ln in block.split("\n") if ln.strip()]
        if len(lines) < 2:
            continue

        # Possible formats:
        # 1) index, time, text...
        # 2) time, text...
        time_line = lines[1] if lines[0].isdigit() else lines[0]
        m = _TIME_RE.match(time_line)
        if not m:
            continue

        start_ms = _time_to_ms(m["sh"], m["sm"], m["ss"], m["sms"])
        end_ms = _time_to_ms(m["eh"], m["em"], m["es"], m["ems"])
        if end_ms <= start_ms:
            continue

        text_lines = lines[2:] if lines[0].isdigit() else lines[1:]
        cleaned: list[str] = []
        for t in text_lines:
            t = strip_html(t)
            t = t.replace("\u200e", "").replace("\u200f", "")
            t = t.strip()
            if t:
                cleaned.append(t)

        if cleaned:
            cues.append(Cue(start_ms=start_ms, end_ms=end_ms, lines=cleaned))

    cues.sort(key=lambda c: (c.start_ms, c.end_ms))
    return cues


def iter_dialogue_lines(cues: Iterable[Cue]) -> list[str]:
    out: list[str] = []
    for cue in cues:
        out.extend(cue.lines)
    return out
