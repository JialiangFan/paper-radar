# RL for Reasoning in Small LLMs

## 主题/Topic: RL reasoning small models

**论文全名:** Reinforcement Learning for Reasoning in Small LLMs: What Works and What Doesn't
**作者:** Quy-Anh Dang, Chris Ngo (VNU University of Science, Vietnam; Knovel Engineering Lab, Singapore)
**arXiv:** 2503.16219v2 (2026年1月20日)
**代码与数据集:** https://github.com/knoveleng/open-rs

---

## 背景/Background

大型语言模型（LLMs）的推理能力提升通常依赖大规模计算资源和庞大的训练数据集，这使得资源受限环境下的研究者和机构难以复现或部署。OpenAI o1 系列通过扩展推理时间（inference-time scaling）并结合 Chain-of-Thought（CoT）推理，展示了卓越的数学、编程和科学推理性能，但其方法不透明且计算成本极高。DeepSeek-R1 利用 Group Relative Policy Optimization（GRPO）算法，在 671B 参数的 DeepSeek-V3 基础上实现了与 o1 相当的推理性能，但同样因参数规模庞大而难以自托管。

小型 LLMs（1B–10B 参数）提供了一种资源高效的替代方案，前期研究（如 DeepScaleR、Still-3）已证明通过 RL-based 微调可以提升小模型推理能力，但这些方法仍依赖数十万乃至数百万样本及大量算力（如 8× A100 80GB，数百小时训练），不适合资源受限场景。

---

## 现有局限与研究问题/Limitations & Research Problem

**现有局限：**
- 当前 RL-based 推理增强方法（DeepScaleR、Still-3 等）依赖大规模数据集（30k–40k 样本 × 8–16 输出）和昂贵硬件（8× A100 80GB，训练成本 $2268–$3629）。
- 绝大多数研究集中于 7B 以上的大模型，小模型（1.5B）在严格资源约束下的 RL 训练行为尚未得到充分研究。
- 长时间训练存在优化不稳定性（optimization instability）和长度约束（length constraint）问题。
- 多语言基础模型在 RL 训练中存在语言漂移（language drift）问题，训练 150–200 步后会出现非英语输出。

**核心研究问题：**
1. 在严格资源约束（有限算力与训练时间）下，小型 LLMs 进行 RL 微调时表现如何？
2. 类似 DeepSeek-R1 的 RL-based 方法能否有效提升小模型（1.5B）的推理性能？若可以，应如何实施？

---

## 贡献/Contributions

1. **系统分析小型 LLMs 的推理潜力：** 在严格计算约束下（4× NVIDIA A40 48GB，24小时）对 `DeepSeek-R1-Distill-Qwen-1.5B` 进行 RL 微调，提供关于其可扩展性和部署可行性的实践视角。
2. **提供可操作的洞察：** 揭示 RL-based 微调在小型 LLMs 上的有效性与挑战，弥合理论进展与实际应用之间的鸿沟。
3. **开源代码与数据集：** 发布训练代码和策划数据集，支持研究社区的复现与探索。

**主要实验结果（Open-RS 系列模型）：**
- AMC23 准确率从 63% 提升至最高 80%（Open-RS2，50步）
- AIME24 达到 46.7%（Open-RS3），超越 o1-preview（44.6%）
- 平均 benchmark 得分：Open-RS1 53.0%，Open-RS2 55.7%，Open-RS3 56.3%
- 训练成本仅约 **$42**（对比 DeepScaleR 的 $3629，Still-3 的 $2268）

---

## 方法论/Methodology

### 数据集策划（High-Quality Dataset Curation）

构建了一个小型、高质量的数学推理数据集，融合两个来源：

**open-s1 数据集（18,615 样本）：**
- 来源：s1 数据集（Muennighoff et al. 2025），涵盖 NuminaMATH、AIME（1983–2021）、OlympicArena、OmniMath、AGIEval 等
- 过滤流程：保留含 `\boxed{}` 格式答案的题目（59,029 → 31,323）→ 用 `DeepSeek-R1-Distill-Qwen-1.5B` 剔除简单题（→ 21,533）→ 用 `Qwen2.5-7B-Instruct` 去除噪声与多部分题目（→ 18,615）

**open-deepscaler 数据集（21,044 样本）：**
- 来源：DeepScaleR 数据集（Luo et al. 2025），40,315 道数学题（AIME 1984–2023、AMC、Omni-MATH、Still 数据集）
- 过滤流程：用 `Qwen2.5-Math-7B-Instruct` 剔除简单题（→ 21,044）

**最终数据集（open-s1 + open-deepscaler）：** 39,659 道高质量数学推理题

实验二和三使用 7,000 样本混合子集（3,000 open-s1 + 3,000 open-deepscaler + 1,000 简单题）。

### 强化学习算法（Reinforcement Learning Algorithm）

采用 **GRPO（Group Relative Policy Optimization）** 算法（Shao et al. 2024），无需独立 critic 模型，通过组内得分估计基线，降低计算开销。

**GRPO 目标函数：**

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\} \sim \pi_{\theta_\text{old}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left(\frac{\pi_\theta(o_i|q)}{\pi_{\theta_\text{old}}(o_i|q)} A_i, \text{clip}(\cdot, 1-\epsilon, 1+\epsilon) A_i\right) - \beta \mathbb{D}_\text{KL}(\pi_\theta \| \pi_\text{ref}) \right) \right]$$

优势 $A_i$ 从一组奖励 $\{r_1, r_2, \ldots, r_G\}$ 中计算：$A_i = \frac{r_i - \text{mean}(\{r_1,\ldots,r_G\})}{\text{std}(\{r_1,\ldots,r_G\})}$

### 奖励模型（Reward Models）

三个组件的规则-based 奖励系统：
- **Accuracy Reward（准确性奖励）：** 检验最终答案是否以 `\boxed{}` 格式正确呈现，二值评分（0或1）。
- **Cosine Reward（余弦奖励）：** 根据响应长度用余弦调度缩放准确性奖励，鼓励简洁正确的解法，对较长错误解法惩罚较轻，避免过度奖励冗长输出。
- **Format Reward（格式奖励）：** 要求模型将推理过程包含在 `<think>` 和 `</think>` 标签内，保证结构清晰。

### 三组实验（Three Experiments）

**实验一（Experiment 1 - Impact of High-Quality Data）：**
- 数据：open-s1（18,615 样本），最大 completion 长度 4096 tokens
- 奖励：accuracy + format
- 结果：50–100 步内 AMC23 从 63% 升至 70%，MATH-500 从 83% 升至 84%；200 步后性能显著下降（AMC23 降至 60% 以下），KL 散度激增，出现多语言输出
- **Insight 1：** 小型 LLMs 可在 50–100 步内用少量高质量数据快速获得推理增益，但在严格长度约束下长期训练导致性能退化

**实验二（Experiment 2 - Balancing Easy and Hard Problems）：**
- 数据：7,000 样本混合集，最大 completion 长度 3584 tokens
- 奖励：accuracy + format
- 结果：50 步内 AMC23 从 63% 升至 80%，MATH-500 从 83% 升至 85%；150–200 步后不稳定性重现，KL 散度升高，多语言内容复现
- **Insight 2：** 混合简单与困难题目可增强早期表现并稳定推理行为，但长期稳定性仍然难以保证

**实验三（Experiment 3 - Controlling Length with Cosine Reward）：**
- 数据：与实验二相同的 7,000 样本，最大 completion 长度 3584 tokens
- 奖励：cosine reward 替换 accuracy reward + format reward；系统提示强制英语输出
- 结果：completion 长度稳定在 1000–3500 tokens；AMC23 提升至 72.5%，MATH-500 提升至 84.4%（低于实验二峰值但更稳定）；多语言输出仍在 200 步后出现
- **Insight 3：** Cosine reward 有效稳定 completion 长度，提升训练一致性；但对极难任务及多语言基础模型，仍需更长的长度限制或显式语言约束

### 实验设置

- **基础模型：** `DeepSeek-R1-Distill-Qwen-1.5B`（15亿参数，跳过 SFT 阶段，直接 RL 微调）
- **硬件：** 4× NVIDIA A40 GPU（48GB VRAM 每块）
- **训练框架：** 基于 open-r1（Face 2025），适配自 DeepSeek-R1 的 HuggingFace 复现版本
- **超参数：** 每步采样 6 个输出，最大 500 全局步，学习率 1e-6，余弦调度，batch size 6/device
- **评估指标：** zero-shot pass@1（无先验示例）
- **评估 benchmark：** AIME24（30题）、MATH-500（500题）、AMC23（40题）、Minerva（272题）、OlympiadBench（675题）
