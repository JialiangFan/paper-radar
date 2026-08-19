---
imported_title: "OpenVLA-OFT: Fine-Tuning Vision-Language-Action Models"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/OpenVLA-OFT - Fine-Tuning VLA for Speed and Success.md"
imported_reason: "Useful for concrete OpenVLA fine-tuning baselines."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success

- **Title:** Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success
- **Authors:** Moo Jin Kim, Chelsea Finn, Percy Liang
- **Venue:** arXiv preprint (arXiv:2502.19645)
- **Year:** 2025
- **Affiliations:** Stanford University


## 主题 - VLA微调策略优化

## 背景
Vision-language-action models (VLAs) 通过在大规模机器人数据集上微调预训练的vision-language models来实现强大的任务执行、语义泛化和语言跟随能力。然而，将VLA适配到新的机器人平台和任务时，面临推理速度慢（autoregressive decoding仅3-5 Hz）和高频控制场景（25-50+ Hz）下性能不佳的问题。当前缺乏对VLA fine-tuning设计空间的系统性实证分析，包括action decoding方案、action representation和learning objective的最优选择。

## 现有局限与研究问题
- 原始OpenVLA的autoregressive decoding生成单步7维动作需0.33秒（A100 GPU），无法满足高频双臂操作的实时性要求
- Autoregressive generation使得action chunking不可行，因为chunk size K会导致延迟增加K倍
- 将连续动作离散化为256个bin会损失精度，影响精细操控任务的表现
- Diffusion-based VLA虽提升了吞吐量，但引入了架构差异大、多步denoising延迟高等问题
- 基于LoRA的vanilla fine-tuning在双臂操作（bimanual manipulation）任务中成功率不理想
- 多视角输入场景下，policy容易因视觉中的spurious correlations而忽略语言指令，导致language following能力下降

## 贡献
- 系统研究了三个关键VLA fine-tuning设计决策：action generation strategy（autoregressive vs. parallel decoding）、action representation（discrete vs. continuous）、learning objective（next-token prediction vs. L1 regression vs. diffusion）
- 提出Optimized Fine-Tuning (OFT) recipe，整合parallel decoding with action chunking、continuous action representation和L1 regression objective，在保持算法简洁性的同时提升推理效率和任务性能
- 在LIBERO benchmark上实现97.1%平均成功率的SOTA，同时通过8步action chunks将吞吐量提升26倍
- 引入FiLM（Feature-wise Linear Modulation）增强语言grounding，形成OFT+变体，在真实ALOHA双臂机器人上以高达15%的绝对优势超越RDT-1B、pi_0等fine-tuned VLA及ACT、Diffusion Policy等from-scratch baseline
- 证明简单的L1 regression在high-capacity VLA上可匹敌diffusion-based方法的性能，同时收敛更快、推理更高效

## 方法论
- **Parallel Decoding**: 将causal attention mask替换为bidirectional attention，输入empty action embeddings，使decoder在single forward pass中同时生成所有动作维度，消除sequential token generation的瓶颈；自然扩展至action chunking，chunk size K下单次前向传播生成K×D个动作值
- **Continuous Action Representation**: 用4层MLP（ReLU activation）action head替代discrete tokenization + softmax输出层，将decoder hidden states直接映射为归一化连续动作值，避免256-bin离散化带来的精度损失
- **L1 Regression Objective**: 采用mean L1 loss最小化预测与ground-truth归一化动作之间的差异，相比diffusion无需多步denoising，训练收敛更快且推理仅需单次前向传播
- **FiLM Language Conditioning（OFT+）**: 对task description的language embeddings取均值后投影得到scaling向量γ和shifting向量β，在SigLIP和DINOv2 vision transformer的每个block中对visual features进行spatially-agnostic affine modulation（F̂ = (1+γ)⊙F + β），增强模型对语言指令的关注
- **灵活输入处理**: 支持多视角图像（通过shared SigLIP-DINOv2 backbone提取256 patch embeddings/view）和低维robot state（通过单独projection network映射至language embedding space），所有输入沿sequence维度拼接后送入Llama-2 decoder
- **实验验证**: 在LIBERO仿真（4个task suite，每个10任务×500 trials）和真实ALOHA双臂平台（4个灵巧操作任务，20-300 demonstrations）上进行系统评估，通过LoRA（rank 32）fine-tuning OpenVLA 7B模型
