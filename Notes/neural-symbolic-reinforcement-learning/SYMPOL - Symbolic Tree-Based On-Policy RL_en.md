# SYMPOL: Symbolic Tree-Based On-Policy RL

> Marton et al., ICLR 2025 (University of Mannheim, Technical University of Clausthal, University of Rostock)

## Topic
Decision Tree RL Policies

## Background
Reinforcement learning (RL) has achieved significant success across diverse domains, yet its reliance on neural network policies creates black-box models that are difficult to interpret, trust, and deploy in safety-critical applications such as autonomous driving and industrial robotics. Decision trees (DTs) offer a natural symbolic alternative due to their hierarchical branching structure and inherent interpretability. However, directly learning symbolic DT policies within on-policy RL frameworks remains challenging because standard DTs are non-differentiable and cannot be straightforwardly integrated into gradient-based optimization pipelines.

## Limitations & Research Questions
- **Limitation:** Existing tree-based RL methods fall into three categories, each with fundamental drawbacks: (1) Post-processing methods (e.g., VIPER) train a neural network policy first and then distill it into a DT, introducing severe information loss between the optimized and interpreted policy (Cohen's D > 2.5); (2) Custom optimization methods rely on evolutionary algorithms or integer programming, cannot integrate into standard RL frameworks, and scale poorly; (3) Soft Decision Tree (SDT) methods are differentiable but use multiple features simultaneously at each node for multidimensional splits, yielding trees that are difficult to interpret, with significant performance degradation upon discretization.
- **Problem:** How to directly optimize interpretable, axis-aligned decision tree policies end-to-end within standard on-policy RL frameworks (e.g., PPO), eliminating information loss from post-processing while maintaining performance competitive with full-complexity models.

## Contributions
- Integration of GradTree into actor-critic architectures via a separate architecture (tree-based actor + NN critic), enabling direct optimization of axis-aligned DT policies within standard on-policy RL and extending support to continuous action spaces.
- A dynamic rollout buffer that exponentially increases environment interaction steps to improve exploration stability, paired with a dynamic batch size that grows in sync via gradient accumulation for gradient stability.
- Selective weight decay applied to split index and leaf action parameters (but not split thresholds) to dynamically adjust parameter distributions and enhance exploration during training.
- Framework-agnostic design: SYMPOL requires no pre-trained NN policy, complex search procedures, or post-processing, and integrates seamlessly into PPO, A2C, and other standard on-policy RL algorithms.
- Empirical demonstration across multiple benchmark environments (CartPole, Acrobot, LunarLander, MountainCarContinuous, Pendulum, and MiniGrid suite) that SYMPOL eliminates information loss (Cohen's D = -0.019), achieves the best performance among interpretable methods, and learns compact DTs averaging only ~50.5 nodes.

## Methodology
- **Arithmetic DT policy formulation:** Building on GradTree, DTs are expressed as arithmetic functions: pi(s|a, tau, iota) = sum_l a_l * L(s|l, tau, iota), where a denotes leaf actions, tau split thresholds, and iota feature indices. A fully-grown complete tree of depth d is pruned post-hoc to remove redundant paths.
- **Dense architecture:** The feature index vector iota is expanded into a one-hot matrix I and split thresholds tau into a per-feature matrix T, enabling efficient gradient-based optimization via matrix operations while the underlying model remains equivalent to a hard, axis-aligned DT at all times.
- **Axis-aligned splitting with straight-through estimator:** The split function S(s|iota, tau) = floor(S(iota * s - iota * tau)) combines a logistic function with rounding. The forward pass executes non-differentiable hard splits; the backward pass employs a straight-through estimator to propagate gradients. SYMPOL is therefore neither a soft DT nor a differentiable DT.
- **Weight decay strategy:** Weight decay is applied to split index (I) and leaf action (a) parameters to narrow distributions and enhance exploration, but not to split thresholds (T) since their values are magnitude-independent.
- **Separate actor-critic architecture:** The actor is a tree-based policy and the critic is a full-complexity neural network capable of capturing complex value functions. Parameters are not shared, ensuring the policy's interpretability is unaffected by critic complexity.
- **Continuous action space extension:** Leaf nodes output the mean of a normal distribution, with an additional learnable parameter sigma_log representing the log standard deviation.
- **Dynamic rollout buffer:** Environment steps n_t = n_init * 2^(floor((t+1)*i / (1+t_total)) - 1), growing exponentially from n_init to n_final = 128 * n_init. Small early rollouts support rapid exploration; large later rollouts provide higher-quality samples.
- **Dynamic batch size:** Batch size grows in sync with the rollout buffer via gradient accumulation, preserving exploration diversity early in training while improving gradient stability later.
- **Evaluation:** Compared against SA-DT, D-SDT, MLP, and SDT across 5 control and 5 MiniGrid environments. All methods trained with PPO for 1M timesteps, evaluated over 5 random seeds x 5 episodes each, with hyperparameters optimized via optuna (60 trials). SYMPOL consistently achieves the highest performance among interpretable methods with Cohen's D near zero (no information loss), learning DTs averaging 50.5 nodes (vs. SA-DT d=5 at 60.3 and d=8 at 291.6 nodes). A case study demonstrates that SYMPOL's interpretable DT structure enables direct detection of goal misgeneralization.
