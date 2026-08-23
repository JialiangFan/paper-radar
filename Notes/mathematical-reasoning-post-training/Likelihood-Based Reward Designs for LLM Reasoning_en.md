# Likelihood-Based Reward Designs for LLM Reasoning

**Authors**: Ariel Kwiatkowski, Natasha Butt, Ismail Labiad, Julia Kempe, Yann Ollivier
**Affiliations**: Meta FAIR, University of Amsterdam, New York University
**Date**: February 5, 2026
**arXiv**: 2602.03979

---

## Topic: Likelihood-based reward design

Using the log-probability of a reference answer as a reward signal for chain-of-thought (CoT) fine-tuning via reinforcement learning, replacing traditional binary correctness rewards and enabling a unified training criterion across both verifiable and non-verifiable domains.

---

## Background

Large language models (LLMs) have made striking progress on reasoning tasks through a post-training paradigm that combines chain-of-thought (CoT) prompting with reinforcement learning (RL). The standard approach treats the CoT as a sequence of actions and uses binary correctness of the final answer as the reward signal. For each prompt $p$, the fine-tuned model first generates a CoT $z$, then an answer $a$, and training optimizes the expected reward:

$$J_\theta = \mathbb{E}_{p \sim \mathcal{D},\, z \sim \pi_\theta(z|p),\, a \sim \pi_\theta(a|p,z)}[R(z, a)]$$

This paradigm works well in verifiable domains such as mathematics and programming, where ground-truth correctness is available. It does not naturally extend to non-verifiable domains such as long-form proofs or open-ended generation, where no external verifier exists. This motivates exploring reward signals that are universally available—specifically, the probability or log-probability of the reference answer given the generated CoT.

---

## Limitations & Research Problem

**Limitations of existing approaches**:

1. **Binary reward sparsity and domain restriction**: Binary 0/1 rewards require a per-benchmark verifier and produce sparse signals. They cannot be applied to non-verifiable domains such as long-form question-answering or theorem proving.

2. **Vanishing probabilities in probability-based rewards**: Methods like VeriFree (Zhou et al., 2025) use the raw probability $\pi_\theta(a^*|p, z)$ as the reward. For long free-form answers, the probability of an exact match approaches zero, causing the reward signal to vanish entirely in non-verifiable settings and producing no learning.

3. **Fragmented prior work**: Related methods—VeriFree (probability rewards), JEPO (Jensen-based ELBO with log-probs), RLPR (average per-token probability), NOVER (geometric mean of per-token perplexities)—each address parts of the problem but have not been systematically compared across both verifiable and non-verifiable domains. JEPO (Tang et al., 2025) included log-prob rewards only as an ablation and reported weaker performance.

4. **No unified criterion**: No prior work demonstrates a single reward design that works well across both short, verifiable answers and long, non-verifiable answers within the same experimental framework.

**Central research question**: Can log-probability of the reference answer serve as a universal reward signal for CoT RL fine-tuning, bridging verifiable and non-verifiable settings?

---

## Contributions

1. **Universality of log-probability rewards**: First comprehensive study establishing that log-probability rewards — $R(z, a) = \log \pi_\theta(a^*|p, z)$ — are the only variant that performs well in every tested scenario (short verifiable + long non-verifiable), while all other methods fail in one or more settings.

2. **Systematic cross-domain evaluation**: Experiments spanning two verifiable math benchmarks (MATH, DeepScaleR) and two non-verifiable long-form datasets (Alpaca, NuminaProof), across two model families (Llama-3.2-3B-Instruct, Qwen-2.5-3B-Instruct).

3. **Perplexity advantage**: In verifiable domains, log-probability rewards match or exceed binary RL in success rate while substantially improving perplexity—a metric aligned with pretraining. Base RL and probability-based rewards yield extremely poor perplexity. This reveals an important quality-of-calibration benefit of log-prob training.

4. **Non-verifiable domain viability**: In non-verifiable domains, log-probability rewards match SFT performance, while probability rewards (VeriFree) collapse completely due to vanishing reward signals.

5. **CoT length dynamics analysis**: Documents and analyzes a consistent pattern of CoT shortening during early training with log-prob rewards, attributing it to an initial negative correlation between CoT length and answer log-probability in the base model. Investigates mitigation strategies (KL penalties, length rewards) and their trade-offs.

---

## Methodology

### Reward Variants

| Method | Reward Formula | Description |
|--------|---------------|-------------|
| **Base RL** | $R = \mathbf{1}_{a=a^*}$ | Standard binary correctness reward (RLOO) |
| **Probability (VeriFree)** | $R = \pi_\theta(a^*\|p, z)$ | Direct probability of reference answer |
| **Avg Probability (RLPR)** | $R = \frac{1}{\|a^*\|}\sum_t \pi_\theta(a^*_t\|p, z, a^*_{1:t-1})$ | Average per-token probability |
| **Log-prob** | $R = \log \pi_\theta(a^*\|p, z)$ | Log-probability of reference answer (primary method) |
| **Avg Log-prob** | $R = \frac{1}{\|a^*\|}\log \pi_\theta(a^*\|p, z)$ | Per-token-averaged log-probability |
| **JEPO** | $R = \log \frac{1}{G}\sum_{i=1}^G \pi_\theta(a^*\|p, z_i)$ | Log-mean-exp reward over G sampled CoTs |
| **SFT (no CoT)** | — | Supervised fine-tuning baseline without CoT |

The log-prob reward can be computed in a single forward pass over $a^*$ without sampling an answer $a$, making it computationally efficient. It is conceptually aligned with the next-token log-likelihood loss used during pretraining.

### Gradient Decomposition

The gradient of the expected log-prob reward decomposes as:

$$\nabla J_\theta = \mathbb{E}_{z \sim \pi_\theta}\bigl[\log \pi_\theta(a^*|p, z)\,\nabla \log \pi_\theta(z|p) + \nabla \log \pi_\theta(a^*|p, z)\bigr]$$

The second term is equivalent to a direct SFT gradient on $a^*$; the first term is a standard Reinforce term weighted by the log-prob reward. These two terms jointly drive improvement.

### RL Algorithm

All methods except JEPO use **RLOO** (leave-one-out advantage estimation), an unbiased variant of GRPO. For a given prompt, the advantage for each sample is computed by subtracting the mean reward of the remaining samples in the minibatch. JEPO uses a group-level reward over $G=4$ samples.

### Experimental Setup

**Models**: Llama-3.2-3B-Instruct, Qwen-2.5-3B-Instruct

**Datasets**:
- Verifiable: MATH (~7,000 training samples, short answers), DeepScaleR Preview (~39,000 training samples, short answers)
- Non-verifiable: Alpaca cleaned (~50,000 long-form training samples), NuminaProof (~50,000 theorem-proof style training samples)

**Group sizes**: $G=32$ for verifiable domains (JEPO uses $G=4$ for efficiency); $G=4$ for non-verifiable domains

**Evaluation metrics**:
- Greedy success rate (deterministic decoding)
- T=1 sampled success rate
- Per-answer and per-token average log-probability (logprob-MC1 and logprob-MC32 estimates)
- Perplexity (geometric mean of per-answer perplexity)
- Average CoT length (in tokens, including formatting tokens)

**Training details**: AdamW optimizer, learning rate $10^{-5}$, cosine schedule with 20-step warm-up, global gradient norm clipping at 1.0, batch of 8 questions × G CoTs per step, DeepSeek-R1-style instruction format, assistant turn prefilled with `<think>`, CoT truncated at `<answer>` for likelihood-based rewards

**Verifier (Base RL only)**: Parses `<answer>answer</answer>` tags; reward 100 for correct answer, 10 for correct format but wrong answer, 0 for unparseable.

### Key Experimental Results

**Verifiable domains (MATH, DeepScaleR)**:
- All ground-truth-based RL methods achieve comparable greedy success rates
- With $G=32$, all log/probability variants slightly outperform Base RL on greedy success
- Sampling at $T=1$ degrades performance for log-prob and avg log-prob methods, closing the gap with probability and Base RL variants
- Log-prob rewards (Logprob, AvgLogprob, JEPO) achieve substantially better perplexity than Base RL and probability rewards, significantly surpassing SFT
- Base RL and probability rewards produce very poor perplexity: these models assign near-zero probability to wrong answers, while log-prob models maintain calibrated distributions

**Non-verifiable domains (NuminaProof, Alpaca)**:
- Log-probability rewards consistently match SFT on per-answer log-prob and perplexity
- Probability rewards (VeriFree, RLPR) fail completely—rewards vanish for long answers, producing no learning signal
- All log-prob methods exhibit a rapid CoT collapse to ~10 tokens, after which they effectively become SFT

**CoT length dynamics**:
- The base model exhibits a negative correlation between CoT length and answer log-probability: shorter CoTs tend to yield higher log-prob rewards
- This drives the model toward shorter CoTs at the start of RL training (the "dip")
- In verifiable domains, CoT length recovers after the dip as the model finds longer, more effective reasoning chains
- In non-verifiable domains, CoT length permanently collapses; the CoT never recovers
- Attempted mitigations: KL divergence regularization to the base model, and a length penalty reward $R_l(z) = r \cdot \min\{|z| - l_0, 0\}$ — both prevent the dip but hurt final task performance
- A "warm-start" SFT initialization (training the model to predict correct answers given synthesized CoTs) partially stabilizes CoT length but does not exceed SFT performance under comparable compute budgets

**Conclusion**: Log-probability rewards establish a simple, unified training criterion for CoT fine-tuning of LLMs that bridges verifiable short-answer and non-verifiable long-answer settings, without requiring domain-specific verifiers.
