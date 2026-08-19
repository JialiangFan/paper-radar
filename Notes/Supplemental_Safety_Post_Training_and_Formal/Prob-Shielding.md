---
imported_title: "Probabilistic Shielding for Safe Reinforcement Learning"
imported_from: "/Users/jfan/ND/看论文/robotics-safety-post-training/papers/Prob-Shielding.md"
imported_reason: "Shielding supplement for stochastic/safe RL settings."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Probabilistic Shielding for Safe Reinforcement Learning

- **Authors**: Court, le, Belardinelli, Goodall
- **Year/Venue**: 2025 / AAAI 2025
- **Tags**: #shielding #formal-guarantee #probabilistic #safe-RL

## Problem
如何在 RL 训练和部署中提供严格的概率安全保证？

## Method
1. State-augment MDP：只用安全动力学（无需完整环境模型）
2. 计算 inductive ε-upper bounds on unsafe state probability
3. Shield 在运行时干预不安全 action
4. **Optimality-preserving**: 证明 shield 不影响最优策略的学习

## Formal Guarantee?
**YES — 严格的概率安全保证**（P(unsafe) ≤ ε）。

## Key Results
- 可扩展到复杂 MDP
- 保证安全的同时不牺牲最优性

## Relevance
可以作为 VLA post-training 的安全层——在 RL fine-tuning 过程中和部署后都提供概率安全保证。

## Related Papers
- [[robotics-safety-post-training/papers/Neural-Lyapunov-Barrier|Neural Lyapunov Barrier]] — deterministic 安全保证
- [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]] — CBF 安全保证
- [[robotics-safety-post-training/papers/HC-RLHF|HC-RLHF]] — 概率安全 + RLHF
