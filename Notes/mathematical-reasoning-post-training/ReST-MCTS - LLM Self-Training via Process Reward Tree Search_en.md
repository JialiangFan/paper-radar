# ReST-MCTS - LLM Self-Training via Process Reward Tree Search

## Topic
MCTS-guided LLM self-training with automatically inferred process rewards

**Paper Info**
- Authors: Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue, Yuxiao Dong, Jie Tang (KEG, Tsinghua University; Caltech)
- Venue: NeurIPS 2024
- ArXiv: 2406.03816
- Code: https://github.com/THUDM/ReST-MCTS

---

## Background

LLM self-training has become a key paradigm for improving reasoning capabilities without relying on externally labeled data. Existing reinforced self-improvement methods (STaR, RFT, ReST^EM, V-STaR) share a common pipeline:
1. Use the LLM to generate multiple candidate reasoning traces (Chain-of-Thought)
2. Filter traces that produce a correct final answer
3. Fine-tune the LLM on these "positive" traces via SFT
4. Repeat for multiple iterations

All such methods require a **reward signal** to identify high-quality samples:
- **Outcome Reward Models (ORM)**: score only the correctness of the final answer
- **Process Reward Models (PRM)**: score each individual reasoning step

PRMs are known to provide denser and more reliable supervision than ORMs, but training a reliable PRM traditionally requires dense **per-step human annotations**, which do not scale.

The LLM self-training loop can be viewed as a model-based RL problem, where the policy (LLM) generates reasoning traces and a value/reward model provides learning signals. The challenge is constructing useful learning signals at the step level without human labor.

---

## Limitations & Research Problem

**Core problem: low-quality training data due to false positive traces and the PRM annotation bottleneck.**

1. **False positive reasoning chains**: LLMs frequently generate incorrect or meaningless intermediate steps that happen to produce the correct final answer by chance. Including such traces in the training set introduces noise and limits fine-tuning gains.

2. **PRM training requires costly human annotation**: Existing PRMs (e.g., Let's Verify Step by Step) treat training as a three-class classification requiring per-step human labels. MATH-SHEPHERD partially addresses this with automated annotation via random rollouts, but quality is still limited.

3. **Sparse reward / credit assignment**: Using only the final answer as supervision creates a credit assignment problem: it is unclear which intermediate steps contributed to the correct outcome.

4. **Search policy quality**: Common search strategies (Self-Consistency, Best-of-N) are sample-inefficient and plateau quickly as the sampling budget grows.

**Research question: How can we automatically acquire high-quality reasoning traces and reliable per-step process reward signals for LLM self-training, without manual annotation?**

---

## Contributions

1. **ReST-MCTS\* framework**: A reinforced self-training approach that integrates a Process Reward Model with a novel MCTS\* tree search algorithm to collect higher-quality reasoning traces and per-step value labels simultaneously.

2. **Automatic process reward inference**: By performing sufficient rollouts from each tree node, ReST-MCTS\* automatically infers the process reward (quality value $v_k$) for every intermediate reasoning step — eliminating the need for human per-step annotation.

3. **Superior search policy**: Under the same search (token) budget, MCTS\* achieves higher accuracy than Self-Consistency (SC) and Best-of-N (BoN) on MATH and SciBench benchmarks.

4. **Continuous self-improvement**: Using MCTS\*-searched traces as training data, three LLM backbones (LLaMA-3-8B-Instruct, Mistral-7B, SciGLM-6B) continuously improve over multiple iterations, outperforming ReST^EM and Self-Rewarding LM.

5. **Higher-quality PRM**: The reward model trained on ReST-MCTS\*-generated labels outperforms MATH-SHEPHERD on GSM8K (87.5% vs. 86.3%) and MATH500 (39.0% vs. 38.3%) verification accuracy.

---

## Methodology

### System Overview

ReST-MCTS\* comprises four interacting components that are jointly trained in an iterative loop:

| Component | Role |
|-----------|------|
| **MCTS\*** (modified Monte Carlo Tree Search) | Guided by PRM to search for high-quality reasoning traces |
| **Process Reward Model (PRM)** $V_\theta$ | Predicts quality value $v_k$ for any partial solution; guides MCTS\* |
| **Policy Model** $\pi_\phi$ | Generates candidate reasoning steps for each question |
| **LLM Self-Training** | Fine-tunes policy on positive traces; trains PRM on all generated traces |

### Key Concepts: Quality Value and Weighted Reward

**Reasoning Distance $m_k$**: The minimum number of reasoning steps needed to reach a correct answer from partial solution $p_k = [s_1, \ldots, s_k]$. It is estimated empirically by performing multiple rollouts from $p_k$ and finding the actual minimum steps to a correct answer.

**Weighted Reward $w_{s_k}$** (single-step contribution):
$$w_{s_k} = \frac{1 - v_{k-1}}{m_k + 1}(1 - 2r_{s_k})$$
where $r_{s_k} \in [0,1]$ is the PRM's sigmoid score for step $s_k$. The weighting by $m_k$ means steps closer to the correct answer receive higher weight.

**Quality Value $v_k$** (cumulative quality of partial solution $p_k$, used as the value target for PRM training and as the MCTS\* backup value):
$$v_k = \max(v_{k-1} + w_{s_k},\ 0), \quad v_0 = 0$$

**Theorem 1 (Boundedness)**: If $r_{s_k} \in [0,1]$, then $w_{s_k} \leq 1 - v_{k-1}$ and $v_k \in [0,1]$.

Key observations:
- $v_k \to 1$ if and only if $r_{s_k} \to 0$ and $m_k = 0$, i.e., quality approaches 1 only when the step is correct and leads directly to the answer.
- A reasoning path requiring more steps to reach the correct answer has a lower single-step weighted reward.
- $w_{s_k}$ decreases as the PRM's confidence in step correctness ($r_{s_k}$) increases.

### MCTS\* Algorithm

Each MCTS\* iteration over a question $q$ maintains a search tree $T_q$ where each node $C = (p_C, n_C, v_C)$ stores a partial solution, visit count, and quality value. Four stages per iteration:

1. **Node Selection**: Select a node to expand using a UCB-style criterion that balances exploitation (high $v_C$) and exploration (low $n_C$).
2. **Thought Expansion**: The policy model $\pi$ generates $N$ candidate next reasoning steps $s_{k+1}$ from the selected node.
3. **Greedy MC Rollout**: From each expanded node, perform a greedy rollout to estimate $m_k$ (minimum steps to correct answer), using hard estimation (HE) from MATH-SHEPHERD to determine step correctness.
4. **Value Backpropagation**: Update $v_k$ for all nodes on the path back to the root using Eq. (1).

A **self-critic mechanism** is incorporated to filter internally inconsistent reasoning steps, enhancing search precision (detailed in Appendix C.1).

### Self-Training Pipeline (Algorithm 1)

```
Input: base LLM π, initial policy dataset D_{S_0}, initial value dataset D_0,
       new problem set D_G, solution count N, value model V_θ, iterations T

1. π_{S_0} ← SFT(π, D_{S_0})           // initialize policy
2. D_{V_0} ← generate_value_data(D_0, w, v)  // initialize value training set
3. V_0 ← train_value_model(V_θ, D_{V_0})    // initialize PRM

for i = 1 to T:
    4. D_{G_i} ← generate_policy_data(π_{S_{i-1}}, V_{i-1}, D_G, N)  // MCTS* search
    5. for j = 1 to N: filter D_{G_i}(A_j = a*)  // keep correct solutions
    6. π_{S_i} ← SFT(π_{S_{i-1}}, D_{G_i}(A_j=a*))  // policy self-training
    7. D_{V_i} ← extract_value_data(D_{G_i})   // extract (Q, p, v) triples
    8. V_i ← train_value_model(V_{i-1}, D_{V_i}) // PRM self-training

Output: π_{S_T}, V_T
```

**Policy model training objective** (SFT, minimize negative log-likelihood):
$$\mathcal{L}_\text{SFT}(\pi) = -\mathbb{E}_{(Q,s)\in D_{S_0}}\left[\sum_{t=1}^T \log\pi(s_t|s_{<t},Q)\right]$$

**PRM training objective** (binary cross-entropy per step):
$$\mathcal{L}_\text{PRM} = \sum_{k=1}^{K} A_{s_k} \log r_{s_k} + (1 - A_{s_k})\log(1 - r_{s_k})$$
where $A_{s_k}$ is automatically derived from the search tree (no human annotation needed).

### Value Model Initialization

Two strategies for building $D_{V_0}$:

**For science data**: Integrate the SciInstruct science dataset (11,554 questions with step-by-step solutions). For each question-solution pair, extract partial solutions and use ChatGLM2 (a weak model) to generate false next steps. False steps receive $r_{s_{k+1}}' = 1$ (incorrect). True steps at position $k$ in a $K_i$-step solution receive $r_{s_k} = 0$, $m_k = K_i - k$, and $v_k = k/K_i$. Total: 473.4k samples.

**For math data**: Use Mistral-7B: MetaMATH to generate BFS-style search trees on MATH training set. Derive quality values from verified trees using the same $v_k$ formula.

### Experimental Results

**Self-training comparison** (Table 2, zero-shot evaluation):
- LLaMA-3-8B-Instruct: ReST-MCTS\* 2nd iter average 29.02 vs. ReST^EM 26.83, Self-Rewarding 27.73
- Mistral-7B: MetaMATH: 26.50 vs. 24.16, 25.22
- SciGLM-6B: 35.90 vs. 33.27, 33.56

**PRM / verifier comparison** (Table 3, Mistral-7B: MetaMATH):
- GSM8K: SC+ReST-MCTS\* (Value) 87.5% vs. SC+MS 86.3%
- MATH500: 39.0% vs. 38.3%

**Search policy comparison** (Figure 2):
- On MATH: ReST-MCTS\* Iter #2 reaches ~48.5% at 40k tokens/question vs. Self-Consistency plateau at ~42.5%
- On SciBench: MCTS\* consistently above SC and BoN across all budgets

**Reasoning policy on SciBench** (Table 4, 3 models × 10 subjects):
- GLM4: ReST-MCTS\* avg 16.77 vs. ToT 15.82, CoT 12.68
- GPT-3.5-turbo: 10.06 vs. 8.44 (ToT), 6.92 (CoT)

### Limitations

- Primarily validated on mathematical reasoning; generalization to coding, agent tasks, and other domains remains to be demonstrated.
- Not yet adapted to tasks without ground-truth answers (e.g., dialogue, SWE-Bench).
- Small-scale policy models (e.g., LLaMA2-13B-Chat) show limited improvement, suggesting that step-wise inference capacity is a prerequisite for MCTS\* to be effective.
- Online RL integration (rather than offline SFT) could further improve both policy and value models.
