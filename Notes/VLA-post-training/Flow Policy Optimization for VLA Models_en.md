# Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models

- **Title:** Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models
- **Authors:** Mingyang Lyu, Yinqian Sun, Erliang Lin, Huangrui Li, Ruolin Chen, Feifei Zhao, Yi Zeng
- **Venue:** arXiv preprint (arXiv:2510.09976)
- **Year:** 2025
- **Affiliations:** Institute of Automation, Chinese Academy of Sciences; University of Chinese Academy of Sciences (UCAS); Long-term AI


## Topic - RL fine-tuning for flow-matching VLAs

## Background
Vision-Language-Action (VLA) models such as OpenVLA, Octo, and π₀ have demonstrated strong generalization by leveraging large-scale behavioral cloning on human demonstrations, yet their performance remains fundamentally constrained by the quality and coverage of offline data. Reinforcement learning offers a promising path to push beyond the imitation ceiling through online interaction. However, conventional policy gradient methods (e.g., PPO, TRPO) require explicit computation of policy ratios via action likelihoods, which are analytically intractable for flow-matching models due to the need to solve probability-flow ODEs and compute Jacobian traces.

## Limitations & Research Problem
- The log-likelihood of flow-matching policies is analytically intractable, precluding direct computation of the importance sampling ratio required by standard policy gradient methods
- Reward-weighted supervised learning approaches avoid likelihood computation but lack active exploration capability, struggling to discover novel, out-of-distribution behaviors
- Existing RL approaches for VLA policies (e.g., VLA-RL, ReinFlow, Flow-GRPO) either target autoregressive heads or introduce stochastic relaxations, and have not achieved stable online RL directly on flow-matching architectures
- Sparse rewards and contact-rich manipulation dynamics impose additional challenges for stable online learning

## Contributions
- Proposes Flow Policy Optimization (FPO), an actor-critic framework that bridges flow-matching policies with PPO-style updates by constructing a likelihood-free policy ratio proxy from per-sample changes in the conditional flow-matching (CFM) objective, bypassing explicit density estimation and Jacobian computation
- Introduces structure-aware credit assignment in the action latent space, using the model's CFM training loss as a per-sample improvement signal combined with a clipped surrogate objective for trust-region control
- Incorporates multi-step latent Euler exploration that generates smooth, temporally correlated perturbations aligned with the actor's generative field to encourage diverse exploration
- Employs a Q-ensemble critic mechanism using the minimum across multiple Q-functions for conservative value estimation, improving training stability under sparse rewards
- Achieves state-of-the-art results on the LIBERO benchmark (87.2% average success rate) and the ALOHA Transfer Cube task (>1.5x baseline), outperforming six strong baselines including OpenVLA, Octo, Diffusion Policy, GRAPE, and π₀-FAST

## Methodology
- **Likelihood-Free Ratio Proxy**: Computes the per-sample CFM loss differential ΔℓCFM,t between the rollout policy and the current policy on the same (state, latent) pair, applies batch standardization, and maps it through an exponential transform exp(βz_t) to produce a monotone ratio proxy ρ_t that substitutes for the intractable π_θ/π_θ_old
- **Clipped Surrogate Actor Update**: Combines the ratio proxy ρ_t with GAE advantages Â_t in a PPO-style objective using clip(ρ_t, 1-ε, 1+ε)·Â_t, with per-minibatch advantage standardization and gradient stopping through ρ_t to prevent policy collapse
- **Q-Ensemble Critic**: Maintains an ensemble of M action-value functions {Q_ϕᵢ}, computes temporal-difference targets using min_i Q(s_{t+1}, x'_{t+1}) to curb overestimation bias, updates target networks via Polyak averaging, and derives advantages through GAE from the conservative ensemble baseline V(s)
- **Multi-Step Latent Euler Exploration**: Starting from a sampled latent x_t⁽⁰⁾, performs K Euler integration steps along the CFM velocity field v_θ: x_t⁽ᵏ⁺¹⁾ = x_t⁽ᵏ⁾ + η·v_θ(x_t⁽ᵏ⁾, τ⁽ᵏ⁾ | s_t), producing smooth, temporally correlated perturbations aligned with the generative structure
- **Alternating Rollout-Update Training**: The rollout phase freezes actor parameters θ_old to collect trajectories and cache per-sample CFM losses into a sliding-window buffer; the update phase recomputes CFM losses under the current actor, constructs ratio proxies, and updates both actor and critic ensemble, with buffer size controlling distributional drift
