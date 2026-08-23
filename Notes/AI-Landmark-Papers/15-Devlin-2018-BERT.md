# BERT: Pre-Training of Deep Bidirectional Transformers for Language Understanding

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova (Google AI) |
| **发表年份** | 2018 (arXiv), 2019 (NAACL，最佳论文奖) |
| **发表会议** | NAACL 2019 |
| **引用量** | 100,000+ |
| **论文链接** | [arXiv](https://arxiv.org/abs/1810.04805) |

## 核心问题

如何让语言模型真正理解上下文？之前的模型（如GPT-1）只能从左到右单向处理，无法同时利用左右两侧的上下文信息。

## 主要贡献

### 1. 双向预训练（Bidirectional Pre-training）
BERT使用Transformer的**编码器（Encoder）**，能同时看到一个词的左右上下文：

```
GPT（单向）：   [The] [cat] [sat] → 只能看左边来预测右边
BERT（双向）：  [The] [?] [sat] → 同时看左右来预测中间
```

### 2. 掩码语言模型（Masked Language Model, MLM）
- 随机遮盖输入中**15%**的token
- 让模型预测被遮盖的词
- 这迫使模型学习双向上下文表示

遮盖策略：
- 80%替换为 [MASK]
- 10%替换为随机词
- 10%保持不变

### 3. 下一句预测（Next Sentence Prediction, NSP）
训练模型判断两个句子是否在原文中相邻，帮助模型理解句子间的关系。

### 4. "预训练+微调"范式
```
预训练（无监督）          微调（有监督）
大规模语料 → BERT → 通用语言表示 → + 少量标注数据 → 具体任务
                                    ↓
                              问答 / 分类 / NER / ...
```

## 模型规格

| 版本 | 层数 | 隐藏维度 | 注意力头 | 参数量 |
|------|------|----------|----------|--------|
| BERT-Base | 12 | 768 | 12 | 110M |
| BERT-Large | 24 | 1024 | 16 | 340M |

## 性能突破

BERT在发布时刷新了**11项NLP基准测试**的最佳成绩：
- GLUE benchmark：+7.7%
- SQuAD v1.1（问答）：超越人类
- SQuAD v2.0：+5.1 F1

## 历史意义

- 开创了NLP的**"预训练+微调"时代**
- 证明了**双向上下文**对语言理解的重要性
- Google搜索引擎在2019年集成了BERT，影响了10%的搜索结果
- 使NLP从"特征工程"时代进入"预训练模型"时代

## 与后续工作的关联

- RoBERTa（2019）：优化BERT训练策略
- ALBERT（2019）：轻量化BERT
- GPT-2/3选择了另一条路：更大的单向模型 + 少样本学习
- 现代大模型综合了BERT的双向理解和GPT的生成能力

#AI #BERT #NLP #pretraining #language-model #Transformer
