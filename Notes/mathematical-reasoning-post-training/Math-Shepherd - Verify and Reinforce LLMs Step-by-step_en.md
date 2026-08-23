# Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations

## Topic
Process Reward Model Auto-Annotation

## Background
Large language models (LLMs) continue to struggle with complex multi-step mathematical reasoning. Verification through reward models has emerged as a promising approach, where the Process Reward Model (PRM) evaluates each reasoning step individually and has been shown to outperform the Outcome Reward Model (ORM), which only scores the final solution. However, training effective PRMs has historically required expensive human-annotated process supervision data (e.g., the PRM800K dataset), creating a critical bottleneck for scalability and practical deployment.

## Limitations & Research Problem
- **Limitation:** Existing PRM training relies on costly human step-level annotations of reasoning correctness (Uesato et al., 2022; Lightman et al., 2023), which is difficult to scale, especially for complex mathematical reasoning tasks requiring advanced annotator expertise.
- **Problem:** How to automatically construct high-quality process supervision data for training effective PRMs without any human annotation?

## Contributions
- Proposed an automatic process annotation framework that generates step-level labels for mathematical reasoning tasks without human involvement.
- Validated Math-Shepherd in two application scenarios -- verification (Best-of-N reranking) and reinforcement learning (step-by-step PPO) -- achieving state-of-the-art performance among open-source models on GSM8K and MATH benchmarks.
- Conducted systematic analysis of key factors affecting PRM training quality (completer capability, data volume, model scale), providing insights for future research on automated process supervision.

## Methodology
- **Step quality definition:** Inspired by Monte Carlo Tree Search, the quality of a reasoning step is defined as its potential to deduce the correct final answer, grounding the evaluation in the ultimate objective of the reasoning process.
- **Automatic annotation pipeline (Completion + Estimation):** For each reasoning step $s_i$ in a given solution, a fine-tuned LLM serves as a "completer" to generate N subsequent reasoning paths from that step and obtain final answers. The step's quality label is then estimated by comparing decoded answers against the golden answer. Two estimation methods are provided: Hard Estimation (HE), which assigns a positive label if at least one completion reaches the correct answer, and Soft Estimation (SE), which computes the proportion of correct completions.
- **Verification application:** Employs a Best-of-N selection paradigm where PRM scores all steps of each candidate solution, takes the minimum score as the overall solution score, and selects the highest-scoring solution. A combined strategy with self-consistency voting is also explored.
- **Reinforcement learning application:** Math-Shepherd serves as the reward model for step-by-step PPO, providing reward signals at the end of each reasoning step rather than only at the response conclusion (as in conventional ORM-PPO), enabling finer-grained policy optimization.
- **Experimental setup:** Extensive experiments conducted across LLaMA2-7B/13B/70B, LLemma-7B/34B, Mistral-7B, and DeepSeek-67B on GSM8K and MATH datasets. Generators and completers are trained on MetaMATH data, with approximately 170k (GSM8K) and 270k (MATH) solutions sampled for constructing training data.

> **Title:** Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations
> **Authors:** Peiyi Wang, Lei Li, Zhihong Shao, R.X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, Zhifang Sui
> **Venue:** arXiv:2312.08935
> **Year:** 2024
> **Affiliations:** Peking University, DeepSeek-AI, University of Hong Kong, Tsinghua University