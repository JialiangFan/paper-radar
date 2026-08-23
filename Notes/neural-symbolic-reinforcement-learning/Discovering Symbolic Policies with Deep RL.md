# Discovering Symbolic Policies with Deep RL

> Landajuela et al., ICML 2021 (Lawrence Livermore National Laboratory)

## 主题
Symbolic Policy Discovery

## 背景
Deep reinforcement learning (DRL) 在连续控制任务中取得了显著成功，但其策略由复杂的 neural network 表示，涉及成千上万的非线性算子与仿射变换，难以理解、验证和部署。相比之下，数学物理与控制理论中的传统方法往往使用紧凑的 symbolic expression 来描述控制器，具有可解释性强、可部署性高的优势。本文提出 Deep Symbolic Policy (DSP)，直接在 symbolic expression 空间中搜索可作为控制策略的数学表达式。

## 现有局限与研究问题
- **Limitation:** 基于 neural network 的 DRL 策略是"black-box"，难以理解、信任和验证，且部署时对硬件和延迟要求高；现有的 symbolic regression 和 model distillation 方法存在 objective mismatch 问题——训练目标（最小化预测误差）与评估目标（最大化环境奖励）不一致，导致 regression-based 方法常出现灾难性失败。
- **Problem:** 如何直接在 RL loop 内用 gradient-based 方法搜索 symbolic policy 空间，同时扩展到多维动作空间并改善 combinatorial optimization 中的 exploration？

## 贡献
- 提出 DSP 框架：使用 autoregressive RNN (Policy Generator) 在 RL loop 内直接搜索 symbolic control policy 空间，以 risk-seeking policy gradient 优化最佳表达式的性能。
- 提出 anchoring 算法：利用预训练的 neural network policy 作为 anchor model，逐维度蒸馏为 symbolic policy，将多维动作空间的组合爆炸从 O(|L|^{nk}) 降至 n 个 O(|L|^k) 的子问题。
- 提出两种新的 exploration 技术：**hierarchical entropy regularizer**（对早期 token 施加指数衰减权重的 entropy bonus，防止 early commitment）和 **soft length prior**（通过高斯先验平滑表达式长度分布，使 Policy Generator 能自主学习最优长度）。
- 在 8 个连续控制 benchmark 上，DSP 发现的 symbolic policy 在 average rank 和 normalized episodic reward 上优于 7 种 state-of-the-art DRL 算法（DDPG, TRPO, A2C, PPO, ACKTR, SAC, TD3），同时复杂度大幅降低。
- 对已知动力学系统（CartPole, Pendulum, MountainCar），证明发现的 symbolic policy 在连续时间系统中是 provably stable 的。

## 方法论
- **Policy Generator:** 单层 LSTM (32 hidden units)，以 autoregressive 方式采样 symbolic expression tree 的 pre-order traversal token 序列。Token library L 包含算术运算符（+, -, x, /）、函数（sin, cos, exp, log）、常数（0.1, 1.0, 5.0）和状态变量 s_i。采样时通过 in situ constraints（长度约束、禁止冗余结构等）在线裁剪无效表达式。
- **Policy Evaluator:** 将采样的 expression 实例化为控制策略 a = f(s)，在环境中运行 N 个 episode，计算 average episodic reward R(tau) 作为 reward signal。
- **Risk-seeking policy gradient:** 优化条件期望 J_risk = E[R(tau) | R(tau) >= R_epsilon]，仅对 top-(1-epsilon) 分位的样本计算梯度，聚焦于最优表达式的发现。
- **Anchoring algorithm:** 对 n 维动作空间，依次学习每一维的 sub-policy f_i，已学维度固定为 symbolic，未学维度由 anchor NN policy 填充，逐步替换直至完全 symbolic。
- **Hierarchical entropy regularizer:** H_gamma = eta * E[sum_i gamma^{i-1} H[p(tau_i | tau_{1:(i-1)})]]，通过指数衰减权重确保早期 token 持续探索。
- **Soft length prior:** 在 RNN emission logits 上加入 Gaussian prior psi_o，使初始表达式长度分布平滑，避免集中在最大长度。
- **Constant optimization:** 对最优 symbolic policy 进行一次 post-hoc 常数微调（DSP^o），进一步提升性能。
- **评估:** 8 个 OpenAI Gym / PyBullet 环境，1000 个随机 seed 的 held-out episodic reward，与 7 种 DRL 算法及 regression baseline 对比。DSP 取得最高 average rank (2.63)、最高 normalized reward (0.96)、最优 worst-case rank (6)。
