# MCTS-DPO - Tree Search Boosts Reasoning via Preference Learning

## 主题 / Topic
MCTS preference learning reasoning

**论文全名**: Monte Carlo Tree Search Boosts Reasoning via Iterative Preference Learning
**作者**: Yuxi Xie, Anirudh Goyal, Wenyue Zheng, Min-Yen Kan, Timothy Lillicrap, Kenji Kawaguchi, Michael Shieh
**机构**: National University of Singapore, Google DeepMind
**arXiv**: 2405.00451v2（2024年6月）
**代码**: https://github.com/YuxiXie/MCTS-DPO

---

## 背景 / Background

大型语言模型（LLM）的对齐（alignment）研究中，偏好学习（preference learning）是关键环节。现有主流方法分为两类：
1. **基于奖励模型的强化学习（RLHF）**：先训练 reward model，再用 PPO 等方法优化策略（policy）。
2. **直接偏好优化（DPO）**：直接利用偏好数据更新模型策略，无需单独训练 reward model。

AlphaZero 的成功表明，将 Monte Carlo Tree Search（MCTS）作为"策略改进算子（policy improvement operator）"，能够将当前策略迭代地变换为更优策略。本文受此启发，将 MCTS 引入 LLM 偏好学习框架中，实现自动化、步骤级别（step-level）的偏好数据采集与策略迭代优化。

---

## 现有局限与研究问题 / Limitations & Research Problem

**传统方法的局限**：
- **实例级（instance-level）偏好信号稀疏**：传统偏好学习在整个回答的层面上收集偏好，忽略了中间推理步骤的质量，导致监督信号粗糙。
- **离线数据的分布偏移（distribution shift）**：DPO 等方法依赖固定的离线偏好数据集，当采样策略与当前策略差异过大时，训练可能失败（Theorem 3.1 形式化证明了此风险）。
- **依赖外部 critic 或 reward model**：MCTS 通常需要一个可靠的 critic 函数来评估 rollout，而训练一个独立的 reward/value 网络本身代价高昂。
- **无法利用推理过程的内部结构**：步骤级别的过程监督（process supervision）相比结果监督（outcome supervision）已被证明更有效，但传统方法难以自动化地提供步骤级信号。

**核心研究问题**：如何利用 MCTS 的前向规划能力（look-ahead ability），自动将实例级奖励分解为步骤级偏好信号，并通过在线迭代方式持续更新 LLM 策略？

---

## 贡献 / Contributions

1. **提出 MCTS-DPO 框架**：将 MCTS 作为在线偏好数据收集器，与 DPO 训练循环结合，构成一个完整的迭代偏好学习框架（MCTS-Enhanced Iterative Preference Learning）。
2. **步骤级偏好数据自动生成**：通过 MCTS 的 Q 值评估，在每个推理步骤深度上自动选取正偏好（高 Q 值）与负偏好（低 Q 值）样本对，无需人工标注。
3. **在线学习设计（online DPO）**：每轮迭代使用当前策略采样新数据，理论证明在线采样能避免离线 DPO 的失败情形（Theorem 3.2）。
4. **自评估机制（self-evaluation）**：模型同时充当 policy 和 critic，用自身评估中间步骤的正确性，既消除外部 reward model 的需求，又提升 Q 值估计质量。
5. **标签平滑（label smoothing via visit counts）**：利用 MCTS 访问计数（visit count）设计自适应标签平滑系数 $\alpha$，减轻 Q 值噪声对训练的影响。
6. **显著性能提升**：在 GSM8K (+5.9%)、MATH (+5.8%)、ARC-C (+15.8%) 等多个推理基准上超越 Mistral-7B SFT baseline，且在未见过的 SciQ 数据集上达到 88.5%。

---

## 方法论 / Methodology

### 整体框架

MCTS-DPO 是一个**迭代在线偏好学习**框架，每次迭代包含两个阶段：

**阶段1：MCTS 采集步骤级偏好数据**
**阶段2：DPO 更新策略**

初始策略 $\pi_{\theta^{(0)}} = \pi_\text{sft}$，经过 $M$ 轮迭代后输出最终策略 $\pi_\theta$。

---

### 2.1 MCTS 步骤级偏好采集

**状态定义**：将推理过程离散化为步骤序列。状态 $s_t$ 定义为推理链的前缀，执行动作 $a$（生成下一推理步骤）后转移至 $s_{t+1}$。

**三阶段 MCTS**：
- **Selection（选择）**：使用 PUCT 公式选择下一节点：
  $$s_{t+1}^* = \arg\max_{s_t} \left[ Q(s_t, a) + c_\text{puct} \cdot p(a \mid s_t) \cdot \frac{\sqrt{N(s_t)}}{1 + N(s_{t+1})} \right]$$
  其中 $p(a \mid s_t) = \pi_\theta(a \mid x, s_t) / |a|^\lambda$（含长度惩罚，防止过长推理链）。
- **Expansion（扩展）**：在叶节点扩展新状态，计算奖励 $R(s_t)$：
  $$R(s_t) = \mathcal{O}(s_t) + \mathcal{C}(s_t)$$
  其中 $\mathcal{O}$ 为结果正确性（1/-1/0），$\mathcal{C}$ 为自评估置信度（模型对当前步骤正确性的 token 概率）。
- **Backup（回溯）**：自底向上更新 Q 值、状态值 V、访问计数 N：
  $$Q(s_t, a) \leftarrow r(s_t, a) + \gamma V(s_{t+1})$$
  $$V(s_t) \leftarrow \sum_a N(s_{t+1}) Q(s_t, a) / \sum_a N(s_{t+1})$$

**偏好对构建**：对深度为 $T$ 的搜索树，每层深度 $t$ 上，选取 Q 值最高的节点作为正样本 $y_w^{(j,t)}$，Q 值最低的节点作为负样本 $y_l^{(j,t)}$（均需来自同一父节点的子节点）。最终得到 $T$ 对步骤级偏好数据。

**搜索广度退火**：初始广度 $b_1$（如4或5），后续步骤减小至 $b_2$（如2或3），在效率与探索之间权衡。

---

### 2.2 迭代偏好学习（DPO 更新）

使用带标签平滑的 DPO 目标函数：
$$\ell_i(\theta) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}_i} \left[ (1 - \alpha_{x,y_w,y_l}) \log \sigma(\beta h_{\pi_\theta}^{y_w, y_l}) + \alpha_{x,y_w,y_l} \log \sigma(-\beta h_{\pi_\theta}^{y_w, y_l}) \right]$$

其中 $h_{\pi_\theta}^{y_w, y_l} = \log \frac{\pi_\theta(y_w \mid x)}{\pi_\text{ref}(y_w \mid x)} - \log \frac{\pi_\theta(y_l \mid x)}{\pi_\text{ref}(y_l \mid x)}$。

标签平滑系数由访问计数决定：
$$\alpha_{x, y_w, y_l} = \frac{1}{N(x, y_w)/N(x, y_l) + 1}$$

访问比例越大（正样本远优于负样本），$\alpha$ 越小（越相信该偏好标签）；访问比例接近1时（偏好不明确），$\alpha$ 接近0.5（软标签）。

---

### 理论分析

- **Theorem 3.1（离线设置可能失败）**：若采样策略 $\pi^{(i)}$ 与当前策略 $\pi_{\theta^{(i-1)}}$ 差异过大（$\epsilon \approx 0$），则以高概率 $1 - 2\epsilon M$ 无法学到最优策略。
- **Theorem 3.2（在线设置保证收敛）**：若 $\pi^{(i)} = \pi_{\theta^{(i-1)}}$（在线采样），则当 $M \geq n+1$ 时，$\pi_{\theta^{(i)}}(y^* \mid x) = 1$。

---

### 实验设置

- **基础模型**：Mistral-7B（SFT 在 Arithmo 数据集，约54万数学与编程题）
- **算术推理数据集**：GSM8K、MATH（CoT 与 PoT 格式）
- **常识推理数据集**：ARC（easy/challenge）、AI2Science、OpenBookQA、CSQA；未见数据集：SciQ
- **Baselines**：SFT baseline、MCTS Offline-DPO、Instance-level Online-DPO、STaR、Crystal、LMSI、Math-Shepherd
- **硬件**：4 x 40GB NVIDIA A100（算术）；搜索深度 $d=4$，MCTS 迭代 $K=5$

---

### 主要结果

| 数据集 | SFT Baseline | MCTS-DPO（Ours） |
|--------|-------------|-----------------|
| GSM8K  | 75.9%       | **81.8%** (+5.9%) |
| MATH   | 28.9%       | **34.7%** (+5.8%) |
| ARC-C  | 60.6%       | **76.4%** (+15.8%) |
| SciQ（未见）| 80.8%  | **88.5%** (+7.7%) |

- 步骤级在线学习一致优于实例级和离线变体。
- 自评估机制（Self-Evaluation）显著提升 MCTS 搜索质量（AUC: 74.7 vs 62.0）。
- 训练计算扩展（training-time compute scaling）优于纯采样推理扩展（inference-time scaling），尤其在 SciQ 上表现出强泛化性。
- Llama2-13B 上验证了框架的泛化性（GSM8K CoT: 74.5% → 78.9%）。
