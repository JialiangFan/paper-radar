# Towards Deep Symbolic Reinforcement Learning

> Garnelo, Arulkumaran & Shanahan, 2016 (Imperial College London) | arXiv:1609.05518

## 主题
Deep Symbolic RL Foundation

## 背景
Deep reinforcement learning (DRL) 已在 Atari 游戏和围棋等任务中展现出强大能力，但其本质上继承了 deep learning 的若干根本性缺陷。传统 symbolic AI 虽具备 compositional representation 和 high-level reasoning 的优势，却长期受困于 symbol grounding problem，即符号语义依赖人工设计而非从真实数据中学习。本文提出将 neural network 与 symbolic reasoning 结合的 end-to-end 架构，试图同时克服两者的不足。

## 现有局限与研究问题
- **Limitation 1:** 当前 DRL 系统需要极大规模的训练数据，学习效率低下（data inefficiency）。
- **Limitation 2:** 系统缺乏 abstract reasoning 能力，无法进行 transfer learning、analogical reasoning 和 causal reasoning。
- **Limitation 3:** DRL 模型的决策过程对人类不透明（opaque），在需要 verifiability 的领域中不适用。
- **Limitation 4:** 传统 symbolic AI 的 symbol grounding problem 使其无法从原始感知数据中自主学习。
- **Problem:** 如何设计一个架构，既能利用 neural network 从 raw perception 中自动学习 symbolic representation，又能通过 symbolic reasoning 实现 data-efficient、可迁移且可解释的 reinforcement learning？

## 贡献
- 提出了一种 hybrid neural-symbolic RL 架构：neural back end 负责将 raw sensory input 无监督地映射为 compositionally structured symbolic representation，symbolic front end 负责基于该表征进行 action selection。
- 明确了该架构的四项核心设计原则：**conceptual abstraction**（概念抽象）、**compositional structure**（组合结构）、**common sense priors**（常识先验）、**causal reasoning**（因果推理）。
- 实现了一个 proof-of-concept 系统，在简单游戏的四个变体上验证了有效性。
- 实验表明，在 stochastic environment（物体随机放置）中，该系统显著优于 DQN，展现出更强的 data efficiency 和 transfer learning 能力。

## 方法论
- **整体架构：** 由 neural back end + symbolic front end 构成的 end-to-end pipeline，包含三个阶段：low-level symbol generation、representation building、reinforcement learning。
- **Low-level symbol generation：** 使用 convolutional autoencoder 以无监督方式从 raw pixel 中提取 salient object，通过 activation spectrum 比较对物体进行类型分类（type assignment）。
- **Representation building（表征构建）：**
  - **Object tracking：** 综合三种度量实现跨帧物体追踪——spatial proximity ($L_{dist} = \frac{1}{1+d}$)、type transition probability ($L_{trans}$，基于学习到的 transition matrix)、neighbourhood similarity ($L_{neigh} = \frac{1}{1+\Delta N}$)；加权组合为 $L = w_1 L_{dist} + w_2 L_{trans} + w_3 L_{neigh}$。
  - **Symbolic interaction extraction：** 将 absolute position 转化为 relative position，构建以物体间 interaction 为核心的 spatio-temporal representation（包含类型变化和相对位移）。
- **Reinforcement learning：** 为每对 object type interaction 训练独立的 Q function（tabular Q-learning），action selection 时对所有相关 Q value 求和取 argmax：$a_{t+1} = \arg\max_a \sum_Q Q(s_{t+1}, a)$；采用 $\epsilon$-greedy 策略（$\epsilon = 0.1$）。
- **Common sense priors：** 在 ontology 层面内建物体持续性（object persistence）、外观相似则行为相似等常识假设，减少学习负担。

## 实验
- **Benchmark：** 四个简单游戏变体——(1) 单类物体/网格布局，(2) 双类物体/网格布局，(3) 单类物体/随机布局，(4) 双类物体/随机布局。
- **关键结果：** 在随机布局的双类物体变体中，DQN 在 1000 epochs 内未能超越随机水平，而本系统在约 200 epochs 内即学到有效策略，正确收集正奖励物体的比例达到约 70%。
- **Transfer learning：** 在网格变体上训练后直接测试随机变体，学习曲线与直接在随机变体上训练相当，证明了 symbolic representation 的迁移能力。
- **可解释性：** 由于 symbolic front end 基于显式的 Q function（每个描述特定 object type interaction），决策过程可被人类追溯和理解。

## 局限性
- 仅在极简的游戏环境中验证，neural back end 较浅，symbolic front end 的推理能力有限。
- Object tracking 中的权重 $w_1, w_2, w_3$ 为手动设定，未自动学习。
- Locality assumption 导致无法保证收敛到全局最优策略。
- 系统整体仍为 preliminary proof-of-concept，距离通用应用尚有较大距离。

## 未来方向
- 引入 inductive logic programming 实现更强的 generalization。
- 集成 analogical reasoning 技术（如 structure mapping engine）。
- 加入 planning component 以利用学到的 causal structure 进行 off-line exploration。
- 采用更先进的 unsupervised learning 方法（如 disentangled representation learning）以处理更复杂的视觉输入。
