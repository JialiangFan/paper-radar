# Attention Is All You Need

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin |
| **发表年份** | 2017 |
| **发表会议** | NeurIPS (NIPS) 2017 |
| **引用量** | 173,000+（21世纪引用量前十） |
| **论文链接** | [arXiv](https://arxiv.org/abs/1706.03762) |

## 核心问题

RNN/LSTM处理序列数据时必须逐步计算，无法并行化。能否完全抛弃循环结构，仅用注意力机制构建序列模型？

## 主要贡献

### 1. Transformer架构
一个完全基于注意力机制的编码器-解码器架构：

```
┌─────────────────┐     ┌─────────────────┐
│    ENCODER ×N   │     │    DECODER ×N   │
│                 │     │                 │
│  Multi-Head     │     │  Masked         │
│  Self-Attention │────→│  Multi-Head     │
│       ↓         │     │  Self-Attention │
│  Add & Norm     │     │       ↓         │
│       ↓         │     │  Add & Norm     │
│  Feed Forward   │     │       ↓         │
│       ↓         │     │  Cross-Attention│
│  Add & Norm     │     │       ↓         │
└─────────────────┘     │  Add & Norm     │
                        │       ↓         │
                        │  Feed Forward   │
                        │       ↓         │
                        │  Add & Norm     │
                        └─────────────────┘
```

### 2. 缩放点积注意力（Scaled Dot-Product Attention）
```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```
- **Q (Query)**：我在找什么？
- **K (Key)**：我有什么可以提供？
- **V (Value)**：我实际包含的信息
- **√d_k 缩放**：防止点积过大导致softmax饱和

### 3. 多头注意力（Multi-Head Attention）
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W_O
其中 head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```
不同的"头"可以关注不同类型的关系（语法、语义、位置等）。

### 4. 位置编码（Positional Encoding）
由于Transformer没有循环结构，需要显式注入位置信息：
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

## Transformer vs RNN/LSTM

| 特性 | RNN/LSTM | Transformer |
|------|----------|-------------|
| 并行化 | 不可能 | 完全并行 |
| 长距离依赖 | 困难 | 直接连接 |
| 训练速度 | 慢 | 快得多 |
| 计算复杂度 | O(n) | O(n²)（但可并行） |
| 可扩展性 | 有限 | 极强 |

## 历史意义

- **毫无疑问是21世纪最重要的AI论文**
- GPT、BERT、T5、PaLM、LLaMA、Claude……几乎所有现代大模型都基于Transformer
- 不仅统治了NLP，还征服了计算机视觉（ViT）、语音、蛋白质结构预测等领域
- 8位作者后来分别创立/加入了多家AI公司

## 论文标题的深意

> "Attention Is All You Need" 不仅是一个技术声明——不需要RNN，只需要注意力——更是一种宣言：注意力机制本身就足以构建强大的序列模型。

## 与后续工作的关联

- **BERT**（2018）：仅使用Encoder
- **GPT系列**（2018-2023）：仅使用Decoder
- **ViT**（2020）：将Transformer应用于图像
- **扩散模型**：很多使用Transformer作为骨干网络
- 所有现代大语言模型的基础架构

#AI #Transformer #attention #NLP #foundational #architecture
