# Generative Adversarial Reasoner

## 主题/Topic: Adversarial RL reasoning

**论文**: Generative Adversarial Reasoner: Enhancing LLM Reasoning with Adversarial Reinforcement Learning
**作者**: Qihao Liu, Luoxin Ye, Wufei Ma, Yu-Cheng Chou, Alan Yuille（Johns Hopkins University）
**发表**: ICLR 2026
**arXiv**: 2512.16917

---

## 背景/Background

大型语言模型（LLMs）在数学推理任务上表现出色，但即便经过大规模训练和先进范式的训练，仍会在推理过程中犯错，包括：
- 错误计算（incorrect calculations）
- 逻辑不严谨（flawed logic）
- 表面合理但实际无效的推理步骤（superficially plausible but invalid steps）

现有改进方向主要有两类：
1. **Process Reward Models（PRMs）**：通过细粒度的步骤级标注来识别和缓解过程错误。PRMs在复杂推理任务上效果显著，但依赖昂贵、易受主观误差影响的标注，且容易出现 over/under-reward 问题。
2. **基于 Prompt 的 LLM-as-critic 方法**：用 LLM 做逐步判断，成本较低，但判断可能嘈杂、不一致、辨别力不足。

此外，DeepSeek-R1 等 RL 后训练方法在数学推理上已是强基线，但仍依赖稀疏的 exact-match 奖励信号，credit assignment 困难，样本效率较低。

---

## 现有局限与研究问题/Limitations & Research Problem

**现有方法的核心局限**：
1. **PRMs** 标注成本高，易发生 reward mis-specification，对噪声敏感；
2. **固定 critic** 方法（包括 prompt-based 和固定判别器）无法随 reasoner 能力提升而自适应校准，导致奖励信号逐渐失准；
3. **稀疏 exact-match 奖励**在长推理链上 credit assignment 困难，样本效率低；
4. **整链评估**（holistic evaluation）在面对数千 token 的推理链时，对 LLM 判别器而言准确性差。

**核心研究问题**：能否在不依赖昂贵人工标注的情况下，通过让 reasoner 和 discriminator 联合训练并共同进化，产生密集、校准良好的在线（on-policy）步骤级奖励，从而提升 LLM 的推理质量？

---

## 贡献/Contributions

1. **提出 GAR（Generative Adversarial Reasoner）框架**：首个将对抗生成网络（GAN）思想引入 LLM 推理 RL 后训练的 on-policy 联合训练框架，让 LLM reasoner 和 LLM-based discriminator 共同进化。

2. **Compute-efficient slice-level 评估机制**：将推理链切分为语义完整的 slice（约 320 token），由 discriminator 对每个 slice 进行局部逻辑合理性判断并给出简洁结构化理由，既提高评估准确性，又控制计算开销。

3. **密集、校准的在线步骤级奖励**：Discriminator 产生的 slice-level 奖励作为对稀疏 exact-match 信号的补充，改善 credit assignment，提升样本效率。

4. **显著的实验性能提升**：在 AIME24 上将 DeepSeek-R1-Distill-Qwen-7B 从 54.0 提升至 61.3（+7.3），将 DeepSeek-R1-Distill-Llama-8B 从 43.7 提升至 53.7（+10.0）；在 LiveMathBench-Hard 上 Qwen 骨干提升 +35.3%，AIME25 上 Llama 骨干提升 +19.5%。

5. **泛化应用能力**：GAR 的模块化 discriminator 还可用于 teacher distillation（推理模式蒸馏）、preference alignment，以及无需完整 chain-of-thought 的部分推理链训练，自然扩展到难以自动验证的任务（如数学证明）。

---

## 方法论/Methodology

### 整体框架

GAR 由两个组件构成，通过强化学习联合训练：
- **Reasoner $\mathcal{M}_r$**：通用 LLM，生成中间推理过程和最终答案；
- **Discriminator $\mathcal{M}_d$**：较小的预训练 LLM 变体，对 $\mathcal{M}_r$ 的输出逐 slice 进行质量评估。

### Slice-level 评估机制

1. **切片方式**：按分隔符切分推理链，将相邻片段合并，直到出现明确的语义起点或达到预设 token 上限（L=320），形成语义完整的 slice；
2. **Discriminator 输出**：对每个 slice $i$ 给出二值 slice reward $r_i^s \in \{0, 1\}$，总体 slice reward 为所有 slice 的均值 $R^s = \frac{1}{n}\sum_{i=1}^n r_i^s$；
3. **生成格式**：Discriminator 依次输出简要分析 → 是/否判断 → 简洁理由，生成长度上限为 K=128 token（截断理由以加速训练，不损失性能）。

### 奖励设计

**Reasoner 奖励**（使用 GRPO 优化）：
$$R^{\text{rea}} = \lambda_1 R^m + \lambda_2 R^s$$
- $R^m \in \{0,1\}$：exact-match 奖励（最终答案是否正确）；
- $R^s \in [0,1]$：来自 discriminator 的 slice-level 连续奖励；
- $\lambda_1, \lambda_2 \geq 0$：权重超参数（实验中均设为 1）。

**Discriminator 奖励**（对抗 RL，GAN 目标）：
$$R^d = \mathbb{E}_{x \sim p_{\text{ref}}}[\log \mathcal{M}_d(x)] + \mathbb{E}_{x \sim p_{\text{gen}}}[\log(1 - \mathcal{M}_d(x))]$$

**Alignment 奖励** $R^a$：衡量 discriminator 的 slice-level 评分与整条推理链最终答案正确性之间的一致性，防止 discriminator 与 reasoner 的表现脱钩。

**Discriminator 总奖励**：
$$R^{\text{dis}} = \lambda_3 R^d + \lambda_4 R^a$$（实验中 $\lambda_3=1, \lambda_4=0.5$）

### 训练流程

**两阶段训练**：
1. **SFT 阶段**：用 GPT-o4-mini 标注的少量训练数据（analysis + judgment + rationale 格式）对 discriminator 做监督微调，适应新的评估格式；
2. **联合对抗 RL 阶段**：用 GRPO 联合优化 reasoner 和 discriminator。每批次中，reasoner 生成答案并切片，与等量参考 slice 混合，discriminator 区分两者并打分，该分数反馈回 reasoner 作为 slice reward。

**实现细节**：
- 基于 OpenR1 和 vLLM 实现；
- Qwen 方案：Reasoner 为 DS-R1-Distill-Qwen-7B，Discriminator 为 DS-R1-Distill-Qwen-1.5B；
- Llama 方案：Reasoner 和 Discriminator 均为 DS-R1-Distill-Llama-8B；
- 训练数据：OpenR1-Math-220k 数据集随机抽取 10%；
- 硬件：8 张 H100 GPU；Discriminator SFT 训练 500 步，联合 RL 训练 400 步。

### Selective-Entropy 效应

GAR 展现出一种 selective-entropy 机制：on-policy slicing 配合对抗 discriminator，在确定性 slice 上产生低熵（对错误答案的 wrong case 分布更紧），在决策关键 slice 上保持随机性探索，从而在不发生全局 entropy collapse 的前提下提升推理准确性。
