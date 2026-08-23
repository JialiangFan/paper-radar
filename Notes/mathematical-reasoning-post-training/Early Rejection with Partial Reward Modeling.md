# Early Rejection with Partial Reward Modeling

**论文标题**: Accelerating LLM Reasoning via Early Rejection with Partial Reward Modeling
**作者**: Seyyed Saeid Cheshmi, Azal Ahmad Khan, Xinran Wang, Zirui Liu, Ali Anwar（明尼苏达大学）
**arXiv**: 2508.01969v1 [cs.LG]，2025年8月4日
**代码**: https://github.com/scheshmi/accelerated-reasoning-ER-PRM

---

## 主题/Topic: PRM-based early rejection

利用 Process Reward Model（PRM）在推理步骤生成过程中途进行评分，实现对低质量 beam 的早期拒绝（Early Rejection），从而在不损失最终性能的前提下大幅降低推理计算开销。

---

## 背景/Background

- 大型语言模型（LLM）在数学、逻辑、多步问答等复杂推理任务中表现出色，推理能力的提升已成为核心研究方向。
- 扩展推理时计算量（inference-time compute scaling）是提升推理质量的主流策略，代表方法包括 Best-of-N（BoN）解码、beam search、Monte Carlo Tree Search（MCTS）等。
- **Outcome Reward Model（ORM）** 对最终输出评分；**Process Reward Model（PRM）** 对每个中间推理步骤评分，提供更密集的监督信号，已被证明能改善推理泛化能力。
- 在 PRM 引导的 beam search 中，模型并行生成 N 条候选推理路径，每步结束后由 PRM 打分并保留得分最高的 beam，逐步构建多步推理链。
- 实际应用中，beam 数量需要扩展到 1000–60000 条，产生大量输出 token，计算代价极高，且候选序列顺序生成带来显著延迟。

---

## 现有局限与研究问题/Limitations & Research Problem

**现有局限：**
- 标准 PRM 引导的 beam search 需等待每步完整生成后才进行评分，大量计算浪费在最终会被淘汰的低质量 beam 上。
- Speculative Rejection（Sun et al., 2024）等方法已尝试用 ORM 在 BoN 中途淘汰弱候选，但针对 PRM 范式下的早期拒绝研究仍不充分。

**核心研究问题：**
- PRM 能否在步骤生成**中途**（仅生成 τ 个 token 后）提供可靠的质量信号，以实现对次优 beam 的提前淘汰？
- 基于部分生成的 partial reward 能否有效预测最终完整步骤的 final reward？

---

## 贡献/Contributions

**(C1) 假设提出**：提出"PRM 同时也是 Partial Reward Model"的假设——PRM 在步骤部分完成时计算的 partial score 与最终 final reward 之间存在强相关性，可作为可靠的早期质量信号。

**(C2) 理论保证**：证明在温和假设下，过早拒绝最优 beam 的概率随 partial generation 长度指数级衰减（sub-Gaussian tail bound）：
$$\Pr(P_{i^*} < T) \leq (N-1)\exp\!\left(-\frac{\Delta^2}{4\sigma^2}\right)$$
其中 Δ 为最优 beam 与次优 beam 期望 partial score 之间的最小间隔，σ 为噪声尺度。

**(C3) 实验验证**：在 AIME、MATH-500、SAT-MATH（AGIEval）三个数学推理基准上，使用中等规模 PRM（7B 参数）时推理 FLOPs 降低 **1.4×–9×**，使用轻量 PRM（1.5B 参数）时降低 **1.5×–4×**，无任何最终性能损失。

---

## 方法论/Methodology

### 核心思想

在 beam search 的每个推理步骤中，不等待完整步骤生成，而是先生成 **τ 个 token** 的前缀，立即调用 PRM 计算 **partial reward**，淘汰低分 beam，仅将幸存 beam 完成剩余生成，再进入下一步扩展。

### 算法：带早期拒绝的 Beam Search（Algorithm 1）

1. 初始化 N 条 beam
2. **for** 每条 beam：生成前 τ 个 token，用 PRM 计算 partial reward
3. 按 partial reward 选出前 N/M 条 beam，将其补全至完整步骤
4. 每条幸存 beam 扩展出 M 条新 beam
5. 重复直至满足停止条件，返回最优序列

### 效率提升机制

**FLOPs 降低**：通过在生成 τ 个 token 后拒绝低质量 beam，避免了对这些 beam 的后续完整生成与完整 PRM 评估。

**两级批处理（Two-tiered Batching）**：
- 生成前 τ 个 token 时，token 较短、内存占用少，可使用**更大 batch size**；
- 补全剩余步骤时，切换为**更小 batch size**，避免 OOM 错误，同时提高整体吞吐量。

### 最优 τ 的选取

在 i.i.d. token 得分假设下，partial reward 与 final reward 之间的 Pearson 相关系数为：
$$\rho(P_i, F_i) = \sqrt{\frac{\tau}{L}}$$
要求 ρ 达到目标水平 ρ* 时，需 τ ≥ (ρ*)² · L。实验中选取 τ ∈ {32, 64, 128}，在 τ = 32 时相关系数已超过 0.78，τ = 64 时两项相关指标均超过 0.9。

### 实验设置

- **基准**: MATH-500、SAT-MATH（AGIEval）、AIME 2024
- **LLM**: Llama-3.2-3B-Instruct、Qwen2.5-3B-Instruct
- **PRM**: MathShepherd-Mistral-7B、Skywork-PRM-1.5B
- **beam 数 N** ∈ {4, 8, 16, 32, 64}，**beam 宽 M** = 4
- 早期拒绝阈值 τ ∈ {32, 64, 128}

### 关键实验观察

1. **极短前缀已具高预测力**：τ = 32 时 Pearson 相关系数 > 0.78，τ = 64 时 > 0.9，可消除 60–85% 的下游 PRM 调用与生成 FLOPs。
2. **小 PRM 可媲美大 PRM**：Skywork-PRM-1.5B 在精度上可达到甚至超越 MathShepherd-7B，同时实现更大幅度的 FLOP 削减。
3. **对探索型 LLM 效果最佳**：Qwen2.5-3B 生成较长探索性推理链，早期拒绝可在小 beam width 时提升精度最多 3.5%；Llama-3.2-3B 生成较短确定性推理链，主要收益体现在计算节省上。
4. **τ = 64 优于 τ = 32**：τ = 64 时相关性超过 0.9 并趋于平稳，几乎没有低质量 beam 漏网，FLOPs 节省进一步增加。
5. **语言模型行为（非大小）决定计算开销**：Qwen 生成更长探索性推理链，总 FLOPs 显著高于 Llama，早期拒绝在阻断探索性失败时效果最显著。

### 局限性

- 依赖 PRM 分数的单调性与校准性；若 partial reward 与最终质量相关性弱（如代码合成含回溯、创意写作等非单调奖励场景），可能误拒最终最优 beam。
- 研究局限于纯文本数学基准，未涵盖多模态或稀疏正奖励场景。
- 未量化存储 τ 个 token 后中间 PRM 状态的内存开销。
- 理论保证假设步骤间噪声独立且 τ 固定，自适应 τ 调度及与 RLHF/DPO 等策略学习框架的集成仍为开放问题。
