# Long Short-Term Memory

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Sepp Hochreiter, Jürgen Schmidhuber |
| **发表年份** | 1997 |
| **发表期刊** | Neural Computation, Vol. 9, No. 8 |
| **引用量** | 90,000+ |
| **论文链接** | [MIT Press](https://direct.mit.edu/neco/article/9/8/1735/6109) |

## 核心问题

传统循环神经网络（RNN）在处理长序列时面临**梯度消失/爆炸**问题，如何让网络有效地记住和遗忘长距离的信息？

## 主要贡献

### 1. LSTM单元架构
提出了包含**门控机制**的记忆单元：

```
┌─────────────────────────────────┐
│          LSTM Cell              │
│                                 │
│  遗忘门(f) ──→ ×                │
│                ↓                │
│  输入门(i) ──→ × ──→ [Cell State] ──→ 输出
│                ↑                │
│  候选值(C̃) ───┘                │
│                                 │
│  输出门(o) ──→ × ──→ hidden     │
└─────────────────────────────────┘
```

### 2. 三种门控机制
- **遗忘门（Forget Gate）**：决定丢弃多少旧信息
  - `f_t = σ(W_f · [h_{t-1}, x_t] + b_f)`
- **输入门（Input Gate）**：决定存储多少新信息
  - `i_t = σ(W_i · [h_{t-1}, x_t] + b_i)`
- **输出门（Output Gate）**：决定输出多少信息
  - `o_t = σ(W_o · [h_{t-1}, x_t] + b_o)`

### 3. 恒定误差传播（Constant Error Carousel）
细胞状态（cell state）通过加法操作更新而非乘法，使梯度能够在长序列中稳定传播，从根本上解决了梯度消失问题。

## 历史意义

- 是引用最多的AI论文之一（超过9万次引用）
- 在Transformer出现之前，LSTM是**序列建模的统治性架构**
- 广泛应用于语音识别、机器翻译、文本生成等领域
- Google用LSTM改进了语音助手和翻译服务

## 经典应用场景

- 语音识别（Siri、Google Assistant）
- 机器翻译（早期Google Translate）
- 文本生成与情感分析
- 时间序列预测（股价、天气）
- 手写体识别

## 与后续工作的关联

- GRU（2014）是LSTM的简化变体
- 注意力机制（2014）最初作为LSTM的增强提出
- Transformer（2017）最终替代了LSTM在大多数NLP任务中的地位
- 但LSTM在某些场景（小数据、实时流处理）仍有优势

#AI #LSTM #RNN #sequence-modeling #NLP
