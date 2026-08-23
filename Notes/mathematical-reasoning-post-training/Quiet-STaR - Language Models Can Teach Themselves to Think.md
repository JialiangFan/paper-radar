# Quiet-STaR - Language Models Can Teach Themselves to Think

## 主题
Internal Rationale Generation for Reasoning

## 背景
语言模型在推理任务中表现有限，尽管 chain-of-thought prompting 等方法已证明中间推理步骤能显著提升性能。此前的 Self-Taught Reasoner (STaR) 方法通过在 question-answering 数据集上采样 rationale 并基于正确答案进行训练来引导推理能力，但其依赖于 curated QA datasets，泛化性和规模受限。Quiet-STaR 将 STaR 推广至任意文本，训练模型在每个 token 处生成内部 rationale 以预测后续文本，从而从多样化的非结构化语料中学习通用推理能力。

## 现有局限与研究问题
- **Limitation:** STaR 依赖 curated QA datasets 训练推理能力，仅覆盖有限的推理任务子集，难以泛化到一般文本中的隐含推理。
- **Problem:** 如何让语言模型从大规模非结构化文本中自主学习通用推理能力，而非局限于特定任务或数据集？

## 贡献
- 将 STaR 推广到任意文本数据，首次实现从非结构化文本中训练语言模型进行通用推理（reason generally）。
- 提出 tokenwise parallel sampling algorithm，在所有 token 位置并行生成 rationale，解决计算效率瓶颈。
- 引入可学习的 meta-tokens（`<|startofthought|>` 和 `<|endofthought|>`）标记 rationale 的起止边界。
- 设计 mixing head（浅层 MLP），学习将 post-rationale prediction 与 base prediction 进行插值，缓解 distribution shift。
- 提出 non-myopic loss，将多个未来 token 纳入损失函数并结合 teacher-forcing，提升 rationale 质量。
- 在无任何 fine-tuning 的情况下，GSM8K zero-shot 准确率从 5.9% 提升至 10.9%，CommonsenseQA 从 36.3% 提升至 47.2%。

## 方法论
- **Think（并行 rationale 生成）：** 对输入序列中每个 token 并行生成长度为 $t$ 的 rationale，利用 attention mask 实现高效并行推理，避免逐 token 独立 forward pass。
- **Talk（混合预测）：** 通过 mixing head 将带 rationale 的 next-token logits 与原始 base logits 加权混合，初始阶段偏向 base prediction 以保持训练稳定性。
- **Learn（优化 rationale 生成）：** 使用 REINFORCE 算法优化 rationale 参数：reward 定义为某条 rationale 的 mixed prediction log-likelihood 与所有 rationale 平均值之差；梯度同时更新 LM 参数、meta-token embeddings 和 mixing head。
- **Non-myopic scoring：** 损失函数涵盖 thought 之后的 $n_{true}$ 个 ground-truth token，结合 teacher-forcing 避免因 parallel sampling 导致的梯度缺失问题。
- **Meta-token 初始化：** 将 start/end thought token embedding 初始化为 em dash（"---"）的 embedding，并对其梯度施加超参数权重以加速优化。
- **实验设置：** 基于 Mistral 7B，在 OpenWebMath 和 C4 语料上训练，使用 8 块 80GB H100 GPU。

> **Title:** Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking
> **Authors:** Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, Noah D. Goodman
> **Venue:** arXiv:2403.09629
> **Year:** 2024
> **Affiliations:** Stanford University, Notbad AI Inc