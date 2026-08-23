# Sample-Efficient Neurosymbolic Deep RL

## 主题
Symbolic Knowledge Transfer RL

## 背景
Deep Reinforcement Learning (DRL) 在解决复杂序列决策问题中表现出色，但其 sample inefficiency 问题严重制约了向更大规模环境的泛化能力，尤其在 planning horizon 更长、sub-goals 更多、reward 更稀疏的场景下。现有方法如 reward shaping 和 reward machines 虽能缓解部分问题，但仍存在样本效率低、对 heuristic 精度敏感等不足。本文提出 SR-DQN，一种将 symbolic knowledge 以 Answer Set Programming (ASP) 逻辑规则形式集成到 epsilon-greedy DRL 训练流程中的 neurosymbolic 方法，通过从简单域实例中学到的 partial policy 来加速复杂环境中的学习。

## 现有局限与研究问题
- **Limitation:** 标准 DRL 算法需要大量训练样本，在 long planning horizons、sparse rewards 和多 sub-goals 环境下难以泛化；现有 neurosymbolic 方法（如 reward machines）依赖精确的 sub-goal 定义或完整的 symbolic task specification，且 reward augmentation 在长 horizon 场景下效率不高。
- **Problem:** 如何利用从简单域实例中获取的不完美 (imperfect) symbolic knowledge，在不需要重新调参的前提下，同时改进 epsilon-greedy DRL 的 exploration 和 exploitation 阶段，提升 sample efficiency 和向复杂环境的泛化能力？

## 贡献
- 提出 SR-DQN 框架，通过 ASP 形式化的 partial logical policy 对 epsilon-greedy DRL 的 exploration 和 exploitation 两阶段进行 symbolic reasoning 引导：exploration 阶段偏置 action distribution 优先选择符号推理推荐的动作，exploitation 阶段根据符号知识重新缩放 Q-values。
- 引入 epsilon-decay 策略和 confidence parameter (rho) 来平衡 neural 与 symbolic 组件的影响，使训练初期更多依赖符号引导，后期逐步转向神经网络学到的策略，类似人类 fast/slow thinking 的切换。
- 该方法对不完美的 symbolic knowledge 具有鲁棒性，不要求完整的 task specification 或精确的 sub-plan 定义，且额外计算开销可忽略不计（约 1.3%-5% 时间增量）。
- 在 OfficeWorld 和 DoorKey 两个 gridworld 基准上验证，SR-DQN 在多种复杂度设定（8x8 到 16x16 地图、1-4 keys、fully/partially observable）下均显著优于标准 DQN 和 reward machine 基线 (RM-DQN)。

## 方法论
- **Logical Representation:** 使用 ASP 将 MDP 的 state 和 action space 映射为逻辑项（feature map F_F 和 action map F_A），在此基础上定义 partial logical policy (pi_ASP) 作为一组 normal rules，编码简单域实例中的策略知识。
- **SR-Exploration (Algorithm 2):** 在 exploration 阶段，对当前状态执行 ASP reasoning 得到符号推荐的动作集合 A_pi_ASP；通过 weighted probability distribution（由 confidence parameter rho 控制）优先采样这些动作，而非标准的 uniform random sampling。
- **SR-Exploitation (Algorithm 3):** 在 exploitation 阶段，先用 Q-network 计算所有动作的 Q-values，再根据符号推荐动作集合对 Q-values 进行 rescaling（乘以因子 k_a = 1 + epsilon * w_a），然后选取 rescaled 后最大 Q-value 对应的动作。
- **Epsilon-Decay 调控:** 通过 epsilon_f（最终 epsilon 值）和 epsilon_r（decay 速率）两个参数控制 symbolic 组件的影响随训练递减，实现从符号主导到神经网络主导的平滑过渡。
- **Ablation 实验:** 分别测试 SR-Exploration only 和 SR-Exploitation only 的效果，发现 SR-Exploitation 贡献更大（接近完整 SR-DQN 的性能），而 SR-Exploration 在训练早期提供更快的 return 增长；同时分析了 rho 值过高或过低都会导致次优表现，验证了 neural-symbolic 平衡的必要性。
