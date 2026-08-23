# Generative Adversarial Reasoner

## Topic: Adversarial RL reasoning

**Paper**: Generative Adversarial Reasoner: Enhancing LLM Reasoning with Adversarial Reinforcement Learning
**Authors**: Qihao Liu, Luoxin Ye, Wufei Ma, Yu-Cheng Chou, Alan Yuille (Johns Hopkins University)
**Venue**: ICLR 2026
**arXiv**: 2512.16917

---

## Background

Large language models (LLMs) have demonstrated remarkable mathematical reasoning abilities, often achieving expert-level performance on diverse benchmarks. However, despite extensive training with sophisticated paradigms, these models still commit process errors including incorrect calculations, flawed logic, superficially plausible but invalid arguments, and repetitive or incoherent reasoning steps.

Prior work has addressed these issues through two main directions:
1. **Process Reward Models (PRMs)**: Provide fine-grained step-level supervision to identify and mitigate errors throughout the reasoning process. PRMs achieve strong results on complex tasks but require expensive annotations that are prone to subjective error and susceptible to over- or under-reward issues.
2. **Prompt-based LLM critics**: Use LLMs as stepwise judges at lower annotation cost, but their judgments tend to be noisy, inconsistent, and less discriminative.

Standard RL post-training methods such as DeepSeek-R1 represent strong baselines but rely on sparse exact-match outcome rewards, making credit assignment difficult and sample efficiency low.

---

## Limitations & Research Problem

**Key limitations of existing approaches**:
1. **PRMs** incur high annotation costs and are prone to reward mis-specification and sensitivity to label noise;
2. **Fixed critic methods** (including prompt-based and fixed discriminators) cannot recalibrate as the reasoner grows stronger, causing reward signals to drift out of alignment with the model's actual capabilities;
3. **Sparse exact-match rewards** make credit assignment difficult over long reasoning chains, limiting sample efficiency;
4. **Holistic evaluation** of lengthy reasoning traces (spanning thousands of tokens) is unreliable for LLM-based discriminators.

**Core research question**: Can a reasoner and a discriminator be jointly trained in an adversarial on-policy scheme — without expensive human annotations — to produce dense, well-calibrated step-level rewards that continuously improve LLM reasoning quality?

---

## Contributions

1. **GAR (Generative Adversarial Reasoner) framework**: The first on-policy joint training framework inspired by GANs that co-evolves an LLM reasoner and an LLM-based discriminator for RL post-training of reasoning.

2. **Compute-efficient slice-level review schedule**: The reasoning chain is segmented into logically complete slices (approximately 320 tokens each); the discriminator evaluates each slice locally, producing concise structured justifications. This improves evaluation accuracy while controlling computational cost.

3. **Dense, calibrated on-policy step-level rewards**: Slice-level discriminator scores supplement sparse exact-match signals, improving credit assignment and sample efficiency throughout training.

4. **Substantial empirical gains**: On AIME24, GAR improves DeepSeek-R1-Distill-Qwen-7B from 54.0 to 61.3 (+7.3) and DeepSeek-R1-Distill-Llama-8B from 43.7 to 53.7 (+10.0); on LiveMathBench-Hard the Qwen backbone gains +35.3%, and on AIME25 the Llama backbone gains +19.5%.

5. **Flexible modular applications**: The modular discriminator enables teacher distillation (aligning reasoning style), preference alignment, and training on partial reasoning traces without requiring complete chains of thought or verifiable final answers — naturally extending to tasks such as mathematical proof-based reasoning.

---

## Methodology

### Overall Framework

GAR consists of two jointly trained components:
- **Reasoner $\mathcal{M}_r$**: A general-purpose LLM that generates step-by-step reasoning processes and final answers given user input;
- **Discriminator $\mathcal{M}_d$**: A smaller pre-trained variant of the reasoner that evaluates the outputs of $\mathcal{M}_r$ slice by slice, assigning quality scores and providing structured rationales.

Both models are jointly trained via reinforcement learning under an on-policy adversarial scheme.

### Slice-Level Review Schedule

Rather than evaluating entire reasoning chains holistically, GAR partitions each reasoning trajectory into shorter, logically complete slices:
1. **Segmentation**: The reasoning chain is split at delimiters; adjacent segments are merged until a new semantic beginning is identified or a token limit of L = 320 is reached;
2. **Discriminator output**: For each slice $i$, the discriminator assigns a binary slice reward $r_i^s \in \{0, 1\}$ indicating logical soundness. The aggregate slice reward is the mean: $R^s = \frac{1}{n}\sum_{i=1}^n r_i^s$;
3. **Efficient generation format**: The discriminator outputs a brief analysis, then a yes/no soundness verdict, then a concise rationale — all within a maximum of K = 128 tokens. Truncating the rationale at this limit preserves performance while substantially accelerating training.

This design offers two core advantages: (i) assessing short slices is more accurate than evaluating a full chain; (ii) it provides a denser and more informative training signal than sparse final-answer matching.

### Reward Functions

**Reasoner reward** (optimized with GRPO):
$$R^{\text{rea}} = \lambda_1 R^m + \lambda_2 R^s$$
- $R^m \in \{0,1\}$: exact-match reward comparing the final answer to the ground truth;
- $R^s \in [0,1]$: continuous slice-level reward from the discriminator;
- $\lambda_1, \lambda_2 \geq 0$ are weighting hyperparameters (set to 1 in experiments).

**Discriminator reward** (adversarial objective following the standard GAN formulation):
$$R^d = \mathbb{E}_{x \sim p_{\text{ref}}}[\log \mathcal{M}_d(x)] + \mathbb{E}_{x \sim p_{\text{gen}}}[\log(1 - \mathcal{M}_d(x))]$$
where $\mathcal{M}_d(x)$ is the estimated probability that slice $x$ is real (from the reference distribution), and $p_{\text{ref}}$, $p_{\text{gen}}$ are the distributions of reference and model-generated reasoning slices, respectively.

**Alignment reward** $R^a$: Measures the mean agreement between the discriminator's slice-level scores $r^s$ and the correctness of the final answer produced by the full reasoning sequence. This term encourages consistency between slice-level evaluation and answer-level correctness, keeping the discriminator calibrated to task outcomes.

**Total discriminator reward**:
$$R^{\text{dis}} = \lambda_3 R^d + \lambda_4 R^a \quad (\lambda_3 = 1,\ \lambda_4 = 0.5)$$

### Training Procedure

Training proceeds in two stages:

1. **SFT stage for the discriminator**: A small subset of training data is annotated by GPT-o4-mini with brief analysis, evaluative judgment, and concise rationale for each reasoning slice. The discriminator is fine-tuned on this data with early stopping to adapt to the analysis–score–rationale format while preserving its base capabilities.

2. **Joint adversarial RL stage**: The reasoner and discriminator are jointly optimized with GRPO. For each batch of questions, the reasoner generates answers and detailed reasoning steps; these are segmented into slices and mixed with an equal number of reference slices to form a balanced training set for the discriminator. The discriminator scores each slice; these scores serve as the slice reward $R^s$ for the reasoner and contribute to both $R^d$ and $R^a$ for the discriminator. Both models are updated with their respective objectives and iterated jointly.

At inference time, only the LLM reasoner is used — the discriminator is not needed.

### Implementation Details

- Built on OpenR1 and vLLM;
- **Qwen setup**: Reasoner = DS-R1-Distill-Qwen-7B; Discriminator = DS-R1-Distill-Qwen-1.5B;
- **Llama setup**: Both reasoner and discriminator = DS-R1-Distill-Llama-8B (no smaller Llama reasoning variant available);
- Training data: 10% random sample of the OpenR1-Math-220k dataset;
- Hardware: 8 H100 GPUs; discriminator SFT for 500 steps, joint RL for 400 steps;
- Reward weights: $\lambda_1 = \lambda_2 = \lambda_3 = 1$, $\lambda_4 = 0.5$.

### Ablation Findings

Progressive ablations confirm the contribution of each component:
- Adding any discriminator (fixed or trainable) over standard RL improves performance;
- Reframing discriminator evaluation from holistic solution grading to slice-level soundness with concise rationales provides further consistent gains;
- The alignment reward and discriminator reward are complementary — combining both yields the best results;
- Joint on-policy training of reasoner and discriminator outperforms using a fixed discriminator, as the co-trained discriminator adapts to detect subtler errors as the reasoner improves.

### Selective-Entropy Effect

GAR exhibits a selective-entropy mechanism: on-policy slicing with an adversarial discriminator encourages low entropy on deterministic slices (producing many zero-entropy tokens and tightening the wrong-case distribution) while sustaining exploration on decision-critical slices (maintaining higher non-zero entropy). This improves reasoning accuracy without global entropy collapse, contrasting with standard RL post-training.

### Additional Applications

- **Training without full chain-of-thought**: GAR can train solely on partial reasoning traces (e.g., only 3 slices) without a final-answer reward, outperforming standard RL in accuracy with significantly less training time. This extends applicability to open-ended tasks such as mathematical proofs.
- **Reasoning style distillation**: By training the discriminator to distinguish between two reasoning trajectory styles (e.g., Gemini vs. DeepSeek), GAR can align the reasoner's style toward a teacher, reducing human distinguishability of generated vs. teacher trajectories from 82.3% to 55.9% (near random-chance baseline of 50%).
