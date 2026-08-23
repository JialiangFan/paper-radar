# End-to-End Neuro-Symbolic RL with Textual Explanations

**Paper:** Luo et al., ICML 2024 (PMLR 235)
**Framework:** INSIGHT

## Topic
Explainable Neuro-Symbolic Reinforcement Learning

## Background
Neuro-symbolic reinforcement learning (NS-RL) is a promising paradigm for explainable decision-making, as symbolic policies offer intrinsic interpretability. For tasks with visual observations, NS-RL requires extracting structured state representations from raw pixels, typically involving object identification and coordinate extraction. However, prior methods either rely on computationally expensive image reconstruction objectives (e.g., SPACE models) or use fixed state representations that cannot be refined with reward signals during policy learning, leading to significant performance degradation compared to neural baselines.

## Limitations and Research Questions
- **Limitation 1 (Efficiency and Performance):** Existing NS-RL approaches for visual tasks use image reconstruction objectives to extract structured states, which are computationally expensive and produce representations that remain frozen during policy learning. The inability to refine states end-to-end with reward signals causes substantial performance loss.
- **Limitation 2 (Accessibility):** While symbolic policies are inherently transparent, interpreting them requires expertise in first-order logic or domain-specific grammars. There is a notable lack of effort in the NS-RL literature to generate natural language explanations accessible to non-expert users.
- **Problem:** How to design an efficient NS-RL framework that jointly learns structured states and symbolic policies end-to-end while providing natural language explanations for non-expert users?

## Contributions
1. Propose the INSIGHT framework that distills vision foundation models (FastSAM + DeAoT) into a scalable perception module, enabling end-to-end joint learning of structured states and symbolic policies with reward signal refinement.
2. Develop a GPT-4-based textual explanation pipeline comprising concept grounding, policy interpretation, and decision explanation, which translates symbolic policies into natural language to reduce cognitive load.
3. Demonstrate efficacy on nine Atari games and a MetaDrive autonomous driving task, where INSIGHT outperforms all existing NS-RL methods and matches or exceeds pure neural baselines.

## Methodology

### Overall Architecture
INSIGHT consists of three modules: a Visual Perception Module, a Policy Learning Module, and a Policy Explanation Module.

### 3.1 Visual Perception Module
- **Frame-Symbol Dataset:** Approximately 10,000 frames are collected using a pre-trained neural agent. FastSAM segments objects and DeAoT tracks them across frames, producing bounding boxes. Object coordinates (centers), widths, and heights are normalized to [0, 1] and paired with images to form the frame-symbol dataset D_symbol.
- **Multi-task Perception Model:** A CNN encoder maps images to hidden representations. Three FCN heads predict object existence (distribution-balanced focal loss), coordinates (L1 loss), and size, with combined loss L_cnn = L_exist + L_coor + L_size.
- **End-to-End Refinement:** The perception module is pre-trained on D_symbol, then fine-tuned during policy learning via reward signals, allowing it to capture task-critical features overlooked during pre-training.

### 3.2 Policy Learning Module (EQL + Neural Guidance)
- **EQL (Equation Learner) Network:** Takes predicted object coordinates as input and produces symbolic expressions for action distributions. The network employs flexible activation functions (square, cube, constant, identity, product, addition) with L1/2 sparsity regularization to yield concise symbolic policies.
- **Neural Guidance Scheme:** Since object coordinates have limited expressiveness (non-distributed representations), a neural actor (pi_neural) operating on the encoder's hidden representations explores the environment. The EQL actor (pi_EQL) is trained to approximate pi_neural's action distribution by minimizing cross-entropy loss L_ng. Both actors are trained simultaneously, improving sample efficiency over sequential training.
- **Training Protocol:** The joint objective L = L_ppo + L_ng + lambda_reg * L_reg + lambda_cnn * L_cnn is optimized only in the final PPO iteration per batch; other iterations optimize L_ppo alone to prevent excessive perturbation to the perception module.

### 3.3 Policy Explanation Module (GPT-4 Pipeline)
- **Concept Grounding:** The LLM receives a task description (game goal, action effects) and a policy description (coordinate system, symbolic expression structure) to associate symbolic quantities with their semantic meanings.
- **Policy Interpretation:** A chain-of-thought approach analyzes the symbolic policy in three steps: input variables to intermediate variables, intermediate variables to action logits, and summary. Predefined rules constrain outputs to remain grounded in the policy's actual expressions.
- **Decision Explanation:** The LLM receives specific coordinate values, the chosen action, and gradients of action log-likelihoods with respect to each coordinate, enabling sensitivity-based reasoning about individual decisions.

## Experimental Results
- **Task Performance:** INSIGHT outperforms all NS-RL baselines (CGP, Diffses, DSP, NUDGE) across all nine Atari tasks and matches or surpasses the Neural baseline (Table 1). On MetaDrive, INSIGHT also outperforms neural baselines at 1M, 2M, and 5M timesteps (Table 2).
- **Inference Efficiency:** Inference time (2ms/step on Pong) is on par with pure neural methods and an order of magnitude faster than SPACE-Neural (50ms) and SA-Neural (40ms) (Table 3).
- **Ablation Studies:** End-to-end fine-tuning (vs. Fixed), pre-training (vs. w/o Pretrain), and neural guidance (vs. w/o NG) each contribute significantly to performance (Figure 3). The framework shows substantial robustness to hyperparameter variations (Figure 4).
- **Explainability:** GPT-4-generated policy interpretations correctly identify influential variables and triggering patterns for actions. Decision explanations leverage gradient-based sensitivity analysis to attribute specific decisions to input features (Figure 5).

## Limitations
- The EQL network cannot express logical operations required by certain reasoning tasks.
- Quantitative evaluation of the generated textual explanations remains an open problem.
