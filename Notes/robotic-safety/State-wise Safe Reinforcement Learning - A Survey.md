# State-wise Safe Reinforcement Learning: A Survey

## 主题
State-wise Safety Constraints RL

## 背景
尽管RL在仿真中取得巨大成功，但将其应用于真实世界仍面临安全保障这一核心挑战。RL智能体基于reward信号学习，可能会为了追求高reward而违反安全约束（如自动驾驶中超速行驶）。State-wise约束是真实应用中最常见也最具挑战性的安全约束类型。

## 现有局限与研究问题
- **Limitation:** 早期安全RL工作主要基于CMDP框架，仅关注累积约束或chance constraints，无法处理即时性、确定性的状态级硬约束
- **Problem:** 如何在RL中持久满足每一步的状态级安全约束（SCMDP），而非仅在期望意义下满足

## 贡献
- 首篇专注于state-wise安全RL的综述，提出State-wise Constrained MDP (SCMDP)框架
- 将现有方法分为两类：收敛后安全（soft penalties引导策略趋向安全）和训练中安全（通过CBF投影或渐进安全探索保证训练全程安全）
- 系统比较各方法在安全保证、可扩展性、训练中/收敛后安全、假设条件等维度的trade-off
- 涵盖CSC、USL、LPG、RL-CBF、ShieldNN、ISSA、RTS、RecoveryRL等代表性算法

## 方法论
- 基于SCMDP形式化，要求 C_i(s_t, a_t, s_{t+1}) <= w_i 在所有时间步成立
- 层次化方法：上层生成任务导向动作，下层安全层投影到安全动作集
- 端到端方法：Lagrangian方法将约束惩罚加入reward函数进行联合优化
- 按动力学知识分类：white-box（CBF等）、black-box（数字孪生仿真）、learned dynamics
