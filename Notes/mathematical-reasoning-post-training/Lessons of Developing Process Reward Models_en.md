# Lessons of Developing Process Reward Models

## Topic
Process Reward Model Development

## Background
Process Reward Models (PRMs) provide fine-grained process supervision for mathematical reasoning in LLMs by evaluating the correctness of intermediate reasoning steps. However, the development of effective PRMs faces significant challenges in data annotation and evaluation methodologies. This paper, from the Alibaba Qwen team, presents critical lessons learned through extensive experiments on PRM training and evaluation, and releases state-of-the-art open-source PRMs.

## Limitations and Research Questions
- **Limitation 1:** Monte Carlo (MC) estimation-based data synthesis relies on completion models to assess step correctness, but these models can generate correct answers from incorrect steps or incorrect answers from correct steps, introducing substantial noise. PRMs trained on MC-estimated data demonstrate significantly inferior performance and generalization compared to LLM-as-a-judge and human annotation methods.
- **Limitation 2:** Best-of-N (BoN) evaluation focuses solely on final answer correctness, creating a fundamental misalignment with the process verification objective of PRMs. Policy models frequently generate responses with correct answers but flawed reasoning processes, leading to inflated BoN scores.
- **Limitation 3:** Existing PRMs exhibit a significant proportion of minimum scores concentrated on the final answer step, indicating a degradation from process-oriented to outcome-oriented assessment, effectively functioning as ORMs rather than PRMs.
- **Problem:** How to construct higher-quality training data and design a more comprehensive evaluation framework for developing genuinely effective PRMs?

## Contributions
- Systematically identified critical deficiencies in MC estimation data synthesis: despite having the largest data volume, MC estimation yields the worst performance on ProcessBench error localization compared to LLM-as-a-judge and human annotation.
- Revealed three systematic biases in BoN evaluation: unreliable policy models causing BoN-PRM misalignment, limited process verification capability leading to inflated BoN scores, and optimization-driven process-to-outcome shift.
- Proposed a consensus filtering mechanism that integrates MC estimation with LLM-as-a-judge, retaining only samples where both methods agree on error step locations. This achieves significant performance gains using only approximately 40% of the data.
- Demonstrated that hard labels (with a threshold of 0) outperform soft labels, and that different data sources yield different optimal BoN scoring strategies (last score for MC estimation; product/minimum for LLM-as-a-judge and human annotation).
- Released Qwen2.5-Math-PRM-7B and Qwen2.5-Math-PRM-72B, which outperform existing open-source PRMs on both BoN evaluation and ProcessBench.

## Methodology
- **Data Expansion:** Collected approximately 500K queries and generated 6-8 responses per query using Qwen2-Math-Instruct and Qwen2.5-Math-Instruct series models. Responses were split into steps by `\n\n`, and each step was evaluated via 8 independent MC completions. Hard labels were applied with a threshold of 0 (a step is correct if any completion reaches the correct answer).
- **Consensus Filtering:** Employed Qwen2.5-Instruct-72B as an LLM-as-a-judge to verify each step of the reasoning process. Only samples where both LLM-as-a-judge and MC estimation agree on the error step location were retained, preserving approximately 40% of the data.
- **Model Training:** Initialized from Qwen2.5-Math-7B/72B-Instruct, replacing the language modeling head with a scalar-value head (two linear layers). Trained using cross-entropy loss on the last token of each step for binary classification.
- **Evaluation Framework:** Combined response-level Best-of-N (prm@8) evaluation with step-level ProcessBench error localization to avoid biases inherent in BoN-only evaluation, providing a comprehensive assessment of PRM process verification capability.

> **Title:** The Lessons of Developing Process Reward Models in Mathematical Reasoning
> **Authors:** Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen Zhang, Runji Lin, Bowen Yu, Dayiheng Liu, Jingren Zhou, Junyang Lin
> **Venue:** arXiv:2501.07301
> **Year:** 2025
> **Affiliations:** Qwen Team, Alibaba Group