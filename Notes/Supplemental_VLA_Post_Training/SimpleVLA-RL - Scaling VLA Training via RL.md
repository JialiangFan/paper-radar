---
imported_title: "SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/SimpleVLA-RL - Scaling VLA Training via RL.md"
imported_reason: "Relevant RL baseline for smaller-scale VLA training experiments."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning

- **Title:** SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning
- **Authors:** Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, Dehui Wang, Dingxiang Luo, Yuchen Fan, Youbang Sun, Jia Zeng, Jiangmiao Pang, Shanghang Zhang, Yu Wang, Yao Mu, Bowen Zhou, Ning Ding
- **Venue:** arXiv preprint (arXiv:2509.09674)
- **Year:** 2025
- **Affiliations:** Tsinghua University, Shanghai AI Lab, Shanghai Jiao Tong University, Peking University, The University of Hong Kong


## 主题 - VLA模型的强化学习训练框架

## 背景
Vision-Language-Action (VLA) 模型已成为机器人操作的主流范式，通常采用大规模预训练加supervised fine-tuning (SFT) 的两阶段训练策略。然而，SFT依赖大量人工操作的机器人轨迹数据，采集成本高昂且难以规模化。近期Large Reasoning Models (如DeepSeek-R1) 的突破表明，reinforcement learning (RL) 仅凭outcome reward即可显著提升模型的逐步推理能力，这启发了将类似方法迁移至VLA模型的研究。

## 现有局限与研究问题
- **数据稀缺性**：SFT所需的高质量人工机器人轨迹数据采集成本极高，严重制约VLA模型的规模化训练
- **泛化能力不足**：SFT训练的VLA模型在面对未见过的任务、环境或物体时，性能显著下降，尤其在compositional、long-horizon及涉及distribution shift的任务中表现突出
- **RL应用于VLA的独特挑战**：与LLM不同，VLA的rollout需要与环境进行多轮交互式采样，速度更慢且计算成本更高；传统机器人RL方法依赖手工设计的process reward，可迁移性差
- **核心研究问题**：RL能否像提升LLM推理能力一样，增强VLA模型的逐步动作生成能力？

## 贡献
- 提出SimpleVLA-RL，一个基于veRL构建的高效端到端VLA在线RL框架，支持VLA-specific的交互式轨迹采样、可扩展的并行化渲染以及优化的loss计算
- 采用简单的binary outcome reward（任务成功为1，失败为0），避免了复杂process reward的设计，具有良好的可扩展性和跨环境通用性
- 引入三项exploration增强策略：Dynamic Sampling（过滤全成功/全失败的group）、Clip Higher（非对称clipping范围[0.8, 1.28]）、Higher Rollout Temperature（T=1.6），各带来10-15%的性能提升
- 在LIBERO上达到SoTA（平均99.1%），在RoboTwin 1.0和2.0上分别实现+30.6和+30.5的提升，超越所有baseline
- 证明RL可有效缓解数据稀缺问题：仅用单条示范轨迹+RL，LIBERO-Long成功率从17.3%提升至91.7%，甚至超过使用全部500条轨迹的SFT
- 发现"pushcut"现象：RL训练中策略自主发现了示范数据中不存在的新型操作模式（如用推代替抓取-移动-放置），类似于DeepSeek-R1中的"Aha Moment"
- Sim-to-real实验表明，仿真训练的RL策略可有效迁移至真实世界，平均成功率从17.5%提升至38.5%

## 方法论
- **基础模型**：基于OpenVLA-OFT（采用LLaMA2-7B backbone），使用action token离散化输出动作，天然兼容PPO-like RL算法的概率分布采样与policy gradient计算
- **交互式VLA Rollout**：区别于LLM的单次生成，VLA rollout需在每个timestep与环境交互获取新观测，实现闭环控制；采用同步多环境并行渲染加速采样
- **Outcome Reward建模**：轨迹级binary reward（成功=1，失败=0），均匀传播至轨迹中每个action token，避免任务特定的reward工程
- **训练目标**：采用GRPO算法，移除KL divergence正则化项（following DAPO），消除对reference model的依赖，降低显存消耗并促进更大范围的exploration
- **Dynamic Sampling**：rollout时过滤reward全同的group，确保非零advantage估计和稳定梯度
- **实验设置**：在LIBERO（长程多任务）、RoboTwin 1.0（双臂）和RoboTwin 2.0（domain randomization）三个benchmark上评估；使用8×NVIDIA A800 80GB训练
- **失败模式分析**：当SFT模型初始能力为零时，RL完全无效（无成功轨迹则无正reward信号）；模型先验能力与RL提升效果正相关，存在最低能力阈值
