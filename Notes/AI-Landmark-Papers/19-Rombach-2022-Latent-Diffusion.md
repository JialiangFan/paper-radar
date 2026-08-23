# High-Resolution Image Synthesis with Latent Diffusion Models

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer |
| **发表年份** | 2022 |
| **发表会议** | CVPR 2022 |
| **引用量** | 15,000+ |
| **论文链接** | [arXiv](https://arxiv.org/abs/2112.10752) |

## 核心问题

扩散模型（Diffusion Models）生成图像质量极高，但直接在**像素空间**操作计算成本极其高昂。如何在保持质量的同时大幅降低计算成本？

## 主要贡献

### 1. 潜在扩散模型（Latent Diffusion Model, LDM）
核心思想：在**潜在空间**而非像素空间进行扩散过程。

```
训练阶段：
图像 (512×512×3) → [VAE编码器] → 潜在表示 (64×64×4) → 扩散训练
                                    ↑ 压缩了约48倍

生成阶段：
随机噪声 (64×64×4) → [去噪过程] → 清晰潜在表示 → [VAE解码器] → 图像 (512×512×3)
```

### 2. 两阶段架构

**阶段一：感知压缩（Perceptual Compression）**
- 训练一个VAE（自编码器）
- 将图像压缩到低维潜在空间
- 保留感知上重要的信息，去除高频细节

**阶段二：扩散模型（Diffusion Model）**
- 在潜在空间中训练扩散模型
- 使用U-Net作为去噪网络
- 配合交叉注意力机制实现条件生成

### 3. 灵活的条件生成机制
通过**交叉注意力**（Cross-Attention）注入各种条件：

```
Attention(Q, K, V) = softmax(QK^T / √d) × V
其中：
  Q = 来自U-Net的特征（图像）
  K, V = 来自条件编码器的特征（文本/图像/语义图等）
```

支持的条件类型：
- **文本描述**（Text-to-Image）：CLIP文本编码器
- **语义分割图**
- **超分辨率**
- **图像修补（Inpainting）**
- **布局（Layout）**

## 计算效率

| 方法 | 训练硬件 | 训练时间 | FID (越低越好) |
|------|----------|----------|-------|
| DALL-E | 1024 V100 | - | 27.5 |
| 像素级扩散 | 256 V100 | - | 7.76 |
| **LDM** | **单张 A100** | **约5天** | **3.60** |

在潜在空间操作使计算效率提升了**数十倍**。

## 历史意义

- **Stable Diffusion的基础论文**——开源AI图像生成的革命
- 证明了在潜在空间做扩散既高效又高质
- 让高质量图像生成从大公司专属变为**人人可用**
- 推动了AI绘画、AI设计的产业爆发
- Stable Diffusion的开源催生了整个社区生态（LoRA、ControlNet等）

## 与后续工作的关联

- **Stable Diffusion**（2022）：基于LDM的开源文生图模型
- **SDXL**（2023）：更高质量的Stable Diffusion
- **ControlNet**（2023）：精确控制生成结果
- **Stable Video Diffusion**：扩展到视频生成
- **Sora**（2024）：OpenAI的视频生成模型也采用了潜在空间扩散的思想

#AI #diffusion-model #image-generation #Stable-Diffusion #generative-model #latent-space
