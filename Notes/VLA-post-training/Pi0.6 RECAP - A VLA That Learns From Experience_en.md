# π*₀.₆: A VLA That Learns From Experience

- **Title:** π*₀.₆: a VLA That Learns From Experience
- **Authors:** Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, ... Sergey Levine, Chelsea Finn, Karol Hausman, et al.
- **Venue:** arXiv preprint (arXiv:2511.14759)
- **Year:** 2025
- **Affiliations:** Physical Intelligence


## Topic - Improving VLAs Through Real-World Experience and Offline RL

## Background
VLA models trained via large-scale imitation learning (pretraining + SFT) achieve flexible task execution, but reaching practically useful levels of robustness and speed in the real world requires learning from autonomous deployment experience — just as humans need repeated practice to master a skill. However, applying RL to large-scale flow matching VLAs presents three major challenges: (1) designing scalable offline RL methods compatible with flow-based models, (2) effectively integrating heterogeneous data sources (demonstrations, autonomous rollouts, human corrections), and (3) setting up RL training with sparse, ambiguous reward signals in the real world.

## Limitations & Research Problem
- Pure imitation learning VLAs never observe the consequences of their own actions, suffering from compounding errors and distribution shift
- Existing VLA RL methods (PPO/REINFORCE variants) rely on policy gradients requiring tractable log-likelihoods, which flow matching models do not provide
- Online RL (e.g., PPO) has extremely low sample efficiency for large models on real robots, making it impractical to scale
- Advantage-weighted regression (AWR) methods discard or heavily downweight suboptimal data, effectively degenerating into filtered imitation learning and failing to fully utilize all collected experience
- Real-world task rewards are inherently sparse (episode-level success/failure) and require human labeling

## Contributions
- Proposes **RECAP** (RL with Experience and Corrections via Advantage-conditioned Policies): a general-purpose offline RL framework enabling VLAs to continuously self-improve from real-world deployment experience
- Designs an **Advantage Conditioning** policy extraction method: trains a distributional value function to estimate per-step advantages, injects a binarized advantage indicator into VLA inputs (analogous to classifier-free guidance), bypassing the need for flow matching log-likelihoods
- Trains a **distributional value function** using a smaller VLM backbone (670M Gemma 3), discretizing returns into B=201 bins for classification, supporting multi-task and language-conditioned evaluation
- Integrates **heterogeneous data sources**: demonstration data, autonomous rollouts (with success/failure labels), and expert teleoperation corrections (interventions) — all unified for value function and policy training
- Validates on complex real-world tasks: folding diverse laundry (11 clothing types), making espresso (professional machine), assembling boxes (factory scenario) — more than 2x throughput improvement and ~2x failure rate reduction
- Achieves industrial-grade continuous operation: 13 hours of uninterrupted espresso making, 2+ hours of laundry folding without human intervention

## Methodology
- **Base model π₀.₆**: Evolved from π₀.₅, uses Gemma 3 (4B) as VLM backbone + 860M-parameter action expert (flow matching), trained end-to-end via Knowledge Insulation (KI); π*₀.₆ extends π₀.₆ by adding the ability to condition on an advantage indicator I_t
- **RECAP three-step iterative loop**:
  1. **Data collection**: Deploy VLA on real robots for autonomous rollouts, labeling each episode with success/failure; optionally, expert teleoperators provide online corrections (interventions) during autonomous execution, with corrective actions marked as advantage=positive
  2. **Value function training**: Train a distributional value function V^π_ref on all collected data (demonstrations + autonomous experience), discretizing normalized return-to-go into B=201 bins and training via cross-entropy loss; the value function uses the same architecture as the VLA but with a smaller VLM backbone (670M Gemma 3)
  3. **Advantage-conditioned policy training**: Compute advantage A^π_ref for each (o_t, a_t) from the value function, set a per-task threshold ε_ℓ (30th percentile), and binarize into improvement indicator I_t; inject "Advantage: positive" or "Advantage: negative" as text tokens into VLA input, training on all data with both conditioned and unconditioned objectives (analogous to CFG conditional/unconditional training)
- **Inference**: Set I_t = True (Advantage: positive); optionally use classifier-free guidance (β>1) to further amplify the probability of optimal actions
- **Reward design**: Minimalist episode-level sparse reward — success: r_T=0, failure: r_T=-C_fail, intermediate steps: r_t=-1; the value function learns to predict the remaining steps to success
- **Comparison with PPO/AWR**: PPO is unstable in the off-policy + flow matching setting (requires extremely small trust region η=0.01); AWR heavily downweights suboptimal data via importance weighting; RECAP trains on all data via advantage conditioning, leveraging both good and bad experience, significantly outperforming both alternatives
- **Training scale**: Pre-training uses tens of thousands of hours of multi-robot demonstration data; each RECAP iteration collects ~300-600 autonomous trajectories (on 4 robots), with 2 iterations yielding substantial improvement
