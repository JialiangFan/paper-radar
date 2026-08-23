# LLM Post-Training for Reasoning, Planning, and Safety

> Literature Review — Structured for Academic Presentation

| Research Topic | Paper Number | PDF Files |
|---|---|---|
| Process Reward Modeling | 4 | 2502.01456v2.pdf (PRIME), 2510.11457v1.pdf (DRM), 2506.18896v2.pdf (ReasonFlux-PRM), 2024.emnlp-main.20.pdf (Jiao et al.) |
| Search-Based LLM Planning | 3 | 2023.emnlp-main.507.pdf (RAP), 2512.23167v1.pdf (SPIRAL), 2410.20007v1.pdf (CoPlanner) |
| Safety in LLM Reasoning & Planning | 2 | 2503.06892v1 (1).pdf (SafePlan), 4405_Towards_Safe_Reasoning_in.pdf (IPO) |
| CoT Effectiveness & Improvement | 2 | NeurIPS-2024-chain-of-thoughtlessness-...pdf (Chain of Thoughtlessness), 20208_Teaching_LLMs_to_Plan_Lo.pdf (PDDL-Instruct) |
| **Total** | **11** | |

---

# Part 1. Literature Taxonomy

---

## Theme 1: Process Reward Modeling

**Papers:**
- PRIME — Process Reinforcement through Implicit Rewards (2025)
- DRM — From \<Answer\> to \<Think\>: Multidimensional Supervision of Reasoning Process (2025)
- ReasonFlux-PRM — Trajectory-Aware PRMs for Long CoT Reasoning (2025)
- Jiao et al. — Learning Planning-based Reasoning via Trajectories Collection and Process Reward Synthesizing (EMNLP 2024)

**Theme Summary:**
This line of work addresses how to provide dense, step-level feedback for LLM reasoning without expensive human annotations. The four papers propose distinct automation strategies: synthesizing from outcome annotations (Jiao et al.), deriving implicit rewards from model logprobs (PRIME), multi-dimensional evaluation (DRM), and trajectory-level context modeling (ReasonFlux-PRM). Their shared conclusion is that process supervision significantly outperforms outcome-only supervision, but the annotation bottleneck must be resolved through automation.

---

## Theme 2: Search-Based LLM Planning

**Papers:**
- RAP — Reasoning with Language Model is Planning with World Model (EMNLP 2023)
- SPIRAL — Symbolic LLM Planning via Grounded and Reflective Search (AAAI 2025)
- CoPlanner — Cooperative Strategic Planning Enhances Reasoning Capabilities in LLMs (2024)

**Theme Summary:**
This cluster explores how to enable genuine multi-step planning in LLMs beyond autoregressive generation. RAP established the "LLM-as-world-model + MCTS" paradigm; SPIRAL advanced it with a tri-agent cognitive architecture and reflection-driven reward shaping; CoPlanner separated the planning agent from the reasoning agent for cooperative execution. The core insight is that structured search compensates for LLMs' lack of lookahead and backtracking capabilities.

---

## Theme 3: Safety in LLM Reasoning and Planning

**Papers:**
- SafePlan — Leveraging Formal Logic and CoT Reasoning for Enhanced Safety in LLM-based Robotic Task Planning (2025)
- IPO — Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention (ICLR 2026)

**Theme Summary:**
These two papers address LLM reasoning safety from complementary angles: inference-time and training-time. SafePlan performs multi-layered safety verification at inference using formal logic (LTL) and structured CoT. IPO targets training-time alignment by identifying "safety triggers" and "compliance cues" in reasoning traces, then optimizing with DPO. Ideally, both training-time (IPO) and inference-time (SafePlan) safety measures should be deployed together.

---

## Theme 4: CoT Effectiveness Analysis and Improvement

**Papers:**
- Chain of Thoughtlessness — An Analysis of CoT in Planning (NeurIPS 2024)
- PDDL-Instruct — Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning (ICLR 2026, under review)

**Theme Summary:**
These two papers form a "problem—solution" dialogue. Chain of Thoughtlessness provides a rigorous negative result: standard CoT does not induce generalizable algorithmic reasoning — it is fundamentally pattern matching. PDDL-Instruct responds with a constructive solution: combining formal verifier (VAL) feedback with instruction tuning makes CoT effective for symbolic planning. Together, they demonstrate that raw CoT is insufficient, but structured CoT + verification feedback can succeed.

---

# Part 2. Representative Paper Deep Dive

---

## Theme 1: Process Reward Modeling

### Representative Paper
**PRIME: Process Reinforcement through Implicit Rewards**

### Publication Information
- **Title:** Process Reinforcement through Implicit Rewards
- **Authors:** Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Wenjie Li, Bingxiang He, Quanquan Gu, Huishuai Zhang, Ningyu Zhang, et al.
- **Venue:** arXiv 2502.01456v2, 2025
- **Year:** 2025

### Suggested Screenshot Materials

- **Screenshot 1:** Paper title page (title + author list)
  - Purpose: Introduce the paper
  - Location: Page 1

- **Screenshot 2:** Implicit PRM vs Explicit PRM comparison diagram
  - Purpose: Visually contrast implicit vs explicit reward derivation and the online update mechanism
  - Location: ~Pages 3-4 (Methods section)

- **Screenshot 3:** Performance comparison table across benchmarks
  - Purpose: Show the 15.1% average improvement
  - Location: ~Pages 6-7 (Experiments section)

---

### Background

Traditional process reward models (PRMs) require extensive step-level annotations, typically produced by human experts, which are expensive and noisy. Even automated approaches like Monte Carlo sampling still require training a separate PRM, which becomes stale as the policy updates — leading to reward hacking.

Moreover, outcome reward models (ORMs) only provide final-answer correctness signals, offering no guidance for intermediate reasoning steps. This makes RL training inefficient with sparse rewards.

---

### Research Problem

> Can we obtain dense process-level reward signals directly from the policy model itself — without training a separate PRM — to enable efficient RL training for reasoning?

---

### Main Contributions

- **Contribution 1:** Implicit process rewards derived from token-level logprob ratios between policy and reference models, requiring zero annotations
- **Contribution 2:** Online PRM updates synchronized with the policy, naturally avoiding reward hacking
- **Contribution 3:** Plug-and-play design compatible with any policy gradient algorithm (REINFORCE, GRPO, PPO)
- **Contribution 4:** 15.1% average improvement across math and coding benchmarks

---

### Methodology

#### Overall Idea

PRIME's core insight: the policy model's logprob changes at each reasoning step inherently encode "reward" information for that step. By computing token-level logprob ratios between the policy and reference models, implicit process rewards are obtained for free and used in RL training.

#### Core Components

- **Implicit PRM:** Computes per-step rewards via $\log \frac{\pi_\theta(a|s)}{\pi_{ref}(a|s)}$ — no additional model needed
- **Online Update:** Implicit rewards update synchronously with the policy, eliminating PRM staleness
- **KL-Regularized Reward:** KL regularization term balances exploration and exploitation

#### Training / Optimization

- **Training Objective:** Policy gradient with implicit process rewards (RLOO variant)
- **Reward Signal:** Step-level aggregation of token-level logprob ratios
- **Inference Workflow:** No additional PRM at inference — standard policy model generation

---

### Key Takeaways

- Most important insight: process rewards can be obtained "for free" — no annotations or additional model training required
- Compared to DRM and ReasonFlux-PRM, PRIME is the most lightweight — zero additional model overhead
- Online update mechanism inherently solves the reward hacking problem that plagues explicit PRMs
- Limitations: the additivity assumption on token-level implicit rewards may not hold for all reasoning types; evaluation focused on math/code domains

---

## Theme 2: Search-Based LLM Planning

### Representative Paper
**SPIRAL: Symbolic LLM Planning via Grounded and Reflective Search**

### Publication Information
- **Title:** SPIRAL: Symbolic LLM Planning via Grounded and Reflective Search
- **Authors:** Wenhan Luo, Zhengyi Lu, Weichuan Liu, et al.
- **Venue:** AAAI 2025
- **Year:** 2025

### Suggested Screenshot Materials

- **Screenshot 1:** Paper title page (title + AAAI 2025)
  - Purpose: Introduce the paper
  - Location: Page 1

- **Screenshot 2:** Tri-agent (Planner-Simulator-Critic) + MCTS architecture diagram
  - Purpose: Core contribution visualization — clearly shows the cognitive architecture
  - Location: ~Pages 3-4

- **Screenshot 3:** Performance comparison on DailyLifeAPIs and HuggingFace benchmarks
  - Purpose: Show the 83.6% accuracy and +16pp improvement over LATS
  - Location: ~Pages 6-7

---

### Background

Existing LLM planning methods (RAP, LATS, ToT) leverage tree search but suffer from two critical limitations: (1) the search process lacks grounding — it cannot accurately simulate the effects of actions; (2) reward signals are sparse, relying solely on final outcome feedback, leading to inefficient search.

---

### Research Problem

> How can we provide grounded state-transition simulation and dense reflective feedback within MCTS-based LLM planning?

---

### Main Contributions

- **Contribution 1:** Tri-agent cognitive architecture (Planner + Simulator + Critic) embedded in MCTS
- **Contribution 2:** Simulator as world model providing grounded state-transition simulation
- **Contribution 3:** Reflection-Driven Reward Shaping: $R_t = \alpha R_{base}(a_t) + (1-\alpha)\rho_{ref}$, combining base rewards with reflection scores

---

### Methodology

#### Overall Idea

SPIRAL assigns each MCTS search step to three specialized agents: the Planner proposes candidate actions, the Simulator models post-action state transitions (world model), and the Critic provides strategic-level reflective feedback.

#### Core Components

- **Planner Agent:** Proposes candidate actions given the current state
- **Simulator Agent:** Simulates environment state changes after action execution, providing grounded verification
- **Critic Agent:** Evaluates current plan quality and generates reflection score $\rho_{ref}$

#### Training / Optimization

- **Training Objective:** None — purely inference-time framework
- **Reward Signal:** Reflection-Driven Reward Shaping combining base reward and critic reflection score
- **Inference Workflow:** MCTS search with each node expansion requiring three LLM calls

---

### Key Takeaways

- Core insight: grounded simulation (Simulator) and dense reflective feedback (Critic) within MCTS dramatically improve search quality
- Compared to RAP and LATS: SPIRAL leads by 16 percentage points on DailyLifeAPIs with superior token efficiency
- The tri-agent architecture echoes dual-process theory from cognitive science
- Limitations: three LLM calls per search step incur high computational cost; evaluated only on API-calling domains

---

## Theme 3: Safety in LLM Reasoning and Planning

### Representative Paper
**IPO: Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention**

### Publication Information
- **Title:** Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention
- **Authors:** Yuntao Liu, Zhangchen Xu, Jianwei Yin, et al.
- **Venue:** ICLR 2026
- **Year:** 2026

### Suggested Screenshot Materials

- **Screenshot 1:** Paper title page (title + ICLR 2026)
  - Purpose: Introduce the paper
  - Location: Page 1

- **Screenshot 2:** Safety Trigger and Compliance Cue analysis in reasoning traces
  - Purpose: Core discovery visualization — shows safety-critical nodes in reasoning trajectories
  - Location: ~Pages 4-5

- **Screenshot 3:** IPO method pipeline (identify → replace → DPO training)
  - Purpose: Show the complete Corrective Intervention pipeline
  - Location: ~Pages 5-6

---

### Background

Large Reasoning Models (LRMs) such as DeepSeek-R1 achieve remarkable reasoning capabilities through extended thinking, but this introduces new safety risks: longer reasoning chains may contain "compliance cues" that gradually steer the model toward unsafe outputs. Traditional safety alignment methods (RLHF/DPO) primarily target final outputs and cannot intervene in the reasoning process itself.

---

### Research Problem

> How can we improve the safety of large reasoning models by intervening at critical nodes in reasoning trajectories — without degrading reasoning capabilities?

---

### Main Contributions

- **Contribution 1:** Discovery that reasoning traces contain identifiable "safety triggers" and "compliance cues" — two distinct structural patterns
- **Contribution 2:** Proposal of Continuation Safety Ratio (CSR) as a metric for quantifying reasoning trajectory safety
- **Contribution 3:** Intervened Preference Optimization (IPO) — constructing preference pairs by replacing compliance cues with safety triggers, then training with DPO

---

### Methodology

#### Overall Idea

IPO first analyzes reasoning traces to identify two types of critical reasoning steps: safety triggers (steps that cause CSR to reach 100%) and compliance cues (steps strongly correlated with unsafe turning points, Pearson R=0.853). It then replaces compliance cues with safety triggers to construct preference data pairs, and trains with DPO on partial trajectories.

#### Core Components

- **Safety Trigger Identification:** Locate reasoning steps that consolidate safe reasoning
- **Compliance Cue Detection:** Locate reasoning steps signaling compliance with harmful requests
- **Corrective Intervention:** Replace compliance cues in unsafe trajectories with safety triggers

#### Training / Optimization

- **Training Objective:** DPO loss on partial trajectory preference pairs
- **Reward Signal:** Preference pairs from corrective intervention (no additional reward model needed)
- **Inference Workflow:** No additional inference-time overhead — standard model generation after training

---

### Key Takeaways

- Most important insight: reasoning traces are not "black boxes" — they contain identifiable safety-critical structures that can be precisely targeted
- Compared to SafePlan (inference-time verification), IPO is a training-time approach with zero inference-time latency overhead
- >30% harmfulness reduction while preserving or enhancing reasoning capabilities — proving safety and capability need not be at odds
- Limitations: safety trigger identification may not generalize to all attack types; validated only on 7B-8B models

---

## Theme 4: CoT Effectiveness Analysis and Improvement

### Representative Paper
**PDDL-Instruct: Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning**

### Publication Information
- **Title:** Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning
- **Authors:** Anonymous (under review)
- **Venue:** ICLR 2026 (under review)
- **Year:** 2026

### Suggested Screenshot Materials

- **Screenshot 1:** Paper title page
  - Purpose: Introduce the paper
  - Location: Page 1

- **Screenshot 2:** Two-phase instruction tuning pipeline (Phase 1 + Phase 2 with VAL verifier)
  - Purpose: Core method visualization
  - Location: ~Pages 3-5

- **Screenshot 3:** Comparison chart showing 94% accuracy on Blocksworld
  - Purpose: Show the +66% improvement over baseline
  - Location: ~Pages 6-8

---

### Background

Chain of Thoughtlessness (NeurIPS 2024) demonstrated that standard CoT prompting does not induce genuine algorithmic reasoning in LLMs — improvements appear only with highly specific prompts and degrade as problem size increases. This implies that LLMs require more fundamental training approaches for symbolic planning, not just prompt engineering.

---

### Research Problem

> How can we teach LLMs genuine symbolic planning capabilities through instruction tuning combined with formal verifier feedback?

---

### Main Contributions

- **Contribution 1:** Two-phase instruction tuning framework — Phase 1 (correct/incorrect plans + explanations) + Phase 2 (CoT + VAL verifier feedback loop)
- **Contribution 2:** 94% plan accuracy on Blocksworld (+66% improvement over baseline Llama-3-8B)
- **Contribution 3:** Cross-domain generalization — transfers to Mystery Blocksworld and Logistics without domain-specific retraining

---

### Methodology

#### Overall Idea

PDDL-Instruct integrates a formal planning verifier (VAL) into LLM instruction tuning. Phase 1 teaches the model to distinguish correct from incorrect plans and understand why; Phase 2 enables the model to learn from its own planning mistakes through an iterative verification feedback loop.

#### Core Components

- **Phase 1 (Initial IT):** Training on correct/incorrect plan pairs with natural language explanations
- **Phase 2 (CoT IT):** Iterative CoT fine-tuning with VAL verifier checking plan correctness and providing feedback each round
- **VAL Verifier:** Formal planning verifier providing binary or detailed feedback (detailed consistently outperforms)

#### Training / Optimization

- **Training Objective:** Standard language model fine-tuning loss (both phases)
- **Reward Signal:** VAL verifier correctness feedback (used as training data, not explicit rewards)
- **Inference Workflow:** Direct plan generation after fine-tuning; optional VAL post-verification

---

### Key Takeaways

- Core insight: formal verifier feedback is the key ingredient that makes CoT effective for planning — directly responding to Chain of Thoughtlessness's negative result
- Detailed feedback consistently outperforms binary feedback, indicating that informative error signals are crucial for learning planning
- Cross-domain generalization suggests the model learns general planning reasoning, not domain-specific patterns
- Limitations: requires PDDL formalization; limited to symbolic planning domains; small model scale

---

# Part 3. Cross-Paper Insights

---

## Overall Research Trends

- **From outcome to process supervision:** The field is shifting from ORM to PRM (PRIME, DRM, ReasonFlux-PRM, Jiao et al.), providing denser and more informative training signals
- **From monolithic to multi-agent reasoning:** CoPlanner and SPIRAL demonstrate that decomposing reasoning into specialized roles (planner/executor/critic) improves performance
- **From prompt engineering to training internalization:** Chain of Thoughtlessness exposes CoT's limitations, driving methods like PDDL-Instruct that internalize reasoning capabilities through training
- **Safety alignment penetrating the reasoning process:** IPO pioneers safety alignment targeting reasoning trajectories themselves, not just final outputs
- **Classical AI methods resurgent:** MCTS (RAP, SPIRAL), LTL (SafePlan), PDDL (PDDL-Instruct) — increasing integration of formal methods with neural LLM capabilities

---

## Common Patterns

### Methodological Frameworks
- **DPO as alignment infrastructure:** Jiao et al., DRM, and IPO all use DPO but construct preference pairs differently
- **MCTS as reasoning search framework:** RAP → SPIRAL forms an evolutionary chain for search-based planning
- **Verifier-in-the-loop:** VAL (PDDL-Instruct), Simulator (SPIRAL), LTL invariants (SafePlan) — verification feedback is a common pattern for improving reasoning quality

### Training Paradigms
- **RL training:** PRIME (RLOO), CoPlanner (PPO), DRM (GRPO), ReasonFlux-PRM (GRPO)
- **Preference optimization:** Jiao et al. (DPO), DRM (DPO), IPO (DPO)
- **Instruction tuning:** PDDL-Instruct (two-phase IT)

### Experimental Design
- **Math reasoning benchmarks:** MATH-500, AIME 2024, GSM8K (PRIME, DRM, ReasonFlux-PRM, Jiao et al., IPO)
- **Planning benchmarks:** Blocksworld (RAP, Chain of Thoughtlessness, PDDL-Instruct)
- **Small vs large model comparisons:** Multiple papers demonstrate 7-8B models surpassing GPT-3.5/GPT-4

---

## Differences Across Themes

| Dimension | Process Reward Modeling | Search-Based Planning | Safety Alignment | CoT Analysis & Improvement |
|-----------|----------------------|----------------------|-----------------|---------------------------|
| **Problem Formulation** | How to obtain step-level rewards | How to achieve multi-step planning | How to ensure safety | Whether/how CoT works |
| **Methodology** | Reward model design + RL | Search algorithms + multi-agent | Formal logic / preference optimization | Empirical analysis / instruction tuning |
| **Training Signal** | Implicit/synthesized process rewards | Search heuristics | Safety preference pairs / formal logic | Verifier feedback |
| **Application Scenario** | Math, code reasoning | API calling, logical reasoning | Robotic tasks, general safety | Symbolic planning |
| **Evaluation Focus** | Reasoning accuracy | Planning success rate | Harmfulness reduction rate | Generalization analysis |

---

## Insights and Inspirations

- **The "free lunch" of process rewards:** PRIME demonstrates that implicit rewards can be obtained without annotations. Can this extend to safety alignment? Are there implicit safety signals in model logprobs?
- **Verification-driven reasoning improvement:** PDDL-Instruct, SPIRAL, and SafePlan all rely on some form of verification. This suggests a universal paradigm: the **generate-verify-correct** loop may be the core mechanism for improving LLM reasoning.
- **Decoupling safety from capability:** IPO shows that safety alignment can precisely target specific nodes in reasoning trajectories without degrading overall capability. This offers a new perspective on the "alignment tax" problem.
- **Small model empowerment:** RAP (33B > GPT-4), Jiao et al. (7B > GPT-3.5), PDDL-Instruct (8B at 94%) — structured reasoning support can substitute for model scale, with significant implications for resource-constrained settings.
- **The right way to use CoT:** Chain of Thoughtlessness negates raw CoT; PDDL-Instruct provides the correction — CoT requires training and verification to be effective. This reframes CoT not as a prompting trick but as a training paradigm.

---

## Open Problems

1. **Cross-domain process reward models:** Current PRMs (PRIME, DRM, ReasonFlux-PRM) are primarily validated on math/code. Can they transfer to open-domain reasoning (commonsense reasoning, ethical judgment)?

2. **Search efficiency vs. practicality:** SPIRAL and RAP achieve strong results but incur high computational overhead. How can inference-time search costs be reduced while maintaining quality?

3. **Robustness of safety alignment:** Can IPO's safety trigger/compliance cue identification generalize to novel attack vectors? Do safety trigger distributions remain consistent in larger models?

4. **Scalability of formal methods:** SafePlan (LTL) and PDDL-Instruct (PDDL) depend on formal representations. How can these approaches scale to real-world tasks that resist easy formalization?

5. **Unified framework for process supervision + search + safety:** The three themes currently develop independently. Is it possible to design a unified framework that simultaneously provides dense process rewards, structured search, and safety guarantees?

6. **Optimal reasoning chain length:** IPO finds that longer reasoning chains may introduce safety risks; Chain of Thoughtlessness finds that longer CoT does not guarantee better results. How should the "optimal length" of reasoning chains be determined?
