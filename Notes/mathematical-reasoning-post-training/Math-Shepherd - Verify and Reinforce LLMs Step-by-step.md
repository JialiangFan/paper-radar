# Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations

## 主题
Process Reward Model Auto-Annotation

## 背景
大语言模型(LLMs)在复杂多步数学推理任务上仍面临显著挑战。验证(verification)作为一种提升推理可靠性的方法日益受到关注，其中 Process Reward Model (PRM) 通过对推理过程中的每一步进行评分，相较于仅评估最终结果的 Outcome Reward Model (ORM) 展现出更优的性能。然而，训练高质量 PRM 所需的 process supervision 数据长期依赖昂贵的人工标注（如 PRM800K 数据集），严重制约了 PRM 的规模化发展与实际应用。

## 现有局限与研究问题
- **Limitation:** 现有 PRM 训练依赖人工逐步标注推理过程的正确性（如 Uesato et al., 2022; Lightman et al., 2023），标注成本高且难以规模化，尤其对于需要高级标注技能的复杂数学推理任务。
- **Problem:** 如何在不依赖人工标注的情况下，自动构建高质量的 process supervision 数据以训练有效的 PRM？

## 贡献
- 提出了一种自动构建 process supervision 数据的框架，无需人工标注即可为数学推理任务生成逐步标签。
- 在 verification（Best-of-N reranking）和 reinforcement learning（step-by-step PPO）两个场景下验证了 Math-Shepherd 的有效性，在 GSM8K 和 MATH 基准上取得了开源模型的领先性能。
- 系统分析了影响 PRM 训练质量的关键因素（completer 能力、数据量、模型规模等），为未来自动化 process supervision 研究提供了方向。

## 方法论
- **推理步骤质量定义：** 受 Monte Carlo Tree Search 启发，将一个推理步骤的质量定义为其"推导出正确最终答案的潜力"（potential to deduce the correct answer）。
- **自动标注流程（Completion + Estimation）：** 对于给定问题的每个推理步骤 $s_i$，使用一个 fine-tuned LLM 作为 completer，从该步骤出发补全 N 条后续推理路径并获取最终答案；然后通过与 golden answer 比对来估计该步骤的质量标签。提供两种估计方式：Hard Estimation (HE) 判断是否存在至少一条正确路径，Soft Estimation (SE) 计算正确路径的比例。
- **Verification 应用：** 采用 Best-of-N 选择范式，使用 PRM 对候选解的所有步骤评分，取最小分数作为整体评分，选择最高分解作为最终答案；同时探索了与 self-consistency 结合的投票加权策略。
- **Reinforcement Learning 应用：** 将 Math-Shepherd 作为 reward model，实施 step-by-step PPO，在每个推理步骤结束时给予奖励信号（区别于传统 ORM-PPO 仅在响应末尾给予奖励），从而实现更细粒度的策略优化。
- **实验设置：** 基于 LLaMA2-7B/13B/70B、LLemma-7B/34B、Mistral-7B、DeepSeek-67B 等模型，在 GSM8K 和 MATH 数据集上进行广泛实验。使用 MetaMATH 数据训练 generator 和 completer，采样约 170k（GSM8K）和 270k（MATH）解用于构建训练数据。

> **Title:** Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations
> **Authors:** Peiyi Wang, Lei Li, Zhihong Shao, R.X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, Zhifang Sui
> **Venue:** arXiv:2312.08935
> **Year:** 2024
> **Affiliations:** Peking University, DeepSeek-AI, University of Hong Kong, Tsinghua University