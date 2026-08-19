---
imported_title: "Diffusion-VLA: Generalizable Robot Foundation Model"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/Diffusion-VLA - Generalizable Robot Foundation Model.md"
imported_reason: "Useful background for diffusion-style VLA action modeling and training."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Diffusion-VLA: Generalizable and Interpretable Robot Foundation Model via Self-Generated Reasoning

- **Title:** Diffusion-VLA: Scaling Robot Foundation Models via Unified Diffusion and Autoregression
- **Authors:** Junjie Wen, Yichen Zhu, Minjie Zhu, Jinming Li, Zhiyuan Xu, Zhengping Che, Chaomin Shen, Yaxin Peng, Dong Li, Feifei Feng, Jian Tang
- **Venue:** ICML 2025 (PMLR 267)
- **Year:** 2025
- **Affiliations:** Midea Group, East China Normal University, Shanghai University


## 主题 - 推理增强的视觉语言动作模型

## 背景
Vision-Language-Action (VLA) 模型已成为机器人策略学习的主流方向，其中autoregressive VLA（如RT-2、OpenVLA）通过next-token prediction生成动作，而diffusion-based策略（如Diffusion Policy）通过噪声去噪过程建模多模态动作分布。然而，autoregressive VLA在动作精度和推理速度上存在不足，而diffusion模型则缺乏推理与语言理解能力。如何将两者的优势统一——即autoregressive模型的推理能力与diffusion模型的高频鲁棒动作生成——成为一个关键的研究问题。

## 现有局限与研究问题
- Autoregressive VLA将连续动作离散化为固定大小的token，破坏了动作的连贯性与精度
- Next-token prediction的自回归生成方式在实时机器人控制中推理效率低下（如OpenVLA仅5Hz）
- Diffusion-based策略虽然动作生成鲁棒，但缺乏language reasoning能力，难以处理复杂语义任务
- 简单组合autoregressive推理与diffusion动作生成存在隐式gap，推理信号未能有效指导策略学习
- 现有方法在视觉泛化（干扰物、背景变化）和未见物体的zero-shot泛化上表现不佳

## 贡献
- 提出Diffusion-VLA (DiVLA)，一个统一autoregressive reasoning与diffusion action generation的端到端框架
- 设计reasoning injection module，通过Feature-wise Linear Modulation (FiLM)将自生成推理的embedding直接注入diffusion policy网络，使推理信号显式参与策略学习
- 基于预训练VLM（Qwen2-VL）构建，保留视觉语言理解与对话能力，同时通过projection layer将action tokens映射至diffusion模型
- 利用GPT-4o将Droid等机器人数据集自动转化为包含reasoning的训练数据格式
- 在多任务学习、工厂分拣、zero-shot bin picking（102个未见物体达63.7%成功率）、双臂机器人table bussing等真实任务中全面超越Diffusion Policy、OpenVLA、Octo、TinyVLA等基线
- DiVLA-2B在单张A6000 GPU上实现82Hz推理速度，DiVLA-7B达42Hz，比同规模OpenVLA快8倍
- 模型可扩展至2B、7B、72B参数，展现出与模型规模一致的泛化性能提升

## 方法论
- **视觉编码**：使用SigLIP编码图像为dense visual features，经Transformer压缩为固定数量的visual embeddings；支持多视角输入（共享SigLIP backbone后拼接）
- **语言-推理主干**：采用Qwen2-VL作为VLM backbone，自回归生成reasoning tokens（任务分解与解释）和action tokens
- **Projection layer**：在VLM最终embedding层之后，通过两层MLP + LayerNorm将action tokens投影至diffusion模型的输入维度
- **Diffusion action head**：采用标准Diffusion Policy设计（随机初始化权重），通过noise-denoising过程生成连续动作序列；底部附加MLP层映射至具体机器人关节空间
- **Reasoning injection module**：取reasoning component最终embedding的tokenized输出，通过FiLM机制注入diffusion policy网络各层，使推理信号作为辅助contextual信号调制策略网络，而非替代主决策流
- **训练目标**：联合优化diffusion loss $L_{diff}$ 与next-token prediction loss $L_{ntp}$，总损失 $L = L_{diff} + \alpha L_{ntp}$（$\alpha=10$）
- **预训练数据**：DiVLA-2B/7B使用Droid数据集预训练，DiVLA-72B使用OXE + Droid联合预训练；利用GPT-4o为缺乏language annotation的数据自动生成reasoning标注
- **微调策略**：使用LoRA微调VLM，视觉编码器冻结；不同embodiment仅需替换最终MLP层即可快速适配
