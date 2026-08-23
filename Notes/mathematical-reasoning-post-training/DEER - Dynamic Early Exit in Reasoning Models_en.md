# DEER - Dynamic Early Exit in Reasoning Models

## Topic
Dynamic early exit reasoning

## Background
Large Reasoning Models (LRMs) such as DeepSeek-R1 and GPT-O1 rely on test-time scaling, generating extended Chain-of-Thought (CoT) sequences to solve complex tasks. However, overly long CoTs not only reduce inference efficiency but also risk accuracy degradation by introducing redundant reasoning steps that derail the model from correct paths. Empirical analysis reveals that approximately 75% of samples contain a "pearl reasoning" point — a critical juncture where the accumulated reasoning information becomes sufficient for a correct answer before the full CoT is exhausted.

## Limitations and Research Questions
- **Limitation 1:** Existing LRMs are not trained to dynamically adjust reasoning length during inference; their Supervised Fine-Tuning and Reinforcement Learning stages overlook this capability, leading to systematic overthinking with verbose and unnecessary reasoning steps.
- **Limitation 2:** Existing efficient reasoning methods (e.g., TCC, CoD, NoThinking, Dynasor-CoT) either fail to generalize to complex tasks, sacrifice accuracy for efficiency, or rely on fixed heuristic early-exit strategies that cannot adapt to the optimal exit position for each individual problem.
- **Problem:** How can an LRM dynamically identify the pearl reasoning point during inference — without any additional training — so that CoT generation can be terminated early when the model has sufficient confidence in a trial answer, simultaneously improving both efficiency and accuracy?

## Contributions
- Proposes **DEER** (Dynamic Early Exit in Reasoning), a training-free, plug-and-play method that seamlessly integrates into existing o1-like LRMs.
- Identifies reasoning transition points via **Action Transition Point (ATP)** monitoring using either linguistic markers (e.g., "Wait") or entropy-based detection as candidate early-exit positions.
- Introduces **DEER-PRo** (Parallel and Robust variant), which performs parallel answer inductions at early-exit candidates and uses MAD (Mean Absolute Deviation)-calibrated confidence scores to substantially reduce sensitivity to answer-inducing prompt phrasing.
- Integrates a **Branch-Parallel Decoding** acceleration strategy that linearizes multi-branch parallel generation with a specialized causal attention mask and confidence-based KV cache pruning, minimizing the latency overhead of answer induction.
- Demonstrates consistent improvements across 10 reasoning benchmarks (GSM8K, MATH-500, AMC, GPQA, AIME, LiveCodeBench, etc.) on 11 models ranging from 1.5B to 671B parameters, reducing CoT length by an average of 19.1%–80.1% while improving accuracy by 0.3%–5.0%.

## Methodology
- **Framework Overview:** DEER comprises three core modules — Reasoning Transition Monitor, Answer Inducer, and Confidence Evaluator — which jointly determine whether to exit early at a given reasoning transition point.
- **Reasoning Transition Monitor:** Detects Action Transition Points (ATPs) as candidate early-exit positions. Two strategies are supported: (i) linguistic marker-based detection, which identifies keywords such as "Wait" and "Alternatively" that LRMs naturally use to demarcate reasoning steps; (ii) entropy-based detection, which computes the entropy H(p(·|x<t)) of the first token in each reasoning step — high-entropy positions indicate deliberation between multiple reasoning paths and are flagged as early-exit candidates.
- **Answer Inducer:** When an ATP is detected, DEER replaces subsequent content with "final answer" tokens (including \boxed{} delimiters) to prompt the model to immediately generate a trial answer: A = LRM(P, T, I), where P is the input prompt, T the generated thoughts, and I the answer inducer prompt.
- **Confidence Evaluator:** Computes the overall confidence C as the geometric mean of the maximum predicted probability for each token in the trial answer. If C > λ (threshold set to 0.95), the model is considered to have reached pearl reasoning; DEER stops further reasoning and outputs the conclusion. Otherwise, answer induction is revoked and reasoning continues on the original path.
- **DEER-PRo:** Performs N parallel answer inductions at each early-exit candidate using varied prompts, then computes a calibrated confidence score C_cali = C_avg − α · C_MAD. The MAD penalty suppresses overestimated confidence caused by prompt noise, effectively decoupling early-exit decisions from the model's intrinsic sensitivity to prompt phrasing.
- **Branch-Parallel Decoding:** Linearizes multi-branch answer induction into a single sequence for parallel generation using a specialized causal attention mask, combined with dynamic KV cache management based on confidence-based pruning. This creates temporal overlap between trial answer evaluation and ongoing reasoning-chain generation, reducing end-to-end latency overhead.
- **Experimental Setup:** Evaluated on DeepSeek-R1-Distill-Qwen series (1.5B/7B/14B/32B), Qwen3 series (1.7B/4B/8B/14B/32B), and QwQ-32B. Metrics: Accuracy (Acc), Token Number (Tok), and Compression Rate (CR). Baselines include Vanilla CoT, TCC, CoD, NoThinking, Dynasor-CoT, and SEAL.
