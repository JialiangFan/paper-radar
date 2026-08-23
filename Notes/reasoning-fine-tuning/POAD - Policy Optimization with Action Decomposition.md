# POAD: Reinforcing LLM Agents via Policy Optimization with Action Decomposition

- **Authors**: NeurIPS 2024
- **Year/Venue**: 2024 / NeurIPS 2024
- **ArXiv**: [2405.15821](https://arxiv.org/abs/2405.15821)
- **Tags**: #token-level-rl #action-decomposition #PPO #credit-assignment

## Problem
Action-level 优化忽略了 token 间的差异。一个 action 是由多个 token 组成的。

## Method
**Bellman backup with Action Decomposition (BAD)**:
1. 推导 intra-action token credit：同一 action 内 token 间的 value 分解
2. 推导 inter-action token credit：跨 action 的 token credit
3. 在 PPO 框架中实现

## Key Results
- WebShop, ALFWorld, HotPotQA, SciWorld 上显著优于标准 PPO

## Related Papers
- [[MA-RLHF - Macro Actions for RLHF]] — 反方向：token→macro action 聚合
- [[GiGPO - Group-in-Group Policy Optimization]] — step-level，比 POAD 粗但更实用
