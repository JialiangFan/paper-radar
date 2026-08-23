# MCTS-DPO - Tree Search Boosts Reasoning via Preference Learning

## 主题 / Topic
MCTS preference learning reasoning

**Full Title**: Monte Carlo Tree Search Boosts Reasoning via Iterative Preference Learning
**Authors**: Yuxi Xie, Anirudh Goyal, Wenyue Zheng, Min-Yen Kan, Timothy Lillicrap, Kenji Kawaguchi, Michael Shieh
**Affiliations**: National University of Singapore; Google DeepMind
**arXiv**: 2405.00451v2 (June 2024)
**Code**: https://github.com/YuxiXie/MCTS-DPO

---

## Background

The alignment of Large Language Models (LLMs) relies heavily on preference learning. Two dominant paradigms exist:
1. **Reward-model-based RL (RLHF)**: Train a reward model on human preferences, then optimize the policy using PPO or similar RL algorithms.
2. **Direct Preference Optimization (DPO)**: Directly update the policy using preference pairs, bypassing a separate reward model.

Both paradigms typically operate in an offline setting, where preference data is collected once and held fixed during training. The success of AlphaZero demonstrated that Monte Carlo Tree Search (MCTS) can serve as an approximate policy improvement operator, iteratively refining the current policy into a stronger one. This paper is motivated by applying that principle to LLM reasoning.

---

## Limitations & Research Problem

**Limitations of existing approaches**:
- **Sparse instance-level supervision**: Conventional preference learning assigns a single preference label to an entire response, ignoring intermediate reasoning step quality and resulting in coarse training signals.
- **Distribution shift in offline DPO**: DPO requires preference data sampled from a distribution close to the current policy. When the sampling policy diverges too far from the current policy, offline DPO can fail with high probability (formalized in Theorem 3.1).
- **Reliance on external critics or reward models**: MCTS traditionally requires a learned value/reward function to evaluate rollouts. Training such a network adds cost and complexity.
- **Lack of automated process supervision**: Step-level supervision has been shown more effective than outcome supervision, but generating it automatically at scale is difficult without a principled mechanism.

**Core research question**: Can MCTS's look-ahead capability be used to automatically decompose instance-level rewards into step-level preference signals, and can this be combined with online iterative DPO to produce a self-improving LLM reasoning system?

---

## Contributions

1. **MCTS-DPO framework**: Combines MCTS-based step-level preference collection with iterative DPO policy updates into a unified online learning loop.
2. **Automated step-level preference generation**: MCTS Q-values are used to automatically label positive (high Q) and negative (low Q) reasoning steps at each tree depth, requiring no human annotation.
3. **Online DPO (avoids offline failure)**: Each iteration resamples preference data using the current policy, theoretically proven to avoid the failure mode of offline DPO (Theorem 3.2).
4. **Self-evaluation as critic**: The model acts as both policy and critic by generating a self-evaluation confidence score for intermediate steps, eliminating the need for a separate reward or value network.
5. **Visit-count-based label smoothing**: Adaptive label smoothing coefficient $\alpha$ derived from MCTS visit counts reduces the impact of noisy Q-value-based preference labels.
6. **Strong empirical gains**: Outperforms the Mistral-7B SFT baseline by +5.9% on GSM8K, +5.8% on MATH, and +15.8% on ARC-C; achieves 88.5% on unseen SciQ dataset.

---

## Methodology

### Overall Framework

MCTS-DPO is an **iterative online preference learning** framework. Each iteration $i$ consists of two stages:

**Stage 1**: Use MCTS under the current policy $\pi_{\theta^{(i-1)}}$ to collect step-level preference data $\mathcal{D}_i$.
**Stage 2**: Update the policy by minimizing the DPO loss on $\mathcal{D}_i$, yielding $\pi_{\theta^{(i)}}$.

Starting from $\pi_{\theta^{(0)}} = \pi_\text{sft}$, the loop runs for $M$ iterations. See Algorithm 1 in the paper.

---

### 2.1 MCTS for Step-Level Preference Collection

**State representation**: The reasoning process is discretized into steps. State $s_t$ is the prefix of the reasoning chain; taking action $a$ (generating the next reasoning step) transitions to $s_{t+1} = \text{concat}(s_t, a)$.

**Three MCTS phases**:

**Selection**: Nodes are selected using the PUCT formula:
$$s_{t+1}^* = \arg\max_{s_t} \left[ Q(s_t, a) + c_\text{puct} \cdot p(a \mid s_t) \cdot \frac{\sqrt{N(s_t)}}{1 + N(s_{t+1})} \right]$$
The prior $p(a \mid s_t) = \pi_\theta(a \mid x, s_t) / |a|^\lambda$ includes a length penalty $\lambda$ to discourage overly long reasoning chains.

**Expansion**: At a leaf node, the reward $R(s_t)$ for executing step $a$ is computed as:
$$R(s_t) = \mathcal{O}(s_t) + \mathcal{C}(s_t)$$
where $\mathcal{O}(s_t) \in \{1, -1, 0\}$ is outcome correctness (correct terminal / incorrect terminal / intermediate), and $\mathcal{C}(s_t) = \pi_\theta(\text{A} \mid \text{prompt}_\text{eval}, x, s_t)$ is the self-evaluation confidence score (token-level probability that the current step is "correct").

**Backup**: Update Q, V, and visit count N bottom-up from the terminal node:
$$Q(s_t, a) \leftarrow r(s_t, a) + \gamma V(s_{t+1})$$
$$V(s_t) \leftarrow \sum_a N(s_{t+1}) Q(s_t, a) \Big/ \sum_a N(s_{t+1})$$
$$N(s_t) \leftarrow N(s_t) + 1$$

**Preference pair construction**: For a search tree of depth $T$, at each depth $t$, the child node with the highest Q value becomes the positive sample $y_w^{(j,t)}$ and the child node with the lowest Q value becomes the negative sample $y_l^{(j,t)}$, where both must share the same parent node. This yields $T$ step-level preference pairs per problem.

**Annealed search breadth**: Initial breadth $b_1$ (e.g., 4 or 5) is reduced to $b_2 < b_1$ (e.g., 2 or 3) for subsequent steps, balancing diversity and computational cost. The parent node at each depth is selected by the highest product of visit count and children visit counts.

---

### 2.2 Iterative Preference Learning via DPO

Given step-level preference pairs $\mathcal{D}_i$, the policy is updated by minimizing a label-smoothed DPO objective:
$$\ell_i(\theta) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}_i} \left[ (1 - \alpha_{x,y_w,y_l}) \log \sigma(\beta h_{\pi_\theta}^{y_w, y_l}) + \alpha_{x,y_w,y_l} \log \sigma(-\beta h_{\pi_\theta}^{y_w, y_l}) \right]$$

where $h_{\pi_\theta}^{y_w, y_l} = \log \frac{\pi_\theta(y_w \mid x)}{\pi_\text{ref}(y_w \mid x)} - \log \frac{\pi_\theta(y_l \mid x)}{\pi_\text{ref}(y_l \mid x)}$ is the standard DPO log-ratio and $\beta$ is the KL constraint hyperparameter (set to 0.1).

The label smoothing coefficient is derived from MCTS visit counts:
$$\alpha_{x, y_w, y_l} = \frac{1}{N(x, y_w)/N(x, y_l) + 1}$$

When positive samples are visited far more often than negative samples ($N(x,y_w) \gg N(x,y_l)$), $\alpha \to 0$ (high confidence in the preference label). When visit counts are similar, $\alpha \to 0.5$ (treat the label as uncertain).

---

### Theoretical Analysis

**Theorem 3.1 (Offline DPO can fail with high probability)**: Let $\pi$ be a fixed sampling distribution and $\pi_{\theta^{(i-1)}}$ the current policy with $\pi_{\theta^{(i-1)}}(y^* \mid x) \geq c$ for optimal answer $y^*$. If the sampling policy assigns low probability to all suboptimal responses ($\pi(y \mid x) \leq \epsilon$ for all $y \neq y^*$), then there exists $\theta \in \Theta$ such that $\pi_\theta(y^* \mid x) \leq 1 - c$ with probability at least $1 - 2\epsilon M$.

The intuition: if the sampling policy never generates suboptimal outputs, DPO cannot learn to distinguish them from the optimal output, and the loss can be minimized without increasing $\pi_\theta(y^* \mid x)$.

**Theorem 3.2 (Online DPO avoids the failure case)**: If $\pi^{(i)} = \pi_{\theta^{(i-1)}}$ (online setting), then for any $\theta \in \Theta$, $\pi_\theta(y^* \mid x) = 1$ if $M \geq n + 1$, where $n$ is the number of distinct suboptimal responses.

The online setting ensures each suboptimal response is eventually sampled and eliminated, guaranteeing convergence.

---

### Experimental Setup

- **Base model**: Mistral-7B, SFT-trained on Arithmo (~540K math/coding problems)
- **Arithmetic reasoning datasets**: GSM8K, MATH (both Chain-of-Thought and Program-of-Thought formats)
- **Commonsense reasoning datasets**: ARC-easy/challenge, AI2Science-elementary/middle, OpenBookQA, CSQA; unseen: SciQ
- **Baselines**: SFT baseline, MCTS Offline-DPO, Instance-level Online-DPO, STaR (Zelikman et al., 2022), Crystal (Liu et al., 2023b), LMSI (Huang et al., 2023), Math-Shepherd (Wang et al., 2023a)
- **Hardware**: 4 x 40GB NVIDIA A100 GPUs; max sequence length 512; DPO batch size 32
- **MCTS settings**: $K=5$ iterations per sample; arithmetic: $b_1=5, b_2=3, d=4$; commonsense: $b_1=4, b_2=2, d=3$; ~2 min/sample

---

### Key Results

**Arithmetic Reasoning (Table 1)**:

| Approach | Base Model | GSM8K | MATH |
|---|---|---|---|
| SFT (Arithmo) | Mistral-7B | 75.9 | 28.9 |
| MCTS Offline-DPO | Mistral-7B | 79.9 | 31.9 |
| Instance-level Online-DPO | Mistral-7B | 79.7 | 32.9 |
| **Ours** | Mistral-7B | **81.8** | **34.7** |
| Ours (w/ G.T.) | Mistral-7B | 80.7 | 32.2 |

**Commonsense Reasoning (Table 2)**:

| Approach | ARC-c | AI2Sci-m | CSQA | SciQ |
|---|---|---|---|---|
| SFT Base (Arithmo) | 60.6 | 70.9 | 54.1 | 80.8 |
| MCTS Offline-DPO | 70.8 | 82.6 | 68.5 | 87.4 |
| Instance-level Online-DPO | 75.3 | 87.3 | 63.1 | 87.6 |
| **Ours** | **76.4** | **88.2** | 74.8 | **88.5** |

**Ablation findings**:
- Step-level online learning consistently outperforms instance-level and offline variants across all tasks.
- Self-evaluation with ground-truth "EXAMPLE ANSWER" in the prompt is critical: AUC 74.7 vs 62.0 without it on GSM8K.
- Training-time compute scaling (iterative learning) achieves higher performance ceilings than inference-time sampling (self-consistency) on ARC-C and SciQ, while MATH benefits more from sampling.
- Self-evaluation mechanism boosts MCTS pass rates: full MCTS achieves 92.1% on ARC-C vs 91.0% without self-evaluation.
- IPO loss function achieves comparable results to DPO, with slightly higher stability on held-out SciQ (89.8% vs 88.5%).
- Results generalize to Llama2-13B: GSM8K-CoT improves from 74.5% to 78.9% (+4.4%).

**Training dynamics**: Online learning shows cyclic performance fluctuations (validation accuracy peaks before dipping), consistent with the theoretical finding that insufficient per-iteration DPO optimization can cause periodic knowledge loss.
