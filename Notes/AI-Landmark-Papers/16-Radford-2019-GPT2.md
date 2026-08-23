# Language Models are Unsupervised Multitask Learners

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever (OpenAI) |
| **发表年份** | 2019 |
| **发表形式** | OpenAI技术报告（未经同行评审） |
| **引用量** | 15,000+ |
| **论文链接** | [OpenAI](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) |

## 核心问题

能否训练一个**通用的语言模型**，不需要针对每个任务进行微调，就能完成多种NLP任务？

## 主要贡献

### 1. 零样本多任务学习（Zero-Shot Multitask Learning）
GPT-2证明了一个足够大的语言模型可以在**零样本**（zero-shot）条件下完成多种任务：
- 机器翻译：`"translate English to French: ..."`
- 摘要生成：`"TL;DR: ..."`
- 问答：`"Q: ... A:"`
- 阅读理解

这些任务无需任何标注数据或微调。

### 2. 规模化（Scaling）
| 版本 | 参数量 | 层数 | 隐藏维度 |
|------|--------|------|----------|
| GPT-2 Small | 117M | 12 | 768 |
| GPT-2 Medium | 345M | 24 | 1024 |
| GPT-2 Large | 774M | 36 | 1280 |
| GPT-2 XL | **1.5B** | 48 | 1600 |

论文的核心发现：**性能随模型规模和数据规模的增加而持续提升**，没有出现饱和。

### 3. WebText数据集
- 从Reddit高质量链接爬取
- 800万个网页文档，约40GB文本
- 相比之前的数据集质量大幅提升

### 4. 文本生成质量的飞跃
GPT-2生成的文本质量之高，以至于OpenAI最初**拒绝公开完整模型**，担心被滥用生成虚假新闻。这是AI领域首次因安全考虑延迟发布模型。

## 核心思想

> **语言模型本质上就是多任务学习器**。预测下一个词的过程中，模型隐含地学会了翻译、摘要、推理等多种能力。

```
p(output | input) ≈ p(output | input, task)
```
当模型足够大时，它能从输入的格式中推断出应该执行什么任务。

## 历史意义

- 提出了**"规模就是一切"（Scaling Hypothesis）**的早期证据
- 开创了**提示工程（Prompt Engineering）**的先河
- 引发了AI安全和负责任发布的广泛讨论
- 为GPT-3的"少样本学习"奠定了基础
- Dario Amodei（本文共同作者）后来创立了Anthropic

## 与后续工作的关联

- **GPT-3**（2020）：将规模扩大100倍，实现少样本学习
- 确立了"更大的模型 = 更强的能力"这一趋势
- 推动了整个AI领域从"微调"转向"提示"的范式转变

#AI #GPT #language-model #zero-shot #OpenAI #scaling
