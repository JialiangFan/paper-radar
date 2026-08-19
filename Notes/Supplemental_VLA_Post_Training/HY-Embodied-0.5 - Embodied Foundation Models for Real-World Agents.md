---
imported_title: "HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/HY-Embodied-0.5 - Embodied Foundation Models for Real-World Agents.md"
imported_reason: "Additional recent embodied foundation model context."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents

- **Title:** HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents
- **Authors:** Tencent Robotics X & HY Vision Team
- **Venue:** arXiv preprint (arXiv:2604.07430)
- **Year:** 2026
- **Affiliations:** Tencent


## 主题 - 面向真实世界具身智能体的基础模型

## 背景
Vision-Language Models (VLMs) 在通用视觉理解方面取得了显著进展，但要让智能体在真实物理环境中感知、推理并执行动作，现有VLM仍存在两大核心不足：(1) **细粒度视觉感知**——主流VLM在静态网页数据上训练，难以捕获具身任务所需的精细空间细节；(2) **具身预测、交互与规划**——缺少对物理世界动态预测、交互反馈和长期规划的建模能力。HY-Embodied-0.5旨在从架构、数据和训练三个维度系统性地弥合通用VLM与具身智能之间的鸿沟。

## 现有局限与研究问题
- 通用VLM在空间推理、3D理解、具身交互等物理感知任务上表现不足，无法直接用于机器人控制
- 边缘端部署对模型大小和推理速度有严格限制，现有大模型难以满足实时性需求
- VLM预训练中视觉训练往往导致语言能力退化（modality conflict）
- 已有的后训练（post-training）方法缺少面向具身任务多样化输出格式（几何grounding、轨迹预测、离散决策、开放推理）的统一奖励设计
- 大模型的推理能力难以高效蒸馏到小模型，传统离线蒸馏存在训练-推理分布不匹配问题

## 贡献
- 提出HY-Embodied-0.5模型族：包含高效的MoT-2B（2B激活参数/4B总参数）和强大的MoE-A32B（32B激活参数/407B总参数）两个变体
- 架构创新——**Mixture-of-Transformers (MoT)**：为视觉和语言分支引入独立的QKV和FFN参数，解耦模态处理，避免重度视觉训练对语言能力的退化；引入**Visual Latent Tokens**桥接视觉与语言模态
- 高效视觉编码器**HY-ViT 2.0**（400M参数）：原生支持任意分辨率输入，通过大模型蒸馏获得精确视觉表征
- 迭代式自进化后训练流程：交替进行RL（GRPO）和Rejection Sampling Fine-tuning（RFT），逐步提升具身推理深度
- **任务感知奖励设计**：针对四类具身任务输出格式（Grounding-Based、Trajectory-Based、Regression-Based、Textual-Based）设计分类奖励函数
- **Large-to-Small On-Policy Distillation (OPD)**：学生模型先生成rollout，教师模型在学生生成的prefix上进行teacher forcing，通过KL散度实现on-policy蒸馏，解决传统离线蒸馏的分布不匹配问题
- MoT-2B在22个具身基准中16个上超越同规模SOTA；MoE-A32B平均得分67.0%，超越Gemini 3.0 Pro（63.6%）
- 在真实机器人实验中（Packing 85%、Stacking 80%、Hanging 75%），显著优于Pi0和Pi0.5基线

## 方法论
- **模型架构**：基于VLM范式（Vision Encoder + LLM），采用MoT架构为视觉和文本分支复制独立的FFN和QKV参数（初始化自预训练LLM权重）；视觉分支使用Local Full Attention，语言分支使用Global Causal Attention；视觉latent tokens附加在visual序列末尾，通过独立监督损失和mixed optimization loss连接视觉与语言
- **预训练数据**：超过1亿样本，覆盖基础视觉感知、具身交互（机器人操作/导航/自动驾驶）、空间推理（3D/深度/多视角）和通用理解四大类
- **三阶段训练策略**：Stage 1 联合优化LLM Loss + Vision Loss + Global Loss进行大规模预训练；Stage 2 中阶段训练仅优化LLM Loss；Stage 3 后训练包含SFT Cold Start → RL（GRPO）→ RFT迭代循环
- **RL训练细节**：使用GRPO目标，group size G=16，异步clip比率[0.8, 1.35]，batch size 128，学习率8e-7，每轮RL在50K新构建样本上训练5个epoch；动态构建训练数据——丢弃全对（过简单）和全错（过难）样本，仅保留部分成功的frontier样本
- **Evolving Deep Thinking**：RL后进行multi-sample rollout，用教师模型评分思维链质量，筛选约30万高质量trace进行RFT，交替RL-RFT循环逐步将偶然成功固化为稳定推理模式
- **On-Policy蒸馏**：学生先rollout生成响应y，教师在学生生成的prefix上计算next-token分布，最小化逐token KL散度，使学生在自身容易犯错的状态上精确获得教师指导
- **VLA扩展**：基于MoT-2B添加Action Expert模块（参照Pi0/Pi0.5架构），先在5K小时UMI数据上微调，再在300-700条任务特定真实演示上SFT后部署
