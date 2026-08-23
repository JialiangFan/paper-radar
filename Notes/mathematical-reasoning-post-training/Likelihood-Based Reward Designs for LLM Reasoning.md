# Likelihood-Based Reward Designs for LLM Reasoning

**作者**: Ariel Kwiatkowski, Natasha Butt, Ismail Labiad, Julia Kempe, Yann Ollivier
**机构**: Meta FAIR, University of Amsterdam, New York University
**日期**: 2026年2月5日
**arXiv**: 2602.03979

---

## 主题/Topic: Likelihood-based reward design

通过参考答案的 log-probability（对数概率）作为 reward 信号，在 chain-of-thought (CoT) fine-tuning 中替代传统的二值正确性 reward，实现对 verifiable 和 non-verifiable 领域的统一训练。

---

## 背景/Background

大语言模型（LLMs）在数学、代码生成等推理任务上的提升主要依赖于 chain-of-thought (CoT) prompting 配合 reinforcement learning (RL) 的 post-training 范式。标准做法是将 CoT 视为一系列动作，以最终答案的正确性作为 reward，即 0/1 binary reward。这种方式在有 verifier 的 verifiable 领域（如数学、编程）表现良好，但无法自然地推广到 long-form proof、open-ended generation 等 non-verifiable 领域。

研究训练框架：对于每个 prompt $p$，fine-tuned 模型先生成 CoT $z$，再生成答案 $a$，优化期望 reward $J_\theta = \mathbb{E}_{p, z, a}[R(z, a)]$，使用 RLOO/GRPO/PPO 等 RL 算法。

---

## 现有局限与研究问题/Limitations & Research Problem

**现有方法的局限**：

1. **Binary reward 的局限性**：0/1 reward 信号稀疏，且需要针对每个 benchmark 设计特定的 verifier，无法扩展到 non-verifiable 领域（如长篇文章、open-ended 问答）。

2. **Probability-based rewards 的问题**：VeriFree（Zhou et al., 2025）等使用参考答案的 probability $\pi_\theta(a^*|p, z)$ 作为 reward，在 non-verifiable 领域会因为长答案的 probability 趋近于零而失效（vanishing probabilities problem）。

3. **相关方法的局部性**：JEPO（Tang et al., 2025）引入了 log-prob 相关的 ELBO loss，但仅作为 ablation 对比，RLPR（Yu et al., 2025）、NOVER（Liu et al., 2025）等各有局限，尚无系统性的跨域对比研究。

**核心研究问题**：是否存在一种统一的 reward 设计，既适用于 verifiable 的短答案数学题，也适用于 non-verifiable 的长篇 proof？

---

## 贡献/Contributions

1. **Log-probability reward 的普适性验证**：首个系统性研究表明，以参考答案的 log-probability $R(z, a) = \log \pi_\theta(a^*|p, z)$ 作为 reward 是唯一在所有场景（short verifiable + long non-verifiable）下均表现良好的方法。

2. **跨域全面评测**：在 verifiable 数学基准（MATH、DeepScaleR）和 non-verifiable 长篇数据集（Alpaca、NuminaProof）上，跨 Llama-3.2-3B 和 Qwen-2.5-3B 两个模型族进行系统对比。

3. **Perplexity 优势的发现**：Log-probability rewards 在 verifiable 领域不仅保持与 binary reward 相当的 success rate，还显著改善了模型 perplexity（即模型对答案保持合理概率分布，避免过度自信），而 Base RL 和 probability-based rewards 在此指标上表现极差。

4. **Non-verifiable 领域的可行性**：在 non-verifiable 领域，log-probability rewards 与 SFT 性能持平，而 probability rewards（VeriFree）完全失效。

5. **CoT 长度行为的分析**：发现 log-probability rewards 训练初期会导致 CoT 显著缩短（dip），在 verifiable 领域后续恢复，但在 non-verifiable 领域 CoT 永久塌缩至极短长度（约 10 tokens），使模型退化为类 SFT 行为。

---

## 方法论/Methodology

### Reward 变体定义

| 方法 | Reward 公式 | 说明 |
|------|-------------|------|
| **Base RL** | $R = \mathbf{1}_{a=a^*}$ | 标准 binary correctness reward |
| **Probability (VeriFree)** | $R = \pi_\theta(a^*\|p, z)$ | 参考答案的直接 probability |
| **Avg Probability (RLPR)** | $R = \frac{1}{\|a^*\|}\sum_t \pi_\theta(a^*_t\|p, z, a^*_{1:t-1})$ | per-token probability 平均 |
| **Log-prob** | $R = \log \pi_\theta(a^*\|p, z)$ | 参考答案的 log-probability（核心方法） |
| **Avg Log-prob** | $R = \frac{1}{\|a^*\|}\log \pi_\theta(a^*\|p, z)$ | per-token log-probability 平均 |
| **JEPO** | $R = \log \frac{1}{G}\sum_{i=1}^G \pi_\theta(a^*\|p, z_i)$ | log-mean-exp of probabilities over G samples |
| **SFT** | — | 无 CoT 的监督微调基线 |

Log-prob reward 的关键优势：无需 verifier，只需对 $a^*$ 做一次 transformer forward pass 即可计算；与 pretraining 的 next-token log-likelihood 损失一致，概念上最接近 pretraining criterion。

### 梯度分析

Log-prob reward 的期望 reward 梯度为：
$$\nabla J_\theta = \mathbb{E}[\log \pi_\theta(a^*|p, z) \nabla \log \pi_\theta(z|p) + \nabla \log \pi_\theta(a^*|p, z)]$$

第二项等价于直接对 $a^*$ 做 SFT，第一项是以 log-prob 为 reward 的 Reinforce 项，两者协同作用。

### RL 算法

所有方法（除 JEPO 外）使用 **RLOO**（leave-one-out advantage estimation，GRPO 的无偏版本）。JEPO 使用 group-level reward with $G=4$。

### 实验设置

- **模型**：Llama-3.2-3B-Instruct、Qwen-2.5-3B-Instruct
- **Verifiable 数据集**：MATH（~7,000 训练样本）、DeepScaleR Preview（~39,000 训练样本），使用 $G=32$
- **Non-verifiable 数据集**：Alpaca cleaned（~50,000 长篇训练样本）、NuminaProof（~50,000 长篇证明训练样本），使用 $G=4$
- **评测指标**：Greedy success rate、T=1 sampled success rate、per-answer/per-token average log-prob、perplexity、average CoT length
- **训练细节**：AdamW optimizer，lr=$10^{-5}$，cosine schedule with 20-step warm-up，global gradient norm clipping at 1.0，DeepSeek-R1 风格的 instruction format，prefill assistant turn with `<think>`

### 核心实验结论

**Verifiable 领域**：
- 所有基于 ground-truth 的 RL 方法在 greedy success rate 上表现相近；$G=32$ 时 log-probability variants 略优于 Base RL
- Log-prob rewards 在 perplexity 上显著优于 Base RL 和 Probability rewards，与 SFT 持平甚至更好
- Probability rewards（VeriFree）在 success rate 上可行，但 perplexity 极差

**Non-verifiable 领域**：
- Log-probability rewards 与 SFT 性能持平
- Probability rewards（VeriFree）完全失效，因为长答案的 probability 趋近于零，无有效学习信号
- Log-prob 模型的 CoT 塌缩至极短（~10 tokens），有效退化为 SFT

**CoT 长度现象**：
- 初始模型存在 CoT 长度与 log-probability reward 的负相关（越短的 CoT 往往对应更高的答案 log-prob）
- 导致训练初期 CoT 长度急剧下降（dip）
- Verifiable 领域中 CoT 长度后续恢复；non-verifiable 领域中永久塌缩
- 尝试的缓解措施（KL divergence penalty、CoT length reward）防止了 dip 但损害了实际性能
