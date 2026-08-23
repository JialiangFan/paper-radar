# Improve Mathematical Reasoning by Automated Process Supervision

## Topic
Automated Process Reward Model Training

## Background
Process supervision, which provides intermediate reward signals at each reasoning step, has been shown to outperform Outcome Reward Models (ORMs) that only evaluate final answers. Training Process Reward Models (PRMs) requires large-scale step-level process supervision data, but existing methods rely on costly human annotation (e.g., PRM800K) or inefficient brute-force Monte Carlo estimation. Google DeepMind proposes OmegaPRM to address this data collection bottleneck in a fully automated and efficient manner.

## Limitations and Research Questions
- **Limitation:** Existing process supervision data collection methods either depend on human annotation (expensive and unscalable) or per-step Monte Carlo rollouts with O(kM) complexity (inefficient), while also suffering from imbalanced positive/negative samples and uncontrolled data quality.
- **Problem:** How to efficiently generate large-scale, high-quality process supervision annotations without human intervention, in order to train superior PRMs that enhance LLM mathematical reasoning?

## Contributions
- Propose OmegaPRM, a divide-and-conquer Monte Carlo Tree Search (MCTS) algorithm for fully automated process supervision data generation.
- Reduce the complexity of locating the first error step from O(kM) to O(k log M) via binary search, and achieve 75x efficiency improvement by reusing rollouts through the MCTS tree structure.
- Automatically collect over 1.5 million process supervision annotations without any human involvement, surpassing existing datasets in both scale and quality.
- Combined with weighted self-consistency decoding, improve Gemini Pro accuracy on MATH500 from 51% to 69.4% and on GSM8K from 86.4% to 93.6%; boost Gemma2 27B on MATH500 from 42.3% to 58.2%.

## Methodology
- **Process Supervision Framework:** PRM predicts correctness of each step x_t as p_t = PRM([q, x_{1:t-1}], x_t), providing finer-grained feedback than ORM.
- **Monte Carlo Estimation with Binary Search:** Perform binary search on erroneous solutions by executing k rollouts at midpoints and comparing with golden answers, locating the first error in O(k log M) complexity.
- **OmegaPRM (MCTS):** Build a state-action tree where each node stores visit count N(s), Monte Carlo estimate MC(s), and rollout value function Q(s,r). The algorithm operates in three phases:
  - **Select:** Choose the most valuable rollout from the candidate pool, prioritizing "supposed-to-be-correct wrong-answer" samples (MC(s) close to 1 but with incorrect final answer), using a PUCT variant to balance exploration and exploitation.
  - **Binary Search:** Perform binary search on the selected rollout to locate the first error, adding intermediate nodes to the tree.
  - **Maintain:** Update tree statistics including N(s), MC(s), and Q(s,r).
- **PRM Training:** Train with binary cross-entropy loss using pointwise soft labels (MC estimates as labels), which outperforms hard label and pairwise methods (70.1% vs 63.3% vs 64.2% accuracy).
- **Weighted Self-Consistency:** Combine PRM scores with majority voting for inference-time solution reranking.

> **Title:** Improve Mathematical Reasoning in Language Models by Automated Process Supervision
> **Authors:** Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat Phatale, Harsh Lara, Yunxuan Li, Lei Shu, Yun Zhu, Lei Meng, Jiao Sun, Abhinav Rastogi
> **Venue:** arXiv:2406.06592
> **Year:** 2024
> **Affiliations:** Google DeepMind, Google