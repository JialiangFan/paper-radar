# VLA-JEPA: Enhancing Vision-Language-Action Model with Latent World Model

> Authors: Jingwen Sun, Wenyao Zhang, Zekun Qi, Shaojie Ren, Zezhi Liu, Hanxin Zhu, Guangzhong Sun, Xin Jin, Zhibo Chen (USTC, Zhongguancun Academy, SJTU, Tsinghua, EIT Ningbo, UCAS, Nankai), 2026, arXiv 2602.10098

## Topic

Leakage-free JEPA pretraining for VLA

## Background

Pretraining Vision-Language-Action (VLA) policies on internet-scale unlabeled video is an attractive alternative to scarce and narrowly distributed robot action data. This has motivated a line of latent-action pretraining methods (LAPA, UniVLA, villa-X, Genie-style pipelines) that first learn latent actions and transition structure from video, then adapt them to downstream control. The authors argue that today's latent-action objectives remain implicitly anchored to pixel variation and therefore fail to learn what control actually needs: action-relevant state transition semantics.

## Limitations & Research Problem

- **Limitation:**
  - **Pixel-level objectives bias representations toward appearance, not action.** Predicting future pixels, or compressing frame-to-frame changes into a latent variable, lets supervision be dominated by texture, illumination, background clutter and viewpoint — high-variance but low-control factors, easy to predict yet only weakly tied to the controllable degrees of freedom a policy must master.
  - **Real-world videos amplify noisy motion.** In human and in-the-wild footage, camera motion and non-causal background change can exceed interaction-induced state change, turning the latent action into a delta-frame encoder of nuisance motion.
  - **Information leakage collapses "latent action" into a shortcut.** Pipelines that feed both current and future observations into the same module, or let future context influence the latent variable, allow the latent action to simply encode the future itself — useful for matching the training loss, semantically empty for control.
  - **Multi-stage pipelines are complex and fragile.** Representation pretraining → latent-action learning/alignment → policy learning introduces stage-wise inconsistency and engineering burden. Mitigations based on optical-flow or object-centric priors bias latent actions toward hand-crafted visual priors that break systematically in novel environments.
- **Problem:** How can a VLA learn genuinely action-relevant latent state transitions from action-free video without pixel reconstruction, without future-information leakage, and within a single-stage pretraining pipeline — such that the learned dynamics transfer effectively to downstream robotic control?

## Contributions

- An analysis of latent-action pretraining pitfalls, attributing four recurring failure modes (pixel-tethered objectives, nuisance motion in real video, information leakage, multi-stage fragility) to a single root cause: objectives implicitly anchored to pixel variation.
- VLA-JEPA, a JEPA-style pretraining framework built on **leakage-free state prediction**: a target encoder builds latent supervision targets from future frames, while the student pathway (the VLM backbone) sees only the current observation — future frames are never inputs, eliminating the shortcut by design.
- Prediction and alignment in latent rather than pixel space, yielding dynamics abstractions robust to camera motion and irrelevant background change.
- A simplified two-stage recipe (JEPA pretraining followed by action-head fine-tuning) that removes the auxiliary modules and multi-stage complexity of prior latent-action pipelines.
- Unified cross-domain training over human video and robot data: human videos are trained with the alignment loss alone, robot data with a joint alignment plus action-prediction objective.
- Consistent empirical gains: 97.2 average success on LIBERO (best overall, best on Object 99.6 and LIBERO-10 95.8), 79.5 average on LIBERO-Plus (best on 5 of 7 perturbation dimensions), competitive SimplerEnv results with <1% of villa-X's training data, and real-world Franka results exceeding π₀ and π₀.₅ in-distribution and under object-layout OOD.

## Methodology

- **Backbone.** Qwen3-VL (Qwen3 LLM + SigLIP-2 vision encoder). Two sets of learnable special tokens are introduced: `<latent_i>` for the latent action at time step i (each replicated K times to allow variable-length latent-action encoding) and `<action>` for action conditioning.
- **World state encoder.** A frozen self-supervised V-JEPA2 encoder produces per-view video state representations, concatenated across viewpoints into a unified world state, $s_{t_i} = \|_v F(I_{v,t_i})$, rather than a single-view representation.
- **Latent action extraction.** The VLM receives only the multi-view observations at the initial step $t_0$ and the language instruction $\ell$, and maps the special tokens to latent representations $z_{t_i} = p^{VLM}_\theta(\langle latent_i\rangle \mid \{I_{j,t_0}\}_{j=0}^{v}, \ell)$. Future frames never enter the VLM input.
- **Latent world model.** An autoregressive transformer world model predicts the next chunk of latent states, $\hat{s}_{t_{i:i+1}} = p^{WM}_\theta(s_{t_{0:i}}, z_{t_{0:i}})$, using time-causal attention: latent-action and world-state tokens attend bidirectionally within a time step, while attention across time steps is strictly causal and future steps are masked.
- **JEPA alignment objective.** $\mathcal{L}_{WM} = \sum_k \mathbb{E}_{s_{t_k}\sim F(\cdot)}(\hat{s}_{t_k} - s_{t_k})$, interpreted as maximizing an ELBO on predictive log-likelihood in semantic space; because the frozen target encoder $F(\cdot)$ (with stop-gradient) yields deterministic embeddings, the KL term vanishes and the ELBO reduces to latent-space reconstruction. WM and VLM are optimized jointly with teacher forcing.
- **Conditional flow-matching action head.** A global conditioning vector $z_a = p^{VLM}(\langle action\rangle \mid \{I_{i,t_0}\}, \ell, \langle latent_i\rangle)$ conditions a velocity field $v_\theta(a_t, t \mid z_a)$ trained against the flow induced by the interpolation $a_t = (1-t)\epsilon + t\,a_{0:H}$; trajectories are recovered by integrating from noise at inference. Overall objective $\mathcal{L} = \mathcal{L}_{FM} + \beta\mathcal{L}_{WM}$.
- **Data and setup.** Latent world-model pretraining on Something-Something-v2 (220K human videos) and Droid (76K action-labeled trajectories); downstream fine-tuning on LIBERO (~2K demonstrations), Fractal/BridgeV2 for SimplerEnv, and 100 real-world Franka demonstrations across three pick-and-place tasks; 8× NVIDIA A100.
- **Key ablations.** (i) Removing human-video pretraining drops LIBERO-Plus from 79.5 to 62.9, and success rates rise monotonically with the proportion of human video — human video mainly strengthens robustness of the existing skill repertoire (e.g. re-opening the gripper to retry a failed grasp) rather than adding new execution capabilities. (ii) Future video horizon $T \in \{4, 8, 16\}$: $T=8$ is best on average; too small under-encodes dynamics, too large adds redundancy. (iii) Attention visualization shows VLA-JEPA's latent-action tokens focus on the arm, the hand and the manipulated objects, whereas LAPA's attention is diffuse (a symptom of pretraining leakage degrading latent actions into compressed target-image representations) and UniVLA over-weights semantics, attending to operation-irrelevant background.

## Relevance to STL×VLA

VLA-JEPA supplies a concrete source of anticipatory signal: the latent world model explicitly rolls out future latent world-state chunks $\hat{s}_{t_{i:i+1}}$ over a horizon of roughly 4–16 frames, exactly the lookahead that predictive runtime monitoring requires. The paper itself never uses it that way — the world model serves purely as a pretraining and joint fine-tuning alignment objective and is not queried as a monitor at inference. No temporal specification, safety constraint, or quantitative safety metric appears anywhere; LIBERO, LIBERO-Plus and SimplerEnv all report success rate only, and robustness is characterized indirectly through seven perturbation dimensions, i.e. distributional robustness rather than specification compliance.

The one safety-adjacent observation is qualitative, from the real-robot deployment: π₀.₅ follows instructions more accurately in contacting the target object but "its position control frequently violates the safety boundaries of the robot arm, leading to execution failures", whereas VLA-JEPA more often grasps objects misaligned with the command yet "rarely breaches the robot arm's safety constraints". This is precisely a task-correctness versus constraint-satisfaction trade-off, reported anecdotally with no predicate definition and no violation statistics — a gap an STL formulation could formalize and quantify.

Two openings follow. First, V-JEPA2 latent states are not interpretable, so grounding STL atomic predicates (distances, contact, workspace bounds, force/velocity thresholds) in this latent space would require an added predicate probe or grounding head, or a partially interpretable state channel alongside the JEPA embedding. Second, the repeated-grasping behavior acquired from human video is an implicit recovery mechanism that maps naturally onto STL patterns of bounded-time recovery after violation, yet the paper only demonstrates it as an appendix case study with no verifiable temporal guarantee.
