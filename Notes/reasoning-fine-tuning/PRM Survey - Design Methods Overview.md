# Process Reward Models: Design Methods Overview

> Source: Survey paper (arXiv:2510.08049v2). One representative work per method. Papers from our collection highlighted with ==yellow==.

## PRM Design Methods

| Design Method                       | Category           | Representative               | Method Description                                                                                                              |
| ----------------------------------- | ------------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Pointwise Scoring**               | Discriminative PRM | PRM800K [1] (May 2023)       | Train a scorer on human-annotated step labels; output correctness probability per step via BCE/MSE loss                         |
| **Pairwise Preference**             | Discriminative PRM | PQM [2] (Oct 2024)           | Recast PRM as Q-value ranking; learn relative preferences between candidate steps via pairwise loss (analogous to DPO)          |
| **Generate-then-Judge**             | Generative PRM     | GenRM [3] (Aug 2024)         | First generate a verification/critique chain ("think"), then score based on it; reward = softmax over yes/no logits             |
| **Self-Training / Self-Rewarding**  | Generative PRM     | GRAM-R² [4] (Sep 2025)       | Self-train a generative reward model that evolves its own reasoning and reward logic without external labels                    |
| **Pseudo-labeling from Outcome**    | Implicit PRM       | AlphaMath [5] (Jul 2024)     | Derive step-level pseudo-rewards directly from outcome supervision via Monte Carlo rollouts, eliminating step annotations       |
| **Self-supervised Process Reward**  | Implicit PRM       | ==P2S [6] (Jan 2026)==       | Compute Path Faithfulness Reward per step via conditional probability of generating a gold-CoT suffix; no extra model needed    |
| **Ensemble / Reverse Verification** | Implicit PRM       | AURORA [7] (Feb 2025)        | Ensemble prompting + reverse verification to produce domain-agnostic self-supervised step rewards                               |
| **Process-level Credit Assignment** | PRM-guided RL      | ==ELPO [8] (Feb 2026)==      | Binary-search replay tree to locate the first unrecoverable error step; apply fine-grained credit only at that point            |
| **Intervention-based Supervision**  | PRM for Safety     | ==IPO [9] (ICLR 2026)==      | Define CSR (Continuation Safety Ratio) as step-level safety reward; replace compliance cues with safety triggers, train via DPO |
| **Graph-based Structure**           | Other Architecture | GraphPRM [10] (KDD 2025)     | Cast reasoning as a graph of steps; learn structured dependencies among nodes for reward prediction                             |
| **Retrieval-augmented**             | Other Architecture | RetrievalPRM [11] (Feb 2025) | Integrate external retrieval to ground reward predictions, improving cross-task generalization                                  |
| **Hierarchical / Multi-level**      | Other Architecture | HRM [12] (Mar 2025)          | Layered reward structures aligned with multi-level reasoning abstractions (step → subtask → task)                               |
| **Adaptive Granularity**            | Other Architecture | AdaptiveStep [13] (Feb 2025) | Dynamically adjust reasoning step granularity based on model confidence for sharper PRM judgments                               |

## References

[1] Lightman et al. (May 2023). PRM800K: Let's verify step by step. ICLR 2024.
[2] Li and Li (Oct 2024). PQM: Process reward model with Q-value rankings. arXiv:2410.11287.
[3] Zhang et al. (Aug 2024). GenRM: Generative verifiers — reward modeling as next-token prediction. arXiv:2408.15240.
[4] Wang et al. (Sep 2025). GRAM-R²: Self-training generative foundation reward models for reasoning. arXiv:2509.02492.
[5] Chen et al. (Jul 2024). AlphaMath: Almost zero process supervision without process. NeurIPS 2024.
[6] Zhong et al. (Jan 2026). P2S: Probabilistic Process Supervision for General-Domain Reasoning QA. arXiv:2601.20649.
[7] Tan et al. (Feb 2025). AURORA: Automated training framework of universal process reward models. arXiv:2502.11520.
[8] Liang et al. (Feb 2026). ELPO: Error-Localized Policy Optimization for Tool-Integrated LLM Reasoning. arXiv:2602.09598.
[9] Zhang et al. (ICLR 2026). IPO: Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention.
[10] Peng et al. (KDD 2025). GraphPRM: Rewarding graph reasoning process makes LLMs more generalized reasoners.
[11] Zhu et al. (Feb 2025). RetrievalPRM: Retrieval-augmented process reward model for generalizable mathematical reasoning. arXiv:2502.14361.
[12] Wang et al. (Mar 2025). HRM: Towards hierarchical multi-step reward models. arXiv:2503.13551.
[13] Liu et al. (Feb 2025). AdaptiveStep: Automatically dividing reasoning step through model confidence. arXiv:2502.13943.

---

## PRM for Agents

- **ArXiv**: [2502.10325](https://arxiv.org/abs/2502.10325) (Feb 2025)

将 PRM 从 reasoning（数学/代码）扩展到 **agent 场景**（工具调用、网页操作、API 交互）。Agent PRM 需要处理环境状态变化、工具调用副作用、多步交互中的 credit assignment。与 step-level RL 方法（GiGPO, SALT）天然互补。




