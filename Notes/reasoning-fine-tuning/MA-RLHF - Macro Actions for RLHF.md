# MA-RLHF: Reinforcement Learning from Human Feedback with Macro Actions

- **Authors**: Yekun Chai, Haoran Sun, et al.
- **Year/Venue**: 2024 / ICLR 2025
- **ArXiv**: [2410.02743](https://arxiv.org/abs/2410.02743)
- **Tags**: #macro-action #RLHF #credit-assignment #token-level

## Problem
Token-level RLHF 中，token 和最终 reward 的时间距离太长，导致 credit assignment 困难。

## Method
**Macro Action Aggregation**:
1. 将 token 序列划分为 macro actions（语义上有意义的 token 块）
2. 在 macro action level 分配 reward
3. 减少 action-reward 的时间距离

## Key Results
- Summarization: +30%, Code generation: significant gains
- 收敛速度: 1.7-2x faster

## Related Papers
- [[POAD - Policy Optimization with Action Decomposition]] — 反方向：action→token 分解
- [[GiGPO - Group-in-Group Policy Optimization]] — step-level
