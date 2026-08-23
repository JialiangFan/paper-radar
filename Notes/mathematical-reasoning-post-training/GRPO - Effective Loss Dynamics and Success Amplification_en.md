# GRPO - Effective Loss, Dynamics, and Success Amplification

## Topic
GRPO Loss Dynamics Analysis

## Background
Group Relative Policy Optimization (GRPO), introduced in DeepSeekMath, estimates the advantage via Monte Carlo rollouts and applies mean+variance whitening to the reward, eliminating the need for a separately trained critic network as in PPO. GRPO has been widely adopted for training LLMs on mathematical reasoning and code generation using verifiable binary rewards, notably in DeepSeek-R1. This paper provides a theoretical analysis of GRPO's effective loss structure, policy iteration dynamics, and probability of success (PoS) convergence under binary verifiable rewards.

## Limitations and Research Questions
- **Limitation:** The optimization effect of GRPO's reward whitening under binary rewards lacks theoretical characterization. The impact of different KL regularization schemes (reference-only vs. mirror descent vs. two-KL) and normalization methods (mean+variance vs. mean-only) on PoS dynamics remains unclear.
- **Problem:** Is GRPO equivalent to a contrastive loss? How does PoS evolve across iterations, does it converge to a fixed point, and does that fixed point exceed the reference policy's success rate (i.e., does GRPO achieve success amplification)?

## Contributions
- Shows that GRPO with calibrated binary rewards is equivalent to an adaptive weighted contrastive loss, where weights depend on the old policy's PoS: low PoS amplifies credit for correct samples, while high PoS increases penalty for incorrect ones.
- Derives closed-form optimal policy recursions for multiple GRPO variants (no-clip GRPO, Mirror GRPO, Dr. GRPO, two-KL mixed), revealing that PoS logits evolve according to concise recurrence relations.
- Proves that the PoS sequence converges to a fixed point p* with p* > p_ref when 0 < p_ref < 1, establishing success amplification for GRPO. Mirror GRPO (alpha=0) further guarantees monotone PoS improvement and global convergence to 1.
- Empirically validates theoretical predictions on GSM8K with Qwen2.5-0.5B: average success rate increases from 21% to 37.5%, and PoS trajectories match fixed-point iteration predictions.

## Methodology
- **Reward calibration analysis:** Under binary reward r(q,o) in {0,1}, expands GRPO's advantage whitening into an explicit calibration function of the old policy's PoS p(q). Correct answers receive positive calibrated reward (rare successes get more credit), while incorrect answers receive negative calibrated reward (penalized more heavily when PoS is high).
- **Contrastive loss equivalence:** Substitutes the calibrated reward into the GRPO objective to show equivalence to a contrastive loss weighted by sqrt((1-p)/p) for the positive term and sqrt(p/(1-p)) for the negative term, encouraging higher likelihood ratios for correct samples and suppressing those for incorrect ones.
- **Closed-form optimal policy:** Maximizes the GRPO objective over the probability space using first-order optimality conditions, yielding the optimal policy pi_n(o|q) proportional to pi_ref(o|q) * exp(calibrated reward / beta).
- **PoS fixed-point iteration:** Derives the PoS recurrence p_n(q) = h(p_{n-1}(q)), where h is a composition of sigmoid, logit, and the weighting function. Applies Brouwer's fixed-point theorem to establish existence and analyzes local convergence and stability via derivative conditions and the Banach fixed-point theorem.
- **Variant comparison:** Systematically compares six GRPO variants in terms of PoS recurrence and fixed-point properties (Table 1), revealing that mean+variance normalization is equivalent to mean-only normalization with an adaptive effective beta.
- **Stabilized GRPO:** Introduces a smoothing factor epsilon to prevent numerical instability when p(q) = 0 or 1 causes zero variance.
- **Experimental validation:** Trains Qwen2.5-0.5B-Instruct as the reference policy on GSM8K using the TRL framework, tracking per-prompt PoS trajectories to verify fixed-point iteration behavior and success amplification.

> **Title:** Reinforcement Learning with Verifiable Rewards: GRPO's Effective Loss, Dynamics, and Success Amplification
> **Authors:** Youssef Mroueh
> **Venue:** arXiv:2503.06639
> **Year:** 2025
> **Affiliations:** IBM Research