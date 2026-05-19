"""recommender.py 单元测试"""
from datetime import date

from recommender import (
    build_arxiv_query,
    diversify,
    final_score,
    keyword_match,
    parse_keyword,
    recommend,
    recency_boost,
    relevance_score,
    tokenize,
)


def _paper(pid, title, abstract="", authors="A", date_str="2026-05-17"):
    return {
        "id": pid,
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "date": date_str,
    }


class TestTokenize:
    def test_basic(self):
        assert tokenize("Chain of Thought") == ["chain", "of", "thought"]

    def test_hyphen_split(self):
        # 连字符规范化为空格，让 "chain-of-thought" 能匹配 "chain of thought"
        assert tokenize("self-supervised learning") == ["self", "supervised", "learning"]
        assert tokenize("Chain-of-Thought") == ["chain", "of", "thought"]

    def test_punctuation(self):
        assert tokenize("RAG: a survey!") == ["rag", "a", "survey"]


class TestParseKeyword:
    def test_single(self):
        assert parse_keyword("LLM") == [["llm"]]

    def test_multi_word_and(self):
        assert parse_keyword("chain of thought") == [["chain", "of", "thought"]]

    def test_hyphenated_keyword_splits(self):
        # 用户写 "chain-of-thought"，应等价于 "chain of thought"
        assert parse_keyword("chain-of-thought") == [["chain", "of", "thought"]]

    def test_comma_or(self):
        assert parse_keyword("LLM, RAG") == [["llm"], ["rag"]]

    def test_mixed(self):
        assert parse_keyword("chain of thought, PDDL planning") == [
            ["chain", "of", "thought"],
            ["pddl", "planning"],
        ]


class TestKeywordMatch:
    def test_phrase_in_title_high_score(self):
        p = _paper("a", "A Survey on Chain of Thought")
        s, m = keyword_match(p, "chain of thought")
        assert m
        assert s == 1.0

    def test_phrase_in_abstract(self):
        p = _paper("a", "Survey", "We study chain of thought prompting in LLMs.")
        s, m = keyword_match(p, "chain of thought")
        assert m
        assert s == 0.6

    def test_no_match(self):
        p = _paper("a", "Differential Equations", "Math paper")
        s, m = keyword_match(p, "chain of thought")
        assert not m
        assert s == 0.0

    def test_token_only_match_lower_than_phrase(self):
        # tokens 都出现但不连成短语
        p = _paper("a", "On the chain in physics, the thought of motion", "")
        s, m = keyword_match(p, "chain of thought")
        # "chain of thought" 短语在标题里没有；"chain" "of" "thought" 都出现 → 0.5
        assert m
        assert s == 0.5

    def test_or_takes_max(self):
        # 一个分支命中标题短语，另一个不命中 → 取最大
        p = _paper("a", "PDDL planning made easy", "")
        s, m = keyword_match(p, "chain of thought, PDDL planning")
        assert m
        assert s == 1.0

    def test_hyphenated_form_matches_phrase(self):
        # 真实 arXiv 标题写法："Chain-of-Thought"，关键词为 "chain of thought"
        p = _paper("a", "COTCAgent: Probabilistic Chain-of-Thought Completion")
        s, m = keyword_match(p, "chain of thought")
        assert m
        # 标题命中 phrase（连字符规范化后），高分
        assert s >= 0.6

    def test_word_boundary(self):
        # "rag" 不应命中 "outrageous"
        p = _paper("a", "An outrageous claim about transformers", "")
        s, m = keyword_match(p, "rag")
        assert not m
        assert s == 0.0


class TestRelevanceScore:
    def test_single_keyword(self):
        p = _paper("a", "Chain of Thought Survey")
        score, matched = relevance_score(p, ["chain of thought"])
        assert score == 1.0
        assert matched == ["chain of thought"]

    def test_multi_keyword_boost(self):
        # 同篇论文命中两个关键词 → 总分 > 单关键词分
        p = _paper("a", "RAG with chain of thought reasoning", "")
        single_score, _ = relevance_score(p, ["chain of thought"])
        multi_score, matched = relevance_score(p, ["chain of thought", "rag"])
        assert multi_score > single_score
        assert set(matched) == {"chain of thought", "rag"}

    def test_no_match_returns_zero(self):
        p = _paper("a", "Quantum chromodynamics")
        score, matched = relevance_score(p, ["LLM", "RAG"])
        assert score == 0.0
        assert matched == []


class TestRecencyBoost:
    def test_today_is_one(self):
        today = date(2026, 5, 17)
        assert recency_boost("2026-05-17", today=today) == 1.0

    def test_half_life(self):
        today = date(2026, 5, 17)
        v = recency_boost("2026-05-03", today=today, half_life_days=14.0)
        assert 0.49 < v < 0.51

    def test_invalid_date(self):
        assert recency_boost("not-a-date") == 0.5

    def test_empty(self):
        assert recency_boost("") == 0.5


class TestFinalScore:
    def test_irrelevant_paper_zero(self):
        p = _paper("a", "Quantum gravity", "Physics paper")
        s, m = final_score(p, ["LLM"])
        assert s == 0.0
        assert m == []

    def test_recent_better_than_old(self):
        today = date(2026, 5, 17)
        recent = _paper("a", "LLM survey", date_str="2026-05-17")
        old = _paper("b", "LLM survey", date_str="2026-01-01")
        s_r, _ = final_score(recent, ["LLM"], today=today)
        s_o, _ = final_score(old, ["LLM"], today=today)
        assert s_r > s_o


class TestDiversify:
    def test_caps_per_first_author(self):
        papers = [
            {"id": "1", "authors": "Yann LeCun, X", "score": 0.9},
            {"id": "2", "authors": "Yann LeCun, Y", "score": 0.8},
            {"id": "3", "authors": "Yann LeCun, Z", "score": 0.7},
            {"id": "4", "authors": "Geoffrey Hinton", "score": 0.6},
        ]
        out = diversify(papers, max_per_first_author=2)
        ids = [p["id"] for p in out]
        assert ids == ["1", "2", "4"]

    def test_handles_empty_authors(self):
        papers = [
            {"id": "1", "authors": "", "score": 0.9},
            {"id": "2", "authors": "", "score": 0.8},
            {"id": "3", "authors": "", "score": 0.7},
        ]
        out = diversify(papers, max_per_first_author=2)
        assert len(out) == 2


class TestRecommend:
    def test_ranks_relevant_first(self):
        today = date(2026, 5, 17)
        candidates = [
            _paper("a", "Quantum gravity"),  # 不相关
            _paper("b", "RAG paper", "abstract about retrieval augmented generation"),  # 摘要弱命中
            _paper("c", "Chain of Thought Survey"),  # 标题强命中
        ]
        out = recommend(candidates, ["chain of thought", "rag"], top_k=10, today=today)
        ids = [p["id"] for p in out]
        # 不相关被过滤；c 标题强命中应排第一
        assert "a" not in ids
        assert ids[0] == "c"
        # b 弱命中应在
        assert "b" in ids

    def test_dedup_by_id(self):
        today = date(2026, 5, 17)
        p1 = _paper("dup", "LLM survey")
        p2 = _paper("dup", "LLM survey")  # 同 id
        out = recommend([p1, p2], ["LLM"], today=today)
        assert len(out) == 1

    def test_top_k_limit(self):
        today = date(2026, 5, 17)
        # 5 篇相关，top_k=3 → 只返回 3 篇
        cands = [_paper(f"p{i}", "LLM paper", authors=f"Author {i}") for i in range(5)]
        out = recommend(cands, ["LLM"], top_k=3, today=today)
        assert len(out) == 3

    def test_score_and_matched_fields(self):
        today = date(2026, 5, 17)
        p = _paper("a", "Chain of Thought Survey")
        out = recommend([p], ["chain of thought"], today=today)
        assert len(out) == 1
        assert "score" in out[0]
        assert out[0]["score"] > 0
        assert out[0]["matched_keywords"] == ["chain of thought"]

    def test_author_diversification(self):
        today = date(2026, 5, 17)
        cands = [
            _paper("a", "LLM A", authors="Alice"),
            _paper("b", "LLM B", authors="Alice"),
            _paper("c", "LLM C", authors="Alice"),
            _paper("d", "LLM D", authors="Bob"),
        ]
        out = recommend(cands, ["LLM"], top_k=10, max_per_first_author=2, today=today)
        ids = {p["id"] for p in out}
        # Alice 最多 2 篇
        alice = [p for p in out if p["authors"] == "Alice"]
        assert len(alice) == 2
        assert "d" in ids

    def test_empty_keywords(self):
        cands = [_paper("a", "LLM")]
        assert recommend(cands, []) == []

    def test_irrelevant_papers_filtered(self):
        today = date(2026, 5, 17)
        cands = [
            _paper("rel", "LLM Reasoning Survey"),
            _paper("irr", "Quantum field theory in physics"),
        ]
        out = recommend(cands, ["LLM"], today=today)
        assert len(out) == 1
        assert out[0]["id"] == "rel"


class TestBuildArxivQuery:
    def test_single_word(self):
        assert build_arxiv_query("LLM") == "all:LLM"

    def test_multi_word_phrase(self):
        assert build_arxiv_query("chain of thought") == \
            '(ti:"chain of thought" OR abs:"chain of thought")'

    def test_comma_or(self):
        q = build_arxiv_query("chain of thought, PDDL planning")
        assert "chain of thought" in q
        assert "PDDL planning" in q
        assert " OR " in q

    def test_mixed(self):
        q = build_arxiv_query("LLM, chain of thought")
        assert "all:LLM" in q
        assert 'ti:"chain of thought"' in q
