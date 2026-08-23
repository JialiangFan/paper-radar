# Discovering Symbolic Policies with Deep RL

> Landajuela et al., ICML 2021 (Lawrence Livermore National Laboratory)

## Topic
Symbolic Policy Discovery

## Background
Deep reinforcement learning (DRL) has achieved remarkable success on continuous control tasks, yet its policies are represented by neural networks involving thousands of composed nonlinear operators, making them difficult to interpret, verify, and deploy. Traditional approaches in mathematical physics and control theory often yield compact symbolic controllers that are transparent and efficient. This paper proposes Deep Symbolic Policy (DSP), a framework that directly searches the space of symbolic mathematical expressions to serve as control policies within the RL loop.

## Limitations & Research Questions
- **Limitation:** Neural network-based DRL policies are black-box models that are hard to understand, trust, verify, and reproduce; they also impose significant hardware and latency requirements for deployment. Existing symbolic regression and model distillation methods suffer from an objective mismatch: training minimizes prediction error while evaluation maximizes environment reward, causing regression-based approaches to frequently fail catastrophically.
- **Problem:** How to use gradient-based methods to search the symbolic policy space directly within the RL loop, while scaling to multi-dimensional action spaces and improving exploration in combinatorial optimization.

## Contributions
- A gradient-based framework (DSP) that uses an autoregressive RNN as a Policy Generator to directly search the space of symbolic control policies, trained with a risk-seeking policy gradient that optimizes for best-case performance.
- A novel anchoring algorithm for multi-dimensional action spaces: leverages a pre-trained neural network policy as an anchor model, distilling it dimension-by-dimension into a fully symbolic policy, reducing combinatorial complexity from O(|L|^{nk}) to n sub-problems of O(|L|^k).
- Two novel exploration techniques for DRL-based combinatorial optimization: a hierarchical entropy regularizer (exponentially decaying entropy bonus across token positions to prevent early commitment) and a soft length prior (Gaussian prior on RNN emission logits to smooth the distribution over expression lengths).
- Empirical demonstration that discovered symbolic policies outperform seven state-of-the-art DRL algorithms (DDPG, TRPO, A2C, PPO, ACKTR, SAC, TD3) in terms of average rank and average normalized episodic reward across eight continuous control benchmarks, despite dramatically lower complexity.
- Formal stability analysis showing that discovered symbolic policies are provably stable in continuous-time systems for environments with known transition dynamics (CartPole, Pendulum, MountainCar).

## Methodology
- **Policy Generator:** A single-layer LSTM with 32 hidden units that autoregressively samples token sequences representing pre-order traversals of symbolic expression trees. The token library L includes arithmetic operators (+, -, x, /), functions (sin, cos, exp, log), pre-specified constants (0.1, 1.0, 5.0), and state variables s_i. In situ constraints (length bounds, prohibition of redundant structures) prune invalid expressions during sampling.
- **Policy Evaluator:** Instantiates sampled expressions as control policies a = f(s), runs N episodes in the environment, and computes the average episodic reward R(tau) as the training signal.
- **Risk-seeking policy gradient:** Optimizes the conditional expectation J_risk = E[R(tau) | R(tau) >= R_epsilon], computing gradients only over the top-(1-epsilon) quantile of samples to focus learning on the best-performing expressions.
- **Anchoring algorithm:** For n-dimensional action spaces, sub-policies f_i are learned sequentially; previously learned dimensions are fixed as symbolic, while remaining dimensions use the anchor neural network policy, until the policy is fully symbolic.
- **Hierarchical entropy regularizer:** H_gamma = eta * E[sum_i gamma^{i-1} H[p(tau_i | tau_{1:(i-1)})]], where exponentially decaying weights ensure sustained exploration of early tokens, addressing the early commitment problem.
- **Soft length prior:** A Gaussian prior psi_o is added to RNN emission logits, producing a smooth initial distribution over expression lengths and enabling the Policy Generator to learn the optimal length autonomously.
- **Constant optimization:** A post-hoc fine-tuning of real-valued constants in the best symbolic policy (denoted DSP^o) further improves performance.
- **Evaluation:** Eight OpenAI Gym / PyBullet environments, evaluated on average episodic reward over 1,000 held-out random seeds. DSP achieves the highest average rank (2.63), highest average normalized episodic reward (0.96), and best worst-case rank (6) compared to all seven DRL baselines and a regression baseline.
