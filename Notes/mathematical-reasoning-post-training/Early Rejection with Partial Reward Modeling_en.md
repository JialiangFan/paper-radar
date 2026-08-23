# Early Rejection with Partial Reward Modeling

**Full Title**: Accelerating LLM Reasoning via Early Rejection with Partial Reward Modeling
**Authors**: Seyyed Saeid Cheshmi, Azal Ahmad Khan, Xinran Wang, Zirui Liu, Ali Anwar (University of Minnesota)
**arXiv**: 2508.01969v1 [cs.LG], 4 Aug 2025
**Code**: https://github.com/scheshmi/accelerated-reasoning-ER-PRM

---

## Topic: PRM-based early rejection

This paper proposes repurposing Process Reward Models (PRMs) as Partial Reward Models to score candidate beams mid-generation — after only τ tokens — enabling early rejection of low-quality beams and substantially reducing inference-time FLOPs without degrading final task performance.

---

## Background

- Large Language Models (LLMs) have demonstrated strong capabilities in complex reasoning tasks including mathematics, logic, and multi-step question answering.
- A major line of work improves reasoning quality by scaling inference-time compute, using strategies such as Best-of-N (BoN) decoding, beam search, and Monte Carlo Tree Search (MCTS).
- **Outcome Reward Models (ORMs)** score the final output; **Process Reward Models (PRMs)** score each intermediate reasoning step, providing denser supervision signals shown to improve reasoning generalization.
- In PRM-guided beam search, the model generates N candidate beams in parallel; after each step, the PRM scores all beams and retains only the top-scoring ones for further expansion, iteratively constructing a multi-step reasoning trace.
- In practice, beam counts must scale to 1,000–60,000 to be competitive, generating a very large number of output tokens at high computational cost, with sequential token generation introducing significant latency.

---

## Limitations & Research Problem

**Existing limitations:**
- Standard PRM-guided beam search waits for each step to be fully generated before scoring, wasting computation on beams that will ultimately be pruned.
- Prior work such as Speculative Rejection (Sun et al., 2024) explored ORM-based mid-generation rejection in BoN settings, but early rejection for the PRM paradigm remained underexplored.

**Core research questions:**
- Can a PRM provide reliable quality signals mid-step — after only τ tokens — to enable early rejection of suboptimal beams before full step generation is complete?
- Are partial rewards computed on incomplete generation sufficiently predictive of the final rewards on completed steps?

---

## Contributions

**(C1) Hypothesis:** The paper introduces the hypothesis that **Process Reward Models are also Partial Reward Models** — the partial scores assigned by a PRM after only a fraction of step generation are strongly correlated with final rewards, making them reliable early quality signals.

**(C2) Theoretical guarantees:** Under mild assumptions (independent sub-Gaussian noise, preserved expected score ordering), the probability of prematurely rejecting the optimal beam decreases exponentially with partial generation length:
$$\Pr(P_{i^*} < T) \leq (N-1)\exp\!\left(-\frac{\Delta^2}{4\sigma^2}\right)$$
where Δ is the minimum expected partial-score gap between the best beam and any other beam, and σ is the sub-Gaussian noise parameter.

**(C3) Empirical validation:** On AIME, MATH-500, and SAT-MATH (AGIEval) benchmarks, the method achieves **1.4×–9× reduction** in inference FLOPs with a mid-sized PRM (7B parameters) and **1.5×–4× reduction** with a lightweight PRM (1.5B parameters), with no loss in final task performance.

---

## Methodology

### Core idea

Within each reasoning step of beam search, instead of waiting for full step completion, generate only the first **τ tokens** of each beam, immediately invoke the PRM to compute a **partial reward**, prune low-scoring beams, complete only the surviving beams, and then proceed to beam expansion.

### Algorithm: Beam Search with Early Rejection (Algorithm 1)

1. Initialize N beams
2. **For** each beam: generate up to τ tokens; compute partial reward using PRM
3. Select top N/M beams by partial reward; complete them to full step length
4. Expand each surviving beam into M new beams
5. Repeat scoring, early rejection, and expansion until stopping condition; return best final sequence

### Efficiency mechanisms

**FLOPs reduction:** By rejecting low-quality beams after τ tokens, the method avoids full generation and full PRM evaluation for the pruned beams at each step, directly reducing both token generation and reward model FLOPs.

**Two-tiered batching:** 
- During the partial τ-token generation phase, sequences are short and memory usage is low, enabling a **larger batch size**.
- When completing surviving beams to full step length, a **smaller batch size** is used to avoid OOM errors, improving overall throughput while maintaining memory efficiency.

### Selecting the optimal τ

Under an i.i.d. token log-score model, the Pearson correlation between partial reward P_i and final reward F_i is:
$$\rho(P_i, F_i) = \sqrt{\frac{\tau}{L}}$$
To reach a target correlation level ρ*, one needs τ ≥ (ρ*)² · L. For example, achieving ρ* = 0.8 requires τ ≥ 0.64L. Empirically, at τ = 32 the correlation already exceeds 0.78, and at τ = 64 both Pearson and Kendall's Tau metrics exceed 0.9.

### Experimental setup

- **Benchmarks**: MATH-500, SAT-MATH (AGIEval), AIME 2024
- **LLMs**: Llama-3.2-3B-Instruct, Qwen2.5-3B-Instruct
- **PRMs**: MathShepherd-Mistral-7B (7B), Skywork-PRM-1.5B (1.5B)
- **Beam count N** ∈ {4, 8, 16, 32, 64}, **beam width M** = 4
- **Early rejection threshold** τ ∈ {32, 64, 128}
- All experiments on HPC cluster with 4× NVIDIA A100 (40 GB) GPUs

### Key empirical observations

**Observation 1 — Very short prefixes reliably predict final scores:** At τ = 32, Pearson correlation already exceeds 0.78; at τ = 64, both correlation metrics exceed 0.9 and plateau. This allows early rejection after the first 32–64 tokens while eliminating 60–85% of downstream PRM calls and generation FLOPs.

**Observation 2 — Smaller PRMs can match or exceed larger PRMs:** Skywork-PRM-1.5B achieves equal or higher accuracy than MathShepherd-Mistral-7B while enabling larger FLOP reductions, contradicting the assumption that "bigger judge = better answers." Skywork also yields more FLOP savings because the 3B LLM becomes the computational bottleneck, allowing more frequent savings.

**Observation 3 — Early rejection is most beneficial for exploratory LLMs at small beam widths:** Qwen2.5-3B generates long exploratory reasoning traces; many beams appear weak after τ = 32–64 tokens. Early rejection frees beam slots for new candidates, expanding the search space without increasing beam width N, improving accuracy by up to 3.5% at N = 4. In contrast, Llama-3.2-3B produces shorter, deterministic outputs, so early rejection mainly improves compute efficiency rather than accuracy.

**Observation 4 — τ = 64 achieves higher accuracy at lower compute than τ = 32:** At τ = 32, correlation ~0.78 means ~20% of beams may be incorrectly ranked. At τ = 64, correlation exceeds 0.90 and flattens, meaning nearly all retained beams are genuinely promising. The number of survivors and FLOPs spent on them actually decreases when increasing τ from 32 to 64.

**Observation 5 — LLM generation behavior (not model size) drives compute cost:** Qwen2.5-3B incurs significantly higher total FLOPs than Llama-3.2-3B under identical early rejection settings because it generates longer, exploratory chains. Early rejection is most effective when it blocks exploratory failures early, preventing costly long completions.

### Limitations

- The approach relies on monotonicity and calibration of PRM scores. In tasks with delayed or non-monotonic utilities (e.g., code synthesis with backtracking, creative writing), early rejection may mis-reject the eventual best beam.
- The study is confined to text-only, math-centric benchmarks; larger models for multimodal tasks or domains with sparse positive signals may exhibit different trade-offs.
- Memory overhead of storing intermediate PRM states after τ tokens is not quantified.
- Theoretical guarantees assume independent step-wise noise and fixed τ; adaptive τ scheduling and integration with policy-learning frameworks (RLHF, DPO) remain open questions.
