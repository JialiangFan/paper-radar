# OpenVLA - An Open-Source Vision-Language-Action Model

## 主题
Open-source generalist VLA model

## 背景
视觉-语言-动作模型 (VLA) 通过在机器人轨迹数据上微调大规模预训练的视觉-语言模型 (VLM)，将互联网级先验知识注入到机器人控制策略中。先前最强的 VLA（如 RT-2-X）取得了出色的泛化能力，但其权重、训练代码和数据混合方式均未开源，限制了下游研究和向新机器人/任务的适配。

## 现有局限与研究问题
- **Limitation:** 现有 SOTA VLA 完全闭源，模型架构、训练流程和数据混合均不可见；同时缺乏对 VLA 在新机器人任务上高效微调（特别是在消费级 GPU 上）的最佳实践研究。
- **Problem:** 如何构建一个完全开源、性能领先的通用 VLA，并为其在新机器人/新任务上的参数高效微调与部署提供可复现的训练-推理流程？

## 贡献
- 发布 OpenVLA：7B 参数开源 VLA，在 29 个评测任务上以 16.5% 的绝对成功率优势超越 55B 的闭源 RT-2-X，参数量仅为后者的 1/7。
- 在 7 个不同操作任务上验证 OpenVLA 在新机器人/新任务上的微调效果，超越 Diffusion Policy 20.4%。
- 首次系统验证 LoRA 低秩微调与 INT8/INT4 量化在 VLA 上的有效性，使 OpenVLA 可在消费级 GPU (RTX 4090) 上微调与部署。
- 完全开源 970k 训练样本、模型权重、PyTorch 训练代码与 HuggingFace 集成的微调/推理 notebook，为社区提供可扩展的 VLA 研究基础设施。

## 方法论
- **骨干网络：** 基于 Prismatic-7B VLM，由 SigLIP + DinoV2 双视觉编码器（融合语义与空间特征）、2 层 MLP 投影器和 Llama 2 7B 语言模型骨干组成；输入分辨率 224×224。
- **动作 tokenization：** 沿用 RT-2 方案，将每维连续动作按训练集 1%-99% 分位数离散化为 256 个 bin，覆盖 Llama tokenizer 中最少使用的 256 个 token，作为 7-DoF 末端执行器动作的输出词表。
- **训练数据：** 从 Open X-Embodiment 数据集筛选 970k 条单臂 + 第三人称相机的操作轨迹，沿用 Octo 的数据混合权重平衡 embodiment、任务与场景多样性。
- **训练配方：** 标准 next-token 交叉熵损失只作用于动作 token；微调视觉编码器（不冻结，对空间细节关键）；学习率 2e-5；27 个 epoch，直到 action token 准确率突破 95%；64 张 A100 训练 14 天 (21,500 GPU-hours)，batch size 2048。
- **高效适配：** 提供 LoRA 微调流程与 INT8/INT4 量化推理，实现单卡微调与远程推理服务器部署。
