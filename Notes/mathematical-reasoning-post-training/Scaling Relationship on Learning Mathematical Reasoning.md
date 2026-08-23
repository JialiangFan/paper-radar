# Scaling Relationship on Learning Mathematical Reasoning

## 主题
Scaling RFT for Math Reasoning

## 背景
大语言模型（LLMs）在数学推理任务上展现出显著能力，但其 scaling relationship 尚未被充分探索。现有研究主要关注 pre-training 阶段的 scaling laws，而对 supervised fine-tuning (SFT) 和数据增强对数学推理能力的影响缺乏系统性分析。本文基于 LLaMA 和 LLaMA2 系列模型，在 GSM8K 基准上系统研究了 pre-training loss、supervised data 数量以及 augmented data 数量与模型数学推理性能之间的 scaling relationship。

## 现有局限与研究问题
- **Limitation:** 已有工作主要通过 in-context learning (ICL) 或 multiple inference 提升推理性能，计算开销大且不适用于在线部署场景；对 SFT 后模型推理能力的 scaling behavior 缺乏系统研究。
- **Problem:** 如何理解并量化 pre-training loss、supervised data 规模和 augmented reasoning paths 数量对 LLM 数学推理性能的影响？如何在不依赖人工标注的情况下有效扩展训练数据以提升推理能力？

## 贡献
- 发现 pre-training loss 是比模型参数量更稳定的数学推理性能指标，与 SFT/ICL 准确率在给定区间内呈近似负线性关系。
- 揭示 SFT 性能与 supervised data 量之间存在 log-linear 关系，且更强的预训练模型从数据增量中获益更少。
- 提出 Rejection Sampling Fine-Tuning (RFT)：利用 SFT 模型自身采样生成正确推理路径作为增强数据，无需人工标注即可提升性能。
- 发现 RFT 性能的关键因素是 distinct reasoning paths 的数量，而非总样本数；通过去重和多样性选择算法（基于 Levenstein distance）可有效提升数据质量。
- 提出跨模型聚合 rejection sampling 数据（RFT-U13B/U33B），将 LLaMA-7B 在 GSM8K 上的准确率从 SFT 的 35.9% 提升至 49.3%。

## 方法论
- **实验设置：** 在 LLaMA（7B/13B/33B/65B）和 LLaMA2（7B/13B/70B）上进行实验，使用 GSM8K 数据集，评估指标为 maj1@1 和 maj1@100。
- **Pre-training loss 分析：** 对比不同系列模型（GPT-3、LLaMA、LLaMA2、GPT-4）的 pre-training loss 与 SFT/ICL 准确率的关系，验证近似线性负相关。
- **SFT 数据量实验：** 使用 {1, 1/2, 1/4, 1/8, 1/16, 1/32} 比例的 GSM8K 训练集进行 fine-tuning，观察 log-linear scaling 行为。
- **Rejection Sampling Fine-Tuning (RFT)：** 对每个训练问题，用 SFT 模型以 temperature=0.7 采样 k=100 条推理路径，通过答案校验筛选正确路径；利用 equation list 去重并基于 Levenstein distance 选择最多样化的推理路径。
- **跨模型聚合：** 将多个不同规模 SFT 模型的 rejection sampling 结果合并（如 U13B 聚合 7B/13B/7B-2/13B-2 的结果），应用去重算法后用于 fine-tuning，以获取更多样的 reasoning paths。
- **计算成本分析：** 估算 pre-training、SFT、RFT inference 和 RFT training 的 FLOPs，发现 SFT 和 RFT 的计算成本相对于 pre-training 可忽略不计。

> **Title:** Scaling Relationship on Learning Mathematical Reasoning with Large Language Models
> **Authors:** Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Keming Lu, Chuanqi Tan, Chang Zhou, Jingren Zhou
> **Venue:** arXiv:2308.01825
> **Year:** 2023
> **Affiliations:** Alibaba DAMO Academy