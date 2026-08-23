# Learning Representations by Back-Propagating Errors

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams |
| **发表年份** | 1986 |
| **发表期刊** | Nature, Volume 323 |
| **引用量** | 45,000+ |
| **论文链接** | [Nature](https://www.nature.com/articles/323533a0) |

## 核心问题

如何有效训练多层神经网络？单层感知机的局限性如何突破？

## 主要贡献

### 1. 反向传播算法（Backpropagation）
提出了通过**链式法则**将输出层的误差逐层回传到隐藏层的方法：

**前向传播**：输入 → 隐藏层 → 输出层 → 计算损失

**反向传播**：
```
∂Loss/∂w = ∂Loss/∂output × ∂output/∂net × ∂net/∂w
```
- 从输出层开始，逐层计算每个权重对损失的贡献
- 使用梯度下降更新权重：`w_new = w_old - η × ∂Loss/∂w`

### 2. 隐藏层表示学习
论文证明了多层网络能自动学习有意义的**内部表示（internal representations）**——这是"表示学习"的先驱概念。

### 3. 可微分激活函数
引入了sigmoid等可微分激活函数替代硬阈值函数，使梯度计算成为可能。

## 技术细节

### 核心算法步骤：
1. **前向传播**：计算每层的输出
2. **计算损失**：比较预测与真实值
3. **反向传播**：计算每层权重的梯度
4. **更新权重**：沿梯度反方向调整

### 关键洞察：
- 链式法则使梯度可以高效地从输出层传播到任意深的隐藏层
- 隐藏层的存在使网络能够学习非线性决策边界

## 历史意义

- 彻底解决了"如何训练多层网络"的问题
- 是现代深度学习**最核心的训练算法**
- 结束了第一次AI寒冬，开启了连接主义的复兴
- 至今几乎所有神经网络都使用反向传播的变体进行训练

## 与后续工作的关联

- 直接使得LSTM、CNN等复杂架构的训练成为可能
- 现代优化器（Adam、SGD with momentum）都是基于反向传播的改进
- 自动微分框架（PyTorch、TensorFlow）本质上是反向传播的工程化实现

#AI #backpropagation #training #foundational #Hinton
