# Dylan: Guiding Deep RL with Differentiable Symbolic Planning

## 主题
Differentiable Symbolic Planning

## 背景
Reinforcement Learning (RL) 在游戏、机器人控制和 LLM post-training 等领域取得了显著成果，但在 sparse reward 环境下面临探索效率低、收敛缓慢的问题。人类在面对复杂任务时会自然地将其分解为子任务并根据观察动态调整计划，而现有 RL agent（如 PPO）缺乏这种 prior knowledge，需要大量交互才能学会类似行为。Reward shaping 是缓解该问题的常见手段，但传统方法依赖手工 potential function 或 preference-based learning，缺乏可解释性和组合泛化能力。

## 现有局限与研究问题
- **Limitation 1:** 传统 reward shaping 方法（potential-based、auxiliary task、preference-based）要么依赖手工启发式、要么生成的 reward 不透明且难以泛化，无法与人类意图语义对齐。
- **Limitation 2:** 经典 symbolic planner（如 STRIPS）是非自适应的（non-adaptive），使用固定搜索策略（DFS/BFS），在存在环路或高分支因子的任务中容易陷入无限循环或效率低下。
- **Limitation 3:** 标准 RL agent 通常 overfit 到单一任务，缺乏模块化组合能力，面对新任务需重新训练。
- **Problem:** 能否设计一个既可作为 reward model 提供可解释中间反馈、又可作为 high-level planner 组合 policy primitives 实现泛化的可微分符号规划框架？

## 贡献
- 提出 Dylan（**d**ifferentiable s**y**mbolic p**lan**ner），首个将 differentiable symbolic planning 集成到 RL 中的框架，同时作为 reward model 提供可解释的、与人类意图对齐的中间奖励信号。
- Dylan 超越单纯 reward shaping 角色，还可作为 differentiable planner，在 hierarchical RL 中充当 high-level policy，通过组合 policy primitives 以模块化方式生成新行为，无需重训练即可泛化到未见任务。
- 通过 learnable weight matrix W 和 gradient descent 优化，Dylan 能自适应选择搜索策略（DFS vs. BFS），克服传统 symbolic planner 的非自适应缺陷。

## 方法论
- **符号化表示:** 利用 LLM (GPT-4o) 从环境手册中提取 first-order logic 规则，将任务分解为 STRIPS 风格的 symbolic transitions（precondition -> action -> postcondition），再经人工验证和修正。
- **可微分前向推理 (Differentiable Forward Chaining):** 将 planning rules 编码为 tensor $\mathbf{I}_i \in \mathbb{N}^{G \times S \times L}$；引入 learnable weight matrix $\mathbf{W} = [\mathbf{w}_1, \dots, \mathbf{w}_M]$，通过 softmax 得到 soft rule selection 概率；每步用 soft logical AND (gather + product) 和 soft OR (softor) 进行可微推理，逐步更新 valuation vector $\mathbf{v}^{(t)}$。
- **Dylan as Static Reward Model (Sec 3.1):** 给定环境逻辑状态和目标，Dylan 推理生成最优 plan $[a_1, a_2, \dots, a_n]$；设计 sequential reward function $r_{\text{reasoner}}$，仅当 agent 按顺序完成子目标时给予奖励，并根据步数效率进行惩罚；shaped reward = 环境奖励 + reasoner 辅助奖励。
- **Dylan as Adaptive Reward Model (Sec 3.2):** 在 static 基础上引入 dense reward $r_{\text{adaptive}}$，利用 log-sum-exp 聚合所有候选 plan 的概率，每步动态评估 agent 进展；通过缩放因子 $\omega$ 和偏移 $\lambda$ 确保 dense auxiliary reward 始终为负，避免 agent 停滞在零奖励吸收态。
- **Dylan as Differentiable Planner (Sec 3.3):** 独立于 RL 训练，直接组合多个 policy primitives（如 get_key、go_through_door）生成新行为；weight matrix W 通过 BCE loss + gradient descent 优化，自适应在 DFS 和 BFS 之间切换搜索策略，避免传统 planner 的无限循环问题。
- **实验评估 (MiniGrid-DoorKey):**
  - Q1 (Static Reward Model): 在 12x12 和 16x16 环境中，PPO+Dylan 和 A2C+Dylan 显著提升收敛速度，尤其在高复杂度 16x16 中优势更明显（baseline 无法收敛）。
  - Q2 (Adaptive Reward Model): 在 8x8 环境中，adaptive reward 比 static reward 进一步加速收敛。
  - Q3 (Compositional Generalization): Dylan 组合 policy primitives 在多种未见任务上达到 100% 成功率（Key Retrieval、Red Door Reaching、Goal Reaching），safe goal reaching 达 98.2%，远超 PPO/A2C baseline。
  - Q4 (Adaptive Search): Dylan 学会对不同任务自动选择 DFS 或 BFS 策略，loss 曲线收敛验证了自适应能力。

## 局限性
- 依赖环境直接提供的 symbolic state，尚未从原始视觉观测中自动提取符号表示。
- 游戏规则由 GPT-4o 生成后需人工校验，自动化 error-correction 机制有待研究。

## 信息
- **作者:** Zihan Ye, Oleg Arenz, Kristian Kersting (TU Darmstadt / hessian.AI / DFKI)
- **来源:** arXiv:2505.11661, 2025, Preprint (under review)
