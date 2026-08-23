# SALT: Step-level Advantage Assignment for Long-horizon Agents via Trajectory Graph

- **Authors**: Amazon Science
- **Year/Venue**: 2025
- **ArXiv**: [2510.20022](https://arxiv.org/abs/2510.20022)
- **Tags**: #step-level-rl #credit-assignment #trajectory-graph #GRPO

## Problem
长 horizon agent 任务中，outcome-only reward 无法有效分配到每个步骤。

## Method
**Trajectory Graph Construction**:
1. 对同一 prompt 采样多条轨迹
2. 构建图：节点 = 状态，边 = action 转移
3. 从图结构中量化每步的质量
4. 将推导出的 step advantage 作为 plug-in 接入 GRPO

## Key Results
- 在 agent benchmarks 上显著提升 GRPO 性能
- 几乎零额外计算开销，plug-and-play

## Related Papers
- [[GiGPO - Group-in-Group Policy Optimization]] — anchor state grouping 方法
- [[CSO - Verified Critical Step Optimization]] — 只关注 critical steps
