# Neural Reward Machines

## 主题
Neurosymbolic Reward Automata

## 背景
Non-Markovian Reinforcement Learning 任务要求 agent 考虑完整的 state-action 历史才能做出合理决策，传统 MDP 框架无法直接处理。现有方法通常使用 Reward Machines (RMs) 等符号自动机将 temporal task specification 编译为 automaton，再与环境状态组合构造 Markovian 表示，但这依赖于已知的 symbol grounding (SG) function 将原始状态映射到逻辑符号。在 non-symbolic 环境（如图像观测）中，SG function 通常未知且难以学习，这严重限制了 RM 方法的适用范围。

## 现有局限与研究问题
- **Limitation 1:** 传统 Reward Machines 方法要求完全已知的 SG function，即环境原始状态到 propositional symbols 的精确映射，这在 non-symbolic 环境（连续状态空间、图像输入）中不可行。
- **Limitation 2:** 纯 Deep RL 方法（如 RNN+A2C）虽可处理原始输入，但无法利用任何 temporal logic 先验知识来加速学习，在复杂时序任务中表现不佳。
- **Limitation 3:** 现有 semi-supervised symbol grounding (SSSG) 研究未充分分析 reasoning shortcuts 问题——即 SG function 的多个解均与数据一致，但仅一个为正确解，其余为"捷径"。
- **Problem:** 如何在 SG function 完全未知的条件下，仍能利用 temporal logic 形式的任务先验知识来提升 non-Markovian RL 的性能？如何系统地发现 temporal specification 中不可消除的 reasoning shortcuts？

## 贡献
- 提出 Neural Reward Machines (NRMs)：一种基于 Probabilistic Moore Machines 的 neurosymbolic 框架，将逻辑推理与神经网络感知统一于单一可微模型中，支持 reasoning、learning 及两者的联合训练。
- 将 NRM 与 semi-supervised symbol grounding 和 RL 结合：在 SG function 完全未知的情况下，仅利用 symbolic task knowledge（automaton 结构）和环境 reward 反馈即可学习 symbol grounding，同时训练 RL policy。
- 提出 Unremovable Reasoning Shortcuts (URS) 的概念及高效发现算法（Algorithm 1）：仅依赖 temporal specification 的结构即可识别所有不可消除的 reasoning shortcuts，速度比暴力搜索快约 10^3 倍。
- 首次在 single RL task 中实现了在 SG function 完全未知条件下利用 temporal logic knowledge 的方法，且实验表明 NRM 性能接近拥有完整先验知识的 RM 上界。

## 方法论
- **NRM 形式化定义：** NRM = (S, P, Q, R, q0, delta_tp, delta_rp, sg)，其中 sg 为 symbol grounding probability function（将环境状态映射到符号概率向量），delta_tp 和 delta_rp 分别为 transition 和 reward 的概率版本。整体为 Probabilistic Moore Machine 的推广。
- **Neural Network 实现：** 将 Moore Machine 的离散操作松弛为连续矩阵运算。使用 temperature-controlled softmax（softmax_tau）逼近离散输出；transition matrix M_t 和 reward matrix M_r 通过 softmax_tau 处理后趋近 one-hot 编码，实现可微的逻辑归纳。SG function 可用任意神经网络（MLP 或 CNN）实现。
- **三种运行模式：** (1) Pure Reasoning——所有 NRM 参数已知，直接推理生成 reward 信号用于 augmented state RL；(2) Pure Learning——所有参数未知，通过 cross-entropy loss 从 reward 数据中学习整个 automaton；(3) Learning and Reasoning Integration——部分参数已知（如 M_t, M_r），通过数据学习未知部分（如 sg），本文重点关注此配置下的 symbol grounding 学习。
- **与 RL 的集成：** 使用 A2C 算法，将 NRM 产生的 automaton state 估计与环境 state 组合作为 augmented state 输入 policy network。SG 通过 RL 探索收集的 (state sequence, reward sequence) 数据进行训练，采用 potential-based reward shaping 提供逐步反馈。SG 训练与 RL 交替进行（每 120 episodes 更新一次 grounder，训练 100 epochs）。
- **Groundability 分析与 URS 算法：** 定义 reasoning shortcuts 为保持 formula 输出一致的非恒等 symbol 重命名。提出 Algorithm 1 在有限但完备的 symbolic support 上迭代验证候选映射，利用 absorbing state 和 working map 性质进行剪枝，高效枚举所有 URS。
- **实验设置：** 在 Minecraft 风格的 grid world 中测试，包括 map environment（2D 坐标）和 image environment（64x64x3 像素图像）。任务使用 LTL 公式定义，涵盖 Visit、Sequenced Visit、Global Avoidance 等模式，分两类难度。对比方法包括 RNN+A2C（无先验知识）和 RM+A2C（完整先验知识上界）。
- **核心结果：** NRM+A2C 性能介于 RNN+A2C 和 RM+A2C 之间，且在 map environment 中几乎收敛至 RM 水平。在所有任务中 NRM 均显著优于 RNN baseline，尤其在复杂时序任务（Class 2）中优势更明显。URS 算法在所有测试任务上比暴力方法快约 1000 倍。
