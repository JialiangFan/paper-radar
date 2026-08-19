---
imported_title: "VLA-RFT: Vision-Language-Action Reinforcement Fine-Tuning with Verified Rewards in World Simulators"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/VLA-RFT - Reinforcement Fine-tuning with Verified Rewards.md"
imported_reason: "Relevant to training VLA policies with verified rewards."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# VLA-RFT: Vision-Language-Action Reinforcement Fine-Tuning with Verified Rewards in World Simulators

- **Title:** VLA-RFT: Vision-Language-Action Reinforcement Fine-Tuning with Verified Rewards in World Simulators
- **Authors:** Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, Weihua Su
- **Venue:** arXiv preprint (arXiv:2510.00406)
- **Year:** 2025
- **Affiliations:** Westlake University, Zhejiang University, OpenHelix Team, Fudan University, Zhengzhou University, BUPT, Hebei University of Technology


## 主题 - World Model驱动的VLA强化微调

## 背景
Vision-Language-Action (VLA) 模型通过大规模imitation learning实现了具身决策能力，但纯模仿学习在distribution shift下容易产生compounding errors，导致策略鲁棒性不足。Reinforcement learning (RL) 可以缓解这些问题，但传统RL方法面临simulation-based RL的sim-to-real gap大、real-world RL成本高且不安全、offline RL无法与环境交互等困境。因此，如何高效且安全地将RL引入VLA post-training仍是一个开放问题。

## 现有局限与研究问题
- 纯imitation learning的VLA在distribution shift下误差累积，偏离expert demonstrations后策略迅速退化
- Simulation-based RL需要大量交互（数百万步），且存在严重的sim-to-real gap
- Real-world RL训练代价高昂且存在安全风险，难以规模化
- Offline RL无法与环境交互，无法从自身动作的后果中学习，仍受distribution shift影响
- 现有reward设计缺乏dense、action-aligned的学习信号，导致样本效率低下

## 贡献
- 提出VLA-RFT框架：利用data-driven world model作为可控simulator，实现高效的reinforcement fine-tuning，避免了真实世界交互的成本与风险
- 设计verified reward机制：通过world model生成视觉轨迹，结合pixel-level（MAE）和perceptual-level（LPIPS）奖励信号，提供dense且task-grounded的反馈
- 引入SDE-Policy参数化：通过Sigma Net将deterministic flow-matching扩展为stochastic differential equation过程，在RL训练中实现有效的exploration
- 仅需400步fine-tuning即超越150K步的supervised baseline（LIBERO标准任务平均SR从86.6%提升至91.1%），训练效率比simulator-based RL高出数个数量级
- 在perturbation settings下展现出显著的out-of-distribution鲁棒性提升，策略能够在环境扰动下保持稳定执行

## 方法论
- **两阶段训练流程**：Stage I预训练world model（基于LLaMA架构的138M参数autoregressive Transformer）和VLA policy（基于VLA-Adapter + flow-matching action head）；Stage II通过world model交互进行reinforcement fine-tuning
- **World Model设计**：采用interactive video prediction model，输入初始图像和action sequence，自回归生成未来visual observations；使用pretrained tokenizer编码图像、action tokenizer离散化动作，通过maximum likelihood训练
- **SDE-Policy参数化**：在flow-matching action head基础上引入Sigma Net，输出variance vector将FM-ODE推广为SDE过程；通过K=10步离散化积分生成action chunks，计算step-wise log-likelihood用于GRPO优化
- **Verified Reward计算**：将policy生成的action和ground-truth action分别送入同一world model生成视觉轨迹，计算两者之间的负MAE和负LPIPS作为reward（Reward Type 3），消除world model生成质量偏差
- **GRPO优化**：采用group-based advantage estimation，N次rollout取均值作baseline；最终目标函数结合clipped policy ratio、auxiliary flow-matching MSE loss和entropy regularization，确保训练稳定性
- **实验评估**：在LIBERO benchmark上验证，涵盖Spatial、Object、Goal、Long四个标准suite及多种perturbation settings（Object Position、Goal Position、RoboState、Combined）
