# Improve Mathematical Reasoning by Automated Process Supervision

## 主题
Automated Process Reward Model Training

## 背景
Process supervision 通过对推理链中每一步提供中间奖励信号，已被证明优于仅关注最终答案的 Outcome Reward Model (ORM)。训练 Process Reward Model (PRM) 需要大量逐步标注的 process supervision 数据，但现有方法依赖昂贵的人工标注（如 PRM800K）或低效的暴力 Monte Carlo estimation，严重制约了 PRM 的规模化应用。Google DeepMind 提出的 OmegaPRM 算法旨在以全自动、高效的方式解决这一数据收集瓶颈。

## 现有局限与研究问题
- **Limitation:** 现有 process supervision 数据收集方法要么依赖人工标注（成本高、难以扩展），要么采用逐步 Monte Carlo rollout（计算复杂度为 O(kM)，效率低下），且正负样本不平衡，数据质量不可控。
- **Problem:** 如何在无需人工干预的前提下，高效、大规模地生成高质量的 process supervision 标注数据，用于训练更优的 PRM 以提升 LLM 的数学推理能力？

## 贡献
- 提出 OmegaPRM，一种基于 divide-and-conquer 思想的 Monte Carlo Tree Search (MCTS) 算法，用于全自动生成 process supervision 数据。
- 利用 binary search 将定位首个错误步骤的复杂度从 O(kM) 降低至 O(k log M)，并通过 MCTS 树结构复用 rollout，实现 75 倍效率提升。
- 自动收集超过 150 万条 process supervision 标注，无需任何人工参与，数据规模与质量均超越现有数据集。
- 结合 weighted self-consistency 解码，将 Gemini Pro 在 MATH500 上的准确率从 51% 提升至 69.4%，GSM8K 上从 86.4% 提升至 93.6%；Gemma2 27B 在 MATH500 上从 42.3% 提升至 58.2%。

## 方法论
- **Process Supervision 框架：** PRM 对推理链中每一步 x_t 预测正确性 p_t = PRM([q, x_{1:t-1}], x_t)，提供比 ORM 更细粒度的反馈。
- **Monte Carlo Estimation with Binary Search：** 对含错误的解答进行二分搜索，在中点处执行 k 次 rollout 并与 golden answer 比较，以 O(k log M) 复杂度定位首个错误步骤。
- **OmegaPRM (MCTS)：** 构建 state-action tree，每个节点存储访问次数 N(s)、Monte Carlo 估计值 MC(s) 和 rollout 价值函数 Q(s,r)。算法包含三个阶段：
  - **Select：** 从 rollout 池中选取最有价值的 rollout，优先选择 "supposed-to-be-correct wrong-answer" 样本（MC(s) 接近 1 但最终答案错误），使用 PUCT 变体平衡探索与利用。
  - **Binary Search：** 对选中 rollout 执行二分搜索定位首个错误，将中间节点加入树中。
  - **Maintain：** 更新树的统计信息，包括 N(s)、MC(s) 和 Q(s,r)。
- **PRM Training：** 使用 pointwise soft label（MC 估计值作为标签）的 binary cross-entropy loss 训练，实验证明优于 hard label 和 pairwise 方法（准确率 70.1% vs 63.3% vs 64.2%）。
- **Weighted Self-Consistency：** 将 PRM 分数与 majority voting 结合，用于推理时的 solution reranking。

> **Title:** Improve Mathematical Reasoning in Language Models by Automated Process Supervision
> **Authors:** Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat Phatale, Harsh Lara, Yunxuan Li, Lei Shu, Yun Zhu, Lei Meng, Jiao Sun, Abhinav Rastogi
> **Venue:** arXiv:2406.06592
> **Year:** 2024
> **Affiliations:** Google DeepMind, Google