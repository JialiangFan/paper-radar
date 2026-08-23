# Gameplay Filters: Robust Zero-Shot Safety through Adversarial Imagination

## 主题
Adversarial Safety Filter Robots

## 背景
自主机器人需要在不确定条件下可靠运行。安全滤波器原则上可以通过覆盖不安全动作来防止灾难性故障，但现有方法仅能系统性地计算5-6维状态空间的最小限制安全滤波器，远不够模拟足式机器人所需的30-50维。

## 现有局限与研究问题
- **Limitation:** HJ可达性方法维度诅咒严重，超过5-6维即不可行；CBF滤波器缺乏一般性构造方法；现有足式机器人安全滤波器依赖简化降阶模型，仅在局部步态附近有效
- **Problem:** 如何为高维（36-D状态空间）足式机器人构建全阶安全滤波器，覆盖广泛运动包络和多种部署条件？

## 贡献
- 提出gameplay filter：新型预测性安全滤波器，通过模拟自博弈（安全策略 vs 对抗干扰）合成
- 首次在足式机器人平台上实现全阶（36维）安全滤波器
- 展现inherent鲁棒性：无需手动调参即可处理sim-to-real gap
- 在两种不同Unitree四足机器人上的物理实验验证零样本安全有效性（抗拉拽、不规则地形等）

## 方法论
- 基于Reach-Avoid Safety Game：控制器 vs 对抗干扰的微分博弈，通过Isaacs方程求解安全值函数
- Offline训练：扩展ISAACS（Iterative Soft Adversarial Actor-Critic for Safety），通过SAC框架对抗训练安全策略和虚拟对手
- Online部署：运行时连续进行对抗想象rollout，预测性地阻止会导致未来失败的候选动作
- 利用全阶物理引擎仿真模型（MuJoCo），仅需单条高信息量轨迹rollout即可实时滤波
- Operational Design Domain (ODD)概念：明确安全保证的适用条件范围
