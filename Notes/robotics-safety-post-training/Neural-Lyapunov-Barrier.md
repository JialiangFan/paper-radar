# Formally Verifying Deep RL Controllers with Lyapunov Barrier Certificates

- **Authors**: Multiple
- **Year/Venue**: 2024
- **ArXiv**: [2405.14058](https://arxiv.org/abs/2405.14058)
- **Tags**: #Lyapunov #barrier-certificate #formal-verification #RL-verification

## Problem
Deep RL 训练的控制器如何提供形式化的稳定性和安全性保证？

## Method
1. 训练 **Neural Lyapunov Barrier (NLB) certificates** 用于离散时间系统
2. **Certificate composition**: 将复杂系统的验证拆解为一系列简单 certificate 的组合
3. 验证流程：训练 RL controller → 训练 NLB certificate → 形式化验证 certificate 条件

## Formal Guarantee?
**YES — Lyapunov barrier certificates** 提供严格的稳定性（convergence）和安全性（invariance）保证。

## Key Results
- 可扩展到复杂控制系统
- Certificate composition 解决了单一 certificate 难以覆盖复杂行为的问题

## Relevance
**Post-training verification 的关键方法**。RL post-training 后，用 NLB 验证策略的安全性。如果验证失败→重新训练/修补。这是 "训练→验证→修补" 闭环的验证环节。

## Key Insight (来自 Lyapunov-stable Neural Control 2024)
> "Cheap adversarial training + post-training strong verification is more practical than expensive in-training verification"

这意味着：先用便宜的方法训练（如 GRPO），然后用严格的形式化方法验证，比在训练过程中强制形式化约束更实用。

## Related Papers
- [[robotics-safety-post-training/papers/SECURE|SECURE]] — CBF 方法（另一种形式化保证）
- [[robotics-safety-post-training/papers/Prob-Shielding|Prob. Shielding]] — 概率安全保证
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — 可以用 NLB 验证其 post-trained policy
