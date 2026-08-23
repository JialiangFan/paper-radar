# STaR: Bootstrapping Reasoning With Reasoning

## Topic
Self-Taught Reasoning via Bootstrapping

## Background
Generating explicit chain-of-thought rationales has been shown to substantially improve LLM performance on complex reasoning tasks such as arithmetic, commonsense QA, and math word problems. However, the two primary methods for inducing rationale generation face critical trade-offs: constructing large-scale rationale datasets requires expensive human annotation or restrictive template-based methods, while few-shot prompting avoids annotation costs but significantly underperforms models fine-tuned on full datasets to directly predict answers. This creates a need for scalable techniques that can bootstrap high-quality reasoning from minimal supervision.

## Limitations & Research Problem
- **Limitation:** Building rationale datasets demands costly manual annotation that does not scale across domains; template-based alternatives only work when general solutions are already known. Few-shot rationale prompting, while annotation-free, substantially underperforms models fine-tuned with direct answer prediction on large datasets, leaving a significant performance gap.
- **Problem:** How can a language model iteratively leverage its own reasoning capacity to generate and learn from high-quality rationales, starting from only a handful of few-shot examples, without requiring external verification of generated rationales?

## Contributions
- Proposes STaR (Self-Taught Reasoner), a bootstrapping mechanism that iteratively generates a large rationale dataset from a small number of few-shot examples, without requiring correctness verification of newly generated rationales.
- Introduces rationalization: for problems the model fails to solve, the correct answer is provided as a hint so the model can reason backward to generate a plausible rationale, breaking the learning bottleneck of pure rationale generation and accelerating the bootstrapping loop.
- Conducts systematic evaluation across arithmetic, CommonsenseQA, and GSM8K, demonstrating that STaR significantly outperforms direct fine-tuning baselines and that a 6B-parameter model achieves performance comparable to a 30x larger model under few-shot settings.
- Presents the first technique enabling a pre-trained LLM to iteratively improve itself by learning from its own generated reasoning.

## Methodology
- **Rationale Generation Bootstrapping:** Given a pretrained model M and a dataset with answer labels, prompt the model with a small set of few-shot rationale examples to generate a rationale and predicted answer for each problem. Filter to retain only rationales that lead to correct answers. Fine-tune the original base model M on this filtered dataset. Repeat the process with the newly fine-tuned model until performance plateaus.
- **Rationalization:** For problems where rationale generation yields incorrect answers, append the correct answer as a hint to the prompt and have the model generate a rationale conditioned on knowing the answer. These rationalized rationales (with the hint removed) are combined with the successfully generated rationales to form the full fine-tuning dataset, exposing the model to difficult problems it would otherwise never learn from.
- **Theoretical Connection:** STaR approximates an RL-style policy gradient objective where answer correctness serves as the reward signal. Greedy decoding approximates sampling, and filtering incorrect rationales approximates the REINFORCE gradient estimate. Rationalization acts as off-policy sampling from the hint-augmented distribution p(r|x,y), providing a more efficient search space for rationales.
- **Training Details:** Uses GPT-J (6B) as the base model. Each iteration retrains from the original pretrained checkpoint to avoid overfitting. Fine-tuning steps increase by 20% per outer-loop iteration, with a 100-step learning rate warmup.

> **Title:** STaR: Self-Taught Reasoner — Bootstrapping Reasoning With Reasoning
> **Authors:** Eric Zelikman, Yuhuai Wu, Jesse Mu, Noah D. Goodman
> **Venue:** arXiv:2203.14465
> **Year:** 2022
> **Affiliations:** Stanford University, Google Research