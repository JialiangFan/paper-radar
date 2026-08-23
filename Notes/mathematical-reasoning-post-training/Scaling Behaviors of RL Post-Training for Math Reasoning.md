# Scaling Behaviors of RL Post-Training for Math Reasoning

> Tan et al., arXiv:2509.25300, 2025年12月
> 机构：中国科大、上海AI实验室、牛津大学、帝国理工、佐治亚大学、香港中文大学、中科院、大连理工、南洋理工、武汉大学
> 代码：github.com/tanzelin430/Mathematical-Reasoning-RL-Scaling-Law
> 数据集：huggingface.co/datasets/Artemis0430/GURU-MATH-CL

## 主题/Topic: RL post-training scaling laws

本文系统地研究了大语言模型（LLM）在强化学习（RL）post-training阶段的scaling behavior，聚焦于数学推理任务，旨在建立类似预训练scaling law的预测性公式。

---

## 背景/Background

- 预训练阶段的scaling law（Kaplan et al. 2020; Hoffmann et al. 2022）已被广泛研究：loss与模型规模N、数据量D、计算量C之间遵循幂律（power law）关系。
- RL post-training近年来成为提升LLM数学推理能力的主流方法（DeepSeek-R1、Kimi k1.5、GRPO等），但其scaling behavior几乎未被系统研究。
- 已有工作（Hilton et al. 2023）在单智能体RL中发现power-law scaling，但针对LLM RL fine-tuning的系统性实证研究仍缺失。
- RL post-training面临三种关键资源约束场景：**compute-constrained**（固定FLOPs预算）、**data-constrained**（固定唯一样本数）、**data reuse**（固定计算预算下权衡唯一数据量与重复优化步数）。

---

## 现有局限与研究问题/Limitations & Research Problem

- **未知问题**：RL post-training的scaling behavior是否也遵循幂律？模型规模、数据量和计算预算如何共同决定最终性能？
- **局限**：现有工作缺乏对RL post-training中模型规模（N）、compute（C）、数据量（D）三者相互作用的定量刻画。
- **核心疑问**：
  1. 在固定计算或数据预算下，应优先选择更大模型还是更多训练步数？
  2. 数据受限时，重复使用高质量数据是否有效？
  3. RL post-training的收益能否迁移到域外任务？
  4. 学习效率k(N)是否随模型规模无限增长？

---

## 贡献/Contributions

本文提出四个核心发现：

1. **大模型具有更高学习效率**：在compute和data两个维度上，更大的模型均表现出更高的learning efficiency，但效率增益存在饱和趋势（超过32B后边际收益递减）。

2. **可预测的幂律公式**：test loss L、模型规模N、资源预算X（计算量C或数据量D）之间的关系可用以下公式建模，对base model和instruction-tuned model均成立：
   $$\log L(N, X) = -k(N) \cdot \log X + E(N)$$
   其中学习效率：
   $$k(N) = \frac{K_{\max}}{1 + \frac{N_0}{N}}$$
   该公式揭示k(N)趋近于上限$K_{\max}$，**不会无限增长**。

3. **k(N)存在潜在饱和趋势**：尽管大模型学习效率更高，但k(N)的增长速度随规模增大而减缓，表明模型规模扩展的收益趋于饱和。

4. **数据受限场景下数据复用高度有效**：最终性能主要由总优化步数（D_total）决定，而非唯一样本数。在reuse factor τ ≤ 25时，性能几乎无显著下降。

---

## 方法论/Methodology

### 实验设置

- **模型家族**：Qwen2.5 dense model系列（0.5B、1.5B、3B、7B、14B、32B、72B），参数量为唯一变量。
- **训练框架**：VeRL（大规模RL平台），确保一致性和可复现性。
- **训练数据**：guru-RL-92k数据集的数学子集，经去重和难度过滤后得到的高质量问题，按通过率升序排列实现curriculum learning（课程学习）。
- **评估集**：500道数学题（held-out set）用于拟合scaling law；泛化评估跨越数学（AIME2024、AMC2023、GSM8K、MATH500）、代码（HumanEval）、逻辑（Zebra Puzzle）、科学（SuperGPQA）。
- **RL算法**：GRPO（Group Relative Policy Optimization），通过对同一prompt的多个输出归一化reward估计advantage：
  $$\mathcal{L}_{\text{GRPO}} = \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t=1}^{|o_i|}\left\{\min\left[\rho(\theta)\hat{A}_{i,t},\,\text{clip}(\rho(\theta), 1-\varepsilon, 1+\varepsilon)\hat{A}_{i,t}\right] - \beta D_{\text{KL}}\right\}$$
- **奖励机制**：二元规则奖励（Pass@1），通过脚本对比模型输出（\\boxed{}格式）与标准答案。
- **评估指标**：test loss $L = 1 - R/R_{\max}$，与预训练scaling law文献保持一致。

### Scaling Law拟合与预测

- **Inter-model Extrapolation**：用小模型（0.5B–32B）拟合scaling law参数，外推预测72B模型性能。
- **Intra-model Prediction**：仅用训练早期数据预测同一模型的后续训练轨迹。
- 每种配置重复**三次**实验（base model和instruct model各一套），提供统计不确定性分析（Average Standard Deviation和Standard Error of the Mean）。

### 三类Scaling场景

| 场景 | 定义 | 核心公式 |
|------|------|---------|
| Compute-Constrained | 固定FLOPs C，求最优N和D | $\log L(N,C) = -k_C(N)\cdot\log C + E_C(N)$ |
| Data-Constrained | 固定唯一样本数D，求最优N | $\log L(N,D) = -k_D(N)\cdot\log D + E_D(N)$ |
| Data Reuse | 固定D_total，变化reuse factor τ | $\arg\min_\tau L(\tau)$ s.t. $D_{\text{unique}} \times \tau = D_{\text{total}}$ |

### 主要实验结论

- **Compute scaling**（Observation 1）：在0.5B–32B范围内，固定计算预算下优先选大模型；但32B–72B之间学习效率饱和，出现模型规模与训练步数的trade-off。
- **Data scaling**（Observation 2）：固定唯一数据量时，大模型一致表现出更高sample efficiency。
- **模型规模扩展**（Observation 3）：训练至收敛后，test loss随模型规模单调递减，但偏离严格幂律（小模型边际收益较弱）。
- **数据复用**（Observation 4）：τ ≤ 25时性能几乎不降；τ = 100时出现明显过拟合。
- **域迁移**（Observation 5）：RL post-training强化域内数学推理泛化，但对域外任务（代码、逻辑推理）迁移效果几乎为零，甚至在逻辑推理（Zebra Puzzle）任务上出现性能退化。

### 实验规模

- 共训练63个LLM（用于scaling law拟合）+ 控制实验若干，横跨0.5B–72B，总计54组受控实验。
