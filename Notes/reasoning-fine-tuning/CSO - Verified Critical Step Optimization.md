# CSO: Verified Critical Step Optimization for LLM Agents

- **Authors**: Mukai Li et al.
- **Year/Venue**: 2025
- **ArXiv**: [2602.03412](https://arxiv.org/abs/2602.03412)
- **Tags**: #step-level-rl #critical-step #preference-learning #agent-training

## Problem
大部分 trajectory 步骤对任务成败无关紧要。全轨迹优化效率低。

## Method
**Verified Critical Step Identification**:
1. 从失败轨迹出发，在每个步骤尝试替换为 alternate actions
2. 如果替换某步后任务从失败→成功，该步为 **critical step**
3. 只在 critical steps 上构建偏好对（DPO）
4. 只需要 **16% 的步骤**进行监督

## Key Results
- GAIA: +37%, XBench: +26%
- **8B 模型匹配 GPT-4.1**

## Related Papers
- [[ELPO - Error-Localized Policy Optimization]] — "首个致命错误" 思路异曲同工
- [[STeCa - Step-level Trajectory Calibration]] — step-level 识别 + reflection
