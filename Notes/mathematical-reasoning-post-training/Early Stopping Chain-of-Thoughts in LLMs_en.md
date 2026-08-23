# Early Stopping Chain-of-Thoughts in LLMs

## Topic
Early stopping of chain-of-thought (CoT) reasoning at inference time

## Background
Reasoning LLMs such as OpenAI o-series, DeepSeek R1, and QwQ achieve strong performance on complex tasks by generating long chain-of-thought traces, but this verbosity incurs substantial inference costs. Studies show these models frequently overthink—continuing to generate redundant steps after already reaching the correct answer. Efficient reasoning research therefore seeks methods that preserve CoT accuracy while minimizing unnecessary token generation.

## Limitations and Research Question
- **Limitation:** Existing output-side efficient reasoning approaches (e.g., Speculative Rejection, Early Stop Self-Consistency) require parallel decoding or auxiliary reward models, adding system complexity and preventing application to single reasoning trajectories without extra supervision.
- **Problem:** When can a reasoning trajectory be safely stopped without harming output quality? Specifically, can answer convergence be detected on a single trajectory with no additional models or retraining?

## Contributions
- Proposes **ES-CoT** (Early-Stop CoT), the first inference-time method that halts CoT generation based on a run-jump test on a single trajectory, requiring no extra reward model, parallel decoding, or retraining.
- Provides both empirical and theoretical support: step answers monotonically converge toward the final answer, and run lengths (consecutive identical step answers) exhibit a statistically significant jump at convergence.
- On five reasoning benchmarks (AIME24, GPQA, MATH500, Minerva, OlympiadBench) across three LLMs (QwQ-32B, Qwen3-8B, DeepSeek-R1-Distill-Llama-8B), ES-CoT reduces inference token usage by approximately **41%** on average while maintaining accuracy comparable to standard CoT.
- ES-CoT integrates seamlessly with self-consistency prompting (ES-CoT+SC), delivering further accuracy gains while keeping token costs near ES-CoT alone levels.

## Methodology
- **Step answer:** At each reasoning step $t$, the prompt "The final answer is" is appended to elicit the model's current best answer $x_t$, captured without interrupting the full generation.
- **Run sequence:** Consecutive steps with the same answer are grouped into a run; the sequence of run lengths is tracked as $R = \langle r_1, r_2, \ldots \rangle$.
- **Run-jump test (core stopping criterion):** A difference sequence $D = \langle d_1, \ldots, d_{n-1} \rangle$ with $d_i = r_{i+1} - r_i$ is maintained. Generation is terminated when the latest difference $d_{n-1} \geq d_{\min}$ and a one-sided t-test confirms $d_{n-1}$ is significantly larger than the prior differences $d_{1:n-2}$.
- **Hyperparameters:** Minimum run-length difference $d_{\min}$ (default 10, acts as a warmup to prevent premature stopping); t-test significance p-value (default 0.05). Sensitivity analysis shows results are robust across a wide range of both parameters, with $d_{\min}$ being the dominant factor governing the accuracy-efficiency trade-off.
- **Theoretical guarantees:** Under the assumption that the final answer is deterministic (Assumption 1) and that the step-answer probability increases monotonically with reasoning progress (Assumption 2), Theorem 1 bounds the ES-CoT error, showing it approaches 0 as the run-length jump grows large.
- **Integration with self-consistency:** ES-CoT is applied independently to each of multiple sampled trajectories; majority voting over the resulting answers yields ES-CoT+SC, which reduces tokens versus standard CoT+SC by 4–24% while matching or improving accuracy.
