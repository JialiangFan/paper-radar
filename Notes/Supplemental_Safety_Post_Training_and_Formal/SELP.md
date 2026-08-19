---
imported_title: "SELP: Safe and Efficient Task Plans for Robot Agents with LLMs"
imported_from: "/Users/jfan/ND/看论文/robotics-safety-post-training/papers/SELP.md"
imported_reason: "Task-plan safety through formal constraints and LLM planning."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# SELP: Generating Safe and Efficient Task Plans for Robot Agents with LLMs

- **Authors**: Yi Wu, Zikang Xiong, Yiran Hu, Shreyas Iyengar, Nan Jiang, Aniket Bera, Lin Tan, Suresh Jagannathan
- **Year/Venue**: 2025 / ICRA 2025 (Best Paper Award Finalist)
- **ArXiv**: [2409.19471](https://arxiv.org/abs/2409.19471)
- **Affiliation**: Purdue University
- **GitHub**: [lt-asset/selp](https://github.com/lt-asset/selp)
- **Tags**: #LTL #formal-verification #constrained-decoding #planning #fine-tuning

## Problem
LLM planners 无法保证生成的计划满足安全的时序约束（如 "先关火再离开厨房"）。

## Method: Three Techniques
1. **Equivalence Voting**: 采样多个 LTL 公式，选择语义等价最多的（majority voting 的形式化版本）
2. **LTL Constrained Decoding**: 将 LTL 公式转为 automaton，在 LLM 自回归生成时强制满足 automaton 约束（只允许符合 LTL 的 token 序列）
3. **Domain-Specific Fine-Tuning**: 在特定领域数据上微调 LLM

## Formal Guarantee?
**YES — LTL 提供严格形式化保证**。Constrained decoding 确保生成的 plan 100% 满足 LTL 规约（当 LTL 公式正确时）。

## Key Results
- Drone: Safety ↑10.8%, Efficiency ↑19.8%
- Manipulation: Safety ↑20.4%
- **ICRA 2025 Best Paper Award Finalist**

## Relevance
**与 SafeGen-LLM 最相似的方法**，但用 LTL 而非 PDDL3。LTL constrained decoding 是一种优雅的形式化安全集成方式——在生成时就保证安全，而非生成后验证。

## Limitation & Opportunity
- 只在 plan-level（和 SafeGen-LLM 一样）
- LTL 公式需要人工定义或 LLM 翻译（可能出错）
- **机会**: 将 LTL constrained decoding 扩展到 action-level（VLA 输出约束）

## Related Papers
- [[robotics-safety-post-training/papers/SafeGen-LLM|SafeGen-LLM]] — 类似思路，PDDL3 + GRPO
- [[robotics-safety-post-training/papers/STL-Decision-Transformer|STL-DT]] — 类似思路，STL + offline RL（control-level）
- [[robotics-safety-post-training/papers/Formal-Methods-Robot-Survey|Formal Methods Survey]] — 全面综述
