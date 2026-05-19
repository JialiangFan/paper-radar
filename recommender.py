"""
论文推荐打分与重排序模块。

设计目标：
- 跨关键词去重 + 联合打分（命中多个关键词的论文得分更高）
- 标题命中权重大于摘要命中
- 短语匹配 > 词级匹配
- 新近度作为辅助因子（候选池已按日期过滤，这里只做微调）
- 作者多样性：同一第一作者最多 N 篇

不依赖外部服务，纯计算。
"""
from __future__ import annotations

import math
import re
from datetime import datetime, date
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def normalize(text: str) -> str:
    """小写化并把连字符当作空格 — 这样 "chain-of-thought" 能匹配 "chain of thought"。"""
    return (text or "").lower().replace("-", " ")


def tokenize(text: str) -> List[str]:
    """小写化、按非字母数字切分。连字符被视为空格（"self-supervised" → ["self", "supervised"]）。"""
    return [t for t in _TOKEN_RE.findall(normalize(text)) if t]


def parse_keyword(keyword: str) -> List[List[str]]:
    """将关键词解析为 OR 组的列表，每组内部是 AND 的 token 序列。

    "chain-of-thought, PDDL planning" → [["chain-of-thought"], ["pddl", "planning"]]
    "LLM reasoning"                  → [["llm", "reasoning"]]
    "RAG"                            → [["rag"]]
    """
    groups: List[List[str]] = []
    parts = [p.strip() for p in keyword.split(",") if p.strip()] or [keyword.strip()]
    for part in parts:
        tokens = tokenize(part)
        if tokens:
            groups.append(tokens)
    return groups


def _phrase_in(text: str, phrase: str) -> bool:
    """对 phrase 做边界感知的子串匹配。连字符被规范化为空格，所以 "chain-of-thought"
    会被当作 "chain of thought" 匹配。"""
    if not phrase:
        return False
    pattern = r"\b" + re.escape(normalize(phrase)) + r"\b"
    return re.search(pattern, normalize(text)) is not None


def _all_tokens_in(text: str, tokens: Sequence[str]) -> bool:
    text_tokens = set(tokenize(text))
    return all(t in text_tokens for t in tokens)


def keyword_match(paper: Dict, keyword: str) -> Tuple[float, bool]:
    """计算单个关键词在某篇论文上的命中分数。

    返回 (score, matched)。score 0-1.5 区间：
      - 标题短语命中：1.0
      - 摘要短语命中：0.6
      - 标题全 token 命中（非短语）：0.5
      - 摘要全 token 命中（非短语）：0.25
    多组（OR）取最大分。

    matched 表示是否命中（用于 matched_keywords 标记）。
    """
    title = paper.get("title", "") or ""
    abstract = paper.get("abstract", "") or ""
    groups = parse_keyword(keyword)
    if not groups:
        return 0.0, False

    best = 0.0
    matched = False
    for tokens in groups:
        if len(tokens) > 1:
            phrase = " ".join(tokens)
            if _phrase_in(title, phrase):
                best = max(best, 1.0)
                matched = True
                continue
            if _phrase_in(abstract, phrase):
                best = max(best, 0.6)
                matched = True
                continue
        if _all_tokens_in(title, tokens):
            best = max(best, 0.5)
            matched = True
        elif _all_tokens_in(abstract, tokens):
            best = max(best, 0.25)
            matched = True
    return best, matched


def relevance_score(paper: Dict, keywords: Sequence[str]) -> Tuple[float, List[str]]:
    """聚合多个用户关键词的命中分。

    多命中加权：第 2 个命中再加 50%，第 3 个再加 30%，依次递减。
    返回 (score, matched_keyword_list)。
    """
    per_keyword: List[Tuple[float, str]] = []
    for kw in keywords:
        s, m = keyword_match(paper, kw)
        if m and s > 0:
            per_keyword.append((s, kw))

    if not per_keyword:
        return 0.0, []

    per_keyword.sort(reverse=True)
    # 多命中加权因子
    weights = [1.0, 0.5, 0.3, 0.2, 0.15]
    total = 0.0
    for i, (s, _) in enumerate(per_keyword):
        w = weights[i] if i < len(weights) else 0.1
        total += s * w
    matched = [kw for _, kw in per_keyword]
    return total, matched


def recency_boost(date_str: str, today: Optional[date] = None, half_life_days: float = 14.0) -> float:
    """指数衰减的新近度系数，范围 (0, 1]。
    14 天半衰期：今天=1，14 天前≈0.5，30 天前≈0.23。
    日期解析失败返回 0.5（保守中性）。
    """
    if not date_str:
        return 0.5
    today = today or datetime.now().date()
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return 0.5
    age_days = max(0, (today - d).days)
    return math.exp(-math.log(2) * age_days / half_life_days)


def final_score(
    paper: Dict,
    keywords: Sequence[str],
    today: Optional[date] = None,
    recency_weight: float = 0.3,
) -> Tuple[float, List[str]]:
    """最终打分 = 相关性 * (1 - w) + 新近度 * w * 相关性。

    新近度只对已经相关的论文做调节（相关性=0 时直接 0），避免"很新但完全不相关"被推上来。
    """
    rel, matched = relevance_score(paper, keywords)
    if rel <= 0:
        return 0.0, []
    rec = recency_boost(paper.get("date", ""), today=today)
    score = rel * ((1 - recency_weight) + recency_weight * rec)
    return score, matched


def _first_author_key(authors: str) -> str:
    if not authors:
        return ""
    return authors.split(",")[0].strip().lower()


def diversify(
    scored_papers: List[Dict],
    max_per_first_author: int = 2,
) -> List[Dict]:
    """同一第一作者最多保留 N 篇，按已有顺序处理。
    scored_papers 应当已按分数降序排好；返回过滤后的子集，保持原顺序。
    """
    author_counts: Dict[str, int] = {}
    out: List[Dict] = []
    for p in scored_papers:
        key = _first_author_key(p.get("authors", ""))
        if author_counts.get(key, 0) >= max_per_first_author:
            continue
        author_counts[key] = author_counts.get(key, 0) + 1
        out.append(p)
    return out


def recommend(
    candidates: Iterable[Dict],
    keywords: Sequence[str],
    top_k: int = 10,
    max_per_first_author: int = 2,
    today: Optional[date] = None,
    recency_weight: float = 0.3,
    min_score: float = 0.0,
) -> List[Dict]:
    """端到端：去重 → 打分 → 排序 → 作者去多 → 取 Top-K。

    每篇返回的 dict 会带上 `score`（float）和 `matched_keywords`（list[str]）字段。
    """
    keywords = [k for k in keywords if k and k.strip()]
    if not keywords:
        return []

    # 去重：以 id 为准
    seen: Dict[str, Dict] = {}
    for p in candidates:
        pid = p.get("id")
        if pid and pid not in seen:
            seen[pid] = p

    scored: List[Dict] = []
    for paper in seen.values():
        score, matched = final_score(paper, keywords, today=today, recency_weight=recency_weight)
        if score <= min_score or not matched:
            continue
        enriched = dict(paper)
        enriched["score"] = round(score, 4)
        enriched["matched_keywords"] = matched
        scored.append(enriched)

    scored.sort(key=lambda p: p["score"], reverse=True)
    scored = diversify(scored, max_per_first_author=max_per_first_author)
    return scored[:top_k]


def build_arxiv_query(keyword: str) -> str:
    """构造 arXiv API 查询字符串，优先用短语匹配以提升相关性。

    - "chain of thought"      → ti:"chain of thought" OR abs:"chain of thought"
    - "LLM"                   → all:LLM
    - "a phrase, single"      → (ti:"a phrase" OR abs:"a phrase") OR (all:single)
    """
    parts = [p.strip() for p in keyword.split(",") if p.strip()] or [keyword.strip()]
    or_clauses: List[str] = []
    for part in parts:
        tokens = part.split()
        if len(tokens) > 1:
            phrase = " ".join(tokens)
            or_clauses.append(f'(ti:"{phrase}" OR abs:"{phrase}")')
        elif tokens:
            or_clauses.append(f"all:{tokens[0]}")
    if not or_clauses:
        return keyword.strip()
    if len(or_clauses) == 1:
        return or_clauses[0]
    return "(" + " OR ".join(or_clauses) + ")"
