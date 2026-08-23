# Scaling Policy Optimization for Temporal Logic Tasks

- **Title:** Scaling Learning based Policy Optimization for Temporal Logic Tasks by Controller Network Dropout
- **Authors:** Navid Hashemi, Bardh Hoxha, Danil Prokhorov, Georgios Fainekos, Jyotirmoy Deshmukh
- **Venue:** ACM Transactions on Cyber-Physical Systems (TCPS), 2024
- **Year:** 2024
- **Affiliations:** University of Southern California; Toyota NA R&D


## 主题
通过 controller network dropout 等技术扩展基于时序逻辑目标的策略优化

## 背景
使用时序逻辑（如 STL、LTL）作为任务规约来训练或优化神经网络控制策略是一个新兴方向。然而，随着任务复杂度和网络规模增大，基于时序逻辑目标的策略优化面临严重的可扩展性挑战。

## 现有局限与研究问题
- **Limitation:** 基于 STL 鲁棒度的策略优化在大规模网络上收敛缓慢；时序逻辑目标的组合性质导致损失景观（loss landscape）复杂，存在大量局部最优；现有方法难以处理长时间窗口和复杂嵌套的时序规约。
- **Problem:** 如何使基于时序逻辑目标的策略优化扩展到更大的网络和更复杂的任务规约？

## 贡献
- 提出 controller network dropout 技术，通过随机丢弃控制网络的部分神经元来正则化训练过程
- 开发分层优化策略，将复杂时序目标分解为子目标逐步优化
- 提供可扩展性的理论分析和实验验证
- 在多个 CPS 基准上展示方法可处理显著更大规模的问题

## 方法论
- **Controller Network Dropout：** 在训练过程中随机丢弃控制器网络的神经元（类似标准 dropout），但专门针对策略网络而非分类网络设计。这迫使网络学习更鲁棒的策略表示，避免过度依赖特定神经元组合
- **分层优化：** 对于复杂的 STL 规约 φ = φ₁ ∧ φ₂ ∧ ... ∧ φₙ，先分别优化每个子规约，再联合优化整体规约。使用课程学习（curriculum learning）策略逐步增加任务难度
- **鲁棒度引导采样：** 在策略梯度方法中，使用 STL 鲁棒度值加权采样轨迹，优先学习高鲁棒度的行为模式
- **评估：** 在自动驾驶、机器人导航等场景中，方法可处理比现有方法大 10 倍以上的网络规模和更复杂的时序规约
