# Adaptive Length-based Reward Shaping for Efficient Reasoning

> **Full Title**: Learn to Reason Efficiently with Adaptive Length-based Reward Shaping
> **Authors**: Wei Liu, Ruochen Zhou, Yiyun Deng, Yuzhen Huang, Junteng Liu, Yuntian Deng, Yizhe Zhang, Junxian He
> **Affiliations**: HKUST, City University of Hong Kong, University of Waterloo, Apple
> **arXiv**: 2505.15612v1 (May 21, 2025)
> **Code**: https://github.com/hkust-nlp/Laser

## 主题 / Topic
Length-aware reward shaping

Using length-based reward shaping to improve the reasoning efficiency of Large Reasoning Models (LRMs) via RL training, achieving substantial reductions in token usage while maintaining or improving accuracy.

---

## 背景 / Background

Large Reasoning Models (LRMs) trained with reinforcement learning (RL) can generate extended chain-of-thought (CoT) trajectories to solve complex problems. However, these long outputs often carry substantial redundancy:

- Models generate thousands of tokens for elementary problems that could be solved in a few hundred ("over-thinking")
- Repeated, meaningless "self-reflection" loops appear even for trivial queries (e.g., repeatedly reconsidering "1+1=?")
- A fundamental efficacy-efficiency trade-off exists: prior methods that improve token efficiency typically sacrifice reasoning accuracy

Standard RL training objectives (e.g., GRPO used in DeepSeek-R1) optimize for correctness alone without constraining output length. The optimization objective is:

$$\pi_\theta^* = \arg\max_\theta \mathbb{E}_{x \sim \mathcal{D}} \left[ \mathbb{E}_{y \sim \pi(\cdot|x)}[R(x,y)] - \beta \mathbb{D}_{KL}[\pi_\theta(\cdot|x) \| \pi_{ref}(\cdot|x)] \right]$$

---

## 现有局限与研究问题 / Limitations & Research Problem

The paper unifies existing efficient reasoning methods under the reward shaping framework:

$$\hat{R}(x,y) = C(y) + \lambda(y) \cdot S(y)$$

where $C(y)$ is a correctness term and $S(y)$ is a length reward. Under this lens, three main families of prior methods each have distinct failure modes:

**1. Truncation-based methods** (e.g., Vanilla Truncation, ThinkPrune):
- Simply reduce the maximum context window during RL training (e.g., $L_T = 8192$)
- Effective on average but disproportionately hurts hard benchmarks: AIME accuracy drops by 4.1 points at 8,192 tokens and 9.7 points at 4,096 tokens, versus only 7% on MATH500
- Over 75% of AIME responses exceed 8,192 tokens, meaning hard problems genuinely need long reasoning
- High truncation ratio at the start of training (>45%) is sub-optimal

**2. Group-based reward methods** (e.g., Efficient Reasoning, Kimi-k1.5):
- Assign higher rewards to shorter responses within a rollout group
- Prone to reward hacking: models exploit $S(y)$ by generating overly brief responses, causing training accuracy to drop while total reward increases
- The length reward signal is noisy and comparison-dependent

**3. Budget-based reward methods** (e.g., L1-Exact, L1-Max):
- Penalize responses that deviate from a query-specific target length
- With large context windows (16,384 tokens), target lengths become sparsely distributed, causing reward fluctuations and training instability
- L1-Max performs well at 4,096 tokens but degrades significantly at 16,384 tokens

**Core research questions**:
- Can we simultaneously improve both accuracy and token efficiency?
- How should the target length adapt as the model's reasoning behavior evolves during training?
- Should length constraints be uniform across all questions regardless of difficulty?

---

## 贡献 / Contributions

1. **Unified framework**: A formal unified view of RL-based CoT compression that subsumes truncation, group-based, and budget-based reward methods under a single length-based reward shaping formulation.

2. **LASER (Length-bAsed StEp Reward)**: A novel reward shaping method using a step function guided by a target length $L_T$. Awards a bonus to correct responses that stay within $L_T$ tokens without penalizing long-but-correct explorations. Achieves a superior Pareto-optimal trade-off compared to all prior methods.

3. **LASER-D (Dynamic and Difficulty-aware)**: Addresses two key limitations of LASER:
   - Dynamic: target length should adapt as the model evolves during training
   - Difficulty-aware: easy questions should face stricter length budgets; hard questions should be allowed longer reasoning
   - Fully automated adaptive mechanism requiring no manual tuning

4. **LASER-DE**: A variant of LASER-D that reduces penalties for incorrect responses exceeding the target length, encouraging further exploration of incorrect trajectories to discover correct reasoning patterns.

5. **Comprehensive evaluation**: Validated across three model sizes (1.5B, 7B, 32B) on four in-domain benchmarks (MATH500, AIME2024, AMC2023, OlympiadBench) and three out-of-domain benchmarks (GPQA, LSAT, MMLU).

---

## 方法论 / Methodology

### Unified Reward Shaping Framework

All methods follow:

$$\hat{R}(x,y) = C(y) + \lambda(y) \cdot S(y)$$

The base correctness reward $R(x,y)$: +1 for correct, -0.5 for incorrect, -1 for invalid format. Training uses GRPO with KL regularization.

### LASER: Length-based Step Reward

$$S(y) = \alpha \cdot \mathbb{1}(L(y) \leq L_T)$$

Key design decisions:
- $\lambda(y) = \mathbb{I}(R)$: the length bonus only applies to **correct** responses (prevents rewarding brevity on wrong answers)
- The context window is set much larger than $L_T$ (e.g., 16,384 vs. 4,096 tokens), so truncation rarely occurs and long correct explorations remain possible
- $\alpha = 0.5$ balances correctness and length rewards
- Unlike truncation, LASER does not penalize over-length correct responses — it only provides a bonus for concise correct ones

Compared to truncation: the only difference is that instead of treating truncated responses as incorrect, LASER rewards responses that naturally stay within the target length.

### LASER-D: Dynamic Difficulty-Aware Extension

**Difficulty classification**: Queries are separated into three difficulty buckets (easy, medium, hard) based on the fraction of correct responses in the rollout group, using thresholds $k/3$ and $2k/3$ (where $k$ is rollout size). Each difficulty level gets its own adaptive target length hyperparameter $L_A^{easy}$, $L_A^{medium}$, $L_A^{hard}$.

**Automatic Adapting Mechanism (ECR-based)**:

Every $N$ training steps (e.g., $N=20$), a small monitoring dataset $\mathcal{D}^M$ (~500 samples) is evaluated. For each difficulty level $d$ and candidate target length $l$, the Expected Correct Responses (ECR) is computed:

$$ECR_d = P_{l,d} \cdot |C_d|$$

where $P_{l,d}$ is the coverage ratio (proportion of responses fitting within $l$ tokens) and $|C_d|$ is the minimum number of correct responses for that difficulty group (set to 6, 3, and 1 for easy, medium, and hard when $K=8$).

The adaptive target length $L_A$ is set to the **smallest** $l$ satisfying $ECR_d \geq 1$ for each difficulty level, enumerated from $L_T$ up to the maximum context window with interval $I$.

**Intuition**: The target length is the minimum generation length such that at least one complete correct response is expected. Shorter would make correct responses unlikely; longer would be redundant since correct responses are already achievable.

**Computational overhead**: Only ~3.5% additional computation due to periodic evaluation on a small monitoring dataset.

**Dynamic behavior observed**:
- Easy problems: target length quickly converges to short values
- Medium problems: gradually decreases from high initial values (~10,000+) to 3,000–4,000
- Hard problems: consistently maintains high target lengths near the context window limit

### LASER-DE: Exploration Variant

$$S(y) = \alpha \cdot \mathbb{1}(R) \cdot \mathbb{1}(L(y) \leq L_A) + \alpha \cdot (1 - \mathbb{1}(R)) \cdot \mathbb{1}(L(y) > L_A)$$

For incorrect responses exceeding the target length, a positive reward is given instead of a penalty. This encourages the model to explore further on incorrect trajectories, potentially discovering the correct reasoning pattern through extended deliberation. Motivated by the observation that incorrect responses tend to produce more tokens as the model searches for the answer.

### Experimental Setup

- **Base models**: DeepSeek-R1-Distill-Qwen-1.5B, 7B, 32B
- **Training data**: DeepScaleR-Preview-Dataset (40K competition-level math QA pairs)
- **Framework**: verl with DAPO clip-higher strategy ($\epsilon_{high} = 0.28$)
- **Rollout**: batch size 128, 8 rollouts per prompt, temperature 0.6, mini-batch size 64
- **Context window during training**: 32,768 tokens (max generation); during evaluation: 32,768 tokens, 4 samples for MATH500/OlympiadBench, 16 samples for AIME/AMC
- **Baselines**: Efficient Reasoning (group-based), L1-Max (budget-based), ThinkPrune (truncation-adaptive), plus vanilla truncation

### Main Results

**1.5B model (DeepSeek-R1-Distill-Qwen-1.5B)**:

| Method | AIME Acc. | Avg. Tokens |
|--------|-----------|-------------|
| Original | 28.9% | 15,956 |
| LASER ($L_T=8192$) | 31.5% | 6,589 |
| LASER-D ($L_T=1024$) | 31.0% | 5,158 |
| LASER-DE ($L_T=1024$) | 33.8% | 4,794 |
| LASER-DE ($L_T=2048$) | 31.5% | 5,263 |

- LASER-D achieves **+5.2 accuracy points on AIME** with **63% fewer tokens** compared to original
- LASER-DE achieves 35% accuracy on AIME2024 with ~5,500 tokens (best Pareto point)
- All LASER variants Pareto-dominate all baseline methods

**7B model**: LASER-D achieves 90.0% on AIME with avg. 5,379 tokens (original: 53.1% at 13,414 tokens).

**32B model**: LASER-DE maintains competitive accuracy (~79.83% avg. vs 80.95%) while reducing avg. tokens from 6,941 to 4,313.

**Out-of-domain**: Consistent improvements on GPQA, LSAT, and MMLU, confirming that length compression generalizes beyond the training distribution.

### Analysis of Reasoning Behavior Changes

**Shift in self-reflection keywords**: The average frequency of keywords ["recheck", "rethink", "try again", "wait", "alternatively", "retry", "however"] per token decreases substantially as response length is reduced. This indicates RL-based compression specifically reduces spurious self-reflection.

**Changes in cognitive behaviors** (analyzed using GPT-4.1-mini following the framework of Gandhi et al. 2025):
- **Backtracking** behavior frequency drops from >30% to ~10%, as many tracked keywords ("recheck", "retry", "rethink") are indicative of backtracking
- **Verification**, **Enumeration**, and **Subgoal Setting** proportions remain stable (with slight increase in Subgoal Setting)
- Conclusion: the model retains core reasoning behaviors while eliminating unnecessary backtracking — it becomes more efficient, not less capable

**Qualitative analysis**: LASER-D-trained models express the same concepts using structured formulas and more direct reasoning paths, versus the original model's verbose, repetitive single-idea explanations.
