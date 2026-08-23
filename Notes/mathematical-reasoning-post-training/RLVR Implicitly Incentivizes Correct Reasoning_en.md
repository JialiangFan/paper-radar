# RLVR Implicitly Incentivizes Correct Reasoning

## Topic
RLVR Incentivizes Correct LLM Reasoning

## Background
The success of DeepSeek-R1 has sparked significant interest in Reinforcement Learning with Verifiable Rewards (RLVR), a paradigm where LLMs generate chain-of-thought (CoT) reasoning and receive binary feedback based solely on answer correctness via GRPO. A prominent hypothesis suggests that all correct reasoning paths already exist in the base model, and RLVR merely improves sampling efficiency rather than extending reasoning capacity. This paper systematically addresses this debate and demonstrates that RLVR genuinely incentivizes correct reasoning in base LLMs.

## Limitations and Research Questions
- **Limitation:** Prior studies observed that post-RLVR models improve Pass@1 but fail to surpass the base model on Pass@K for large K, concluding that RLVR does not expand reasoning capacity. However, Pass@K is unreliable for math reasoning because base LLMs can produce incorrect CoTs that coincidentally arrive at correct answers through spurious guesses, inflating the metric.
- **Problem:** Should the hypothesis that RLVR only improves sampling efficiency be accepted as a fundamental limitation, or should conflicting empirical findings be re-examined? Can RLVR be shown, both theoretically and empirically, to genuinely extend the reasoning capability boundary of base LLMs?

## Contributions
- Introduced CoT-Pass@K, a metric that evaluates both final answer and intermediate reasoning correctness, revealing that RLVR extends the reasoning capability boundary for both math and code tasks.
- Established a theoretical framework (Theorem 1) proving that under a Logic Prior assumption, the GRPO gradient implicitly increases the probability of generating correct CoTs and decreases that of incorrect CoTs, even when rewards are based solely on answer correctness.
- Analyzed RLVR training dynamics, showing that correct reasoning is incentivized from early training stages, with P(CC|CA) steadily improving and generalizing to unseen test sets.
- Validated through SFT experiments that CoT quality generated during RLVR progressively improves, and SFT on RLVR-produced CoT data can nearly replicate the generalization performance of the post-RLVR model.

## Methodology
- **CoT-Pass@K metric design:** Employed an LLM-as-a-CoT-Judge paradigm using DeepSeek-R1-0528-Qwen3-8B as verifier, conducting multiple independent verifications per CoT with three aggregation strategies (any-correct, all-correct, majority-correct) to mitigate false positives and false negatives.
- **Theoretical analysis:** Introduced a Logic Prior assumption stating that correct CoTs lead to correct answers with higher probability than incorrect CoTs (alpha > beta). Under this assumption, proved that the expected GRPO advantage is positive for correct CoTs and negative for incorrect CoTs, causing the policy gradient to monotonically increase the generation probability of correct CoTs.
- **Empirical evaluation:** Reproduced GRPO training via DAPO (Qwen2.5-32B base, 17k math training set) and evaluated Pass@K and CoT-Pass@K on AIME 2024/2025, MATH-500, AMC23, Minerva, and multiple LiveCodeBench versions for code reasoning.
- **Training dynamics analysis:** Tracked the evolution of P(CA) and P(CC|CA) throughout training, confirming that correct reasoning is incentivized from early stages and generalizes to held-out test sets.
- **CoT quality assessment:** Conducted SFT on the same base model using CoT data from different RLVR training stages, measuring post-SFT model performance on test sets (Pass@1 and CoT-Pass@K) as a proxy for CoT data quality.

> **Title:** Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs
> **Authors:** Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu, Yang Wang, Zhijian Xu, Xiao Liang, Junjie Li, Ziming Miao, Jiang Bian, Mao Yang
> **Venue:** arXiv:2506.14245
> **Year:** 2025
> **Affiliations:** Microsoft Research Asia, Peking University, CUHK, UCLA