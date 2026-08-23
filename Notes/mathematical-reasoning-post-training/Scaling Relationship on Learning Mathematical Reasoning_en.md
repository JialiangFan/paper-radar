# Scaling Relationship on Learning Mathematical Reasoning

## Topic
Scaling RFT for Math Reasoning

## Background
Large language models (LLMs) have demonstrated considerable mathematical reasoning abilities, yet the scaling relationship governing these abilities with respect to LLM capacity remains under-explored. While scaling laws for pre-training are well studied, the interplay among pre-training loss, supervised data amount, and augmented data amount in shaping a supervised LLM's reasoning performance has not been systematically investigated. This paper conducts a comprehensive empirical study on the LLaMA and LLaMA2 model families using the GSM8K benchmark.

## Limitations & Research Problem
- **Limitation:** Existing approaches rely heavily on in-context learning (ICL) or multiple-inference strategies (e.g., majority voting, verifiers) to boost reasoning performance, which are computationally expensive and impractical for online deployment. The scaling behavior of supervised LLMs for mathematical reasoning lacks systematic characterization.
- **Problem:** How do pre-training loss, supervised data scale, and augmented reasoning path quantity jointly influence mathematical reasoning performance? How can training data be effectively scaled without human annotation to improve reasoning ability?

## Contributions
- Demonstrated that pre-training loss is a more stable performance indicator for mathematical reasoning than model parameter count, exhibiting an approximately negative linear correlation with SFT/ICL accuracy within a given interval.
- Revealed a log-linear relationship between SFT performance and supervised data amount, with diminishing gains for stronger pre-trained models.
- Proposed Rejection Sampling Fine-Tuning (RFT), which leverages SFT models to self-sample correct chain-of-thought reasoning paths as augmented fine-tuning data without human annotation.
- Identified distinct reasoning path count as the key factor driving RFT performance, and introduced a deduplication and diversity selection algorithm based on Levenshtein distance to improve data quality.
- Proposed cross-model aggregation of rejection sampling data (RFT-U13B/U33B), boosting LLaMA-7B accuracy on GSM8K from 35.9% (SFT) to 49.3%.

## Methodology
- **Experimental setup:** Experiments conducted on LLaMA (7B/13B/33B/65B) and LLaMA2 (7B/13B/70B) with the GSM8K dataset; evaluation metrics are maj1@1 (greedy accuracy) and maj1@100 (majority voting over 100 samples).
- **Pre-training loss analysis:** Compared pre-training losses and SFT/ICL accuracies across GPT-3, LLaMA, LLaMA2, and GPT-4, verifying an approximately negative linear correlation within a given loss interval.
- **SFT data scaling:** Fine-tuned models on {1, 1/2, 1/4, 1/8, 1/16, 1/32} fractions of the GSM8K training set to characterize log-linear scaling behavior.
- **Rejection Sampling Fine-Tuning (RFT):** For each training question, sampled k=100 candidate reasoning paths from the SFT model at temperature 0.7; filtered correct paths via answer verification; deduplicated using equation lists and selected the most diverse paths via Levenshtein distance.
- **Cross-model aggregation:** Combined rejection sampling outputs from multiple SFT models of different sizes (e.g., U13B aggregates results from 7B, 13B, 7B-2, 13B-2), applied the deduplication algorithm, and used the merged dataset for fine-tuning to maximize reasoning path diversity.
- **Computational cost analysis:** Estimated FLOPs for pre-training, SFT, RFT inference, and RFT training, showing that SFT and RFT costs are negligible compared to pre-training.

> **Title:** Scaling Relationship on Learning Mathematical Reasoning with Large Language Models
> **Authors:** Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Keming Lu, Chuanqi Tan, Chang Zhou, Jingren Zhou
> **Venue:** arXiv:2308.01825
> **Year:** 2023
> **Affiliations:** Alibaba DAMO Academy