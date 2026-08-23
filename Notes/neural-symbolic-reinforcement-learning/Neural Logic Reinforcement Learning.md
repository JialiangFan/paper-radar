# Neural Logic Reinforcement Learning

## 主题
Logic-Based RL Policies

## 背景
Deep Reinforcement Learning (DRL) 在游戏、机器人等任务中取得了突破性进展，但其学到的 policy 依赖于 neural network 的黑箱表示，缺乏 interpretability 且难以 generalize 到训练环境之外。传统 symbolic methods 虽具备可解释性和泛化能力，但依赖已知的系统动力学模型，且在复杂任务中 scalability 较差。Differentiable Inductive Logic Programming (DILP) 作为一类可微的神经符号架构，在 supervised learning 中展现出兼顾可解释性与泛化性的优势，但尚未被应用于 sequential decision-making 场景。

## 现有局限与研究问题
- **Limitation 1:** 基于 neural network 的 DRL policy 不可解释，无法进行系统验证、调试或合规性检查，且在训练与测试环境存在差异时 generalization 能力严重不足。
- **Limitation 2:** 传统 relational RL 方法使用非可微的 symbolic reasoning，无法与现代 policy gradient 方法兼容，扩展性有限。
- **Problem:** 如何在 RL 中用 first-order logic 表示 policy，使其同时具备 interpretability、generalizability，并能通过 gradient-based 方法端到端训练？

## 贡献
- 提出 Neural Logic Reinforcement Learning (NLRL) 框架，首次将 DILP 引入 RL，用 first-order logic 表达 policy，兼容标准 policy gradient 方法。
- 设计 Differentiable Recurrent Logic Machine (DRLM)，改进了 dILP 架构，将权重直接关联到 clause 而非 clause combination，从而降低内存消耗、提升 scalability 并支持更长的 logic chaining。
- 提出 MDP with Logic Interpretation 的形式化框架，将状态编码为 ground atoms 集合、动作编码为 action predicates，通过 state encoder $p_S$ 和 action decoder $p_A$ 桥接 MDP 与 DILP。
- 在 Blocks World (STACK, UNSTACK, ON) 和 Cliff-Walking 任务上实验验证：NLRL 学到的 policy 接近最优、可解释为人类可读的逻辑规则，并能泛化到不同初始状态和更大规模的环境。

## 方法论
- **DRLM 架构：** 在 valuation vector $e \in [0,1]^{|G|}$ 上迭代执行可微逻辑推导 $f_\theta^t(e_0)$；每步通过 probabilistic sum ($a \oplus b = a + b - a \odot b$) 聚合所有 clause 的加权推导结果；权重通过 softmax 约束归一化，直接赋予每条 clause 而非 clause combination。
- **MDP with Logic Interpretation：** 定义为三元组 $(M, p_S, p_A)$：$p_S$ 将 raw state 映射为 ground atoms 的 valuation vector；DRLM 对其执行多步逻辑推导生成 action atoms 的 valuation；$p_A$ 根据 action atoms 的 valuation 确定动作概率分布（valuation 总和 $\geq 1$ 时按比例选择，$< 1$ 时将剩余概率均分给所有动作）。
- **训练：** 使用 vanilla policy gradient (REINFORCE) 结合 generalized advantage estimation (GAE, $\lambda=0.95$) 和 RMSProp ($lr=0.001$)；value function 由单隐层 neural network 估计。
- **规则模板：** 统一使用少量 rule templates（如 arity $\in \{0,1,2\}$，existential variables $\in \{0,1,2\}$），无需为特定任务手工设计辅助谓词——agent 通过训练自主发明 auxiliary invented predicates。
- **实验设计：** 在 Blocks World 三种子任务和 Cliff-Walking（含 stochastic windy 变体）上评估；泛化测试包括改变初始状态、增加 block 数量、扩大 grid 尺寸；对照组为 MLP agent 和 random agent。
