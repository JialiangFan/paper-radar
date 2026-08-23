# BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

- **Title:** BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- **Authors:** Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
- **Venue:** NAACL 2019
- **Year:** 2019
- **arXiv:** 1810.04805

## 主题
双向 Transformer 预训练语言模型，奠定现代 NLP 的基础范式

## 背景
GPT 等模型仅利用单向（从左到右）上下文进行预训练，限制了对双向语境的建模能力。ELMo 虽然结合了双向 LSTM，但属于浅层特征融合而非深度双向建模。

## 贡献

- 提出 **Masked Language Model (MLM)**：随机遮盖 15% 的输入 token，让模型预测被遮盖的词，实现深度双向上下文建模
- 提出 **Next Sentence Prediction (NSP)**：判断两个句子是否相邻，捕捉句子间关系
- 在 11 项 NLP 基准任务上取得 SOTA，包括 GLUE、SQuAD v1.1/v2.0、SWAG
- 开创了"预训练 + 微调"范式，成为后续 RoBERTa、ALBERT、XLNet 等模型的基础

## 方法论

- **架构**：Transformer Encoder（BERT-Base: 12层, 768隐藏, 12头；BERT-Large: 24层, 1024隐藏, 16头）
- **预训练**：BooksCorpus + English Wikipedia，约 3.3B 词
- **微调**：在下游任务上仅需在顶部添加简单分类层，端到端微调
