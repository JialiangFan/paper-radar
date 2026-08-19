---
imported_title: "Temporal Logic Specification-Conditioned Decision Transformer"
imported_from: "/Users/jfan/ND/看论文/robotics-safety-post-training/papers/STL-Decision-Transformer.md"
imported_reason: "Relevant to training policies conditioned on formal safety specifications."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Temporal Logic Specification-Conditioned Decision Transformer for Offline Safe RL

- **Authors**: Multiple
- **Year/Venue**: 2024
- **ArXiv**: [2402.17217](https://arxiv.org/abs/2402.17217)
- **Tags**: #STL #temporal-logic #decision-transformer #offline-RL #formal-guarantee

## Problem
如何在 offline RL 中指定和满足复杂的时序安全约束（如 "在 t1 之前到达 A，且全程避开区域 B"）？

## Method
1. 用 **Signal Temporal Logic (STL)** 编码安全和任务约束
2. 将 STL specification 作为 conditioning signal 输入 Decision Transformer
3. Offline RL 训练：学习在给定 STL 规约下的最优策略
4. 支持不同 STL 公式的 zero-shot 泛化

## Formal Guarantee?
**YES — STL temporal logic** 提供严格的时序安全规约。模型被训练来满足这些规约。

## Key Results
- 显著优于 pure behavior cloning
- 支持 STL 公式的组合和泛化

## Relevance
**将 temporal logic 从 plan-level 带到 control-level 的关键工作**。SafeGen-LLM 和 SELP 在 plan-level 用 PDDL3/LTL，STL-DT 在 control-level 用 STL。这填补了 SafeGen-LLM 向下延伸的方法论空白。

## Limitation & Opportunity
- Offline RL only（不是 online post-training）
- **机会**: STL-conditioned GRPO/PPO for VLA — 将 STL 约束集成到 VLA 的 online RL post-training

## Related Papers
- [[robotics-safety-post-training/papers/SELP|SELP]] — LTL constrained decoding（plan-level）
- [[robotics-safety-post-training/papers/SafeGen-LLM|SafeGen-LLM]] — PDDL3 reward machine（plan-level）
- [[robotics-safety-post-training/papers/Formal-Methods-Robot-Survey|Formal Methods Survey]] — STL/LTL 在 robot learning 的全景
