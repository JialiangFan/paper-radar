# Model-Free Reinforcement Learning for Spatiotemporal Tasks

- **Title:** Model-Free Reinforcement Learning for Spatiotemporal Tasks
- **Authors:** Anand Balakrishnan, Stefan Jaksic, Edgar A. Aguilar, Dejan Nickovic, Jyotirmoy V. Deshmukh
- **Venue:** IROS 2024 (IEEE/RSJ International Conference on Intelligent Robots and Systems)
- **Year:** 2024
- **Affiliations:** University of Southern California; AIT Austrian Institute of Technology GmbH


## 主题
将符号自动机方法扩展到时空任务，支持 RL 学习具有空间和时间约束的复杂策略

## 背景
机器人任务通常同时涉及空间约束（到达特定区域、避开障碍）和时间约束（在时限内完成、按顺序访问）。时空任务逻辑（spatiotemporal task logic）可以精确描述这类复合需求，但将其与 RL 结合面临状态空间爆炸和奖励稀疏的双重挑战。

## 现有局限与研究问题
- **Limitation:** 标准时序逻辑 + RL 方法忽略空间结构，导致在高维空间中探索效率低下；时空规约的自动机表示可能具有指数级状态数；现有方法在连续空间环境中的可扩展性差。
- **Problem:** 如何将符号自动机 reward shaping 方法高效扩展到时空任务，同时保持在连续空间中的可扩展性？

## 贡献
- 将 CDC 2023 的符号自动机 RL 框架扩展到时空任务逻辑
- 提出空间感知的自动机构造方法，利用空间结构减少自动机状态数
- 设计时空 reward shaping 函数，同时提供空间距离和时间进展的引导信号
- 在多机器人协调等复杂场景中验证方法的有效性

## 方法论
- **时空任务逻辑：** 扩展标准时序逻辑，加入空间算子（如区域到达、距离约束），形成时空任务规约
- **空间感知自动机：** 在符号自动机构造中利用空间拓扑信息，合并等价状态，减少自动机规模。空间谓词的评估使用连续距离函数而非二值判断
- **时空 Reward Shaping：** 奖励函数 = 时间进展奖励 + 空间距离奖励。空间距离奖励基于当前位置到下一个目标区域的距离，提供平滑的梯度信号
- **层次化策略：** 高层策略选择当前的自动机子目标，低层策略执行具体的运动控制。自动机结构自然提供了任务的层次化分解
- **评估：** 在 IROS 仿真环境中，包括多机器人协调任务和复杂导航场景，方法显著优于无 reward shaping 的基线和手工设计奖励的方法
