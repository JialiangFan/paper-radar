# ThinkPrune - Pruning Long CoT via RL (English)

## Topic
RL-based CoT length pruning

## Background
Large language models (LLMs) trained with reinforcement learning (RL) for inference-time scaling — such as DeepSeek-R1 and OpenAI o1 — have developed strong long chain-of-thought (CoT) reasoning abilities, achieving impressive performance on math and coding benchmarks. However, these long-CoT LLMs frequently produce inefficient and redundant thinking steps; for example, DeepSeek-R1-Distill-Qwen-1.5B averages over 15,000 tokens on MATH500, even though many problems could be solved in under 1,000 tokens. Existing approaches to limit generation length primarily rely on budget-forcing, which forces early exit at a token limit, but this does not teach the model to consolidate its reasoning and leads to substantial performance drops under tight budgets.

## Existing Limitations and Research Questions
- **Limitation:** Budget-forcing methods (e.g., S1) truncate the reasoning process when the token budget is exhausted and force an immediate answer output. Because the model is not fine-tuned to compress its reasoning, it wastes tokens on problem re-reading and cannot complete a second reasoning round within the budget, resulting in a sub-optimal length-performance tradeoff and sharp accuracy drops at low budgets.
- **Problem:** Can an LLM with long CoT be fine-tuned to actively prune its thinking length while minimizing performance loss? What is the resulting length-performance tradeoff? What reasoning steps or words are most likely to be pruned?

## Contributions
- Proposes ThinkPrune, a simple and effective RL-based CoT length pruning method that requires no reward function modification — it adds only a length clipping constraint during RL training to encourage length reduction.
- Introduces an iterative length pruning strategy that conducts multiple rounds of RL training with progressively tighter token limits, better preserving model performance compared to one-shot pruning.
- For DeepSeek-R1-Distill-Qwen-1.5B, reduces average generation length from 10,355 to 3,574 tokens with no average accuracy loss (slight improvement on some benchmarks); on AIME, halves reasoning length with only a 2% performance drop.
- Provides a detailed analysis of reasoning behavior change: after pruning, models reduce hesitation and self-correction steps ("Wait", "But wait", "Alternatively") while preserving core computation steps ("Therefore", "let me compute"), and reasoning trace perplexity remains nearly unchanged.

## Methodology
- **RL with Length Clipping:** ThinkPrune adopts the same GRPO training scheme as DeepSeek-R1, with one modification: before reward computation, the model output is clipped to a hard token limit L. If a correct answer cannot be extracted from the clipped output, the reward is 0. This forces the model to produce complete reasoning and answers within L tokens. A system prompt explicitly states the token limit during training.
- **Iterative Length Pruning:** Given a target length L*, a schedule L1 > L2 > ... > L* is defined. At each iteration t, RL training continues from the best checkpoint of the previous iteration with the tightened limit Lt. The stopping criterion per round is: among checkpoints with at most a 10% relative accuracy drop on AIME22/23 validation, select the one with the shortest average output length as the starting point for the next round.
- **Experiment Setup:** Training data consists of 2,470 historical AIME-AMC problems. Backbone models: DeepSeek-R1-Distill-Qwen-1.5B (unsaturated), DeepScaleR-1.5B-Preview (saturated), QwQ-32B (saturated). Evaluation benchmarks: MATH-500, AIME24, AMC23, OlympiadBench. Training uses the Verl RL framework with batch size 128 and 16 rollouts per question.
- **Reasoning Behavior Analysis:** Keyword frequency analysis tracks phrases signaling hesitation/self-correction (e.g., "Wait", "But wait", "Alternatively", "double-check") vs. core reasoning (e.g., "Therefore", "let me compute"). GPT-4o is used to segment reasoning traces into 9 high-level problem-solving phases (e.g., "Understanding the Problem", "Applying Known Theorems/Properties", "Reassess and Verify Local Steps") to quantify how time allocation across phases shifts after pruning. Reasoning readability is measured via perplexity on Math-500 using Qwen2.5-Math-7B.
