# Survey of Process Reward Models

## Topic
Process reward model (PRM) survey — a systematic overview of process reward models for reasoning alignment in large language models, covering the full loop from data generation to model training to deployment.

Full title: *A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for Large Language Models*
Authors: Congmin Zheng, Jiachen Zhu, Zhuoying Ou, et al. (Shanghai Jiao Tong University, UCL, CMU, University of Bristol)
arXiv: 2510.08049v2, October 21, 2025

---

## Background

- Large language models (LLMs) exhibit advanced reasoning ability, but conventional alignment is dominated by outcome reward models (ORMs) that judge only final answers, providing a single coarse signal.
- As reasoning chains grow longer and more complex, the static, outcome-centric view fails to capture stepwise progress, diagnose intermediate errors, or allocate computation adaptively.
- Process Reward Models (PRMs) address this gap by explicitly evaluating and guiding reasoning at the step or trajectory level.
- PRMs form a closed loop: **generate process data → train PRMs → use PRMs (test-time scaling or RL) → produce better data**, enabling finer credit assignment, richer diagnostics, and improved robustness.
- Unlike ORMs, PRMs assess partial solutions and trajectories, provide context for adaptive "reason-then-rate" verification, and integrate with inference-time controllers and reinforcement learning (RL) objectives — supervision becomes proactive rather than passive.

---

## Limitations & Research Problem

**Existing limitations:**
- Prior surveys focus on test-time scaling paradigms (Zhang et al., 2025f), broad reward modeling taxonomies (Zhong et al., 2025), or generic deep RL reward design (Yu et al., 2025) — none systematically covers the full PRM loop.
- Human-annotated data (e.g., PRM800K) is high-fidelity but expensive and limited in scale.
- Automated methods risk error propagation and verifier limitations.
- Discriminative PRMs depend on explicit step labels and struggle with cross-domain generalization and reward hacking.
- Implicit PRMs avoid step labels but have lower precision; generative PRMs carry higher compute overhead.
- Standardized evaluation benchmarks are immature; cross-domain generalization and robustness verification remain open problems.

**Core research questions:**
1. How to generate high-quality process supervision data (fidelity vs. scalability trade-off)?
2. How to build PRMs (choice of modeling paradigm)?
3. How to use PRMs (test-time scaling vs. RL for policy learning)?

---

## Contributions

1. **Systematic taxonomy**: Organizes the field around the full PRM loop — data generation (Sec. 2), PRM construction (Sec. 3), PRM usage (Sec. 4), downstream applications (Sec. 5), benchmarks (Sec. 6), and discussion (Sec. 7).
2. **Data generation taxonomy**: Three paradigms — Human Annotation, Automated Supervision, and Semi-automated Approaches — with analysis of fidelity–scalability trade-offs in each.
3. **PRM training paradigm taxonomy**: Four classes — Discriminative PRMs, Generative PRMs, Implicit PRMs, and Other Architectures.
4. **PRM usage taxonomy**: Two primary paradigms — Test-Time Scaling (re-ranking, verification-guided decoding/search) and PRM-guided RL (dense step-wise rewards, credit assignment).
5. **Application survey**: Math, code, multimodal reasoning, robotics, agents, and high-stakes domains (medicine, finance).
6. **Benchmark compilation**: PRMBench, ProcessBench, Socratic-PRMBench, ViLBench, VisualProcessBench, MPBench, WebRewardBench, GSM-DC, UniversalBench.
7. **Six-dimensional comparative discussion**: Evaluates rule-based rewards, ORMs, and PRMs across resource efficiency, granularity, anti-hacking robustness, generalization, interpretability, and functionality.

---

## Methodology

### Section 2: How to Generate Data

**2.1 Human Annotation**
- The earliest and most straightforward form: annotators explicitly verify the correctness of intermediate reasoning steps.
- Representative work: PRM800K (Lightman et al., 2023) — human labelers carefully validated each step of multi-hop reasoning chains, demonstrating that capturing human judgments about process correctness substantially improves PRM training.
- Limitations: resource-intensive and limited in scale; primarily serves as high-fidelity seed material and benchmark foundation.

**2.2 Automated Supervision**
- Large body of work generates process supervision via symbolic verification, consistency checks, execution feedback, or synthetic self-evolution — without human annotation.
- Math-Shepherd (Wang et al., 2023): validates math reasoning steps using symbolic tools and consistency-checking heuristics.
- FOVER (Kamoi et al., 2025): uses formal verification tools (Z3, Isabelle) to auto-generate accurate step-level error labels.
- OmegaPRM (Luo et al., 2024): divide-and-conquer Monte Carlo Tree Search (MCTS) to efficiently identify the first error in a reasoning chain.
- URSA (Luo et al., 2025): fully automated dual-view pipeline for multimodal math reasoning, combining MCTS-based error localization and misinterpretation insertion engines.
- MT-RewardTree (Feng et al., 2025b): adapts MCTS to machine translation for token-level preference pair generation.
- CodePRM (Li et al., 2025a): automated tree search and execution feedback for step-level supervision in code reasoning.
- AlphaMath (Chen et al., 2024): derives pseudo process supervision directly from outcome supervision, eliminating the need for stepwise labels.
- rStar-Math (Guan et al., 2025) and Qwen2.5-Math PRM (Zhang et al., 2025j): self-evolutionary and consensus-filtering strategies to create massive reasoning datasets.
- EpicPRM (Sun et al., 2025b): balances precision and scale in constructing process-supervised training data.
- SCAN (Ding et al., 2025): self-denoising annotation framework to automatically detect and correct noisy labels.

**2.3 Semi-automated Approaches**
- Blend selective human input with scalable automated expansion.
- VRPRM (Chen et al., 2025f) and Athena (Wang et al., 2025b): start with limited human-curated reasoning steps, expand via automated verification or synthetic generation, for multimodal reasoning.
- MedS³ (Jiang et al., 2025): ~8,000 human-curated medical examples expanded via MCTS-based exploration and rule-verifiable trajectory generation.
- VersaPRM (Zeng et al., 2025): synthetic reasoning data across multiple domains via auto-labeling with small-scale manual evaluation.
- Web-Shepherd (Chae et al., 2025): supervises web navigation reasoning traces by mixing human oversight with automatic checks.
- ActPRM (Duan et al., 2025): active learning — queries human annotators only when automated signals are uncertain.

---

### Section 3: How to Build PRMs

**3.1 Discriminative PRMs**
- Learn a scoring function over intermediate reasoning states to predict per-step correctness, plausibility, or progress.
- Given input $x$ and partial solution $s_{1:t}$, the model outputs a scalar score: $r_t = \sigma(f_\theta(x, s_{1:t})) \in (0,1)$.
- **Pointwise loss**: binary cross-entropy (BCE) or mean squared error (MSE).
- **Pairwise (preference) loss**: analogous to the DPO objective — minimizes $\mathcal{L}_\text{pair} = \mathbb{E}[-\log \mathbb{P}_\theta(u \succ v)]$.
- Representative works: DreamPRM (Cao et al., 2025b), PQM (Li and Li, 2024), ER-PRM (Zhang et al., 2024), EDU-PRM (Cao et al., 2025a), Q-RM (Chen et al., 2025b), BiPRM (Zhang et al., 2025d), BiRM (Chen et al., 2025e), CoLD (Zheng et al., 2025), ProgRM (Zhang et al., 2025a).

**3.2 Generative PRMs**
- Two-stage operation: first generates a verification or critique chain $z_t$ ("think"), then judges/scores the original reasoning step based on that chain ("judge").
- Formally: $z_t \sim p_\phi(z_t \mid x, s_{1:t})$; $r_t = h_\psi(x, s_{1:t}, z_t)$.
- Joint training objective: $\mathcal{L}_\text{gen} = -\log p_\phi(z_t^* \mid x, s_{1:t}) + \lambda \text{BCE}(r_t, y_t)$.
- In many works, $h_\psi$ is the confidence of answer logits (softmax over yes/no tokens).
- Representative works: ThinkPRM (Lee et al., 2025), GenRM (Zhang et al., 2025e), GenPRM (Zhao et al., 2025), GRAM-R² (Wang et al., 2025a), GM-PRM (Zhang et al., 2025b), rStar-Math (Guan et al., 2025), Test-Time Scaling with Reflective Generative Model (Wang et al., 2025g).

**3.3 Implicit PRMs**
- Infer fine-grained rewards without step-level labels, leveraging weaker or indirect supervision: outcome feedback, model self-evaluation, or consistency constraints.
- FreePRM (Sun et al., 2025a): trains a reward model without ground-truth process class labels via pseudo-labeling from outcome correctness.
- Self-PRM (Feng et al., 2025a): shows LLMs under RL training internally develop a PRM-style self-rewarding capability.
- SP-PRM (Xie et al., 2025a): transfers reasoning knowledge from an ORM into process reward modeling to reduce label dependency.
- SPARE (Rizvi et al., 2025): single-pass reference guidance to automatically generate supervision signals for intermediate steps.
- Universal PRM / AURORA (Tan et al., 2025): ensemble prompting and reverse verification for domain-agnostic self-supervised reward signals.
- Process-based Self-Rewarding Language Models (Zhang et al., 2025g): the model generates and evaluates its own reasoning chain, closing the loop for self-supervision.

**3.4 Other Architectural Innovations**
- GraphPRM (Peng et al., 2025): casts reasoning as a graph of steps, learning structured dependencies.
- ASPRM / AdaptiveStep (Liu et al., 2025): dynamically adjusts reasoning step granularity based on model confidence.
- Reward-SQL (Zhang et al., 2025i): structured PRM tailored to Text-to-SQL.
- RetrievalPRM (Zhu et al., 2025): integrates external retrieval to ground reward predictions and improve cross-task generalization.
- OpenPRM (Zhang et al., 2025c): organizes reward judgments into an open preference tree.
- MM-PRM (Du et al., 2025): unified multimodal PRM architecture.
- Multilingual PRM (Wang et al., 2025e): cross-language CoT transfer via representational mapping.
- PathFinder-PRM (Pala et al., 2025a): hierarchical error-aware architecture distinguishing different types of reasoning errors.
- HRM / Hierarchical Reward Model (Wang et al., 2025d): layered reward structures aligned with multi-level reasoning abstractions.

---

### Section 4: How to Use PRMs

**4.1 Test-Time Scaling**
- Goal: improve model performance by strategically allocating computation during inference — via candidate sampling, re-ranking, or guided search — rather than enlarging model size.
- **Re-ranking**: early work used PRMs as re-rankers; Best-of-N with PRM scores consistently improves final performance (Lightman et al., 2023; Wang et al., 2023; Zheng et al., 2025).
- **Generative verification**: GenPRM (Zhao et al., 2025) generates reasoning or code checks before scoring; ThinkPRM fine-tunes long CoT verifiers with limited process labels.
- **Search integration**: PRM-BAS (Hu et al., 2025a) — beam annealing search with PRM pruning; CodePRM — Generate–Verify–Refine pipeline; Web-Shepherd — filtering web-agent trajectories; MCTS or retrieval-augmented reasoning with PRMs (Chan et al., 2025; Ma et al., 2025; Chen et al., 2025d).
- **Adaptive granularity**: AdaptiveStep dynamically partitions reasoning steps based on confidence; SP-PRM extends reward-guided search across multiple granularity levels.
- **Safety-aware scaling**: SAFFRON-1 reduces costly PRM calls with caching mechanisms for robust, efficient inference under adversarial conditions.

**4.2 RL for Policy Learning**
- PRMs provide dense step-level or trajectory-level feedback to replace sparse outcome signals in RL training loops, enabling more stable credit assignment and faster policy learning.
- **Foundational applications**: Math-Shepherd (Wang et al., 2023) — automatic verifier scoring each intermediate step, used as PPO rewards; Dai et al. (2024) — line-level PRM signals injected into RL for code generation.
- **Formalizing PRM signals in RL objectives**:
  - PAV (Setlur et al., 2024): reframes step-level PRM outputs as advantage-like progress indicators for dense step-level rewards.
  - ER-PRM (Zhang et al., 2024): embeds PRM rewards into KL-constrained RL objectives, stabilizing training while preserving exploration.
  - PURE (Cheng et al., 2025): addresses reward hacking by replacing sum-of-rewards with a min-form objective integrating PRM signals more robustly.
  - Q-RM (Chen et al., 2025c): models Q-values over tokens and uses them directly as rewards during RL optimization.
  - CAPO (Xie et al., 2025c): verifiable generative credit assignment producing reliable step-level rewards, replacing sparse outcome signals and improving exploration efficiency.
- **He et al. (2025b)**: generative, thought-level PRM assigning grouped step-level rewards for policy RL with off-policy algorithm and adaptive reward balancing.
- **PROF (Ye et al., 2025)**: ranks and filters responses based on process–outcome consistency between PRMs and ORMs, maintaining balanced training and integrating with GRPO.
- **Domain-specific RL**: GraphPRM for graph reasoning preference optimization; AgentPRM integrating PRMs into actor-critic loop for LLM-based agents.
- **Scaling frameworks**: OpenR (Wang et al., 2024) — open-source infrastructure systematizing PRM integration into offline and online RL pipelines.

---

### Section 5: Downstream Applications

| Domain | Representative Applications |
|--------|----------------------------|
| Math | Validating algebraic/logical steps; automated grading, tutoring, proof validation |
| Code | Assessing partial programs via execution or proxy testing feedback; text-to-SQL; software engineering |
| Multimodal | Checking visual-text coherence; re-ranking multimodal reasoning traces; grounded explanations |
| Text | Evaluating partial translations; scoring intermediate hops in QA and retrieval-augmented reasoning |
| Robotics | Decomposing long-horizon manipulation/navigation into subgoal rewards, accelerating policy learning |
| Agents | Trajectory critics; pruning dead ends; improving safety during inference |
| Industry | Medicine (MedS³) and finance (Fin-PRM): verifiable, evidence-based reasoning for high-stakes decisions |

---

### Section 6: Benchmarks

| Benchmark | Key Features |
|-----------|-------------|
| PRMBench (Song et al., 2025) | 6,000+ problems, 80,000 step annotations, multidimensional labels (simplicity, soundness, sensitivity) |
| ProcessBench (Zheng et al., 2024) | Competition-level tasks; emphasis on earliest-error detection for precise symbolic reasoning |
| Socratic-PRMBench (Li et al., 2025b) | ~3,000 flawed trajectories in six error patterns; tests generalization across reasoning styles |
| ViLBench (Tu et al., 2025) | Compares PRMs with outcome models in vision-language reasoning |
| VisualProcessBench (Wang et al., 2025f) | Human-labeled multimodal errors |
| MPBench (Xu et al., 2025) | Multi-task: step correctness, answer aggregation, reasoning-guided search |
| WebRewardBench (Chae et al., 2025) | 40,000 step-level preference pairs; evaluates web agent navigation (clicks, form entries) |
| GSM-DC (Yang et al., 2025b) | Injects distractors to test resilience |
| UniversalBench (Tan et al., 2025) | Cross-distribution generalization and reproducibility across diverse policy distributions |

---

### Section 7: Discussion — Three Reward Mechanisms Compared Across Six Dimensions

| Dimension | Rule-based | ORM | PRM |
|-----------|-----------|-----|-----|
| Resource Efficiency | Highest (no data/training needed) | Moderate | Lower (requires step annotations and complex pipelines) |
| Granularity | Moderate (adjustable by rule design) | Coarse (final outcome only) | Finest (step-level evaluations) |
| Anti-Hacking Robustness | Strongest (signal tied to final output correctness) | Strong | Moderate (susceptible to step annotation biases and over-fitting human-preference artifacts) |
| Generalization | Poor (rules must be re-engineered per new environment) | Strong (outcome-centric principle transfers easily) | Moderate (step-level evaluation idea generalizes, but specific model often needs re-adaptation to new task structure) |
| Interpretability | Strongest (logic explicitly encoded in rules) | Weak (only final judgment, no intermediate insight) | Moderate (step-wise supervision richer than ORMs, but internal scoring mechanisms may still lack full transparency) |
| Functionality | Restricted (limited to originally designed scenarios) | Moderate (applicable across multiple tasks for outcome evaluation) | Strongest (seamlessly integrates with RL and test-time scaling, enabling fine-grained optimization and guided reasoning) |

**Conclusion**: PRMs shift reasoning alignment from coarse outcome judgments to fine-grained, step-level feedback, forming a closed loop of data generation, model training, and usage that continually improves reasoning quality. Key challenges ahead: reducing annotation cost via robust automatic supervision, improving cross-domain generalization, integrating PRMs with agentic planning and memory, and establishing standardized evaluation protocols.
