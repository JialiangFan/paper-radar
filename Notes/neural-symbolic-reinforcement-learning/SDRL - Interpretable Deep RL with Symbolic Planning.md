# SDRL: Interpretable Deep RL with Symbolic Planning

> Lyu, Yang, Liu, Gustafson (2019). AAAI.

## 主题
Symbolic Planning + Hierarchical RL + Interpretability

## 背景
Deep reinforcement learning (DRL) 在高维感知输入的序列决策任务中取得了巨大成功，但长期面临 interpretability 不足和 data efficiency 低下的问题。神经科学研究表明人类通过 object-based 的确定性 transition model 进行 hierarchical planning 来玩视频游戏，这启发了将 symbolic planning 引入 DRL 以提升可解释性和样本效率的思路。此前的 SP+RL 集成工作（如 PEORL）主要局限于 tabular representation，尚未扩展到高维感知输入的复杂环境。

## 现有局限与研究问题
- **Limitation 1:** 传统 DRL（如 DQN）是 black-box 模型，其学到的 policy 难以被人类理解和信任，且在 sparse reward 和 long-horizon 任务中需要大量样本。
- **Limitation 2:** 已有 hierarchical RL 方法（如 hDQN、options framework）虽引入了时间抽象，但 subtask/option 的定义缺乏 interpretability，且通常需要预定义好 option 集合。
- **Limitation 3:** 先前的 SP+RL 集成框架（如 PEORL）依赖 tabular state representation 和固定的 planning goal，无法处理高维感知输入，也无法根据学习反馈动态调整 plan。
- **Problem:** 如何设计一个框架，既能利用 symbolic knowledge 进行 interpretable 的高层 planning，又能通过 DRL 从 raw pixel inputs 学习低层 control policy，并让两者相互促进、共同收敛到最优？

## 贡献
- 提出 SDRL 框架，首次将 symbolic planning 与 hierarchical DRL 集成，实现 task-level interpretability，同时支持高维感知输入。
- 设计 **planner--controller--meta-controller** 三层架构：planner 基于 action language BC 和 CLINGO solver 生成 symbolic plan（subtask 序列）；controller 用 DRL 学习每个 subtask 的 sub-policy；meta-controller 通过 R-learning 评估 subtask 的 extrinsic reward 并提出新的 intrinsic goal 反馈给 planner。
- 引入 **intrinsic goal** 机制（区别于 PEORL 的固定 goal），用 plan quality 度量 symbolic plan 的累计 gain reward，使 planner 能根据 controller 的实际学习效果动态更新 plan。
- 将 symbolic transition 映射为 semi-Markov option，通过 perception module（symbol grounding function F）桥接 symbolic state 与高维感知状态。
- 提供收敛性和最优性的理论保证：证明当 meta-controller 的 R-learning 收敛时，算法终止当且仅当最优 symbolic plan 存在，且输出的 plan 是最优的。
- 在 Taxi domain 和 Montezuma's Revenge 上验证了 SDRL 的 interpretability 和 data efficiency 优势。

## 方法论
- **Symbolic Representation:** 使用 action language BC 描述 domain knowledge（objects、fluents、causal laws），通过 CLINGO answer set solver 求解 symbolic plan。Action description D 中加入 gain reward fluent $\rho(s,a)$ 和 plan quality fluent 来衡量 plan 的质量。
- **Intrinsic Goal:** 定义为 linear constraint $quality > quality(\Pi)$，驱动 planner 在每轮迭代中寻找更优的 plan，而非固定的 goal constraint。
- **Symbol Grounding:** 预训练 perception module $\mathbb{F}: S \times \tilde{S} \to \{t, f\}$，将高维感知状态映射到 symbolic state，从而将 symbolic transition 转化为 semi-Markov option（含 initiation set、intra-option policy、termination condition）。
- **Controller (DRL):** 对每个 subtask 用 Deep Q-learning 学习 sub-policy，intrinsic reward $r_i$ 在达到 subtask goal 时给予大奖励 $\phi$，否则为环境原始 reward。
- **Meta-Controller (R-learning):** 基于 extrinsic reward 执行 R-learning，评估每个 subtask 的长期平均 reward。Extrinsic reward $r_e(s,g) = f(\epsilon)$：当 sub-policy 的 success ratio $\epsilon \geq 0.9$ 时为实际环境 reward，否则为大负值 $-\psi$（惩罚 unlearnable subtask）。
- **Planning-Learning Loop (Algorithm 1):** 每轮 episode 中，planner 生成 plan $\Pi_t$，controller 学习各 subtask 的 sub-policy，meta-controller 计算 extrinsic reward 并更新 $R(s,g)$ 和 $\rho$ 值，然后更新 intrinsic goal 并将学到的 $\rho$ 值回传给 symbolic formulation，触发 planner 重新规划。三个组件交叉优化，直至 symbolic plan 无法继续改进。
- **实验:** Taxi domain（5x5 grid, tabular）对比 PEORL 和 SR-learner，展示 intrinsic goal 带来的灵活性和策略适应性；Montezuma's Revenge（Atari, pixel input）对比 hDQN，展示 SDRL 在 interpretability（subtask 可读）和 data efficiency（1.5M samples 达到 ~400 reward vs. hDQN 2.5M samples）方面的优势。
