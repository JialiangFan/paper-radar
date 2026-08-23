# SafeGen-LLM: Enhancing Safety Generalization in Task Planning for Robotic Systems

- **Authors**: Jialiang Fan, Weizhe Xu, Mengyu Liu, Oleg Sokolsky, Insup Lee, Fangxin K.
- **Year/Venue**: 2025/2026
- **ArXiv**: [2602.24235](https://arxiv.org/abs/2602.24235)
- **Tags**: #planning #GRPO #formal-verification #reward-machine #PDDL

## Problem
LLM 作为 robot task planner 时，预训练知识不包含特定领域的安全约束，导致生成不安全的计划。

## Method
1. **SFT Phase**: 在安全约束合规的 planning 数据集上做监督微调
2. **GRPO Phase**: 用 **reward machines**（从 PDDL3 形式化约束自动构建）引导 GRPO 强化学习
   - Reward machine 将形式化安全规约转化为 RL 的 reward signal
   - 支持 curriculum learning（逐步增加约束复杂度）
3. **Multi-domain PDDL3 Benchmark**: Blocksworld, Ferry, Grippers, Spanner

## Formal Guarantee?
**YES — Reward machines 来自 PDDL3 形式化规约**。安全约束被编码为 temporal constraints，reward machine 精确反映约束满足情况。

## Key Results
- Success: 0% (pretrained) → 66% (SFT) → 82% (GRPO)
- Safety violations: 10% (SFT) → 4% (GRPO)

## Relevance
**你的论文** —— 是本综述的出发点。在 plan-level 做了 formal verification + GRPO post-training。核心问题是如何将这个思路向下延伸到 control-level。

## Related Papers
- [[robotics-safety-post-training/papers/SELP|SELP]] — 类似思路但用 LTL（非 PDDL3）
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — control-level 安全 post-training（CMDP, 无形式化）
- [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]] — control-level CBF（有形式化）
