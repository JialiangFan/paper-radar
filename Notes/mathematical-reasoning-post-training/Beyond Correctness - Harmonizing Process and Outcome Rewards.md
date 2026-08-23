# Beyond Correctness - Harmonizing Process and Outcome Rewards

## 主题 / Topic
Process-outcome reward harmonization

本文提出 **PROF（PRocess cOnsistency Filter）**，一种数据筛选框架，通过协调粗粒度的 Outcome Reward Model（ORM）与细粒度的 Process Reward Model（PRM），提升大语言模型在数学推理任务中的强化学习训练质量。

- arXiv: 2509.03403
- 作者：Chenlu Ye, Zhou Yu, Ziji Zhang, Hao Chen, Narayanan Sadagopan, Jing Huang, Tong Zhang, Anurag Beniwal（Amazon / UIUC）
- 代码：https://github.com/Chenluye99/PROF

---

## 背景 / Background

- 带可验证奖励的强化学习（RLVR）是当前数学推理任务的主流训练范式，能持续提升模型推理能力。
- **ORM（Outcome Reward Model）**：仅根据最终答案是否正确给出奖励（+1/-1），奖励信号粗糙、稀疏，无法区分"正确答案但推理过程有缺陷"与"完全正确的推理"。
- **PRM（Process Reward Model）**：对推理链中每个中间步骤打分，提供细粒度过程监督，但存在严重的 reward hacking 风险——模型可能通过生成冗长、重复步骤来虚抬平均 PRM 分。
- 直接将 PRM 与 ORM 加权混合（Blend-PRM-GRPO）会导致熵崩塌（entropy collapse）和响应长度不受控增长，测试性能甚至低于纯 GRPO baseline。
- Chain-of-Thought（CoT）的质量与可解释性对模型的实际推理能力至关重要，不仅仅是最终答案的准确率。

---

## 现有局限与研究问题 / Limitations & Research Problem

**核心问题**：如何将准确但粗粒度的 ORM 与细粒度但嘈杂的 PRM 在强化学习中有效协同？

**现有方法的局限：**

1. **ORM 粒度不足**：无法识别"答案正确但推理有缺陷"的样本，将错误推理引入训练会引入噪声梯度，干扰学习。
2. **PRM 的 reward hacking**：预训练 PRM 在 online 训练时遭遇分布偏移，边界问题上判断失准；模型可通过过度生成冗长步骤骗取高 PRM 分。
3. **简单加权混合脆弱**：Blend 方法（Zha et al., Cui et al., Zou et al.）将 PRM 直接加入梯度，暴露于 reward hacking，导致熵崩塌与性能下降。
4. **在线 PRM 协同训练代价高**：需要 LLM-as-a-judge 或 Monte Carlo 步骤级评估，推理成本极高。

---

## 贡献 / Contributions

1. **提出 PROF 框架**：一种数据筛选（data curation）方法，利用 PRM-ORM 一致性（consistency）对训练样本进行排序与过滤，而非将 PRM 直接引入梯度。
   - 过滤掉"答案正确但过程得分低（推理有缺陷）"的样本。
   - 过滤掉"答案错误但过程得分高（含合理推理步骤）"的样本（但保留合理比例）。
2. **正负样本分组过滤**：分别对正确组（G+）和错误组（G-）独立排序过滤，维持正负样本平衡比例，防止偏差性移除。
3. **实验验证**：
   - 在 Math500、Minerva Math、Olympiad Bench、AMC2023、AIME2024 五个基准上，PROF-GRPO 相比 GRPO 平均提升 4%+，相比 Blend-PRM-GRPO 提升更大。
   - Qwen2.5-Math-7B-base 上达到平均 51.7%（GRPO: 49.9%，Blend: 47.3%）。
4. **中间推理质量提升**：Monte Carlo 估计、PRM 平均分、LLM-as-a-judge 三项指标均显示 PROF-GRPO 生成更详细、可验证的推理步骤。
5. **抗 reward hacking**：PROF 通过将 PRM 用于筛选而非梯度，有效规避 reward hacking 与熵崩塌问题。

---

## 方法论 / Methodology

### 基础设置

- **策略模型**：LLM 作为策略分布 π(a|x)，对每个 prompt x 生成 n 个 rollout。
- **ORM**：验证最终答案正确性，给出二值奖励 r_o ∈ {-1, +1}。
- **PRM**：对 CoT 中每个步骤 a^h 打分，得到步骤级奖励序列 {r^1, ..., r^H}。
- **基础 RL 算法**：GRPO（Group Relative Policy Optimization），通过组内标准化优势函数更新策略，无需额外 value network。

### PROF 核心算法（Algorithm 1）

**输入**：n 个 rollout，policy update size m，ORM 奖励，步数正则化参数 λ 和 H_λ。

**步骤：**

1. **计算轨迹级一致性分数 r^pro**：
   - 对每个 rollout，调用 PRM 获取各步骤奖励。
   - 计算平均 PRM 分，加入步数惩罚项（若步数 = 1 或步数 ≥ H_λ，则扣分），再乘以 ORM 奖励：
     `r^pro_i = [mean(r^h) - λ·I(H_i=1 or H_i≥H_λ)] · r_o,i`
   - 步数正则化确保过短（无推理）或过长（冗余堆砌）的响应不进入训练。

2. **分组**：将 n 个 rollout 分为正确组 G+（r_o=+1）和错误组 G-（r_o=-1）。

3. **计算各组丢弃数 k+, k-**：
   - 保持正负比例平衡，使最终 kept size = m，且 Δ = n+ - n- 的偏差通过两组丢弃数调节：
     `k+ = min(n-m, ⌈(Δ+n-m)/2⌉), k- = n-m-k+`

4. **分组排序过滤**：
   - G+ 按 r^pro 降序排列，保留分数高的（高 PRM-ORM 一致性的正确样本）。
   - G- 按 r^pro 升序排列，保留分数低的（低 PRM-ORM 一致性的错误样本，即"答案错误且推理也差"）。
   - 最终保留 K+ ∪ K-，共 m 个轨迹用于策略更新。

5. **策略更新**：使用 GRPO 在保留轨迹上更新策略。

### 关键设计选择

- **分组独立过滤的必要性**：若不分组，PRM 倾向于给错误样本较低分（因为错误样本通常含多个错误中间步骤，步数越多平均分越低），导致错误样本被过度丢弃，破坏正负平衡。实验表明不分组（w/o Separation）会造成 >2% 的训练奖励偏差。
- **使用均值而非最小值/求和**：均值对单个差步骤不过敏，也不偏向长轨迹，是最稳定的一致性估计。
- **Rollout 数 n 的权衡**：n=8 为最优（PROF-GRPO Both），更大的 n 会因 PRM 影响过强而触发 reward hacking。

### 实验设置

- **训练数据**：Numina-Math（~860k 数学题，含高中至国际竞赛题）。
- **基础模型**：Qwen2.5-Math-1.5B-base、Qwen2.5-Math-7B-base、LLaMA-3.2-3B-instruct。
- **PRM**：Qwen2.5-Math-PRM-7B。
- **评估**：5 个基准，average@16（temperature=1.0，每题 16 次采样取平均）。
- **实现**：基于 verl 框架，AdamW 优化器，lr=1e-6，8 张 H100 GPU，mini-batch=256，最大生成长度 4096 tokens。

### 消融研究结论

- **Filter-Correct（只过滤正确组）vs Filter-Both（两组都过滤）**：两者性能相近，Filter-Correct 在跨模型泛化（LLaMA）时更稳健（PRM 可靠性较低时）；Filter-Both 在 PRM 高质量时收敛更快。
- **LLaMA-3.2-3B 泛化**：PROF-GRPO (Both) 达 23.9%（GRPO: 23.6%），Filter-Correct 达最高 25.4%，均优于 Blend-PRM-GRPO（15.7%）。
