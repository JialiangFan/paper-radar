# ImageNet Classification with Deep Convolutional Neural Networks

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton |
| **发表年份** | 2012 |
| **发表会议** | NeurIPS (NIPS) 2012 |
| **引用量** | 130,000+ |
| **论文链接** | [NeurIPS](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) |

## 核心问题

如何大幅提升大规模图像分类的准确率？传统计算机视觉方法已触及天花板。

## 主要贡献

### 1. AlexNet架构
一个8层深度CNN，包含5个卷积层和3个全连接层：

```
输入(227×227×3) 
→ Conv1(96, 11×11, stride 4) → ReLU → MaxPool → LRN
→ Conv2(256, 5×5) → ReLU → MaxPool → LRN
→ Conv3(384, 3×3) → ReLU
→ Conv4(384, 3×3) → ReLU
→ Conv5(256, 3×3) → ReLU → MaxPool
→ FC(4096) → ReLU → Dropout
→ FC(4096) → ReLU → Dropout
→ FC(1000) → Softmax
```
总参数量：约6000万

### 2. 关键技术创新
- **ReLU激活函数**：替代sigmoid/tanh，训练速度提升6倍，缓解梯度消失
- **GPU训练**：首次用两块GTX 580 GPU并行训练深度CNN
- **Dropout正则化**：以0.5概率随机丢弃神经元，有效防止过拟合
- **数据增强**：随机裁剪、水平翻转、颜色扰动
- **局部响应归一化（LRN）**：增强泛化（后来被BatchNorm取代）

### 3. 惊人的性能
- ILSVRC 2012 Top-5错误率：**16.4%**
- 第二名（传统方法）：**26.2%**
- 领先近**10个百分点**，这在竞赛史上前所未有

## 历史意义

- **公认的"深度学习大爆炸"起点**
- 让整个学术界和工业界相信深度学习的威力
- 之后几乎所有ILSVRC获胜者都使用深度CNN
- 直接推动了GPU制造商NVIDIA的崛起
- Ilya Sutskever后来联合创立了OpenAI

## 关键洞察

> 这篇论文的真正贡献不仅是一个更好的模型，而是**证明了一个范式**：足够大的数据 + 足够深的网络 + 足够强的算力 = 突破性性能。

## 与后续工作的关联

- VGGNet（2014）：更深更规整的架构
- GoogLeNet（2014）：Inception模块
- ResNet（2015）：残差连接，实现更深网络
- 奠定了"更大更深"的深度学习发展方向

#AI #AlexNet #CNN #computer-vision #GPU #deep-learning
