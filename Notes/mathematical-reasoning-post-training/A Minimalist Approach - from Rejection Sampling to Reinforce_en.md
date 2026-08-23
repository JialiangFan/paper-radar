# A Minimalist Approach - from Rejection Sampling to Reinforce

## Topic
RL Sample Selection for LLMs

## Background
Reinforcement learning has become the prevailing approach for fine-tuning LLMs on complex reasoning tasks. GRPO gained prominence through its role in training DeepSeek-R1, yet the sources of its effectiveness remain poorly understood. Meanwhile, RAFT (rejection sampling fine-tuning), one of the simplest baselines, has been consistently underestimated. This work revisits GRPO from a Reinforce-like algorithm perspective and systematically analyzes its core components.

## Limitations and Research Questions
- **Limitation:** The algorithmic details of GRPO remain largely undocumented, and it is unclear whether its performance gain over vanilla Reinforce stems from reward normalization or from its handling of negative samples. The community broadly assumes that RL methods leveraging negative feedback significantly outperform SFT-like approaches that use only positive samples, but rigorous experimental validation is lacking.
- **Problem:** Does GRPO's core advantage arise from reward normalization? What role do negative samples play in on-policy RL training? Can a simpler yet equally effective policy gradient variant be designed?

## Contributions
- Re-evaluated RAFT as a baseline, showing surprisingly competitive performance against GRPO on Math500, Minerva Math, and Olympiad Bench (52.3% vs 56.3% average accuracy on Qwen2.5-Math-7B), with faster early-stage convergence. Proposed RAFT++, incorporating importance sampling and clipping, which further closes the gap to 56.1%.
- Through systematic ablations, revealed that GRPO's primary advantage stems not from reward normalization but from implicitly filtering out prompts where all sampled responses are incorrect. Training on such all-wrong prompts produces high-variance misleading gradients that significantly harm performance.
- Proposed Reinforce-Rej, a minimal policy gradient extension that filters out both entirely correct and entirely incorrect prompts. It achieves comparable final performance to GRPO (56.4% vs 56.3% on Qwen2.5-Math-7B) while demonstrating superior KL efficiency and entropy stability.
- Identified that training exclusively on positive samples causes rapid policy entropy collapse and distributional collapse, limiting exploration and explaining why RAFT++ converges faster initially but is eventually surpassed by GRPO.

## Methodology
- **Experimental framework:** Implemented on the verl framework using Numina-Math (~860k math problems) as the training set. Experiments conducted on Qwen2.5-Math-7B-base and LLaMA-3.2-3B-instruct. Evaluation metric is average@16 accuracy (temperature 1.0, max 4096 tokens).
- **Algorithm comparison:** Unified comparison of RAFT, RAFT++, vanilla Reinforce, GRPO, PPO, Iterative DPO, and Reinforce-Rej. RAFT performs log-likelihood fine-tuning on positive samples only; RAFT++ adds importance sampling ratios and clipping on top of RAFT; GRPO normalizes rewards by mean/std within each prompt to compute advantages.
- **Ablation design:** Incrementally added components to vanilla Reinforce — Mean Zero (subtract per-prompt mean), Remove all correct, Remove all wrong, Remove both, Remove both + Normalize Std — to isolate individual contributions. Results show "Remove all wrong" yields the largest performance gain, while normalization contributes minimally.
- **Reinforce-Rej definition:** Equivalent to "Reinforce + Remove both," filtering out prompts where all sampled responses are either entirely correct or entirely incorrect during on-policy training. Policy gradients are computed only on prompts containing a mixture of positive and negative responses. The method requires no reward normalization, is simple to implement, and exhibits more stable KL divergence and entropy dynamics.

> **Title:** A Minimalist Approach to LLM Reasoning: from Rejection Sampling to Reinforce
> **Authors:** Wei Xiong, Jiarui Yao, Yuhui Xu, Bo Pang, Lei Wang, Doyen Sahoo, Junnan Li, Nan Jiang, Tong Zhang, Caiming Xiong, Hanze Dong
> **Venue:** arXiv:2504.11343
> **Year:** 2025
> **Affiliations:** Salesforce AI Research, UIUC