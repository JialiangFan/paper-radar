# VLA-RFT: Vision-Language-Action Reinforcement Fine-Tuning with Verified Rewards in World Simulators

- **Title:** VLA-RFT: Vision-Language-Action Reinforcement Fine-Tuning with Verified Rewards in World Simulators
- **Authors:** Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, Weihua Su
- **Venue:** arXiv preprint (arXiv:2510.00406)
- **Year:** 2025
- **Affiliations:** Westlake University, Zhejiang University, OpenHelix Team, Fudan University, Zhengzhou University, BUPT, Hebei University of Technology


## Topic - World-Model-Driven VLA Reinforcement Fine-Tuning

## Background
Vision-Language-Action (VLA) models have achieved strong embodied decision-making capabilities through large-scale imitation learning, but pure imitation learning is prone to compounding errors under distribution shift, leading to poor robustness. Reinforcement learning (RL) can mitigate these issues, yet conventional RL approaches face critical challenges: simulation-based RL suffers from a pronounced sim-to-real gap, real-world RL is prohibitively costly and unsafe, and offline RL cannot learn from the consequences of the agent's own actions. How to efficiently and safely incorporate RL into VLA post-training remains an open problem.

## Limitations & Research Problem
- Pure imitation learning in VLAs leads to error accumulation under distribution shift, with rapid policy degradation once deviating from expert demonstrations
- Simulation-based RL requires millions of interactions and suffers from significant sim-to-real gaps
- Real-world RL training is prohibitively expensive and raises safety concerns, making it difficult to scale
- Offline RL cannot interact with the environment and remains vulnerable to distribution shift
- Existing reward designs lack dense, action-aligned learning signals, resulting in low sample efficiency

## Contributions
- Proposes VLA-RFT: a reinforcement fine-tuning framework that leverages a data-driven world model as a controllable simulator, enabling efficient policy optimization without real-world interaction costs or risks
- Designs a verified reward mechanism: the world model generates visual trajectories compared against goal-achieving references using pixel-level (MAE) and perceptual-level (LPIPS) reward signals, providing dense, task-grounded feedback
- Introduces SDE-Policy parameterization: extends deterministic flow-matching into a stochastic differential equation process via a Sigma Net, enabling effective exploration during RL training
- Achieves superior performance with only 400 fine-tuning steps, surpassing a 150K-step supervised baseline (average SR on LIBERO standard suites: 86.6% to 91.1%), with orders-of-magnitude greater efficiency than simulator-based RL
- Demonstrates significant out-of-distribution robustness improvements under perturbation settings, maintaining stable task execution under environmental variations

## Methodology
- **Two-stage training pipeline**: Stage I pretrains the world model (a 138M-parameter autoregressive Transformer based on LLaMA architecture) and the VLA policy (VLA-Adapter with a flow-matching action head); Stage II performs reinforcement fine-tuning through world model interaction
- **World model design**: An interactive video prediction model that takes an initial image and action sequence as input and autoregressively generates future visual observations; images are encoded via a pretrained tokenizer and actions are discretized via an action tokenizer, trained with maximum likelihood
- **SDE-Policy parameterization**: A Sigma Net is added alongside the flow-matching action head, outputting a variance vector that generalizes the deterministic FM-ODE into an SDE process; action chunks are generated via K=10 discretized integration steps, with step-wise log-likelihoods computed for GRPO optimization
- **Verified reward computation**: Both policy-generated and ground-truth actions are fed into the same world model to produce visual trajectories; the reward is computed as the negative weighted sum of MAE and LPIPS between them (Reward Type 3), eliminating generation-quality bias from the world model
- **GRPO optimization**: Uses group-based advantage estimation with N rollouts averaged as a baseline; the final objective combines a clipped policy ratio, auxiliary flow-matching MSE loss, and entropy regularization to ensure training stability
- **Experimental evaluation**: Validated on the LIBERO benchmark across four standard suites (Spatial, Object, Goal, Long) and multiple perturbation settings (Object Position, Goal Position, RoboState, Combined)
