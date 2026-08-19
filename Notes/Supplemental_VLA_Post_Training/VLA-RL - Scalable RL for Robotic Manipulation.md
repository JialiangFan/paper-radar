---
imported_title: "VLA-RL: Scalable Reinforcement Learning for Robotic Manipulation"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/VLA-RL - Scalable RL for Robotic Manipulation.md"
imported_reason: "Supports the inherent-safety-training direction through RL post-training."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning

- **Title:** VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning
- **Authors:** Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, Ziwei Wang
- **Venue:** arXiv preprint (arXiv:2505.18719)
- **Year:** 2025
- **Affiliations:** Tsinghua Shenzhen International Graduate School (Tsinghua University), Nanyang Technological University


## 主题 - 强化学习提升VLA操控能力

## 背景
大规模Vision-Language-Action (VLA) 模型通过模仿学习在多种机器人操控任务上表现优异，但其依赖离线数据的本质导致在Out-of-Distribution (OOD) 场景下性能显著下降。Reinforcement Learning (RL) 通过在线探索可突破离线数据的局限，而近期RL在LLM推理增强上的成功（如DeepSeek-R1、GRPO）表明，类似的test-time scaling收益有望迁移至机器人领域。VLA-RL正是首个系统性地将可扩展RL应用于预训练auto-regressive VLA模型的框架。

## 现有局限与研究问题
- VLA模型基于imitation learning训练，仅利用离线demonstration数据，状态覆盖有限，OOD场景失败率高
- 传统RL from scratch数据效率低，需要大量reward engineering，且多局限于低维状态空间、小型网络和单任务设定
- 机器人操控任务的reward天然稀疏（仅任务完成时给出binary信号），不利于长horizon任务的策略优化
- 缺乏将trajectory-level RL系统性地应用于大规模auto-regressive VLA的算法框架与工程实践
- 核心问题：能否在机器人操控领域实现类似LLM中基于RL的test-time scaling收益？

## 贡献
- 提出VLA-RL框架：首个将online RL系统性应用于预训练auto-regressive VLA的统一算法框架，将机器人操控trajectory建模为multi-modal multi-turn conversation
- 提出Robotic Process Reward Model (RPRM)：利用预训练vision-language model微调，通过自动提取pseudo reward label实现reward densification，无需人工标注
- 系统性工程优化：识别并验证了curriculum selection strategy、GPU-balanced vectorized environments、batch decoding、critic warmup等关键实现细节对训练稳定性和效率的影响
- 实验验证：在LIBERO benchmark的40个任务上，基于OpenVLA-7B，VLA-RL超越最强SFT baseline 4.5%，匹配商业模型π₀-FAST的性能，仅需48 GPU hours
- 观察到test-time scaling的初步证据：随训练步数增加，性能持续提升，暗示机器人领域的inference scaling law

## 方法论
- **问题建模**：将auto-regressive VLA的操控过程形式化为MDP，状态空间为图像与文本token的笛卡尔积，动作空间为VLA输出的离散token序列，采用PPO进行策略优化
- **Rollout阶段**：合并LoRA权重至原始checkpoint后进行推理，agent与环境交互生成trajectory，action log-probability分解为token级对数概率之和
- **Robotic Process Reward Model**：将reward建模重构为next-token prediction问题；通过自动化pipeline生成pseudo reward label——(1) Milestone Segmentation：按gripper开合变化分割子任务；(2) Progress Labeling：在末端执行器速度趋近零的keyframe处标注正向pseudo-reward
- **Reward densification**：最终reward为环境稀疏reward与RPRM预测reward的直接求和，提供更频繁的学习信号
- **Curriculum Selection Strategy**：自适应任务选择，采样概率与成功率距50%的偏差成指数关系，优先训练处于agent能力边界的任务
- **Critic Warmup**：在策略-价值联合优化前，先用imitation pretrained policy收集trajectory单独预训练value network，避免早期不准确的value估计误导策略梯度
- **GPU-balanced Vectorized Environments**：每个GPU worker分配独立的vectorized环境子集，通过all_reduce聚合环境状态，平衡GPU显存与计算
- **基础设施**：基于vLLM加速推理，PyTorch FSDP分布式训练，bfloat16精度，OpenRLHF风格的1 GPU推理 + (G-1) GPU训练架构
