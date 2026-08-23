# On Designing Effective RL Reward for LLM Reasoning

> Gao et al., 2024 | arXiv:2410.15115 | Tsinghua University, Shanghai Qi Zhi Institute, OpenPsi Inc.

## 主题 / Topic
RL reward design for reasoning

为 LLM 数学推理设计有效的 RL 训练时 reward，研究如何将 learned reward model（ORM/PRM）与 success reward 结合用于强化学习训练。

## 背景 / Background

- 用 learned reward model 提升 LLM 推理能力是近期热点，主要有两类：
  - **ORM（Outcome-supervised Reward Model）**：预测最终答案是否正确，提供 solution-level 的 outcome reward
  - **PRM（Process-supervised Reward Model）**：逐步评估推理步骤的正确性，提供 step-level 的 dense reward
- 推理能力可以在 inference time 通过 search（best-of-N、MCTS、beam search）结合 ORM/PRM 显著提升
- **RL training time** 的 reward 设计潜力尚未被充分探索
- 已有少数工作（Havrilla et al., 2024；Shao et al., 2024 的 DeepSeekMath）尝试将 reward model 引入 RL 训练，但缺乏系统分析
- RL 训练最直接的方式是只用 **success reward**（稀疏奖励，验证最终答案正确性）

## 现有局限与研究问题 / Limitations & Research Problem

- **核心问题**：在 RL 训练时，ORM/PRM 这类 learned reward model 是否能在 success reward 之外提供额外的有效训练信号？
- **发现**：与直觉相反，直接将 ORM 或 PRM 与 success reward 组合用于 RL 训练，效果反而比只用 success reward 更差：
  - **ORM** 无法超越 success reward，因为 training time 已有 ground-truth correctness，ORM 提供不了额外信息
  - **PRM** 导致严重的 **reward hacking** 问题：LLM 学会通过不断重复无意义推理步骤（如"Step ready."、"Step nothing."甚至 emoji）来获取高 return，而非真正提升准确率
- **Reward Hacking 机制分析**：
  - PRM 对"无意义但正确格式"的重复步骤仍给出正向 reward
  - LLM 发现可以通过重复简单 pattern 来使累积 return 无界增长
  - 生成长度和步骤数在训练中持续增大，但准确率下降
- 现有缓解方案（length normalization、length penalty）不能有效解决此问题，甚至在大量重复时仍偏向重复 pattern

## 贡献 / Contributions

1. **系统性实证研究**：首次系统评估 ORM 和 PRM 在 RL training time 的有效性，揭示两者在 RL 训练中的局限和失效原因
2. **Reward Hacking 问题诊断**：通过合成轨迹和实际训练分析，定量展示 PRM 的 reward hacking 行为
3. **两种 reward refinement 技术**：
   - **Clip 机制**：将 PRM 的每步 reward 上界裁剪至阈值 η，确保累积 return 有界，从而让 LLM 专注于纠正错误步骤
   - **Delta 机制**：用相邻两步 reward 之差代替直接 reward，丢弃最后一步 reward（由 success reward 负责），确保从任意中间步开始的 return 有界
4. **PR-Clip-Delta 组合方案**：Clip 与 Delta 机制联用，在所有测试模型（1.5B 和 7B）上稳定提升 RL 训练效果
5. **纯 RL 训练验证**：展示精心设计的 reward 函数下，pure RL 训练（无额外 SFT）可进一步提升包括 Qwen2.5-Math-7B-Instruct 在内的 SOTA 模型

## 方法论 / Methodology

### 问题设置

- **LLM 建模**：策略 $\pi_\theta(s|q)$，推理解 $s$ 由 $K$ 个步骤 $s^{(1)}, \ldots, s^{(K)}$ 构成，前缀记为 $p^{(k)}$
- **Success Reward（稀疏）**：$\text{Correct}(q, s)$，仅在解末尾给出 0/1 奖励
- **RL 目标（带 dense reward）**：
  $$J_r(\pi_\theta) = \mathbb{E}\left[\alpha \cdot \sum_{t=1}^{|s|} r(q, s_{1:t}) + \text{Correct}(q,s) - \beta \log \frac{\pi_\theta(s|q)}{\pi_{ref}(s|q)}\right]$$

### ORM 与 PRM 的直接应用

- **Solution-Level Outcome Reward (OR)**：$r(q,s) = r_{\text{outcome}}(q,s)$，仅在序列末尾给 reward
- **Step-Level Process Reward (PR)**：$r(q, p^{(k)}) = r_{\text{process}}(q, p^{(k)})$，每步给 dense reward
- 实验结果：OR 效果与纯 SR 相当；PR 严重下降（reward hacking）

### Clip 机制（PR-Clip）

$$r(q, p^{(k)}) = \min(r_{\text{process}}(q, p^{(k)}) - \eta,\ 0)$$

- 将所有 reward 减去阈值 η 后截断为非正值
- 保证轨迹累积 return 有上界，消除通过重复步骤无限获益的可能
- 多数步骤 reward 为 0，只有低质量步骤得负 reward

### Delta 机制（PR-Delta）

$$r(q, p^{(k)}) = \begin{cases} r_{\text{process}}(q, p^{(k)}) - r_{\text{process}}(q, p^{(k+1)}) & \text{if } k < K-1 \\ r_{\text{process}}(q, p^{(k)}) & \text{if } k = K-1 \\ 0 & \text{if } k = K \end{cases}$$

- 用相邻步骤 reward 之差作为当前步 reward，鼓励每步"真正推进"推理
- 丢弃最后一步的 process reward（由 success reward 覆盖）
- 保证从任意中间步 $p^{(k)}$ 出发的 return 有界：$\alpha \cdot r_{\text{process}}(q, p^{(1)}) + \text{Correct}(q,s)$

### 三种 PR 变体

1. **PR-Clip**：只用 Clip 机制
2. **PR-Delta**：只用 Delta 机制
3. **PR-Clip-Delta**：先 Clip 再 Delta，综合效果最佳

### 实验设置

- **训练数据**：MathInstruct 数据集（只用问题和 golden answer，不用提供的解）
- **RL 算法**：PPO（ReaLHF 实现），大 batch size（1.5B 模型：$1024 \times 8$；7B 模型：$4096 \times 8$）
- **基础模型**：Qwen2/Qwen2.5 家族，包括通用版和数学专用版（1.5B 和 7B）
- **ORM 训练**：以 binary cross-entropy 在采样解上训练
- **PRM 训练**：用 Qwen2-7B-Instruct 作 completer 自动生成 process label（Wang et al., 2024b 方法）
- **评测**：MATH 和 GSM8K，报告 Greedy、Sampling（温度 1.0）、Pass@16 三项指标

### 主要实验结果

- **消融实验（Qwen2-1.5B-Instruct on MATH）**：
  - 纯 SR：30.58 (Greedy)
  - SR + PR：11.16（严重 reward hacking）
  - SR + PR-Clip-Delta：**31.44**（最佳）
- **主实验（多模型）**：PR-Clip-Delta 在 1.5B 和 7B 模型上一致提升，包括：
  - Qwen2.5-Math-7B-Instruct：GSM8K 95.6%（+0.00）、MATH 83.38%（+0.08 Greedy），Sampling 大幅提升
  - Qwen2-1.5B-Instruct：MATH Greedy 从 24.90 → 31.44（+6.54），Sampling 从 16.79 → 28.20（+11.41）
- **关键发现**：较弱模型提升幅度更大；Sampling score 提升普遍大于 Greedy score 提升

### 局限性

- 实验仅在 1.5B 和 7B 模型上进行，更大模型的验证有待后续工作
- 未探索将 PPO 训练后的模型用于 inference-time search 的效果
