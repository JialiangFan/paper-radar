# Gradient-Based Learning Applied to Document Recognition

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Yann LeCun, Léon Bottou, Yoshua Bengio, Patrick Haffner |
| **发表年份** | 1998 |
| **发表期刊** | Proceedings of the IEEE, Vol. 86, No. 11 |
| **引用量** | 50,000+ |
| **论文链接** | [IEEE Xplore](https://ieeexplore.ieee.org/document/726791) |

## 核心问题

如何设计一个端到端的系统，直接从原始像素学习到识别结果，而不需要手工设计特征？

## 主要贡献

### 1. LeNet-5架构
提出了经典的卷积神经网络架构：

```
输入(32×32) → Conv1(6@28×28) → Pool1(6@14×14) → Conv2(16@10×10) 
→ Pool2(16@5×5) → FC1(120) → FC2(84) → 输出(10)
```

### 2. 卷积神经网络的核心概念
- **局部感受野（Local Receptive Fields）**：每个神经元只看输入的一小部分
- **权重共享（Weight Sharing）**：同一个卷积核在整个图像上滑动
- **池化（Pooling/Subsampling）**：降低空间维度，增加平移不变性
- **多层特征提取**：从低级边缘到高级语义的层次化特征

### 3. 端到端学习
论文展示了从原始像素到最终分类的完整可训练流水线，无需手工特征工程。

### 4. Graph Transformer Network
论文还提出了GTN的概念——将多个可训练模块组合成更大的可训练系统。

## 技术影响

### CNN的核心设计原则：
1. **平移不变性**：物体在图像中的位置不影响识别
2. **参数效率**：权重共享大幅减少参数量
3. **层次化特征**：底层→边缘，中层→纹理，高层→物体部件

## 历史意义

- 成功应用于美国银行支票上的手写数字识别
- 确立了CNN作为**图像识别标准架构**的地位
- LeCun因此工作（与Hinton、Bengio一起）获得2018年图灵奖
- LeNet是所有现代CNN（AlexNet、VGG、ResNet等）的祖先

## 与后续工作的关联

- AlexNet（2012）是LeNet的规模化版本
- 所有现代计算机视觉架构（ResNet、EfficientNet等）都基于CNN
- 即使是Vision Transformer（ViT），其patch embedding也可视为一种卷积操作

#AI #CNN #computer-vision #LeCun #deep-learning
