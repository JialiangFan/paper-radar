# Reward Modeling for RL-Based LLM Reasoning

## Topic: RL reward modeling survey

**Full Title**: Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation
**Authors**: Pei-Chi Pan (University of Houston), Yingbin Liang (The Ohio State University), Sen Lin (University of Houston)
**arXiv**: 2602.09305v1 [cs.LG] 10 Feb 2026

---

## Background

Large Language Models (LLMs) demonstrate transformative potential for scientific discovery and complex reasoning, yet their reasoning remains inconsistent and unreliable in practice. Reinforcement learning (RL)-based fine-tuning has emerged as the key mechanism for improving LLM reasoning, with reward design serving as its central governing force.

Key contextual observations:
- Current LLM reasoning behavior resembles sophisticated heuristic aggregation rather than robust logical deduction; chain-of-thought (CoT) outputs are riddled with inconsistencies and factual errors.
- The RL fine-tuning landscape has evolved beyond Reinforcement Learning from Human Feedback (RLHF) to encompass paradigms better suited for rigorous reasoning: Reinforcement Learning from AI Feedback (RLAIF), Reinforcement Learning with Verifiable Rewards (RLVR), and preference optimization methods such as DPO.
- The fine-tuning problem is naturally formalized as a Markov Decision Process (MDP), denoted $\mathcal{M} = (\mathcal{S}, \mathcal{A}, P, r, \pi, H)$, where the LLM acts as agent with the objective of maximizing cumulative reward: $J(\pi_\theta) = \mathbb{E}_{\pi_\theta}\left[\sum_{t=1}^H r(s_t, a_t)\right]$.
- Evaluating reward design efficacy is inherently difficult: performance gains are confounded by RL algorithm choice, data curation, value estimation, and the black-box nature of LLMs, making results hard to attribute and reproduce.

---

## Limitations & Research Problem

**Gaps in prior surveys**:
- Zhong et al. (2025): broad taxonomy with data collection frameworks, but not focused on reward modeling.
- Liu et al. (2025d): reasoning-centric reward classification, but lacks comprehensive connection to broader reasoning challenges.
- Zheng et al. (2025b): focuses narrowly on outcome and process reward models across reasoning tasks.
- Wu (2025): covers general RL paradigms (RLHF, RLAIF, DPO, GRPO) but does not deeply map how reward modeling interacts with hallucination control, planning-based inference, dynamic evaluation, or efficiency-accuracy trade-offs at test-time scaling.

**Core research problems**:
1. How do reward functions fundamentally shape the internal computation and generalization behavior of LLMs across settings and domains?
2. How can reward signals serve as a unifying mechanism to address system-level challenges: inference-time scaling, LLM bias mitigation, augmented reasoning?
3. What vulnerabilities exist in current evaluation benchmarks (data contamination, reward misalignment), and what directions lead to more robust assessment?

---

## Contributions

1. **The RARL (Reasoning-Aligned Reinforcement Learning) unified framework**: integrates RLHF, RLAIF, RLVR, DPO, and LLM-as-a-judge under a single reasoning-centric lens, enabling paradigm complementarity, cross-domain methodological transfer, and systematic failure mode discovery.

2. **Systematic taxonomy of reward mechanisms**: organizes reward design in RARL along three principal paradigms—model-based reward, rule-based reward, and self-reward—with a detailed sub-taxonomy across architecture, granularity, and reward semantics dimensions.

3. **Comprehensive reward hacking analysis**: identifies and categorizes bias-induced reward hacking mechanisms (Credit Assignment Bias, Distribution-shift Bias, Length Bias, Position Bias, Faithfulness Bias / Chain-of-Thought Hacking) and reviews representative mitigation strategies.

4. **Bridging reward design with core LLM research topics**:
   - Inference-time scaling: rewards guide planning and computation allocation.
   - LLM bias mitigation: reward signals reduce hallucinations, sycophancy, and social biases in multi-step reasoning.
   - Augmented reasoning systems: external information sources and tools extend reasoning via reward-shaped supervision.
   - RL training challenges: diversity collapse and RL debate.

5. **Evaluation benchmark analysis**: identifies key vulnerabilities in existing benchmarks (data contamination in static benchmarks, reward misalignment), discusses multimodal reward evaluation, and outlines directions for more robust assessment.

---

## Methodology

### 1. RARL Framework and Three Reward Design Paradigms

The **RARL unified framework** formalizes RL fine-tuning as an MDP where rewards derive from either human- or AI-annotated ground truth, or from learned/heuristic objectives that approximate or correlate with such supervision. This subsumes RLHF, RLAIF, RLVR, and LLM-as-a-judge.

**Three reward paradigms**:

#### (a) Model-based Reward Design
Training a task-specific Reward Model (RM) to provide nuanced feedback. Organized along three dimensions:

**Architecture**:
- *Discriminative models*: linear head atop decoder-only architectures producing scalar scores. Training via Bradley-Terry (BT) loss for pairwise comparisons or BCE loss for pointwise classification. Limitations: (1) lack of interpretability, (2) temporal inconsistency across reasoning steps, (3) task shift degrading backbone generalizations, (4) underutilization of LLM generative capabilities. Improvements include ArmoRM (multi-objective MoE scalarization), SRM (Side Branch Models per evaluation dimension), PQM (Q-value ranking for step interdependency), CRM (conditional probability reward), TDRM (temporal difference bootstrapping).
- *Generative models*:
  - *Probability-based*: token probability (e.g., "yes"/"no") as reward signal, or log-likelihood comparisons of chosen vs. rejected responses. Works include Lightman et al. (2023), Xiong et al. (2024), Zhang et al. (2024c), Yuan et al. (2024a), Li et al. (2025f).
  - *Critique-based (LLM-as-a-judge)*: generates textual feedback rather than scalar scores. Con-J (Ye et al., 2025) produces preference predictions with explanations. ReasonGRM (Chen et al., 2025a) uses self-consistent, high-confidence paths for training data selection. Generative RMs exhibit stronger OOD generalization and support chain-of-thought and long-form analytic processes.

**Granularity**:
- *Outcome Reward Model (ORM)*: reward assigned only at the final answer; label-efficient but blind to intermediate reasoning errors. EORM (Jiang et al., 2025a) uses an energy function for outcome-level correctness.
- *Process Reward Model (PRM)*: fine-grained intermediate rewards at step-level or token-level. Step boundaries defined by fixed symbols ("Step 1"), adaptive confidence (Liu et al., 2025g), or semantic segmentation (StepWiser, Xiong et al., 2025b). Token-level PRMs (Yuan et al., 2024a; Lee et al., 2024; Chen et al., 2025b) provide continuous feedback throughout the trajectory. PRM training data: human-labeled (PRM800K, Lightman et al., 2023), AI-labeled (Gao et al., 2024a), or synthesized (MR-GSM8K, Zeng et al., 2023). ReasonFlux-PRM (Zou et al., 2025) integrates GPT-4 quality, coherence, and alignment scores.

**Reward semantics**:
- *Correctness-based*: direct step correctness labels (PRM800K, MR-GSM8K, P-FOLIO).
- *Value-based*: Monte Carlo rollout estimates the Q-value (probability of reaching the correct answer) as a surrogate label. Representative: Math-Shepherd (Wang et al., 2023b), OmegaPRM (Luo et al., 2024), AgentPRMs (Choudhury, 2025), PQM (Li & Li, 2024). Limitations include early-step bias and overly pessimistic value estimates; addressed by TVM (Lee et al., 2024), ReST-MCTS (Zhang et al., 2024a), SORM (Havrilla et al., 2024), OVM (Yu et al., 2023a), HPM (Wang et al., 2025c). DuaShepherd (Wu et al., 2025d) separates step correctness and value estimation into two reward heads.
- *Potential-based Reward Shaping*:
  - *DPO-Implicit Reward*: $\beta \log \frac{\pi^*(s_t, a_t)}{\pi_{\text{ref}}(s_t, a_t)}$, dense token-level reward embedded within DPO. RTO (Zhong et al., 2024) pre-trains a DPO model as standalone dense reward generator for PPO. Q-RM (Chen et al., 2025b) decouples reward from generation by training a dedicated discriminative model for token-level Q-values. DICE (Chen et al., 2024a) adds length regularization. Limitations: optimal policy $\pi^*$ is unknown during training, reference model uncertainty causes misattribution.
  - *Endogenous Reward*: grounded in Inverse RL; LLM logits represent the optimal Q-function for an IRL objective. Dense, shaped reward $= \log \pi_{\text{ref}}(a_t|s_t)$ derived via inverse soft Bellman operator—training-free (Li et al., 2025f). Dense-Path REINFORCE (Li et al., 2025b) extracts baseline-relative token-level rewards from SFT, establishing a formal equivalence between SFT and Inverse Q-Learning.

#### (b) Rule-based Reward Design
Relying on verifiable signals (accuracy and format alignment); rewards are typically sparse and binary.

- Formalized as **RLVR**: $v(x,y) = \alpha$ if correct, $0$ otherwise. Objective: $\max_{\pi_\theta} \mathbb{E}[v(x,y) - \beta D_{\text{KL}}(\pi_\theta(y|x) \| \pi_{\text{ref}}(y|x))]$.
- DeepSeek-R1 uses an accuracy component (correct answer in correct format) plus a format component (`<think>`/`</think>` tag constraint).
- Advantages: inexpensive, interpretable, less susceptible to reward hacking.
- Challenges: sparse rewards exacerbate credit assignment and gradient instability. GRPO suffers gradient vanishing and explosion (Wei et al., 2025); addressed by **reward dithering** (adding zero-mean Gaussian perturbation to smooth discrete rewards).
- Hybrid strategies: Qwen2.5-Math combines sparse outcome reward with RM-based scalar reward. PPR (Xu et al., 2025) grounds step-wise judgments in interpretable principles. CAPO (Xie et al., 2025) initializes tokens with sparse rewards, penalizing erroneous steps via LLM-as-PRM. TDPM (Zhang et al., 2025a) uses a discriminative PRM as the final reward.

#### (c) Self-Reward
The policy model leverages feedback from itself to iteratively improve, without external rules or models.

- *Self-Supervised Rewards*: self-consistency (majority voting), maximum-likelihood optimization ($\log \pi_{\text{base}}(y|x)$, Huang et al., 2024a), model confidence (Wang & Zhou, 2024). Yuan et al. (2024b) demonstrate a virtuous cycle where the model simultaneously improves as actor and judge via iterative DPO.
- *Learned Self-Rewards from Data*: Fei et al. (2025) use DPO-implicit reward to eliminate separate reward models. Guo et al. (2025d) extract token-level reward signals from the LLM's own hidden states via a linear transformation of concatenated, flattened hidden states from all layers, weighted by a learned gating mechanism, trained with binary cross-entropy.

### 2. Integration into RL Algorithms

| Algorithm | Mechanism | Key Features |
|-----------|-----------|--------------|
| **PPO** (Schulman et al., 2017) | Online RL with clipped surrogate objective | Advantage: $\hat{A}(x,y) = \sum_{t=1}^T \gamma^{t-1} r_t - V_\phi(x)$; KL penalty; computationally expensive |
| **DPO** (Rafailov et al., 2023) | Offline preference optimization | No explicit reward model; implicit reward $\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)}$; fixed preference dataset |
| **GRPO** (Shao et al., 2024) | PPO variant without value network | Group-wise normalized advantage: $\hat{A}_i = \frac{r_i - \text{mean}(r_1,\ldots,r_G)}{\text{std}(r_1,\ldots,r_G)}$; sparse reward; diversity collapse risk |
| **DAPO** (Yu et al., 2025b) | Decoupled asymmetric clipping | $\epsilon_{\text{low}}$ / $\epsilon_{\text{high}}$ decouple exploration and exploitation; mitigates entropy collapse |

Additional advantage estimation methods: Monte Carlo Returns / RLOO (Cui et al., 2025a; Cheng et al., 2025b); Token-Level Credit Assignment via ORM (Lyu et al., 2025); Implicit Value Function without separate value network (Kiruluta et al., 2025).

### 3. Reward Hacking: Taxonomy and Mitigations

Reward hacking occurs when agents exploit flaws in the reward function rather than learning intended behavior, ultimately reducing alignment. Categorized as **bias-induced reward hacking**:

| Bias Type | Mechanism | Representative Mitigations |
|-----------|-----------|---------------------------|
| **Credit Assignment Bias** | Standard RL summation-form credit lets high-reward steps compensate for incorrect ones | PURE: min-form credit assignment (weakest link); VinePPO: Monte Carlo unbiased value estimation |
| **Distribution-shift Bias** (Extrapolation Error) | RM trained on limited data assigns high rewards to OOD policy outputs | Online RM updates (Cui et al., 2025a; Lyu et al., 2025); KL regularization: $r(x,y) = r_\phi(x,y) - \beta \log \frac{\pi_\theta(y|x)}{\pi_{\text{ref}}(y|x)}$; Reward Ensemble (LoRA-based, Zhang et al., 2024d; Zhai et al., 2023); RetrievalPRM (Zhu et al., 2025a) |
| **Length Bias** | RMs and LLM-as-a-judge favor longer responses regardless of quality, driving overthinking | Local average reward correction (Huang et al., 2024c); step-level length penalty (Zheng et al., 2025a); DICE length regularization; balanced efficiency-accuracy reward design |
| **Position Bias** | LLM-as-a-judge favors candidates at certain positions | Position-aware judge calibration |
| **Faithfulness Bias (CoT Hacking)** | Reasoning chain semantically inconsistent with final answer; correct answers via incorrect logic | Chain-of-thought faithfulness supervision |
