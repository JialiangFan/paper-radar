# Language Models are Few-Shot Learners

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Tom Brown, Benjamin Mann, Nick Ryder, et al. (OpenAI, 31位作者) |
| **发表年份** | 2020 |
| **发表会议** | NeurIPS 2020 |
| **引用量** | 40,000+ |
| **论文链接** | [arXiv](https://arxiv.org/abs/2005.14165) |

## 核心问题

当语言模型扩大到前所未有的规模时，会发生什么？模型能否仅通过几个示例就学会执行新任务？

## 主要贡献

### 1. 少样本学习（Few-Shot Learning）
GPT-3展示了三种不使用梯度更新的学习模式：

```
Zero-shot：  "Translate English to French: cheese =>"
One-shot：   "sea otter => loutre de mer, cheese =>"
Few-shot：   "sea otter => loutre de mer, 
              peppermint => menthe poivrée,
              cheese =>"
```

通过在提示中提供少量示例，GPT-3就能理解任务并执行，**无需任何参数更新**。

### 2. 前所未有的规模

| 指标 | 数值 |
|------|------|
| 参数量 | **1750亿 (175B)** |
| 训练数据 | 约45TB文本（过滤后约570GB） |
| 训练算力 | 约3640 PetaFLOP/s-days |
| 训练成本 | 估计约460万美元 |
| 上下文长度 | 2048 tokens |

### 3. 涌现能力（Emergent Abilities）
GPT-3展现了许多未被显式训练的能力：
- **算术运算**：两位数加减法准确率接近100%
- **代码生成**：根据自然语言描述生成代码
- **类比推理**：`"king - man + woman = queen"` 风格的推理
- **文章写作**：生成难以与人类区分的文章
- **SAT类比题**：接近大学生平均水平

### 4. In-Context Learning（上下文学习）
论文首次系统研究了**上下文学习**现象：模型通过观察提示中的示例来"学习"，而不是通过传统的梯度下降。这是一种全新的学习范式。

## Scaling Laws

论文展示了清晰的规模定律：

```
性能 ∝ log(参数量) ∝ log(数据量) ∝ log(算力)
```

从125M到175B参数，性能在几乎所有任务上**平滑且持续地提升**。

## 历史意义

- 引发了**大模型军备竞赛**
- 证明了"规模假说"——足够大的模型会涌现出意想不到的能力
- 直接催生了ChatGPT（GPT-3.5）和整个大语言模型产业
- 上下文学习成为了AI新范式
- 让"提示工程"成为一种新技能

## 局限性（论文自述）

- 文本生成中仍有重复和逻辑不一致
- 对双向任务（如填空）表现较弱
- 上下文窗口有限
- 训练成本极高，难以复现
- 无法持续学习——知识截止于训练数据

## 与后续工作的关联

- **InstructGPT**（2022）：用RLHF让GPT-3更好地遵循指令
- **ChatGPT**（2022）：GPT-3.5 + 对话微调，引爆公众关注
- **GPT-4**（2023）：多模态，更强推理能力
- 推动了LLaMA、PaLM、Claude等大模型的发展

#AI #GPT #large-language-model #few-shot #scaling #OpenAI #emergent-abilities
