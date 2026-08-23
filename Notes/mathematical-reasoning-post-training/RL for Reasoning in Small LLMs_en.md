# RL for Reasoning in Small LLMs

## Topic: RL reasoning small models

**Full Title:** Reinforcement Learning for Reasoning in Small LLMs: What Works and What Doesn't
**Authors:** Quy-Anh Dang, Chris Ngo (VNU University of Science, Vietnam; Knovel Engineering Lab, Singapore)
**arXiv:** 2503.16219v2 (January 20, 2026)
**Code & Datasets:** https://github.com/knoveleng/open-rs

---

## Background

Enhancing reasoning in large language models (LLMs) typically demands massive compute and expansive datasets, making it inaccessible for resource-constrained settings. OpenAI's o1 series demonstrated remarkable reasoning performance through inference-time scaling and extended Chain-of-Thought (CoT), but relies on proprietary, opaque methodologies. DeepSeek-R1 achieved comparable reasoning via Group Relative Policy Optimization (GRPO) on a 671B-parameter model, but its sheer scale makes self-hosting impractical for most organizations.

Small LLMs (1–10B parameters) offer a resource-efficient alternative with potential for widespread deployment. Prior works (DeepScaleR, Still-3) showed that RL-based fine-tuning can enhance small model reasoning, but these approaches still rely on hundreds of thousands of samples and significant hardware (e.g., 8× A100 80GB, 150–240 hours), undermining their accessibility for resource-constrained settings.

---

## Limitations & Research Problem

**Existing Limitations:**
- Current RL-based reasoning enhancement (DeepScaleR, Still-3, etc.) requires large-scale datasets (30k–40k samples × 8–16 outputs) and expensive hardware, with training costs ranging from $2268 to $3629.
- Most research targets models of 7B parameters or larger; RL training behavior of 1.5B models under strict resource constraints is understudied.
- Prolonged training suffers from optimization instability and output length constraint violations.
- Multilingual base models exhibit language drift after 150–200 training steps, producing non-English outputs despite English-only datasets.

**Core Research Questions:**
1. How do small LLMs behave when fine-tuned under strict resource constraints (limited compute and training time)?
2. Can their reasoning performance be elevated using an RL-based approach akin to DeepSeek-R1's methodology, and if so, how?

---

## Contributions

1. **Systematic analysis of small LLM reasoning potential:** Fine-tuned `DeepSeek-R1-Distill-Qwen-1.5B` under strict constraints (4× NVIDIA A40 48GB, 24 hours), providing a practical lens on scalability and deployment feasibility.
2. **Actionable insights:** Illuminated the efficacy and challenges of RL-based fine-tuning for small LLMs, bridging the gap between theoretical advancements and real-world applicability.
3. **Open-source release:** Published code and curated datasets to foster reproducibility and further exploration by the research community.

**Key Experimental Results (Open-RS model series):**
- AMC23 accuracy improved from 63% to a peak of 80% (Open-RS2, 50 steps)
- AIME24 reached 46.7% (Open-RS3), surpassing o1-preview (44.6%)
- Average benchmark scores: Open-RS1 53.0%, Open-RS2 55.7%, Open-RS3 56.3% (vs. DeepScaleR-1.5B-Preview at 57.0%)
- Total training cost: approximately **$42** (vs. $3629 for DeepScaleR, $2268 for Still-3)

---

## Methodology

### High-Quality Dataset Curation

A compact, high-quality mathematical reasoning dataset was constructed from two sources:

**open-s1 dataset (18,615 examples):**
- Source: s1 dataset (Muennighoff et al. 2025), a general-purpose reasoning corpus of 59,029 problems spanning NuminaMATH, AIME (1983–2021), OlympicArena, OmniMath, AGIEval, Stanford Stats PhD qualifying exams, and PuzzledQuant brainteasers.
- Filtering pipeline: Retain only problems with `\boxed{}` solutions (59,029 → 31,323) → Use `DeepSeek-R1-Distill-Qwen-1.5B` to eliminate trivial questions (→ 21,533) → Use `Qwen2.5-7B-Instruct` to remove noisy or multi-part questions (→ 18,615 final examples).

**open-deepscaler dataset (21,044 examples):**
- Source: DeepScaleR dataset (Luo et al. 2025), 40,315 mathematics-specific problems drawn from AIME (1984–2023), AMC (prior to 2023), Omni-MATH, and the Still dataset. Pre-filtered to remove redundant questions; solutions extracted via RAG and advanced LLMs.
- Filtering: Apply `Qwen2.5-Math-7B-Instruct` to exclude easy problems (→ 21,044 final examples). `Qwen2.5-Math-7B-Instruct` was chosen over `DeepSeek-R1-Distill-Qwen-1.5B` (used for s1) to introduce diversity in filtering criteria and avoid excessive overlap.

**Final combined dataset:** 39,659 high-quality mathematical reasoning examples (open-s1 + open-deepscaler). Experiments 2 and 3 use a 7,000-sample mixed subset (3,000 open-s1 + 3,000 open-deepscaler + 1,000 easier problems from the raw DeepScaleR dataset).

### Reinforcement Learning Algorithm

The study adopts **GRPO (Group Relative Policy Optimization)** (Shao et al. 2024), as used in DeepSeek-R1. GRPO eliminates the need for a separate critic model by estimating baselines from group scores, reducing computational overhead.

**GRPO objective:**

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\} \sim \pi_{\theta_\text{old}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left(\frac{\pi_\theta(o_i|q)}{\pi_{\theta_\text{old}}(o_i|q)} A_i, \text{clip}(\cdot, 1-\epsilon, 1+\epsilon) A_i\right) - \beta \mathbb{D}_\text{KL}(\pi_\theta \| \pi_\text{ref}) \right) \right]$$

The advantage $A_i$ is computed from a group of rewards $\{r_1, r_2, \ldots, r_G\}$: $A_i = \frac{r_i - \text{mean}(\{r_1,\ldots,r_G\})}{\text{std}(\{r_1,\ldots,r_G\})}$

Here $\epsilon$ and $\beta$ are hyperparameters controlling clipping range and KL penalty respectively. The SFT warm-up phase is bypassed entirely, hypothesizing that pretraining suffices to leverage RL directly.

### Reward Models

A rule-based reward system with three components, avoiding computationally expensive neural reward models:

- **Accuracy Reward:** Binary score (1 for correct, 0 for incorrect) evaluating whether the final answer appears in `\boxed{}` format. Ensures simplicity and objectivity.
- **Cosine Reward:** Augments accuracy reward by scaling it based on response length using a cosine schedule. Shorter correct solutions receive higher rewards; longer incorrect solutions are penalized less severely, incentivizing concise yet accurate reasoning and stabilizing completion length.
- **Format Reward:** Enforces structural clarity by requiring the model to encapsulate its reasoning within `<think>` and `</think>` tags, awarding a positive score for compliance.

### Three Experiments

**Experiment 1 — Impact of High-Quality Data:**
- Data: open-s1 (18,615 samples); max completion length: 4,096 tokens
- Rewards: accuracy + format
- Results: AMC23 improved from 63% to 70%, MATH-500 from 83% to 84% within 50–100 steps. After 200 steps, accuracy degraded significantly (AMC23 dropped below 60%, MATH-500 to 80%). Completion lengths fluctuated near 4,000 tokens then decreased to ~3,000 before rising again post-200 steps, accompanied by unreadable content and non-English outputs. KL divergence spiked, indicating reward misalignment.
- **Insight 1:** Small LLMs can achieve rapid reasoning improvements with limited high-quality data within 50–100 steps, but performance degrades with prolonged training under strict length constraints.

**Experiment 2 — Balancing Easy and Hard Problems:**
- Data: 7,000-sample mixed dataset (3,000 open-s1 + 3,000 open-deepscaler + 1,000 easier problems); max completion length: 3,584 tokens
- Rewards: accuracy + format
- Results: Initial completion lengths dropped to ~2,800 tokens. AMC23 rose from 63% to 80%, MATH-500 from 83% to 85% within 50–100 steps — a significant improvement over Experiment 1. After ~150–200 steps (~4,000 local steps), performance declined and KL divergence became unstable, with mixed-language outputs reemerging.
- **Insight 2:** Incorporating a mix of easy and hard problems under reduced length constraints enhances early performance and stabilizes reasoning behavior, though long-term stability remains elusive.

**Experiment 3 — Controlling Length with Cosine Reward:**
- Data: Same 7,000-sample dataset as Experiment 2; max completion length: 3,584 tokens
- Rewards: cosine reward (replacing accuracy reward) + format reward. System prompt added: "Reply in English only, do not use other languages."
- Results: Completion lengths stabilized between 1,000–3,500 tokens (a marked improvement). AMC23 improved modestly to 72.5%, MATH-500 to 84.4% — below Experiment 2's peak but more consistent. Mixed-language content persisted after 200 steps, reflecting the multilingual nature of `DeepSeek-R1-Distill-Qwen-1.5B`.
- **Insight 3:** Cosine rewards stabilize completion lengths and improve training consistency, but extending length limits is necessary for extremely hard tasks, particularly with multilingual base models.

### Experimental Setup

- **Base Model:** `DeepSeek-R1-Distill-Qwen-1.5B` — a 1.5B-parameter model distilled from larger architectures, chosen for its balance of efficiency and reasoning potential. SFT phase bypassed entirely.
- **Hardware:** 4× NVIDIA A40 GPUs (48 GB VRAM each); training restricted to 1 epoch within a 24-hour window
- **Training Framework:** Adapted from open-r1 (Face 2025), an open-source reproduction of DeepSeek-R1 by the HuggingFace team
- **Key Hyperparameters:** 6 outputs sampled per step, max 500 global steps, learning rate 1e-6 (cosine schedule with min LR 0.1), batch size 6 per device, max prompt length 512 tokens
- **Evaluation Metric:** Zero-shot pass@1 (proportion of problems correctly solved on the first attempt without prior examples); final answers required in `\boxed{}` format
- **Benchmark Datasets:**
  - AIME24: 30 problems (2024 American Invitational Mathematics Examination)
  - MATH-500: 500 problems (Lightman et al. 2023b; Hendrycks et al. 2021)
  - AMC23: 40 problems (2023 American Mathematics Competition)
  - Minerva: 272 undergraduate-level problems across physics, biology, chemistry, economics
  - OlympiadBench: 675 Olympiad-level problems in mathematics and physics
- **Baselines:** Llama-3.1-70B-Instruct, o1-preview, Qwen-2.5-Math-7B-Instruct, rStar-Math-7B, Eurus-2-7B-PRIME, Qwen2.5-7B-SimpleRL, DeepSeek-R1-Distill-Qwen-1.5B, DeepScaleR-1.5B-Preview, Still-3-1.5B-Preview

### Key Limitations

- Training constrained to 500 global steps (vs. a potential 1,500 for one epoch), preventing full observation of long-term behavior.
- Max completion length of 4,096 tokens proved insufficient for extremely hard problems in open-s1, forcing premature truncation of reasoning chains.
- Multilingual base model introduced language drift after 150–200 steps despite English-only prompting.
- Evaluation focused exclusively on mathematical reasoning; generalizability to scientific reasoning or coding remains unexplored.
