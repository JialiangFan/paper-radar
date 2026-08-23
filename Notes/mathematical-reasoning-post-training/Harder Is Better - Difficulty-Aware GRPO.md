# Harder Is Better - Difficulty-Aware GRPO

## 主题
Difficulty-Aware Mathematical Reasoning RL

## 背景
Reinforcement Learning with Verifiable Rewards (RLVR) 是提升 LLM 数学推理能力的主流范式，其中 Group Relative Policy Optimization (GRPO) 是最具代表性的算法，通过对同一问题的一组回答估计相对优势来优化策略。然而，现有方法在算法和数据两个层面均忽视了对高难度问题的关注，限制了模型在边界能力上的提升。本文提出 MathForge 框架，从算法（DGPO）和数据（MQR）双重视角协同地聚焦更难的问题，以增强数学推理性能。

## 现有局限与研究问题
- **Limitation 1 (算法层面):** GRPO 的 group relative advantage estimation (GRAE) 存在隐式不平衡——update magnitude 在 accuracy rate p=0.5 时最大，而对更难（p 接近 0）或更简单（p 接近 1）的问题更新幅度均被抑制，导致模型难以从高难度但仍可解的问题中充分学习。
- **Limitation 2 (数据层面):** 传统 data augmentation 方法主要通过改写问题增加多样性，但未系统性地提升问题难度；且生成全新 question-answer pair 时答案质量难以保证，尤其对竞赛级别问题。
- **Problem:** 如何从算法和数据两个维度同时优先处理更具挑战性的问题，以突破模型的数学推理能力边界？

## 贡献
- 提出 Difficulty-Aware Group Policy Optimization (DGPO) 算法，包含两个关键技术：(1) Difficulty-Balanced Group Advantage Estimation (DGAE)，用 mean absolute deviation (MAD) 替代 standard deviation 归一化优势值，使所有难度问题的 total update magnitude 恒为常数 G；(2) Difficulty-Aware Question-level Weighting (DQW)，通过 softmax 温度机制对 batch 内更难的问题赋予更高权重。
- 提出 Multi-Aspect Question Reformulation (MQR) 数据增强策略，从三个方面改写原始问题以提升难度：添加 story background、引入 abstract terminology、嵌套 sub-problem，同时严格保持原始 gold answer 不变。
- 两者形成协同闭环：MQR 扩展数据难度前沿，DGPO 高效地从增强数据中学习。在 Qwen2.5-Math-7B 上，MathForge 在六个 benchmark 上平均得分达 42.17%，较 GRPO baseline (37.61%) 提升 +4.56%。

## 方法论
- **DGAE:** 将 GRPO 优势函数的归一化分母从 std 替换为 MAD，即 $\hat{A}_{\text{DG},i} = (r_i - \text{mean}) / \text{MAD}$。数学证明（Theorem 2）表明使用 DGAE 后，单个问题的 total update magnitude 恒等于 G，消除了 GRAE 中对难题的隐式抑制。
- **DQW:** 为 batch 中每个 valid query 分配权重 $\lambda_s = B_v \cdot \exp(D_s/T) / \sum \exp(D_s/T)$，其中 $D_s = -\text{mean}(\{r_{si}\})$ 衡量难度，T 为温度超参数（最优值 T=2.0）。难度越高权重越大，形成 "balance-then-reweight" 的两步策略。
- **MQR:** 使用 reformulator model（默认 OpenAI o3，也可用开源模型）对训练问题从三个方面改写：(1) Background——添加与数学内容无关但看似相关的故事背景；(2) Term——发明新的抽象数学术语重新表述问题；(3) Sub-Problem——将某个数值条件转化为独立子问题。所有改写必须保持原始答案不变。
- **MathForge 整体框架:** MQR 将原始数据集扩展 4 倍（原始 + 三种改写），DGPO 在该增强数据上进行 RL 训练。实验覆盖 AIME24/25、AMC23、MATH500、Minerva、Olympiad 等 benchmark，并验证了跨模型（1.5B-7B）、跨方法（与 GPG/DAPO/GSPO 兼容）及多模态（GEOQA-8k）的泛化性。

> **Title:** Harder Is Better: Boosting Mathematical Reasoning via Difficulty-Aware GRPO and Multi-Aspect Question Reformulation
> **Authors:** Yanqi Dai, Yuxiang Ji, Xiao Zhang, Yong Wang, Xiangxiang Chu, Zhiwu Lu
> **Venue:** ICLR 2026 / arXiv:2601.20614
> **Year:** 2026
> **Affiliations:** Renmin University of China, Alibaba Group, Xiamen University, Dalian University of Technology