# From Novice to Expert: LLM Agent Policy Optimization via Step-wise Reinforcement Learning

- **Authors**: 2024
- **Year/Venue**: 2024
- **ArXiv**: [2411.03817](https://arxiv.org/abs/2411.03817)
- **Tags**: #step-level-rl #curriculum-learning #agent-training

## Problem
从零开始训练 agent policy 效率低，早期失败率极高。

## Method
**Progressive Step-wise RL Curriculum**:
1. 将长 horizon 任务拆解为逐步的决策点
2. 先训练靠近目标的简单决策点
3. 逐步扩展到更早、更难的决策点

## Key Results
- 比直接全轨迹 RL 训练更快收敛、更稳定

## Related Papers
- [[CSO - Verified Critical Step Optimization]] — 识别 critical steps 可作为 curriculum 依据
- [[STeCa - Step-level Trajectory Calibration]] — 从次优到最优的改进思路
