# SYMPOL: Symbolic Tree-Based On-Policy RL

> Marton et al., ICLR 2025 (University of Mannheim, Technical University of Clausthal, University of Rostock)

## 主题
Decision Tree RL Policies

## 背景
Reinforcement learning (RL) 在各领域取得了巨大成功，但其依赖的 neural network policy 本质上是 black-box，难以解释和信任，在 safety-critical 场景（如自动驾驶、工业机器人）中部署受限。Symbolic policy 通过紧凑、可解释的结构表达决策策略，其中 decision tree (DT) 因其层级分支结构天然具备 interpretability，是 symbolic RL policy 的理想载体。然而，在 on-policy RL 框架中直接学习 symbolic DT policy 仍然极具挑战性，因为传统 DT 不可微分，无法直接嵌入 gradient-based 优化。

## 现有局限与研究问题
- **Limitation:** 现有的 tree-based RL 方法主要分为三类，均存在根本性缺陷：(1) Post-processing 方法（如 VIPER）先训练 NN policy 再蒸馏为 DT，训练与推理策略之间存在严重的 information loss（Cohen's D > 2.5）；(2) Custom optimization 方法使用进化算法或线性整数规划等非标准训练流程，无法嵌入现有 RL 框架，可扩展性差；(3) Soft Decision Tree (SDT) 方法虽可微分但在每个节点同时使用多个 feature 进行 multidimensional split，导致树结构难以解释，且离散化后性能大幅下降。
- **Problem:** 如何在标准 on-policy RL 框架（如 PPO）中，端到端地直接优化可解释的 axis-aligned decision tree policy，避免 post-processing 导致的 information loss，同时保持与 full-complexity model 可比的性能？

## 贡献
- 将 GradTree 集成到 actor-critic 架构中，通过 separate architecture（tree-based actor + NN critic）在标准 on-policy RL 框架中直接优化 axis-aligned DT policy，并扩展至 continuous action space。
- 提出 dynamic rollout buffer 和 dynamic batch size 机制：rollout buffer 按指数函数逐步增大环境交互步数以改善 exploration stability；batch size 同步增长以通过 gradient accumulation 提高 gradient stability。
- 提出对 split index 和 leaf action 参数施加 weight decay（不对 split threshold 施加），动态调整参数分布，增强训练过程中的 exploration 能力。
- SYMPOL 不依赖预训练 NN policy、复杂搜索过程或 post-processing 步骤，可无缝嵌入 PPO、A2C 等标准 on-policy RL 算法。
- 在多个 benchmark 环境（CartPole, Acrobot, LunarLander, MountainCarContinuous, Pendulum 及 MiniGrid 系列）上，SYMPOL 消除了 information loss（Cohen's D = -0.019），在可解释方法中取得最优性能，且学到的 DT 平均仅约 50.5 个节点。

## 方法论
- **Arithmetic DT policy formulation:** 基于 GradTree，将 DT 表达为算术函数形式 pi(s|a, tau, iota) = sum_l a_l * L(s|l, tau, iota)，其中 a 为叶节点动作，tau 为 split threshold，iota 为 feature index。完全生长的 complete tree（depth d）通过 post-hoc pruning 去除冗余路径。
- **Dense architecture:** 将 feature index iota 展开为 one-hot 矩阵 I，split threshold tau 展开为逐 feature 矩阵 T，实现矩阵运算的高效 gradient-based 优化，同时底层模型始终等价于 hard, axis-aligned DT。
- **Axis-aligned splitting with straight-through estimator:** Split 函数 S(s|iota, tau) = floor(S(iota * s - iota * tau)) 使用 logistic function + rounding，前向传播为 non-differentiable hard split，反向传播通过 straight-through estimator 传递梯度，因此 SYMPOL 不是 soft DT 也不是 differentiable DT。
- **Weight decay 策略:** 对 split index (I) 和 leaf action (a) 施加 weight decay 以窄化分布、增强探索；不对 split threshold (T) 施加，因为其值域与量级无关。
- **Separate actor-critic architecture:** Actor 为 tree-based policy，critic 为 full-complexity NN（可捕获复杂 value function），二者不共享参数，确保 policy 的可解释性不受 critic 复杂度影响。
- **Continuous action space 扩展:** 叶节点输出正态分布均值，附加可学习参数 sigma_log 表示 log 标准差。
- **Dynamic rollout buffer:** 环境交互步数 n_t = n_init * 2^(floor((t+1)*i / (1+t_total)) - 1)，从 n_init 指数增长到 n_final = 128 * n_init，早期小 rollout 支持快速探索，后期大 rollout 提供高质量样本。
- **Dynamic batch size:** Batch size 与 rollout buffer 同步增长，通过 gradient accumulation 虚拟增大 batch，早期小 batch 保持探索多样性，后期大 batch 提升梯度稳定性。
- **评估:** 在 5 个 control 环境和 5 个 MiniGrid 环境上与 SA-DT、D-SDT、MLP、SDT 对比，使用 PPO 训练 1M timesteps，5 次随机训练 * 5 次评估 episode，hyperparameter 经 optuna 60 trials 优化。SYMPOL 在可解释方法中一致性地取得最高性能，Cohen's D 接近 0（无 information loss），学习到的 DT 平均 50.5 节点（SA-DT d=5 为 60.3，d=8 为 291.6）。Case study 展示 SYMPOL 可通过 inspect DT 结构直接检测 goal misgeneralization。
