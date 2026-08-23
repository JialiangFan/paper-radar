# TraD-RL: Expert Knowledge-driven RL for Autonomous Racing via Trajectory Guidance and Dynamics Constraints

- **Authors**: Bo Leng, Weiqi Zhang, Zhuoren Li, Lu Xiong, Guizhe Jin, Ran Yu, Chen Lv
- **Affiliations**: Tongji University, Nanyang Technological University
- **Year/Venue**: 2026 / arXiv preprint (submitted to Elsevier)
- **ArXiv**: [2603.05842](https://arxiv.org/abs/2603.05842)
- **Tags**: #safe-RL #CBF #autonomous-racing #dynamics-constraints #curriculum-learning #CMDP

## Problem
自动驾驶赛车中，标准 RL 方法面临三大挑战：
1. **探索效率低**：连续动作空间 + 稀疏奖励 → 收敛慢
2. **安全约束缺失**：高速弯道中 yaw rate 和 sideslip angle 容易超出稳定极限 → 失控/甩尾
3. **性能-安全权衡**：传统方法要么保守（安全但慢），要么激进（快但不稳定）

## Method: TraD-RL Framework

### 1. Trajectory Prior Guidance（轨迹先验引导）
- **MCRL (Minimum Curvature Racing Line)**: 基于赛道几何优化最小曲率赛车线，提供全局路径+速度参考
- **观测空间增强**: 将 MCRL 编码为 ego-centric 占用栅格，直接嵌入观测空间
- **Reward Shaping**: 三维奖励 — 轨迹跟踪误差 $r_{MCRL}$、目标速度跟踪 $r_{TS}$、航向对齐 $r_H$

### 2. Dynamics Constraints（动力学约束）— 核心安全机制
- **安全操作包络**: 在 sideslip angle-yaw rate ($\beta$-$\omega$) 相平面中定义安全边界
- **CBF 形式化约束**:
  - Yaw rate 约束: $\dot{h}_\omega \geq -\alpha h_\omega$, 其中 $h_\omega = \frac{\mu g}{u} - |\omega|$
  - Sideslip angle 约束: $\dot{h}_{\beta} \geq -\alpha h_{\beta}$, 其中 $h_{\beta} = \beta_{max} - \beta$ (双边)
- **Cost 函数**: $c_\omega = \max(-(\dot{h}_\omega + \alpha h_\omega), 0)$, $c_\beta$ 类似
- **Lagrangian 优化**: Adaptive dual Lagrangian multipliers $\lambda_\omega, \lambda_\beta$ 动态调节安全-性能权衡

### 3. Two-Stage Curriculum Learning
- **Stage 1 — Trajectory Guidance**: 跟踪 MCRL 参考速度，学习基本驾驶技能
- **Stage 2 — High-Speed Exploration**: 切换到最大物理极限速度，突破保守先验

### 4. 算法架构
- Actor: CNN backbone + MLP，输出加速度和转向角
- Critic + Cost Critic: 双头价值网络，分别估计 reward Q 值和 cost Q 值
- 优化: Actor loss = reward objective + $\sum_k \lambda_k \cdot \text{ReLU}(\max_j Q^{\xi_j}_{C_k} - d_k)$

## Formal Guarantee?
**Partial — CBF-inspired constraints**。使用 CBF 形式定义安全约束，但通过 Lagrangian relaxation 软化执行（非严格 CBF 硬保证）。安全性体现在：
- 训练中通过 cost critic 估计约束违反
- 动态 Lagrangian 乘子自适应调节
- 不是 inference-time 的硬约束（不同于 VLSA/AEGIS 的即时 CBF 修正）

## Key Results
在 Berlin Tempelhof Airport Street Circuit (Formula E) 仿真环境中：

### Racing Performance
| Algorithm | Avg Speed (m/s) | Lap Time (s) |
|-----------|----------------|--------------|
| DDPG | 30.49 | 75.65 |
| PPO | 28.37 | 84.67 |
| TAL | 38.67 | 61.31 |
| **TraD-RL** | **39.79** | **58.83** |

### Safety Metrics
| Algorithm | ω-unsafe Times | β-unsafe Times |
|-----------|---------------|---------------|
| DDPG | 18.31 | 8.34 |
| PPO | 14.53 | 1.86 |
| TAL | 17.65 | 5.85 |
| **TraD-RL** | **16.50** | **4.61** |

- 相比 TAL: 速度 ↑2.90%, 圈速 ↓4.05%, β-unsafe ↓21.20%
- 100% lap progress（15k steps 后稳定完成全程）
- Ablation: 去除 dynamics constraints (w/o DC) → β-unsafe 增加 39.90%

## Relevance
**CBF + RL 训练的典型案例**，展示了如何将 CBF 安全约束融入 RL 训练过程（而非仅作为 inference-time filter）。与 robotics safety post-training 的关系：

1. **CBF 作为训练约束**: 不同于 VLSA/AEGIS（inference-time CBF），TraD-RL 将 CBF 约束融入训练损失
2. **Lagrangian CMDP**: 方法论与 SafeVLA 一致（都用 CMDP + Lagrangian），但 cost 来自 CBF 而非学习的 cost model
3. **Curriculum learning**: 两阶段课程学习可能适用于 VLA post-training

## Limitation & Opportunity
- 仅在仿真中验证，无 real-world deployment
- 特定于自动驾驶赛车，未泛化到通用机器人操作
- **核心启发**: CBF cost + Lagrangian CMDP 的组合可迁移到 VLA safety post-training — 用物理约束（而非学习的 cost model）作为安全信号

## Related Papers
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — 同样用 CMDP + Lagrangian，但 cost model 是学习的
- [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]] — CBF 作为 inference-time filter（硬保证）
- [[robotics-safety-post-training/papers/PE-RLHF|PE-RLHF]] — 类似地用物理先验作为安全下界
- [[robotics-safety-post-training/papers/FOSP|FOSP]] — 也用 reachability/safety guidance 在 RL 训练中
