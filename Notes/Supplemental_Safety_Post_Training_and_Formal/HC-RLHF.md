---
imported_title: "HC-RLHF: RLHF with High-Confidence Safety Constraints"
imported_from: "/Users/jfan/ND/看论文/robotics-safety-post-training/papers/HC-RLHF.md"
imported_reason: "Useful training-side safety alignment prior."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# HC-RLHF: Reinforcement Learning from Human Feedback with High-Confidence Safety Constraints

- **Authors**: Extension of Safe RLHF
- **Year/Venue**: 2025 / Reinforcement Learning Journal
- **ArXiv**: [2506.08266](https://arxiv.org/abs/2506.08266)
- **Tags**: #probabilistic-guarantee #safe-RLHF #high-confidence #safety-certificate

## Problem
Safe RLHF 的 CMDP 在实践中可能出现 "safety compensation" — 模型在某些场景过度安全、另一些场景不够安全，平均满足约束但分布不均。

## Method
1. 训练后进行 **held-out safety test**
2. 计算 **upper-confidence bound** of safety cost
3. 只有当 UCB 满足安全阈值时才部署模型
4. **Pessimistic cost constraints**: 使用保守估计避免过度乐观

## Formal Guarantee?
**Partial — 提供概率安全证书**（high-confidence bound）。

## Relevance
为 post-training 流程添加了 **部署前安全认证** 环节。可以应用于任何 safe post-training 方法（SafeVLA, VLA-RFT 等）的部署验证。

## Related Papers
- [[robotics-safety-post-training/papers/Safe-RLHF|Safe RLHF]] — 基础方法
- [[robotics-safety-post-training/papers/Prob-Shielding|Prob. Shielding]] — 另一种概率安全保证
- [[robotics-safety-post-training/papers/Neural-Lyapunov-Barrier|Neural Lyapunov Barrier]] — 形式化验证
