# GiGPO: Group-in-Group Policy Optimization for LLM Agent Training

- **Authors**: Lang Feng et al.
- **Year/Venue**: 2025 / NeurIPS 2025
- **ArXiv**: [2505.10978](https://arxiv.org/abs/2505.10978)
- **Tags**: #step-level-rl #credit-assignment #GRPO #agent-training

## Problem
GRPO 只提供 episode-level advantage（整条轨迹好/坏），在长 horizon agent 任务中无法区分每步的贡献。

## Method
**两级 advantage estimation**:
1. **Macro relative advantage** (episode-level): 标准 GRPO 的轨迹间比较
2. **Micro relative advantage** (step-level): 通过 **anchor state grouping** 实现——在不同轨迹中找到相同的状态，在组内计算 step-level relative advantage

## Key Results
- ALFWorld: +12% over GRPO
- WebShop: +9% over GRPO
- 无额外内存开销

## Related Papers
- [[SALT - Step-level Advantage via Trajectory Graph]] — trajectory graph 方法
- [[POAD - Policy Optimization with Action Decomposition]] — 更细粒度：action→token 分解
- [[f-GRPO - Divergence-Based RL for LLM Alignment]] — GRPO 的理论基础
