# DeepSeek-R1 - Incentivizing Reasoning via RL

## 主题
RL-Incentivized LLM Reasoning

## 背景
大语言模型(LLMs)在推理任务上取得了显著进展，但现有方法严重依赖人工标注的 chain-of-thought (CoT) 数据进行 supervised fine-tuning (SFT)，这不仅限制了可扩展性，还将模型的推理能力约束在人类思维模式之内。Reinforcement learning (RL) 提供了一种替代路径，通过奖励信号引导模型自主探索推理策略，而无需显式的人工示范。DeepSeek-R1 系列基于 DeepSeek-V3-Base，采用 Group Relative Policy Optimization (GRPO) 算法，探索了纯 RL 训练在激发 LLM 推理能力方面的潜力。

## 现有局限与研究问题
- **Limitation:** 传统 post-training 依赖大量人工标注的推理轨迹进行 SFT，不仅成本高昂、难以扩展，而且人工编写的 reasoning traces 往往缺少 self-reflection 和 verification 等关键步骤，模型性能受限于人类标注者的推理水平。Neural reward models 在大规模 RL 训练中容易出现 reward hacking 问题。
- **Problem:** 能否跳过 SFT 阶段，仅通过纯 RL 训练（使用 rule-based rewards）激发 LLM 自主发展出高级推理行为（如 self-verification、reflection、dynamic strategy adaptation），并在数学、编程等可验证任务上超越传统 SFT 方法？

## 贡献
- 提出 DeepSeek-R1-Zero：首次证明纯 RL 训练（无 SFT）即可激发 LLM 涌现出 self-verification、reflection 和 "aha moment" 等高级推理行为，AIME 2024 pass@1 从 15.6% 提升至 71.0%，cons@64 达 86.7%
- 提出 DeepSeek-R1：设计多阶段训练流水线（cold-start SFT → RL with rule-based & language consistency rewards → rejection sampling SFT → second RL with preference rewards），在保持强推理能力的同时改善可读性、语言一致性和通用任务表现
- 采用 GRPO 替代 PPO 进行大规模 RL 训练，去除 value model 以降低计算开销，通过 group-level advantage estimation 简化训练流程，实验表明 GRPO 性能优于或持平于精调后的 PPO
- 将 DeepSeek-R1 的推理能力蒸馏至多个小模型（1.5B–70B），蒸馏后的小模型在推理 benchmark 上显著超越同规模的 instruction-tuned 基线模型
- 开源全部模型（DeepSeek-R1 及 6 个蒸馏版本），推动社区对 long CoT reasoning 机制的研究

## 方法论
- **DeepSeek-R1-Zero（纯 RL 路线）：** 基于 DeepSeek-V3-Base，直接使用 GRPO 进行 RL 训练，不经过任何 SFT。Reward 设计包括 accuracy reward（基于规则验证最终答案正确性）和 format reward（要求输出包含 `<think>` 和 `<answer>` 标签）。训练过程中模型自主发展出递增的 thinking time、self-reflection 和 alternative strategy exploration 等涌现行为
- **GRPO 算法：** 对每个问题采样一组输出 {o₁, ..., o_G}，利用组内奖励的均值和标准差计算 advantage A_i，通过 clipped surrogate objective 和 KL divergence 正则化优化策略，无需训练额外的 value model
- **DeepSeek-R1 多阶段流水线：** (1) Cold-start SFT：收集数千条具有人类对齐思维过程的长 CoT 数据进行初始微调；(2) 第一阶段 RL：使用 rule-based reward（reasoning 任务）+ language consistency reward + model-based reward（general 任务）进行 GRPO 训练；(3) Rejection sampling SFT：从 RL checkpoint 采样推理数据并结合非推理 SFT 数据进行再训练；(4) 第二阶段 RL：使用 rule-based reward 和 preference-based reward 进一步对齐人类偏好，提升 helpfulness 和 harmlessness
- **Reward 体系：** Reasoning 任务使用 rule-based reward（答案匹配、代码编译执行）；General 任务使用 helpful reward model（pairwise preference）和 safety reward model（point-wise 安全评分）；Language consistency reward 按目标语言词比例计算，缓解语言混用问题
- **知识蒸馏：** 利用 DeepSeek-R1 生成的推理轨迹对 Qwen 和 Llama 系列小模型进行 SFT 蒸馏，将大模型的长链推理能力迁移至小模型

> **Title:** DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
> **Authors:** DeepSeek-AI
> **Venue:** arXiv:2501.12948
> **Year:** 2025
> **Affiliations:** DeepSeek-AI