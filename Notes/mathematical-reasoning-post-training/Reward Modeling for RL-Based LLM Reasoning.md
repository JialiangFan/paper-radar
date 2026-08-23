# Reward Modeling for RL-Based LLM Reasoning

## 主题/Topic: RL reward modeling survey

**论文全称**: Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation
**作者**: Pei-Chi Pan (University of Houston), Yingbin Liang (The Ohio State University), Sen Lin (University of Houston)
**arXiv**: 2602.09305v1 [cs.LG] 10 Feb 2026

---

## 背景/Background

Large Language Models (LLMs) 展现出变革性的推理潜力，但其推理能力仍然不稳定且不可靠。基于 Reinforcement Learning (RL) 的 fine-tuning 是提升 LLM 推理能力的关键机制，而 reward design 是其核心。具体背景如下：

- LLM 当前的推理行为更接近于复杂的启发式聚合（heuristic aggregation），而非真正的逻辑推导；chain-of-thought (CoT) 推理步骤中充斥着不一致和事实错误。
- RL fine-tuning 的范式已超越传统的 Reinforcement Learning from Human Feedback (RLHF)，向更严格的推理对齐演进，包括 Reinforcement Learning from AI Feedback (RLAIF)、Reinforcement Learning with Verifiable Rewards (RLVR) 等。
- 该 fine-tuning 问题可自然地形式化为 Markov Decision Process (MDP)，记作 $\mathcal{M} = (\mathcal{S}, \mathcal{A}, P, r, \pi, H)$，其中 LLM 推理模型作为 agent，目标是最大化累积 reward：$J(\pi_\theta) = \mathbb{E}_{\pi_\theta}\left[\sum_{t=1}^H r(s_t, a_t)\right]$。
- Reward design 的效果受多重因素干扰：RL 算法选择、数据质量、value estimation 方式、采样策略，以及 LLM 的黑箱特性，导致性能提升难以归因与复现。

---

## 现有局限与研究问题/Limitations & Research Problem

**现有工作的局限**:
- Zhong et al. (2025) 提供了广泛的分类体系，但未专注于 reward modeling；
- Liu et al. (2025d) 提供了以 reward 为中心的分类，但缺乏与更广泛推理挑战的全面关联；
- Zheng et al. (2025b)、Wu (2025) 等工作聚焦于 outcome/process reward 模型或通用 RL 方法（RLHF、DPO、GRPO），但未深入探讨 reward modeling 与核心推理挑战（如幻觉控制、基于规划的推理、动态评估、效率-准确性权衡）之间的交互。

**核心研究问题**:
1. Reward modeling 如何从根本上影响 LLM 的内部计算与泛化行为？
2. 在 inference-time scaling、幻觉缓解、augmented reasoning 等系统级挑战中，reward 信号如何作为统一机制发挥作用？
3. 现有 benchmark 评测存在哪些漏洞（如数据污染 data contamination、reward misalignment），如何构建更鲁棒的评测？

---

## 贡献/Contributions

1. **统一框架 RARL (Reasoning-Aligned Reinforcement Learning)**：整合 RLHF、RLAIF、RLVR、DPO 等多种范式，以推理对齐为核心目标，构建统一的 reward modeling 分析视角。

2. **系统性 reward 机制探索与分类**：在 RARL 框架下，将 reward design 分为三大范式——model-based reward、rule-based reward、self-reward，并提供结构化的 taxonomy（涵盖架构、粒度、reward 语义三个维度）。

3. **Reward hacking 的全面分析**：识别并分类 reward hacking 的底层机制，包括 Credit Assignment Bias、Distribution-shift Bias、Length Bias、Position Bias、Faithfulness Bias（Chain-of-Thought Hacking），并综述相应的缓解策略。

4. **将 reward design 与核心 LLM 研究议题关联**：
   - Inference-time scaling（推理时计算扩展）
   - LLM bias 缓解（幻觉、sycophancy、social bias）
   - Augmented reasoning（RAG、tool-integrated reasoning）
   - RL 训练中的多样性崩溃（diversity collapse）与 RL debate

5. **评测基准分析**：针对 text-only 和 multimodal reward 模型，识别现有 benchmark 的关键缺陷（数据污染、静态 benchmark 的局限），并提出更鲁棒评测的方向。

---

## 方法论/Methodology

### 1. RARL 框架与 Reward Design 三大范式

**RARL 统一框架**将 RL fine-tuning 形式化为 MDP，其中 reward 来源于：
- 人类或 AI 标注的 ground truth（human- or AI-annotated supervision）
- 学习得到的或启发式的代理目标（learned or heuristic objectives）

**三大 Reward 范式**：

#### (a) Model-based Reward Design
训练专用 Reward Model (RM) 提供细粒度反馈，沿三个维度分类：

- **架构维度**：
  - *判别式模型 (Discriminative)*：在 decoder-only 架构上加线性头输出标量分数，训练方式包括 Bradley-Terry (BT) loss（成对比较）和 BCE loss（点式分类）。局限：可解释性差、时序不一致性、任务迁移时的 backbone 偏移。
  - *生成式模型 (Generative)*：
    - *概率型 (Probability-based)*：用 token 概率（如 "yes"/"no"）作为 reward 信号，或用对数似然比较 "chosen" vs "rejected" 回复。
    - *批评型 (Critique-based / LLM-as-a-judge)*：生成文本反馈而非标量分数，代表性工作 Con-J (Ye et al., 2025)、ReasonGRM (Chen et al., 2025a)。

- **粒度维度**：
  - *Outcome Reward Model (ORM)*：仅对最终答案赋予 reward，标签效率高但无法区分错误推理步骤。
  - *Process Reward Model (PRM)*：对每个推理步骤赋予 reward，分为 step-level 和 token-level，提供细粒度监督。Step boundary 定义策略包括固定分隔符和自适应置信度方法（Liu et al., 2025g; StepWiser）。

- **Reward 语义维度**：
  - *正确性型 (Correctness-based)*：代表性数据集 PRM800K (Lightman et al., 2023)、MR-GSM8K；
  - *价值型 (Value-based)*：用 Monte Carlo rollout 估计到达正确答案的概率作为 Q-value 标签，代表性工作 Math-Shepherd、OmegaPRM、AgentPRMs；
  - *潜力塑形 (Potential-based Reward Shaping)*：
    - *DPO-Implicit Reward*：$\beta \log \frac{\pi^*(s_t, a_t)}{\pi_{\text{ref}}(s_t, a_t)}$，内嵌于 DPO 训练的 token 级密集 reward，代表性工作 RTO (Zhong et al., 2024)、Q-RM (Chen et al., 2025b)；
    - *Endogenous Reward*：基于 Inverse RL 视角，将 LLM 的 logits 视为最优 Q-function，reward = $\log \pi_{\text{ref}}(a_t|s_t)$，无需额外训练（Li et al., 2025f; 2025b）。

#### (b) Rule-based Reward Design
依赖可验证信号（accuracy、format alignment），reward 稀疏且二元（正确/错误）。代表性范式：
- **RLVR**：$v(x,y) = \alpha$ if correct, 0 otherwise；目标函数：$\max_{\pi_\theta} \mathbb{E}[v(x,y) - \beta D_{\text{KL}}(\pi_\theta(y|x) \| \pi_{\text{ref}}(y|x))]$。
- DeepSeek-R1 的规则：accuracy 组件 + format 组件（`<think>`/`</think>` 标签约束）。
- 挑战：稀疏 reward 导致梯度不稳定（gradient vanishing/explosion in GRPO，Wei et al., 2025），通过 reward dithering（添加零均值扰动噪声）缓解。
- 混合策略：Qwen2.5-Math 将稀疏 outcome reward 与 trained RM 的标量 solution-level reward 结合；PPR (Xu et al., 2025) 训练基于可解释原则的 step-wise PRM。

#### (c) Self-Reward
模型利用自身反馈迭代改进，无需外部规则或模型：
- *Self-Supervised Rewards*：majority voting（自洽性）、maximum-likelihood 优化、model confidence (Wang & Zhou, 2024)；
- *Learned Self-Rewards from Data*：DPO-implicit reward (Fei et al., 2025)、基于 LLM hidden states 的轻量 reward 模型（Guo et al., 2025d，提取各层 concatenated hidden states 经线性变换得到 token-level reward）。

### 2. RL 算法集成

- **PPO (Proximal Policy Optimization)**：在线 RL，clip 目标防止策略过度偏移，advantage 函数 $\hat{A}(x,y) = \sum_{t=1}^T \gamma^{t-1} r_t - V_\phi(x)$；
- **DPO (Direct Preference Optimization)**：离线偏好优化，无需显式 reward 模型；
- **GRPO (Gradient Regularized Policy Optimization)**：去除 value network，使用组内 advantage 估计（normalized group rewards），提升训练效率；
- **DAPO (Decouple Clip and Dynamic sampling PO)**：引入非对称 clip（$\epsilon_{\text{low}}$、$\epsilon_{\text{high}}$），缓解 GRPO 的 entropy collapse。

### 3. Reward Hacking 分类与缓解

| 类型 | 描述 | 代表性缓解方法 |
|------|------|----------------|
| Credit Assignment Bias | 累积 reward 传播导致错误步骤被高奖励覆盖 | PURE (min-form credit assignment), VinePPO (Monte Carlo value estimation) |
| Distribution-shift Bias | 训练分布外输出获得错误高分（extrapolation error） | 在线更新 RM (Cui et al., 2025a)、KL 正则化、Reward Ensemble（LoRA-based，Zhang et al., 2024d）、RetrievalPRM (Zhu et al., 2025a) |
| Length Bias | RM 偏好更长回复，与质量无关 | 局部平均 reward 校正 (Huang et al., 2024c)、step-level length penalty (Zheng et al., 2025a)、DICE (Chen et al., 2024a) |
| Position Bias | LLM-as-a-judge 偏好特定位置的候选答案 | — |
| Faithfulness Bias (CoT Hacking) | 推理链与最终答案语义不一致 | — |
