# A Minimalist Approach - from Rejection Sampling to Reinforce

## 主题
RL Sample Selection for LLMs

## 背景
Reinforcement learning (RL) 已成为在复杂推理任务上 fine-tune LLMs 的主流方法。GRPO 因在训练 DeepSeek-R1 中的成功而备受关注，但其性能优势的来源尚不明确。与此同时，RAFT（rejection sampling fine-tuning）作为最简单的 baseline 之一，其潜力在先前研究中被低估。本文从 Reinforce-like algorithm 的视角重新审视 GRPO，系统分析其各组件的贡献。

## 现有局限与研究问题
- **Limitation:** GRPO 的算法细节在文献中缺乏充分记录，其相较于 vanilla Reinforce 的性能增益究竟来自 reward normalization 还是 negative sample 的处理方式，尚无定论。此外，社区普遍认为利用 negative feedback 的 RL 方法显著优于仅使用 positive samples 的 SFT-like 方法，但缺乏严格实验验证。
- **Problem:** GRPO 的核心优势是否源于 reward normalization？Negative samples 在 on-policy RL training 中扮演什么角色？能否设计更简洁且同样有效的 policy gradient 变体？

## 贡献
- 重新评估 RAFT baseline，发现其在 Math500、Minerva Math、Olympiad Bench 上的表现与 GRPO 差距极小（Qwen2.5-Math-7B 上 RAFT 52.3% vs GRPO 56.3%），且早期收敛速度更快。提出 RAFT++ 变体（加入 importance sampling 和 clipping），进一步将准确率提升至 56.1%。
- 通过系统 ablation 揭示 GRPO 的主要优势并非来自 reward normalization，而是来自其隐式过滤掉所有 response 均错误的 prompts（"Remove all wrong"）。在全错 prompt 上训练会产生 high-variance misleading gradients，显著损害模型性能。
- 提出 Reinforce-Rej，一种最小化 policy gradient 扩展，同时过滤掉全对和全错的 prompts。该方法在最终性能上与 GRPO 相当（Qwen2.5-Math-7B 上 56.4% vs 56.3%），同时具有更优的 KL efficiency 和 entropy stability。
- 发现仅在 positive samples 上训练会导致 policy entropy 快速下降和 distributional collapse，限制 exploration 能力，解释了 RAFT++ 早期快但后期被 GRPO 超越的现象。

## 方法论
- **实验框架：** 基于 verl 框架实现，使用 Numina-Math（约 860k 数学题）作为训练集，在 Qwen2.5-Math-7B-base 和 LLaMA-3.2-3B-instruct 两个模型上实验。评估指标为 average@16（温度 1.0，最大生成 4096 tokens）。
- **算法对比：** 统一比较 RAFT、RAFT++、vanilla Reinforce、GRPO、PPO、Iterative DPO 和 Reinforce-Rej。其中 RAFT 仅在 positive samples 上做 log-likelihood fine-tuning；RAFT++ 在 RAFT 基础上加入 importance sampling ratio 和 clipping；GRPO 在每个 prompt 内用 mean/std 对 reward 做 normalization 并计算 advantage。
- **Ablation 设计：** 在 Reinforce 基础上逐步叠加组件——Mean Zero（减去 prompt 内均值）、Remove all correct、Remove all wrong、Remove both、Remove both + Normalize Std——以隔离各因素的贡献。结果表明 "Remove all wrong" 带来最大性能提升，而 normalization 的贡献有限。
- **Reinforce-Rej 定义：** 即 "Reinforce + Remove both"，在 on-policy 训练中过滤掉所有 sampled responses 全对或全错的 prompts，仅在包含混合正负 response 的 prompts 上计算 policy gradient。该方法不需要 reward normalization，实现简洁，且在 KL divergence 和 entropy 方面表现更稳定。

> **Title:** A Minimalist Approach to LLM Reasoning: from Rejection Sampling to Reinforce
> **Authors:** Wei Xiong, Jiarui Yao, Yuhui Xu, Bo Pang, Lei Wang, Doyen Sahoo, Junnan Li, Nan Jiang, Tong Zhang, Caiming Xiong, Hanze Dong
> **Venue:** arXiv:2504.11343
> **Year:** 2025
> **Affiliations:** Salesforce AI Research, UIUC