# RIPT-VLA: Interactive Post-Training for Vision-Language-Action Models

- **Title:** Interactive Post-Training for Vision-Language-Action Models
- **Authors:** Shuhan Tan, Kairan Dou, Yue Zhao, Philipp Krahenbuhl
- **Venue:** arXiv preprint (arXiv:2505.17016)
- **Year:** 2025
- **Affiliations:** UT Austin, Nankai University


## 主题 - VLA模型强化学习后训练

## 背景
Vision-Language-Action (VLA) 模型旨在使agent能够感知、推理并在物理世界中执行动作，通常采用两阶段监督学习范式进行训练：大规模预训练和监督微调 (SFT)。然而，这种纯监督方法存在固有局限——模型从未观察到自身动作的后果，且在少样本场景下性能显著退化。受大语言模型 (LLM) 中reinforcement learning作为第三阶段训练范式的启发，本文探索将交互式强化学习引入VLA模型的后训练阶段。

## 现有局限与研究问题
- 现有VLA训练流程依赖离线专家演示数据和监督模仿学习，缺乏与环境的交互反馈，导致学到的policy在实际rollout中因distribution shift和compounding errors而频繁失败
- 任务特定的SFT阶段依赖大规模、高质量的人类演示数据，数据采集成本高昂，且在仅有少量演示时性能大幅下降
- 已有的VLA强化学习方法（如iRe-VLA、ConRFT）依赖learned value critic或shaped reward function，训练复杂度高且需要离线与在线阶段的精细协调
- 在多任务环境中，不同任务context的难度差异导致rollout group中出现全成功或全失败的情况，产生零advantage，造成梯度信号不稳定

## 贡献
- 提出RIPT-VLA：一种简洁、可扩展的第三阶段VLA训练范式，仅使用稀疏binary success reward即可对预训练VLA模型进行交互式后训练，无需shaped reward、value function或critic model
- 设计了基于LOOP框架的Dynamic-Sampling Leave-One-Out Proximal Policy Optimization算法，结合RLOO advantage estimation与PPO，并引入dynamic rejection策略过滤零advantage的rollout group，确保训练稳定性
- 在LIBERO和MetaWorld基准上取得SOTA结果：QueST模型平均提升10.9%，7B OpenVLA-OFT模型达到97.5% success rate；在LIBERO-90（94.3%）和MetaWorld ML45（92.2%）上也取得最优多任务性能
- 展现极端数据高效性：仅用1条演示即可在15次RL迭代内将不可用的SFT模型（4% success rate）提升至97% success rate
- 验证了跨场景（cross-scenario）和跨目标（cross-goal）的泛化能力，证明RIPT-VLA能够高效激活预训练阶段习得的潜在视觉运动技能

## 方法论
- **三阶段训练范式**：Stage 1 大规模预训练学习通用视觉语言表征；Stage 2 在少量任务特定数据上进行SFT；Stage 3 通过Reinforcement Interactive Post-Training与环境交互优化policy
- **LOOP框架适配**：结合RLOO (Leave-One-Out) advantage estimation和PPO进行critic-free的policy optimization——对同一context采样K条rollout，用leave-one-out方式计算baseline，通过binary reward差异获得稳定的advantage信号
- **Dynamic Rollout Sampling**：在rollout collection阶段，若某个context的K条rollout全部获得相同reward（全成功或全失败），则丢弃该group并重新采样新context，确保每个batch中所有样本具有非零advantage，避免zero-gradient问题
- **兼容不同action表征**：对tokenized action head（如QueST），直接从classification logits获取log-probability；对regression action head（如OpenVLA-OFT），额外训练轻量Laplace scale header以建模action分布，从而计算log-probability和importance ratio
- **训练流程**：每个optimization step交替进行rollout collection（采样context、生成K-group rollout、计算RLOO advantage、dynamic rejection）和policy optimization（使用PPO clipped objective在collected rollout上进行N轮更新）
