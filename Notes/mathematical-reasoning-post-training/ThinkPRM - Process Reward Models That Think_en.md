# ThinkPRM - Process Reward Models That Think

## Topic
CoT-based process reward model

**Paper Info**
- Authors: Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng, Moontae Lee, Honglak Lee, Lu Wang
- Affiliations: University of Michigan, LG AI Research, University of Illinois Urbana-Champaign, Mila
- arXiv: 2504.16828v5, December 2025
- Code: https://github.com/mukhal/thinkprm

---

## Background

- Large language models (LLMs) increasingly rely on test-time scaling to improve reasoning performance by investing more compute at inference time.
- Process Reward Models (PRMs) are a key component of test-time scaling, scoring each step in a candidate solution to guide Best-of-N selection and verifier-guided beam search.
- Traditional discriminative PRMs treat verification as a classification task, directly outputting correct/incorrect scores for each step using a classification head.
- Early generative verification approaches (LLM-as-a-Judge, GenRM) treat verification as language generation, producing short chain-of-thought (CoT) rationales before a binary judgment.

---

## Limitations & Research Problem

**Limitations of discriminative PRMs:**
1. Training requires extensive step-level annotations — e.g., PRM800K contains ~712K step labels, which are expensive to obtain via human annotation or compute-intensive Monte Carlo rollouts.
2. They do not leverage the language model's generative capabilities, making training expensive and labor-intensive.
3. They use fixed compute at inference time and cannot dynamically scale with test-time compute budgets.

**Limitations of existing generative verification (LLM-as-a-Judge / GenRM):**
1. Highly sensitive to instruction wording — minor changes can shift F1 scores by 3–4 points.
2. Produce a large fraction of invalid judgments — outputs lacking an extractable label (e.g., \boxed{yes}/\boxed{no}); for R1-Qwen-1.5B this rate reaches 53.2%.
3. Prone to severe overthinking and infinite looping/repetition, causing verification chains to exceed token budgets without terminating.
4. GenRM is limited to short verification CoTs, fundamentally constraining its test-time scaling ability.
5. General-purpose LLMs frequently fail to identify reasoning errors, performing worse than specialized reward models as verifiers.

**Core research question:**
How can we build data-efficient PRMs that verify reasoning step-by-step through extended CoT generation, while supporting test-time compute scaling?

---

## Contributions

1. **ThinkPRM**: A generative process reward model that verifies every step in a solution by generating an extended verification chain-of-thought.
2. **Extreme data efficiency**: Trained on only ~1% of PRM800K step labels (~8K labels), yet significantly outperforms discriminative PRMs trained on the full dataset.
3. **Strong empirical results**:
   - Outperforms LLM-as-a-Judge and discriminative verifiers on ProcessBench, MATH-500, and AIME '24.
   - In out-of-domain evaluation on GPQA-Diamond and LiveCodeBench, surpasses discriminative verifiers trained on full PRM800K by 8% and 4.5% respectively.
   - Under the same token budget, scales verification compute more effectively than LLM-as-a-Judge, outperforming it by 7.2% on a ProcessBench subset.
4. **Strong generalization**: Despite training only on math data, ThinkPRM generalizes to scientific reasoning (GPQA-Physics) and code generation (LiveCodeBench).
5. **Two-dimensional scaling support**:
   - Parallel scaling: Sample K independent verification CoTs and average their scores.
   - Sequential scaling: Use a trigger phrase (e.g., "Let's verify again") to elicit self-correction of the initial verification.

---

## Methodology

### Core Idea
Treat verification as a generation task: given a problem and a multi-step solution, the model generates an extended chain-of-thought that critiques each reasoning step and outputs a \boxed{correct}/\boxed{incorrect} label for each step.

### Data Collection Pipeline (Rejection Sampling Finetuning)

**Step 1 — Sample verification chains:**
- Use QwQ-32B-Preview as the sampling model. For each problem-prefix pair in PRM800K, sample multiple verification CoTs.
- The prompt instructs the model to verify each step, provide a critique, and output \boxed{correct} or \boxed{incorrect}.

**Step 2 — Filter using process labels (key contribution):**
Retain chains satisfying all of:
- (i) The CoT contains an extractable step-level label for every step (correct format).
- (ii) The generated step judgments match the gold process labels from PRM800K.
- (iii) The CoT length is within the maximum token budget (to avoid overthinking).
- ~20% of initial samples pass all criteria. Final dataset: ~1K verification CoTs corresponding to ~8K step labels.
- Ablation shows process-based filtering substantially outperforms outcome-based filtering (retaining chains only if the final answer correctness matches).

**Training data statistics (1K dataset):**
- 486 correct solutions (48.6%), 514 incorrect (51.4%)
- Step labels: 7,474 correct (92.3%), 625 incorrect (7.7%)
- Average verification chain length: 1,037 tokens

### Training Details

**Models trained:**
- R1-Distill-Qwen-{1.5B, 7B, 14B}: full fine-tuning
- QwQ-32B-Preview: LoRA fine-tuning (rank=32, α=16)

**Training procedure:**
- Supervised fine-tuning on the filtered 1K verification CoTs.
- Training time: ~30 min for 1.5B, ~1.5 hrs for 14B models (single A100 80GB or RTX A6000 48GB GPU).
- Special tokens `<think>` and `</think>` delineate the verification reasoning process.

### Inference-Time Scoring

- The model generates up to 8,192 tokens of verification chain.
- The string "Is the solution correct?" is force-decoded, and the solution score is computed as P("yes") / (P("yes") + P("no")).
- For parallel scaling: average scores across K independent verification CoTs.
- For sequential scaling: a trigger phrase prompts the model to re-examine its verification (self-correction).

### Analysis of LLM-as-a-Judge Problems (RQ1)

Directly using off-the-shelf reasoning models as process verifiers (LLM-as-a-Judge) exhibits key failure modes:
- **High invalid output rate**: R1-Qwen-1.5B produces 53.2% invalid judgments (no extractable label).
- **Overthinking and infinite looping**: Accurate verification CoTs are typically short (<3K tokens); inaccurate ones show a heavy tail peaking sharply at 7K–8K tokens.
- **Instruction sensitivity**: Minor changes to prompt wording shift F1 by 3–4 points.

Fine-tuning on the 1K synthetic chains largely resolves these issues, substantially reducing invalid outputs and overthinking across all model sizes (with a 70+ F1 improvement for the 1.5B model).

### Main Experimental Results

**ProcessBench (verification accuracy):**
- ThinkPRM-14B achieves F1 of 87.3 on OlympiadBench and 85.7 on OmniMath, far exceeding LLM-as-a-Judge (72.8 / 67.8) using the same base model.
- ThinkPRM-14B is trained on ~100x fewer process labels than DiscPRM yet achieves higher verification F1.

**Best-of-N selection (MATH-500, AIME '24):**
- ThinkPRM-14B consistently outperforms or matches DiscPRM and LLM-as-a-Judge at all sampling budgets.

**Verifier-guided beam search (MATH-500):**
- ThinkPRM-1.5B (trained on 8K step labels) surpasses LLM-as-a-Judge, DiscPRM, and even off-the-shelf PRMs (RLHFFlow-Deepseek-PRM, MathShepherd-7B) trained on far more data.

**Out-of-domain generalization (GPQA-Physics, LiveCodeBench):**
- ThinkPRM-14B outperforms DiscPRM-14B by ~8% on GPQA-Physics and ~4.5% on LiveCodeBench under Best-of-N.
- Discriminative PRMs are fragile under domain shift; generative PRMs are more robust.

**Compute-matched comparison vs. self-consistency:**
- At low sampling budgets, Best-of-N with ThinkPRM performs comparably to self-consistency (majority vote).
- As compute budget increases, ThinkPRM has a clear advantage over self-consistency.

### Key Ablations

1. **Long CoT vs. Short CoT training**: Training on long verification CoTs outperforms training on compressed short CoTs by 20+ F1 points, confirming the value of extended reasoning for verification.
2. **Process-based vs. outcome-based filtering**: Process-level data filtering significantly outperforms filtering based only on final answer correctness, highlighting that step supervision is critical.
3. **Monte Carlo step labels**: ThinkPRM-1.5B trained with automatically generated step labels (Math-shepherd dataset via Monte Carlo rollouts) achieves performance comparable to training with manual labels, showing the pipeline is label-source agnostic.
4. **Generalization to long reasoning traces**: Although trained only on short solutions, ThinkPRM generalizes to verifying long CoTs with backtracking (e.g., Qwen3-1.7B thinking-mode outputs) by extracting and verifying individual steps embedded in long traces.

### Limitations

- **Overconfidence**: Generative PRM scores may cluster near extremes (close to 0 or 1), making calibrated probability estimation difficult.
- **Step label interference**: Autoregressive generation causes verification errors on early steps to propagate and influence judgments on later steps.
- **Additional inference overhead**: Generating verification CoTs introduces more compute than discriminative classification, though the authors argue the performance gains justify this cost.
