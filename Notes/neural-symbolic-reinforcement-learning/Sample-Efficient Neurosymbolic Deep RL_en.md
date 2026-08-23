# Sample-Efficient Neurosymbolic Deep RL

## Topic
Symbolic Knowledge Transfer RL

## Background
Deep Reinforcement Learning (DRL) suffers from severe sample inefficiency when scaling to environments with long planning horizons, sparse rewards, and multiple sub-goals. Existing approaches such as reward shaping and reward machines either remain sample-inefficient or are sensitive to heuristic accuracy. This paper proposes SR-DQN, a neurosymbolic method that integrates background symbolic knowledge, formalized as Answer Set Programming (ASP) rules representing partial policies from simpler domain instances, into the epsilon-greedy DRL training loop to accelerate learning in more complex settings.

## Limitations and Research Questions
- **Limitation:** Standard DRL algorithms require prohibitively large training datasets and fail to generalize across increasing environment complexity. Existing neurosymbolic DRL methods (e.g., reward machines) depend on precise sub-goal definitions or complete symbolic task specifications, and reward augmentation degrades in long-horizon, sparse-reward scenarios.
- **Problem:** How can imperfect symbolic knowledge acquired from simple domain instances be leveraged to jointly improve both the exploration and exploitation phases of epsilon-greedy DRL, enhancing sample efficiency and generalization to complex environments without requiring hyperparameter re-tuning?

## Contributions
- Proposes SR-DQN, a framework that integrates partial logical policies (formalized in ASP) into both exploration and exploitation of epsilon-greedy DRL: biasing the action distribution during exploration toward symbolically entailed actions, and rescaling Q-values during exploitation according to symbolic recommendations.
- Introduces an epsilon-decay strategy combined with a confidence parameter (rho) to modulate the balance between neural and symbolic components over training, progressively transitioning from symbol-guided to network-guided decision-making.
- Demonstrates robustness to imperfect symbolic knowledge, requiring neither complete task specifications nor exact sub-plan definitions, with negligible computational overhead (approximately 1.3%--5% time increment).
- Empirically validates on OfficeWorld and DoorKey gridworld benchmarks across multiple complexity settings (8x8 to 16x16 maps, 1--4 keys, fully and partially observable), consistently outperforming standard DQN and reward machine baselines (RM-DQN).

## Methodology
- **Logical Representation:** The MDP state and action spaces are mapped to ASP terms via a feature map (F_F) and an action map (F_A). A partial logical policy (pi_ASP) is defined as a set of normal ASP rules encoding policy knowledge from simpler domain instances.
- **SR-Exploration (Algorithm 2):** During exploration, ASP reasoning over the current state yields a set of symbolically recommended actions (A_pi_ASP). Actions are sampled from a weighted probability distribution controlled by the confidence parameter rho, favoring symbolic suggestions over uniform random selection.
- **SR-Exploitation (Algorithm 3):** During exploitation, Q-values from the Q-network are rescaled by a factor k_a = 1 + epsilon * w_a for each action, where w_a is determined by membership in the symbolically recommended action set and the confidence parameter rho. The action with the highest rescaled Q-value is selected.
- **Epsilon-Decay Schedule:** Parameters epsilon_f (final epsilon) and epsilon_r (decay rate) govern the diminishing influence of the symbolic component over training, enabling a smooth transition from symbol-dominated to network-dominated action selection.
- **Ablation Study:** Independent evaluation of SR-Exploration and SR-Exploitation reveals that SR-Exploitation contributes more substantially to overall performance (approaching full SR-DQN), while SR-Exploration provides faster initial return growth. Analysis of rho demonstrates that both excessively low and high confidence values yield suboptimal performance, confirming the necessity of balanced neural-symbolic integration.
