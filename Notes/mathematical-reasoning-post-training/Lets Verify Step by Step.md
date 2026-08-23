# Let's Verify Step by Step

## 主题
Process Supervision for Reward Models

## 背景
大语言模型在 multi-step reasoning 任务中表现日益强大，但即使是最先进的模型仍然频繁产生逻辑错误和 hallucination。为了训练更可靠的模型，可以使用 reward model 来区分优劣输出，进而通过 reinforcement learning 或 rejection sampling 来改善推理质量。训练 reward model 的监督信号有两种范式：outcome supervision（仅对最终答案提供反馈）和 process supervision（对每一步推理提供反馈），但二者的优劣对比尚未被充分研究。

## 现有局限与研究问题
- **Limitation:** Outcome supervision 仅依据最终答案的正误来训练 reward model，无法精确定位推理链中的错误位置，导致 credit assignment 困难；此外，推理正确但答案碰巧正确的 false positive 会污染训练信号。
- **Problem:** 在数学推理这一高难度场景下，process supervision 是否能训练出比 outcome supervision 更可靠的 reward model？如何高效收集 step-level 的人类反馈数据？

## 贡献
- 在 MATH 数据集上系统比较了 outcome-supervised reward model (ORM) 与 process-supervised reward model (PRM)，证明 PRM 显著优于 ORM（best-of-1860 准确率：78.2% vs 72.4%）
- 证明大规模 PRM 可以可靠地替代人类标注者，用于为小规模模型提供 synthetic process supervision，从而大幅降低数据收集成本
- 提出基于 active learning 的数据收集策略（优先标注 convincing wrong-answer solutions），使 process supervision 的数据效率提升约 2.6 倍
- 公开发布 PRM800K 数据集，包含约 800,000 条 step-level 人类反馈标签，覆盖 75K 个解题过程

## 方法论
- **实验框架:** 固定一个 generator 模型生成候选解，单独训练 reward model 进行 best-of-N 选择，以选中正确解的比例评估 reward model 的可靠性
- **Base model:** 所有大规模模型基于 GPT-4 微调，额外使用约 1.5B token 的数学相关语料（MathMix）进行预训练增强
- **ORM 训练:** 对每个问题均匀采样解，根据最终答案正误作为 label，在 solution 最后一个 token 处输出预测分数
- **PRM 训练:** 人类标注者对每一步标记 positive / negative / neutral，PRM 预测每步的正确概率；solution 级别分数定义为所有步骤正确概率的乘积
- **Active learning:** 使用小规模 PRM_selector 筛选出最具欺骗性的 wrong-answer solutions（被当前 PRM 评分高但答案错误的解）优先送标，迭代更新 PRM 并重复
- **Small-scale synthetic ablation:** 使用大规模 PRM_large 作为 labelling oracle 为小模型提供 process / outcome supervision，在受控条件下验证 process supervision 在所有数据规模上均优于 outcome supervision
- **OOD 泛化验证:** 在 AP Physics、AP Calculus、AP Chemistry、AMC10/12 等域外 STEM 测试上确认 PRM 的优势具有泛化性（aggregate best-of-100: PRM 72.9% vs ORM 63.8%）

> **Title:** Let's Verify Step by Step
> **Authors:** Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, Karl Cobbe
> **Venue:** arXiv:2305.20050
> **Year:** 2023
> **Affiliations:** OpenAI