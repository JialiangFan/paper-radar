# Demystifying Long Chain-of-Thought Reasoning

## 主题/Topic: Long CoT reasoning analysis

**作者**: Edward Yeo, Yuxuan Tong, Morry Niu, Graham Neubig, Xiang Yue
**机构**: IN.AI, Tsinghua University, Carnegie Mellon University
**日期**: 2025年2月5日
**arXiv**: 2502.03373

---

## 背景/Background

大型语言模型（Large Language Models, LLMs）在数学、编程等复杂推理任务上取得了显著进展，其中 chain-of-thought (CoT) prompting 是提升推理能力的关键技术。CoT 通过引导模型生成中间推理步骤来改善最终答案质量。

然而，面对高难度任务（如数学竞赛、博士级科学 QA、软件工程），即便有 CoT，LLMs 仍然表现不足。OpenAI 的 o1 模型通过使用 long CoT（长链推理）实现了突破性进展——long CoT 的核心特征是能够识别并纠正错误、分解难题、迭代备选方案，从而形成更长、更结构化的推理过程。

强化学习（Reinforcement Learning, RL）已被证明是培养 long CoT 能力的关键方法，但长 CoT 在何种条件下涌现、RL 训练需要哪些关键设计选择，目前仍不清楚。

---

## 现有局限与研究问题/Limitations & Research Problem

1. **Long CoT 涌现条件不明**: 已有工作（如 DeepSeek-R1、Kimi k1.5、QwQ 等）尝试复现 o1 的 long CoT 能力，但对其底层机制缺乏系统性理解。
2. **SFT 与 RL 的角色不清**: Supervised Fine-Tuning (SFT) 对 long CoT 的影响、以及 SFT 初始化对后续 RL 的作用，尚未被深入研究。
3. **RL 训练不稳定**: 使用经典 reward 时，CoT 长度可能无节制增长，突破 context window 限制，导致训练精度崩溃。
4. **可验证信号稀缺**: 高质量、人工标注的可验证数据获取困难，限制了 RL 的规模化。
5. **涌现行为难以度量**: 错误纠正、分支回溯等 long CoT 核心能力的涌现难以被量化评估。

---

## 贡献/Contributions

本文系统性研究了 long CoT 推理的机制，提出了四项核心发现：

1. **SFT 并非严格必要，但能简化训练、提升效率**: Long CoT SFT 初始化使模型能达到更高性能上限，且更容易从 RL 中进一步获益；Short CoT SFT 则无此效果。

2. **推理能力随训练计算量涌现，但不保证稳定**: 提出 Cosine Reward（余弦长度奖励）配合重复惩罚（repetition penalty），有效稳定 CoT 长度增长，防止 reward hacking。

3. **可验证 reward 信号的规模化对 RL 至关重要**: 利用含噪声的网络抓取数据（如 WebInstruct）配合过滤机制，在分布外（OOD）任务（如 STEM 推理）上展现出强大潜力，混合 MATH 与 WebInstruct 数据可获得最佳平均性能。

4. **错误纠正等核心能力已潜在于 base model 中**: RL 通过激励可以有效诱导这些能力，但对复杂任务的诱导需要大量计算，且度量其涌现需要细致方法。

---

## 方法论/Methodology

### 问题形式化

- 给定 query $x$，模型输出序列 $y$，其中 $\text{CoT}(y) \subseteq y$ 为推理轨迹部分
- **Long CoT** 定义为：不仅 token 长度较大，且展现 **Branching and Backtracking**（系统性探索多路径并回溯）与 **Error Validation and Correction**（检测中间步骤错误并修正）两类核心行为

### 监督微调 (SFT)

- **数据来源**: 从 QwQ-32B-Preview 蒸馏 long CoT 轨迹（使用 rejection sampling，N=32~256 候选）；或通过 Action Prompting 框架构造（primitive actions: clarify, decompose, solution_step, reflection, answer）
- **关键发现**: 蒸馏自涌现 long CoT 模式的数据显著优于构造数据，在 OOD 基准（AIME 2024、MMLU-Pro-1k）上提升 15-50%

### 强化学习 (RL)

- **算法**: 默认使用 PPO（Proximal Policy Optimization），也探讨了 REINFORCE++（发现其比 PPO 更不稳定）
- **Reward 设计**:
  - *Classic Reward*: 对正确答案给固定奖励（+1），会导致 CoT 长度不稳定增长（reward hacking via repetition）
  - *Cosine Reward*: 分段余弦函数，以生成长度 $L_\text{gen}$ 为输入，正确答案给较高奖励且奖励随长度递减（鼓励效率），错误答案给惩罚且惩罚随长度递减（鼓励模型在不确定时继续思考）；同时附加超长惩罚 $r_e$
  - *N-gram 重复惩罚*: 对重复 token 施加稀疏惩罚（作用于整条轨迹），配合较低的 discount factor $\gamma$ 使其具有时间局部性
- **可验证信号规模化**:
  - 使用 WebInstruct-462k（网络抓取的 QA 对，deduplicated via MinHash）
  - Rule-based verifier + 过滤短答案的 prompt set 效果最佳
  - 混合 50% MATH + 50% WebIT 在多个基准上达到最优平均性能

### 训练设置

- **Base models**: Llama-3.1-8B（通用）和 Qwen2.5-Math-7B（数学专用）
- **SFT 数据**: MATH 训练集 7,500 条
- **RL 框架**: OpenRLHF
- **评估基准**: MATH-500（领域内）、AIME 2024（领域外数学）、TheoremQA（STEM）、MMLU-Pro-1k（通用）

### 从 Base Model 进行 RL 的探索

- 复现 DeepSeek-R1 的 long CoT 涌现实验：RL 从 Qwen2.5-Math-7B base model 出发，确实能提升精度，但未能有效提升 "recheck"、"alternatively" 等反思性关键词频率
- 分析发现 CoT 长度的增加部分源于 KL penalty（而非真正的探索能力增长），且 7B 参数量可能不足以支撑复杂 long CoT 能力的涌现
- Long CoT 模式的前身可能来自预训练数据中的人类对话（如互联网讨论论坛中含有 backtracking 和 error correction 的多轮对话）

### 关键 Takeaways 总结

| # | 结论 |
|---|------|
| 3.1 | Long CoT SFT 的性能上限高于 Short CoT SFT |
| 3.2 | Long CoT SFT 初始化使 RL 提升更容易 |
| 3.3 | SFT 数据质量至关重要：涌现模式 >> 构造模式 |
| 4.1 | CoT 长度在经典 reward 下不稳定 |
| 4.2 | Reward shaping（Cosine Reward）可稳定并控制 CoT 长度 |
| 4.5 | 足够计算量下会出现 length reward hacking，重复惩罚可缓解 |
| 5.1 | 加入噪声多样数据到 SFT 有助于跨任务平衡性能 |
| 5.2 | Rule-based verifier + 过滤 short-form answers 的 prompt set 效果最佳 |
