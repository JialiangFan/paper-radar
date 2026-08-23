# Safe Reinforcement Learning for Legged Locomotion

## 主题
Safe RL Legged Robot Control

## 背景
深度RL在解决复杂高维问题方面展现出巨大潜力，但训练RL策略需要探索大量不安全的状态和动作，对四足机器人等固有不稳定系统尤其危险。将RL策略从仿真迁移到真实世界时，安全是主要瓶颈。

## 现有局限与研究问题
- **Limitation:** 现有Recovery RL方法使用safety critics预测违规概率，但这些critics在simulation中训练，在real world部署时可能不准确；且safety critics作为黑盒神经网络，无法正式验证其对unseen状态的正确性
- **Problem:** 如何在四足机器人运动学习中确保训练全程安全，同时最小化对学习过程的干预？

## 贡献
- 提出双策略安全RL框架：安全恢复策略（pi_safe）防止机器人进入不安全状态，学习策略（pi_learner）优化任务完成
- 基于模型的可达性判据（而非黑盒neural network）判断何时切换策略，利用质心动力学模型（CDM）进行前向rollout
- 仿真中平均减少48.6%的摔倒，在real-world Unitree A1四足机器人上实现34%能量效率提升
- 理论分析：建立性能上界与动力学模型误差的关系（regret-type bound）

## 方法论
- 基于CMDP建模，定义safety trigger set C_tri、safe set C_safe和failure set C_failure
- 利用近似动力学模型T̂前向预测w步轨迹，基于Reachability Planning Criteria判断pi_learner能否保持安全
- pi_safe的触发条件：当前状态在C_tri中，或pi_safe交回控制权时验证pi_learner的未来轨迹不进入C_tri
- 在四个任务上验证：efficient gait、catwalk、two-leg balance、pacing
