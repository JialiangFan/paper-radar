# ReST-MCTS - LLM Self-Training via Process Reward Tree Search

## 主题 / Topic
MCTS-guided LLM self-training（基于蒙特卡洛树搜索引导的大语言模型自训练）

**论文信息**
- 作者：Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue, Yuxiao Dong, Jie Tang（清华大学知识工程组 KEG，加州理工学院）
- 会议：NeurIPS 2024
- ArXiv：2406.03816
- 代码：https://github.com/THUDM/ReST-MCTS

---

## 背景 / Background

大语言模型（LLM）的自训练（self-training）已成为提升推理能力的重要范式。现有方法（如 STaR、RFT、ReST^EM）通常依赖以下流程：
1. 用 LLM 生成多个候选解答（CoT traces）
2. 筛选最终答案正确的解答作为训练数据
3. 用这些"正样本"对 LLM 进行 SFT 微调
4. 重复迭代

这类方法需要一个 **reward signal**（奖励信号）来选取高质量样本。奖励信号通常来自：
- **ORM（Outcome Reward Model）**：只看最终答案是否正确
- **PRM（Process Reward Model）**：对每个推理步骤评分

此前研究表明 PRM 比 ORM 能提供更可靠的反馈，尤其在有假阳性（最终答案偶然正确但推理过程错误）时。

---

## 现有局限与研究问题 / Limitations & Research Problem

**核心问题**：现有自训练方法的训练数据质量低。

1. **假阳性推理链**：LLM 经常生成错误或无用的中间推理步骤，但最终凑巧得到正确答案。这类"低质量正样本"污染训练集，限制微调效果。

2. **PRM 训练依赖人工标注**：训练可靠的 PRM 通常需要对每个推理步骤进行密集的人工标注（per-step human annotation），代价极高，难以扩展。

3. **奖励信号稀疏**：若只用最终答案作为监督信号，则面临类似 RL 中的 credit assignment 问题——难以判断哪些中间步骤真正有贡献。

**研究问题**：**如何在无需人工标注的前提下，自动获取高质量推理轨迹与可靠的逐步过程奖励信号？**

---

## 贡献 / Contributions

1. **提出 ReST-MCTS\***：一个将 Process Reward Model（PRM）与改进版 MCTS\* 树搜索结合的强化自训练框架，能够同时提升 policy model 和 PRM 的质量，无需人工标注过程奖励。

2. **自动推断过程奖励**：通过在搜索树中执行充分次数的 rollout，自动为每个中间推理节点估计 process reward（quality value $v_k$），绕过了人工标注瓶颈。

3. **更优的树搜索策略**：在相同搜索预算下，ReST-MCTS\* 的搜索策略比 Self-Consistency（SC）和 Best-of-N（BoN）等基线达到更高精度。

4. **超越现有自训练方法**：在 LLaMA-3-8B-Instruct、Mistral-7B、SciGLM-6B 三种 backbone 上，多轮迭代后显著优于 ReST^EM 和 Self-Rewarding LM。

5. **PRM 质量提升**：ReST-MCTS\* 生成的过程奖励数据训练出的 PRM 在 GSM8K 和 MATH500 上优于 MATH-SHEPHERD。

---

## 方法论 / Methodology

### 整体框架

ReST-MCTS\* 由四个核心模块组成，交替迭代运行：

| 模块 | 功能 |
|------|------|
| **MCTS\***（改进版蒙特卡洛树搜索）| 以 PRM 为 value function 进行树搜索，收集高质量推理轨迹 |
| **Process Reward Model（PRM）** $V_\theta$ | 评估任意部分解答的质量值 $v_k$，引导 MCTS\* 搜索 |
| **Policy Model** $\pi_\phi$ | 生成各问题的多步推理候选步骤 |
| **LLM Self-Training** | 用 MCTS\* 收集的正样本训练 policy model；用全部轨迹训练 PRM |

### 核心概念：Quality Value 与 Weighted Reward

**Reasoning Distance $m_k$**：部分解答 $p_k = [s_1, \ldots, s_k]$ 距离正确答案还需要的最少推理步数。$m_k$ 通过在 $p_k$ 起点进行多次 rollout 估计。

**Weighted Reward $w_{s_k}$**（单步加权奖励）：
$$w_{s_k} = \frac{1 - v_{k-1}}{m_k + 1}(1 - 2r_{s_k})$$
其中 $r_{s_k}$ 是 PRM 对步骤 $s_k$ 的 sigmoid 输出分数。

**Quality Value $v_k$**（部分解答的累积质量值，用于引导搜索）：
$$v_k = \max(v_{k-1} + w_{s_k},\ 0), \quad v_0 = 0$$

性质（Theorem 1）：$w_{s_k} \leq 1 - v_{k-1}$，$v_k \in [0,1]$；$v_k \to 1$ 当且仅当推理路径趋向正确答案。

### MCTS\* 搜索算法

每次迭代包含四个阶段：
1. **Node Selection**（节点选择）：用 UCB 类策略选择质量值高且探索不足的节点
2. **Thought Expansion**（思维扩展）：policy model 从当前节点扩展新推理步骤
3. **Greedy MC Rollout**（贪心蒙特卡洛模拟）：从扩展节点快速模拟至终态，估算 $m_k$
4. **Value Backpropagation**（价值回传）：将 $v_k$ 向根节点回传更新

Self-critic 机制：PRM 内置一致性检验，过滤矛盾推理步骤，提升搜索精度。

### 自训练流程（Algorithm 1）

```
初始化：policy π_{S_0}（SFT on D_{S_0}），value model V_0（训练于 D_{V_0}）
for i = 1 to T do:
    1. 用 π_{S_{i-1}} + V_{i-1} 引导 MCTS* 在 D_G 上搜索，生成合成数据 D_{G_i}
    2. 筛选正确解答（答案匹配），形成 D_{G_i}(A_j=a*)
    3. SFT 微调 policy model → π_{S_i}
    4. 从 D_{G_i} 提取 (Q, p, v) 三元组 → D_{V_i}
    5. 训练 value model V_{i-1} on D_{V_i} → V_i
```

**Policy Model 训练**：SFT，最小化负对数似然：
$$\mathcal{L}_\text{SFT}(\pi) = -\mathbb{E}_{(Q,s)\in D_{S_0}}\left[\sum_{t=1}^T \log\pi(s_t|s_{<t},Q)\right]$$

**PRM 训练**：Binary cross-entropy，对每一步预测 $r_{s_k}$，label 由树搜索自动推断（无需人工）。

### 实验亮点

- **SciBench + MATH 上的搜索效率**（Figure 2）：相同 token 预算下，ReST-MCTS\* 精度显著优于 SC 和 Best-of-N，且随预算增加持续提升（SC 很快饱和）。
- **GSM8K 验证器对比**（Table 3）：SC+ReST-MCTS\*（Value）在 GSM8K 上达 87.5%，MATH500 上达 39.0%，均超过 MATH-SHEPHERD。
- **多轮自训练**（Table 2）：在三种 backbone 上，第 2 轮迭代后 ReST-MCTS\* 均优于 ReST^EM 和 Self-Rewarding。
- **SciBench 推理策略对比**（Table 4）：ReST-MCTS\* 在化学、物理、数学三大学科上超越 CoT 和 ToT 基线。

### 局限性

- 目前主要验证在数学推理领域，尚未充分扩展至编程、Agent 等任务
- 对无 ground-truth 的场景（如对话、SWE-Bench）的适用性有待探索
- 小规模 policy（如 LLaMA2-13B-Chat）提升有限，逐步推理能力不足时树搜索优势受限
