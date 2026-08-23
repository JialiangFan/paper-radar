# NSAM: Neuro-symbolic Action Masking for Deep RL

## 主题
Symbolic Action Masking

## 背景
Deep reinforcement learning (DRL) 在自动驾驶、资源管理、算法交易等复杂领域取得了显著成功，但在实际场景中，智能体常常探索不可行（infeasible）的动作，导致违反 domain constraints。现有的 neuro-symbolic RL 方法通常依赖预定义的 symbol grounding function 将高维状态映射为符号表示，并手动指定 action masking 规则，这在状态空间高维或无限时往往不切实际。因此，如何自动从高维数值状态中学习符号模型并据此过滤不安全动作，是一个关键的开放问题。

## 现有局限与研究问题
- **Limitation 1:** 现有方法假设存在预定义的 symbolic grounding function，需要完整的环境先验知识，当状态空间高维或连续时难以手工构建。
- **Limitation 2:** 获取每个状态的完整符号真值标注（full supervision）在 DRL 环境中不现实，因为环境很少提供逐状态的 ground-truth symbolic description。
- **Limitation 3:** 符号推理过程本质上不可微（non-differentiable），与基于梯度的 DRL 算法难以兼容，阻碍了 end-to-end 训练。
- **Problem:** 如何在 minimal supervision 下自动学习符号模型，并将其无缝集成到 gradient-based DRL 中，以 end-to-end 的方式同时优化 symbolic grounding 与 policy learning？

## 贡献
- 提出 NSAM (Neuro-symbolic Action Masking) 框架，首次实现从高维数值状态自动学习符号模型并构建 action mask，无需预定义 symbol grounding function。
- 引入 Probabilistic Sentential Decision Diagrams (PSDDs) 作为核心符号结构：PSDD 天然满足 domain constraints，同时支持可微的参数学习，弥合了符号推理与梯度优化之间的鸿沟。
- 设计了 end-to-end 训练框架（Algorithm 1），在训练过程中交替更新 gating function（symbolic grounding）和 policy network，使两者相互增强。
- 仅需 minimal supervision：利用 action explorability 反馈 (s, a, s', y) 自动标注，无需逐状态的完整符号标注。
- 在四个约束决策域（Sudoku、N-Queens、Graph Coloring、Visual Sudoku）上进行了系统实验，在 sample efficiency 和 constraint violation rate 两个指标上均显著优于 Rainbow、PPO、PPO-Lagrangian、KCAC、RC-PPO、PLPG 等基线方法。

## 方法论
- **问题建模：** 将标准 MDP 扩展为包含 atomic propositions P、action preconditions AP 和 domain constraint phi 的增强 MDP，其中每个动作的可执行性由 precondition 和 constraint 共同决定。
- **知识编译（Knowledge Compilation）：** 将 domain constraint phi 编译为 Sentential Decision Diagram (SDD)，再参数化为 PSDD。SDD 是一种规范化的 Boolean circuit，保证所有满足约束的模型具有非零概率，而违反约束的模型概率为零。
- **Symbolic Grounding 学习：** 使用 neural gating function g 将高维状态 s 映射为 PSDD 参数 Theta = g(s)，使 PSDD 在给定状态下输出满足约束的 symbolic model 的概率分布 Pr(m | Theta, m |= phi)。通过 cross-entropy loss 与 explorability label y 进行训练。
- **符号推理与动作屏蔽：** 对当前状态执行 MAP inference 获取最可能的 symbolic model m-hat，再根据每个动作的 precondition phi 评估 C_phi(m-hat)，构建 symbolic mask。将 policy network 的输出概率与 mask 相乘并重归一化，屏蔽不可行动作。
- **End-to-End 训练：** 在每个 episode 中，智能体与环境交互时同步收集 (s, a, s', y) 反馈存入 buffer D；定期从 D 中采样更新 gating function g（Eq. 3），同时通过 masked PPO（Eq. 6）更新 policy network。两个模块交替优化、相互促进。
- **关键设计优势：** PSDD 的 MAP inference 可在线性时间内完成（利用 decomposability 和 determinism 性质），使实时 action masking 在 DRL 中可行；0-1 masking 加重归一化保留了有效的 policy gradient，保证了优化的理论正确性。
