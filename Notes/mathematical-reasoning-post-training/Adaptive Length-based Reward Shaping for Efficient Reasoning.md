# Adaptive Length-based Reward Shaping for Efficient Reasoning

> **完整标题**: Learn to Reason Efficiently with Adaptive Length-based Reward Shaping
> **作者**: Wei Liu, Ruochen Zhou, Yiyun Deng, Yuzhen Huang, Junteng Liu, Yuntian Deng, Yizhe Zhang, Junxian He
> **机构**: 香港科技大学, 香港城市大学, 滑铁卢大学, Apple
> **arXiv**: 2505.15612v1 (2025年5月21日)
> **代码**: https://github.com/hkust-nlp/Laser

## 主题 / Topic
Length-aware reward shaping

利用基于长度的 reward shaping 方法提升 Large Reasoning Models (LRMs) 的推理效率，通过 reinforcement learning (RL) 训练使模型在保持准确率的同时大幅减少 token 使用量。

---

## 背景 / Background

Large Reasoning Models (LRMs) 通过 RL 训练获得了强大的推理能力，能够生成长 chain-of-thought (CoT) 轨迹来解决复杂问题。然而，这些扩展输出往往包含大量冗余，具体表现为：

- 对简单问题生成数千 token 的冗长推理过程（"over-thinking"问题）
- 反复出现无意义的 "self-reflection" 模式（如 "recheck", "rethink", "try again", "wait"）
- token 效率低下，推理性能与 token 消耗之间存在显著的 efficacy-efficiency trade-off

现有的 RL 训练框架（如 DeepSeek-R1 使用的 GRPO）主要优化推理正确性，未对输出长度进行约束。

---

## 现有局限与研究问题 / Limitations & Research Problem

**已有方法的分类与局限**：

论文将现有高效推理方法统一为 reward shaping 框架 $\hat{R}(x,y) = C(y) + \lambda(y) \cdot S(y)$，其中 $C(y)$ 为正确性奖励，$S(y)$ 为长度奖励，并分析了各类方法的不足：

1. **Truncation（截断法）**：直接限制 context window（如 T_8192），虽然有效但对困难问题影响过大（AIME 上准确率下降 4.1 分），因为困难问题本身需要更长推理。截断比例在训练初期高达 45%+。

2. **Group-based Reward**（如 Efficient Reasoning, Kimi-k1.5）：在 rollout group 内比较长度、鼓励简短回复。容易导致 reward hacking——模型通过生成过短回答来最大化 $S(y)$，初期 training accuracy 下降而 reward 上升。

3. **Budget-based Reward**（如 L1-Exact, L1-Max）：使用 query-specific target length，对偏离目标长度的回复进行惩罚。在大 context window（16,384 tokens）下 target 分布稀疏，导致训练不稳定、reward 波动大。

**核心问题**：
- 现有方法无法同时在 accuracy 和 token efficiency 上取得改进
- 固定 target length 无法适应模型训练过程中推理行为的动态变化
- 未区分问题难度，对简单和困难问题施加相同的长度压力

---

## 贡献 / Contributions

1. **统一框架**：首次将截断法、group-based reward、budget-based reward 等多种高效推理方法统一在 length-based reward shaping 的框架下，便于系统比较和分析。

2. **LASER（Length-bAsed StEp Reward）**：提出以 step function 为 reward 形式、以 target length $L_T$ 为门限的新方法。对长度不超过 $L_T$ 的正确回复给予额外奖励，避免对过长但正确的探索施加过重惩罚，实现比所有 baseline 更优的 Pareto-optimal 均衡。

3. **LASER-D（Dynamic and Difficulty-aware）**：识别 LASER 的两个关键局限并提出改进：
   - **动态性**：target length 应随训练进程动态调整
   - **难度感知**：简单问题应有更严格的长度约束，困难问题应允许更长推理
   - 引入**自动自适应机制**（无需人工干预）

4. **LASER-DE**：LASER-D 的变体，对错误且超长的回复施加较小惩罚，鼓励对困难问题的进一步探索。

5. **实验验证**：在 1.5B、7B、32B 三种规模模型上，跨 MATH500、AIME2024、AMC2023、OlympiadBench 四个 benchmark 全面验证，并测试 out-of-domain 泛化能力（GPQA、LSAT、MMLU）。

---

## 方法论 / Methodology

### 统一 Reward Shaping 框架

$$\hat{R}(x,y) = C(y) + \lambda(y) \cdot S(y)$$

- $C(y)$：正确性奖励（rule-based：正确 +1，格式错误 -1，答案错误 -0.5）
- $S(y)$：长度奖励项，各方法设计不同
- $\lambda(y)$：控制变量，调节长度奖励的应用方式

使用 GRPO 优化目标（KL-constrained RL）。

### LASER 设计

$$S(y) = \alpha \cdot \mathbb{1}(L(y) \leq L_T)$$

- 对长度不超过 $L_T$ 的**正确**回复给予 $\alpha$ 的额外奖励（$\alpha = 0.5$）
- Context window 设置远大于 $L_T$（如 16,384 vs 4,096），使截断极少发生
- 与截断法的本质区别：不惩罚过长但正确的探索，只奖励简洁正确的回复

### LASER-D：动态难度感知机制

**难度分级**：将问题分为 easy/medium/hard 三档，基于 rollout group 内的正确率（使用 $k/3$ 和 $2k/3$ 为阈值，$k$ 为 rollout 数量），三档各有独立的 target length 超参数 $L_A^{easy}, L_A^{medium}, L_A^{hard}$。

**自动自适应模块（ECR 机制）**：
- 每 N 步（如 20 步）从监控数据集 $\mathcal{D}^M$（约 500 样本）评估一次
- 定义 **Expected Correct Responses (ECR)**：$ECR_d = P_{l,d} \cdot |C_d|$，其中 $P_{l,d}$ 为覆盖率（长度 $\leq l$ 的回复比例），$|C_d|$ 为该难度档的最少正确回复数
- 选取满足 $ECR_d \geq 1$ 的**最小** target length 作为 $L_A$，确保至少期望有一个完整正确回复
- 从 $L_T$ 开始向上枚举（步长 $I$），直到最大 context window（16,384）

**难度-长度对应关系**：简单问题 target length 小（training 中快速收敛到短 target）；困难问题 target length 维持在接近 context window 的较大值。

### LASER-DE 变体

$$S(y) = \alpha \cdot \mathbb{1}(R) \cdot \mathbb{1}(L(y) \leq L_A) + \alpha \cdot (1 - \mathbb{1}(R)) \cdot \mathbb{1}(L(y) > L_A)$$

对错误且**超过** target length 的回复也给予正向奖励，鼓励模型对错误答案进行更多探索，有助于发现潜在正确的推理模式。

### 实验设置

- **基础模型**：DeepSeek-R1-Distill-Qwen-1.5B / 7B / 32B
- **训练数据**：DeepScaleR-Preview-Dataset（40K 竞赛级数学题）
- **训练框架**：verl，使用 DAPO clip-higher 策略
- **Rollout**：batch size 128，每 prompt 8 次 rollout，temperature 0.6
- **评估**：MATH500、AIME2024、AMC2023、OlympiadBench；out-of-domain: GPQA、LSAT、MMLU

### 主要实验结果

**1.5B 模型（DeepSeek-R1-Distill-Qwen-1.5B）**：
- LASER-D ($L_T=1024$) 在 AIME2024 上达到 **58.3% 准确率**，token 平均仅 **5,379**（原始模型 28.9% 准确率，15,956 tokens）
- LASER-DE 在 AIME2024 上准确率 **35%**，token 约 5,500（比原始模型减少 **63%**）
- 相比原始模型：+6.1 准确率，-63% token 用量

**7B 模型**：LASER-D 在 AIME 上达到 90.0% 准确率，平均 5,379 tokens。

**32B 模型**：LASER-DE 在保持接近原始准确率的同时减少约 38% token。

**Out-of-domain 泛化**：LASER、LASER-D、LASER-DE 在 GPQA、LSAT、MMLU 上均显示出显著的 accuracy 和 token 效率双重提升，证明方法的泛化能力。

### 推理行为分析

- **Self-reflection 关键词**下降：训练后 "recheck"、"rethink"、"try again" 等词频显著降低，冗余 self-reflection 减少
- **Backtracking 行为**比例从 30%+ 降至约 10%，而 Verification、Enumeration、Subgoal Setting 等核心推理行为保持稳定
- 模型转向更简洁、结构化的表达方式，减少无效回溯而非简单截短推理
