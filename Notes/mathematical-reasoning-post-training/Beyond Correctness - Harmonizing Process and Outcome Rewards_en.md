# Beyond Correctness - Harmonizing Process and Outcome Rewards

## 主题 / Topic
Process-outcome reward harmonization

This paper introduces **PROF (PRocess cOnsistency Filter)**, a data curation framework that harmonizes coarse-grained Outcome Reward Models (ORMs) with fine-grained Process Reward Models (PRMs) to improve reinforcement learning training quality for mathematical reasoning in LLMs.

- arXiv: 2509.03403
- Authors: Chenlu Ye, Zhou Yu, Ziji Zhang, Hao Chen, Narayanan Sadagopan, Jing Huang, Tong Zhang, Anurag Beniwal (Amazon / UIUC)
- Code: https://github.com/Chenluye99/PROF

---

## 背景 / Background

- Reinforcement Learning with Verifiable Rewards (RLVR) has emerged as the dominant training paradigm for mathematical reasoning, providing stable improvements in reasoning ability.
- **ORMs** reward only based on final answer correctness (+1/-1), producing sparse and coarse signals that cannot distinguish flawed reasoning reaching a correct answer from genuinely correct reasoning.
- **PRMs** score each intermediate step in the reasoning chain, providing fine-grained process supervision, but are prone to severe reward hacking — models can inflate average PRM scores by generating verbose, repetitive steps.
- Naively blending PRM and ORM rewards (Blend-PRM-GRPO) causes entropy collapse and uncontrolled response length growth, with test performance often falling below the plain GRPO baseline.
- The quality and interpretability of Chain-of-Thought (CoT) reasoning matter for practical model capability, not just final answer accuracy.

---

## 现有局限与研究问题 / Limitations & Research Problem

**Core question**: How to robustly harmonize accurate but coarse-grained ORMs with fine-grained but noisy PRMs in reinforcement learning?

**Limitations of existing approaches:**

1. **ORM granularity**: ORMs cannot identify samples with correct answers but flawed reasoning; including such samples introduces noisy gradients that destabilize training.
2. **PRM reward hacking**: Pre-trained PRMs suffer from distribution shift during online training and fail on boundary problems; models exploit PRMs by over-generating long, repetitive steps to maximize averaged process rewards.
3. **Simple blending is fragile**: Blend methods (Zha et al., Cui et al., Zou et al.) directly incorporate PRM into gradients, exposing training to reward hacking, entropy collapse, and performance degradation.
4. **Online PRM co-training is expensive**: Step-level evaluation via LLM-as-a-judge or Monte Carlo estimation is prohibitively costly at each training iteration.

---

## 贡献 / Contributions

1. **PROF framework**: A data curation method that uses PRM-ORM consistency to rank and filter training samples, rather than incorporating PRM directly into gradients.
   - Removes correct-answer samples with low process scores (flawed reasoning).
   - Removes incorrect-answer samples with high process scores (sound intermediate steps), while maintaining sample balance.
2. **Separate group filtering**: Correct group (G+) and incorrect group (G-) are ranked and filtered independently, maintaining the positive-negative sample balance to prevent biased removal.
3. **Experimental results**:
   - Across five benchmarks (Math500, Minerva Math, Olympiad Bench, AMC2023, AIME2024), PROF-GRPO improves over GRPO by more than 4% on average and substantially outperforms Blend-PRM-GRPO.
   - On Qwen2.5-Math-7B-base: PROF-GRPO achieves 51.7% average (vs. GRPO 49.9%, Blend 47.3%).
4. **Improved intermediate reasoning quality**: Monte Carlo step-value estimation, averaged PRM scores, and LLM-as-a-judge all confirm PROF-GRPO generates more detailed, verifiable, and easy-to-follow reasoning steps.
5. **Robustness against reward hacking**: Using PRM for filtering rather than for gradient computation effectively prevents reward hacking and entropy collapse.

---

## 方法论 / Methodology

### Setup

- **Policy model**: An LLM as policy distribution π(a|x), generating n rollouts per prompt x.
- **ORM**: Verifies final answer correctness, binary reward r_o ∈ {-1, +1}.
- **PRM**: Scores each step a^h in the CoT, producing step-level reward sequence {r^1, ..., r^H}.
- **Base RL algorithm**: GRPO (Group Relative Policy Optimization), which standardizes advantages within a group and updates the policy without a separate value network.

### PROF Core Algorithm (Algorithm 1)

**Input**: n rollouts, policy update size m, ORM rewards, step-number regularization parameters λ and H_λ.

**Steps:**

1. **Compute trajectory-wise consistency score r^pro**:
   - Call PRM to obtain step-level rewards for each rollout.
   - Compute the mean PRM score, apply a step-count penalty (if steps = 1 or steps ≥ H_λ), then multiply by the ORM reward:
     `r^pro_i = [mean(r^h) - λ·I(H_i=1 or H_i≥H_λ)] · r_o,i`
   - Step-count regularization discards responses with no reasoning (1 step) or excessively long/repetitive responses (≥ H_λ steps).

2. **Split into groups**: Divide n rollouts into correct group G+ (r_o=+1) and incorrect group G- (r_o=-1).

3. **Compute removal counts k+, k-**:
   - Balance positive-negative ratio so that the total kept size equals m, adjusting for the imbalance Δ = n+ - n-:
     `k+ = min(n-m, ⌈(Δ+n-m)/2⌉), k- = n-m-k+`

4. **Group-wise ranking and filtering**:
   - G+: rank by r^pro descending; keep samples with higher consistency (correct answers with sound reasoning).
   - G-: rank by r^pro ascending; keep samples with lower consistency (incorrect answers with poor reasoning), discarding incorrect responses that contain mostly valid intermediate steps.
   - Final kept set K+ ∪ K-, totaling m trajectories for policy update.

5. **Policy update**: Run GRPO on the retained trajectories.

### Key Design Choices

- **Why separate group filtering**: Without separation, PRMs tend to assign lower scores to incorrect responses (which typically contain more error-accumulating steps), causing disproportionate removal of negative samples and breaking the correct-incorrect balance. Experiments show that training without separation (w/o Separation) creates a >2% reward gap before and after filtering.
- **Mean vs. Min/Sum for consistency score**: Mean is less sensitive to a single poorly-scored step than Min, and unlike Sum it does not bias toward longer trajectories, providing the most stable consistency estimate.
- **Rollout size n trade-off**: n=8 is optimal for PROF-GRPO (Both). Larger n amplifies PRM influence and reintroduces reward hacking risk. Filter-Correct (filtering only the correct group) is more robust at higher n since PRM influence is constrained to correct samples only.

### Experimental Setup

- **Training data**: Numina-Math (~860k math problems, Chinese high school to international olympiad level).
- **Base models**: Qwen2.5-Math-1.5B-base, Qwen2.5-Math-7B-base, LLaMA-3.2-3B-instruct.
- **PRM**: Qwen2.5-Math-PRM-7B.
- **Evaluation**: 5 benchmarks, average@16 (temperature=1.0, 16 samples per prompt).
- **Implementation**: verl framework, AdamW optimizer, lr=1e-6, 8 H100 GPUs, mini-batch=256, max generation length 4096 tokens. KL loss coefficient = 0.001, entropy loss coefficient = 0.001.

### Main Results (Table 2)

| Model | Algorithm | Math500 | Minerva Math | Olympiad Bench | AIME24 | AMC23 | Avg |
|---|---|---|---|---|---|---|---|
| Qwen2.5-Math-1.5B-base | GRPO | 70.3 | 29.1 | 33.0 | 9.0 | 44.5 | 37.2 |
| | Blend | 67.6 | 27.8 | 31.1 | 7.7 | 42.5 | 35.3 |
| | **PROF-GRPO** | **73.2** | **30.0** | **36.1** | **9.6** | **49.1** | **39.6** |
| Qwen2.5-Math-7B-base | GRPO | 81.6 | 37.2 | 45.5 | 20.6 | 64.4 | 49.9 |
| | Blend | 81.7 | 36.7 | 45.0 | 15.2 | 58.0 | 47.3 |
| | **PROF-GRPO** | **83.1** | **39.0** | **47.8** | 17.5 | **70.9** | **51.7** |

### Ablation Study Findings

- **Filter-Correct vs. Filter-Both**: Both achieve comparably best performance; Filter-Both converges faster when the PRM is reliable. Filter-Correct is more robust when the PRM is less reliable or subject to distribution shift (cross-model scenario with LLaMA).
- **LLaMA-3.2-3B generalization** (Table 4): PROF-GRPO (Both) achieves 23.9% (GRPO: 23.6%); Filter-Correct achieves the best at 25.4%; Blend-PRM-GRPO scores worst at 15.7%.
- **Filtration method variants** (Table 3, Qwen2.5-Math-7B-base): Mean (51.7%) > Minimum (50.9%) ≈ Sum (50.6%) > Ratio (50.6%), confirming mean averaging is the best consistency estimator.
- **Intermediate step quality** (Figure 4): PROF-GRPO achieves higher MC step-value estimates on all five benchmarks (improvements of 9.2% on Math500, 37.4% on Minerva Math, 15.9% on Olympiad Bench), and LLM-as-a-judge strongly prefers PROF-GRPO responses (366 vs. 22 preference counts on Math500).
