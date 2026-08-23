# Dylan: Guiding Deep RL with Differentiable Symbolic Planning

## Topic
Differentiable Symbolic Planning

## Background
Reinforcement learning (RL) has achieved remarkable success in games, robotics, and LLM post-training, yet sparse reward environments remain a fundamental bottleneck causing inefficient exploration and slow convergence. Humans naturally decompose complex tasks into subtasks and adaptively adjust plans based on observations, but standard RL agents such as PPO lack such prior knowledge and require significantly more training interactions. Reward shaping is a common remedy, but existing approaches rely on hand-crafted potential functions, task-agnostic auxiliary signals, or preference-based learning, lacking interpretability and compositional generalization.

## Limitations and Research Questions
- **Limitation 1:** Existing reward shaping methods (potential-based, auxiliary tasks, preference-based) either depend on hand-crafted heuristics or produce opaque reward models that are difficult to interpret and generalize, failing to align semantically with human intent.
- **Limitation 2:** Classical symbolic planners (e.g., STRIPS) are non-adaptive, employing fixed search strategies (DFS/BFS) that are prone to infinite loops or inefficiency in environments with cyclic rules or high branching factors.
- **Limitation 3:** Standard RL agents tend to overfit to a single task and lack modular compositionality, requiring full retraining for every new task.
- **Problem:** Can we design a differentiable symbolic planning framework that simultaneously serves as an interpretable reward model providing semantically aligned intermediate feedback and as a high-level planner composing policy primitives for generalization to unseen tasks?

## Contributions
- Introduces Dylan (differentiable symbolic planner), the first framework integrating differentiable symbolic planning into RL as a reward model that provides interpretable, human-intent-aligned intermediate rewards through subgoal decomposition.
- Beyond reward shaping, Dylan also operates as a differentiable planner in a hierarchical RL setting, composing reusable policy primitives in a modular fashion to generate novel behaviors and generalize to previously unseen tasks without retraining.
- Through a learnable weight matrix W optimized via gradient descent, Dylan adaptively selects search strategies (DFS vs. BFS), overcoming the non-adaptive limitation of traditional symbolic planners.

## Methodology
- **Symbolic Representation:** An LLM (GPT-4o) extracts first-order logic rules from environment manuals, decomposing tasks into STRIPS-style symbolic transitions (precondition -> action -> postcondition), followed by human verification and refinement.
- **Differentiable Forward Chaining:** Planning rules are encoded as tensors $\mathbf{I}_i \in \mathbb{N}^{G \times S \times L}$. A learnable weight matrix $\mathbf{W} = [\mathbf{w}_1, \dots, \mathbf{w}_M]$ is introduced, with softmax-normalized probabilities for soft rule selection. At each reasoning step, soft logical AND (gather + product) and soft OR (softor) operations perform differentiable inference, progressively updating the valuation vector $\mathbf{v}^{(t)}$.
- **Dylan as Static Reward Model (Sec 3.1):** Given the environment's logical state and goal, Dylan reasons over candidate plans and selects the optimal action sequence $[a_1, a_2, \dots, a_n]$. A sequential reward function $r_{\text{reasoner}}$ grants reward only when the agent completes planned subgoals in order, penalized by step efficiency. The shaped reward combines the environment reward and the reasoner auxiliary reward.
- **Dylan as Adaptive Reward Model (Sec 3.2):** Extends the static model with a dense reward $r_{\text{adaptive}}$ computed via log-sum-exp aggregation over all candidate plan probabilities at each step. A scaling factor $\omega$ and offset $\lambda$ ensure the dense auxiliary reward remains strictly negative, preventing the agent from stagnating in zero-reward absorbing states.
- **Dylan as Differentiable Planner (Sec 3.3):** Operating independently of RL training, Dylan composes multiple policy primitives (e.g., get_key, go_through_door) to generate novel behaviors. The weight matrix W is optimized via BCE loss and gradient descent, enabling adaptive switching between DFS and BFS search strategies to avoid the infinite loop problem of traditional planners.
- **Experimental Evaluation (MiniGrid-DoorKey):**
  - Q1 (Static Reward Model): PPO+Dylan and A2C+Dylan achieve significantly faster convergence on 12x12 and 16x16 grids; the advantage is most pronounced in the 16x16 setting where baselines fail to converge.
  - Q2 (Adaptive Reward Model): On the 8x8 grid, adaptive rewards further accelerate convergence beyond the static reward model.
  - Q3 (Compositional Generalization): Dylan composes policy primitives to achieve 100% success rate on multiple unseen tasks (Key Retrieval, Red Door Reaching, Goal Reaching) and 98.2% on Safe Goal Reaching, substantially outperforming PPO and A2C baselines.
  - Q4 (Adaptive Search): Dylan learns to automatically select DFS or BFS strategies for different tasks, with converging loss curves validating its adaptivity.

## Limitations
- Relies on symbolic states provided directly by the environment; automatic extraction of symbolic representations from raw visual observations remains unexplored.
- Game rules are generated by GPT-4o and require human verification; an automated error-correction mechanism is left for future work.

## Metadata
- **Authors:** Zihan Ye, Oleg Arenz, Kristian Kersting (TU Darmstadt / hessian.AI / DFKI)
- **Source:** arXiv:2505.11661, 2025, Preprint (under review)
