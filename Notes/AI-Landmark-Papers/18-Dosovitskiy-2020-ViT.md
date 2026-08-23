# An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, et al. (Google Brain) |
| **发表年份** | 2020 (arXiv), 2021 (ICLR) |
| **发表会议** | ICLR 2021 |
| **引用量** | 45,000+ |
| **论文链接** | [arXiv](https://arxiv.org/abs/2010.11929) |

## 核心问题

Transformer在NLP中取得了巨大成功，它能否**直接应用于计算机视觉**，替代统治了近10年的CNN？

## 主要贡献

### 1. Vision Transformer (ViT) 架构
将图像视为一个"词序列"：

```
输入图像 (224×224)
    ↓
切分为 patch (16×16)  →  14×14 = 196 个 patch
    ↓
每个 patch 展平并线性投影  →  196 个 token (每个维度 D)
    ↓
加上 [CLS] token + 位置编码  →  197 个 token
    ↓
送入标准 Transformer Encoder (L层)
    ↓
[CLS] token 的输出 → MLP Head → 分类结果
```

### 2. 关键发现：规模是关键

| 数据规模 | ViT vs CNN |
|----------|------------|
| ImageNet (1.3M) | ViT **不如** CNN |
| ImageNet-21k (14M) | ViT ≈ CNN |
| JFT-300M (300M) | ViT **大幅优于** CNN |

核心洞察：ViT缺乏CNN的**归纳偏置**（局部性、平移不变性），因此需要更多数据来学习这些特性，但一旦有足够数据，ViT的上限更高。

### 3. ViT模型变体

| 模型 | 层数 | 隐藏维度 | 头数 | 参数量 |
|------|------|----------|------|--------|
| ViT-Base | 12 | 768 | 12 | 86M |
| ViT-Large | 24 | 1024 | 16 | 307M |
| ViT-Huge | 32 | 1280 | 16 | 632M |

## 为什么把图像切成 patch？

直接对每个像素做自注意力，224×224=50176个token，计算量 O(n²) 是不可承受的。切成16×16的patch后，只有196个token，计算量降低了约65000倍。

## CNN vs ViT

| 特性 | CNN | ViT |
|------|-----|-----|
| 归纳偏置 | 强（局部性、平移不变性） | 弱 |
| 数据效率 | 高（小数据也行） | 低（需要大数据） |
| 可扩展性 | 有限 | 极强 |
| 全局关系 | 需要很深的网络 | 第一层就能捕获 |
| 性能上限 | 较低 | 更高 |

## 历史意义

- 打破了CNN在计算机视觉中近10年的统治
- 证明了Transformer是一个**通用架构**，不限于NLP
- 推动了视觉与语言的**统一建模**
- 论文标题 "An Image is Worth 16x16 Words" 已成为经典

## 与后续工作的关联

- **DeiT**（2021）：用知识蒸馏在ImageNet上训练ViT
- **Swin Transformer**（2021）：引入层次化和窗口注意力
- **CLIP**（2021）：ViT + 文本，视觉-语言对齐
- **DALL-E、Stable Diffusion**：Transformer/ViT在生成模型中的应用
- 多模态大模型（GPT-4V、Claude Vision）的视觉编码器

#AI #ViT #Transformer #computer-vision #image-classification
