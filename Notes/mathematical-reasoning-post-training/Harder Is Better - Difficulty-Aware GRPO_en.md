# Harder Is Better - Difficulty-Aware GRPO

## Topic
Difficulty-Aware Mathematical Reasoning RL

## Background
Reinforcement Learning with Verifiable Rewards (RLVR) has emerged as a leading paradigm for enhancing mathematical reasoning in LLMs, with Group Relative Policy Optimization (GRPO) being the most representative algorithm that estimates relative advantages across a group of responses to the same query. However, existing methods systematically neglect harder questions from both algorithmic and data perspectives, limiting the refinement of models' frontier capabilities. This paper introduces MathForge, a two-pronged framework that targets harder questions via a Difficulty-Aware Group Policy Optimization (DGPO) algorithm and a Multi-Aspect Question Reformulation (MQR) strategy.

## Limitations and Research Questions
- **Limitation 1 (Algorithmic):** GRPO's group relative advantage estimation (GRAE) introduces an implicit imbalance where the total update magnitude peaks at accuracy rate p=0.5 and is suppressed for both harder (p near 0) and easier (p near 1) questions. This prevents the model from adequately learning from challenging yet solvable questions that are most informative for targeted improvement.
- **Limitation 2 (Data):** Traditional data augmentation methods primarily rephrase questions to increase diversity without systematically raising difficulty. Approaches that generate entirely new question-answer pairs face quality assurance challenges, especially for competition-level problems.
- **Problem:** How to simultaneously prioritize harder questions from both algorithmic and data dimensions to push the boundaries of mathematical reasoning capabilities?

## Contributions
- Proposes DGPO with two key techniques: (1) Difficulty-Balanced Group Advantage Estimation (DGAE), which replaces standard deviation with mean absolute deviation (MAD) for advantage normalization, provably equalizing the total update magnitude to a constant G across all difficulty levels; (2) Difficulty-Aware Question-level Weighting (DQW), which assigns higher weights to harder questions within each batch via a softmax-temperature mechanism.
- Proposes Multi-Aspect Question Reformulation (MQR), a data augmentation strategy that reformulates questions across three aspects -- adding story background, introducing abstract terminology, and nesting sub-problems -- while strictly preserving the original gold answer.
- The two components form a synergistic loop: MQR expands the data difficulty frontier and DGPO efficiently learns from the augmented data. On Qwen2.5-Math-7B, MathForge achieves an average score of 42.17% across six benchmarks, a +4.56% gain over the GRPO baseline (37.61%).

## Methodology
- **DGAE:** Replaces the standard deviation denominator in GRPO's advantage function with MAD, yielding $\hat{A}_{\text{DG},i} = (r_i - \text{mean}) / \text{MAD}$. Theorem 2 proves that under DGAE, the total update magnitude for any single question equals the constant G, eliminating the implicit suppression of harder questions inherent in GRAE.
- **DQW:** Assigns a weight $\lambda_s = B_v \cdot \exp(D_s/T) / \sum \exp(D_s/T)$ to each valid query in the batch, where $D_s = -\text{mean}(\{r_{si}\})$ measures difficulty and T is a temperature hyperparameter (optimal at T=2.0). Higher difficulty yields higher weight, forming a "balance-then-reweight" two-step strategy.
- **MQR:** Uses a reformulator model (default: OpenAI o3; also effective with open-source models) to reformulate training questions along three aspects: (1) Background -- adds a story background unrelated to the core mathematical content; (2) Term -- invents a new abstract mathematical term to restate the question; (3) Sub-Problem -- converts a key numerical condition into an independent sub-problem. All reformulations must preserve the original answer.
- **MathForge Framework:** MQR expands the original dataset by 4x (original + three reformulation types), and DGPO performs RL training on this augmented data. Experiments span AIME24/25, AMC23, MATH500, Minerva, and Olympiad benchmarks, demonstrating generalization across model scales (1.5B--7B), compatibility with other policy optimization methods (GPG, DAPO, GSPO), and applicability to multimodal settings (GEOQA-8k).

> **Title:** Harder Is Better: Boosting Mathematical Reasoning via Difficulty-Aware GRPO and Multi-Aspect Question Reformulation
> **Authors:** Yanqi Dai, Yuxiang Ji, Xiao Zhang, Yong Wang, Xiangxiang Chu, Zhiwu Lu
> **Venue:** ICLR 2026 / arXiv:2601.20614
> **Year:** 2026
> **Affiliations:** Renmin University of China, Alibaba Group, Xiamen University, Dalian University of Technology