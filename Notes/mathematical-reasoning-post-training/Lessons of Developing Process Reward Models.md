# Lessons of Developing Process Reward Models

## 主题
Process Reward Model Development

## 背景
Process Reward Models (PRMs) 是一种用于数学推理中过程监督的方法，旨在识别和纠正 LLMs 推理过程中的中间错误。当前 PRM 的开发面临数据标注和评估方法两大核心挑战：广泛使用的 Monte Carlo (MC) estimation 方法在数据合成方面表现不佳，而 Best-of-N (BoN) 评估存在系统性偏差。本文由 Alibaba Qwen 团队发表，通过大量实验总结了 PRM 开发中的关键经验教训，并发布了 state-of-the-art 的开源 PRM 模型。

## 现有局限与研究问题
- **Limitation 1:** MC estimation 数据合成方法依赖 completion model 评估当前步骤正确性，但 completion model 可能从错误步骤生成正确答案，或从正确步骤生成错误答案，引入大量噪声，导致训练出的 PRM 在性能和泛化能力上显著弱于 LLM-as-a-judge 和 human annotation 方法。
- **Limitation 2:** BoN 评估仅关注最终答案的正确性，与 PRM 的过程验证目标存在根本性 misalignment——policy model 常生成答案正确但推理过程有误的 response，导致 BoN 分数虚高。
- **Limitation 3:** 现有 PRM 的 minimum score 大量集中在最终步骤，表明模型从 process-oriented 退化为 outcome-oriented 评估，本质上变成了 ORM。
- **Problem:** 如何构建更高质量的训练数据并设计更全面的评估框架，以开发真正有效的 PRM？

## 贡献
- 系统揭示了 MC estimation 数据合成的关键缺陷：相比 LLM-as-a-judge 和 human annotation，MC estimation 在 ProcessBench 错误定位任务上表现最差，尽管其数据量最大。
- 揭示了 BoN 评估的三大系统性偏差：policy model 的不可靠性导致 BoN-PRM misalignment、PRM 有限的过程验证能力导致 BoN 分数膨胀、以及模型优化导致的 process-to-outcome shift。
- 提出了一种 consensus filtering 机制，结合 MC estimation 与 LLM-as-a-judge，仅保留两者对错误位置达成共识的样本，在仅使用约 40% 数据的情况下显著提升了模型性能和数据效率。
- 发现 hard labels（阈值为 0）优于 soft labels，且不同训练数据源的 PRM 在 BoN 中具有不同的最优 scoring strategy（MC estimation 适合 last score，LLM-as-a-judge/human annotation 适合 product/minimum）。
- 发布了 Qwen2.5-Math-PRM-7B 和 Qwen2.5-Math-PRM-72B，在 BoN 和 ProcessBench 上均超越现有开源 PRM。

## 方法论
- **数据构建（Data Expansion）：** 基于约 50 万条 query，使用 Qwen2-Math-Instruct 和 Qwen2.5-Math-Instruct 系列模型生成 6-8 条 response，按 `\n\n` 分割步骤，对每步进行 8 次 MC completion 评估正确性，使用 hard labels（任一 completion 到达正确答案即为正确，阈值为 0）。
- **Consensus Filtering（数据过滤）：** 使用 Qwen2.5-Instruct-72B 作为 LLM-as-a-judge 逐步验证 response，仅保留 LLM-as-a-judge 与 MC estimation 对错误步骤位置达成一致的样本，过滤后仅保留约 40% 数据。
- **模型训练：** 基于 Qwen2.5-Math-7B/72B-Instruct 初始化，替换 language modeling head 为 scalar-value head（两层线性层），在每步最后一个 token 上使用 cross-entropy loss 进行二分类训练。
- **评估框架：** 结合 response-level 的 Best-of-N（prm@8）评估和 step-level 的 ProcessBench 错误定位评估，避免单一 BoN 评估的偏差，全面衡量 PRM 的过程验证能力。

> **Title:** The Lessons of Developing Process Reward Models in Mathematical Reasoning
> **Authors:** Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen Zhang, Runji Lin, Bowen Yu, Dayiheng Liu, Jingren Zhou, Junyang Lin
> **Venue:** arXiv:2501.07301
> **Year:** 2025
> **Affiliations:** Qwen Team, Alibaba Group