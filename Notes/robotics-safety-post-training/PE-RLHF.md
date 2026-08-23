# PE-RLHF: Reinforcement Learning with Human Feedback and Physics Knowledge for Safe Autonomous Driving

- **Authors**: Zilin Huang et al.
- **Year/Venue**: 2025 / Transportation Research Part C
- **ArXiv**: [2409.00858](https://arxiv.org/abs/2409.00858)
- **GitHub**: [zilin-huang/PE-RLHF](https://github.com/zilin-huang/PE-RLHF)
- **Tags**: #autonomous-driving #physics #RLHF #safety-floor

## Problem
人类反馈质量不稳定（疲劳、注意力分散），纯 RLHF 的安全性无法保证。

## Method
1. **Physics-enhanced RLHF**: 集成 traffic flow model 作为物理先验
2. **Dynamic action selection**: 在人类 action 和 physics-based action 之间动态切换
3. **Safety floor**: 物理模型提供最低安全保障——即使人类反馈质量退化，策略也不会比物理 baseline 差

## Formal Guarantee?
**Partial — Physics-based policy 提供 minimum safety guarantee**。

## Key Results
- 优于 SOTA in safety, sample efficiency, robustness
- 人类反馈质量退化时仍能保持安全

## Relevance
**Physics prior 作为 safety floor** 的思路可迁移到机器人操作——用 dynamics model / CBF 作为安全下界，RL post-training 在此基础上优化性能。

## Related Papers
- [[robotics-safety-post-training/papers/Safe-RLHF|Safe RLHF]] — 基础 CMDP 方法
- [[robotics-safety-post-training/papers/FOSP|FOSP]] — 也用 world model 保障安全
