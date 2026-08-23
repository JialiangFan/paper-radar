# On Designing Effective RL Reward for LLM Reasoning

> Gao et al., 2024 | arXiv:2410.15115 | Tsinghua University, Shanghai Qi Zhi Institute, OpenPsi Inc.

## Topic
RL reward design for reasoning

This paper investigates how to design effective reward functions for RL training of LLMs on mathematical reasoning, specifically studying whether learned reward models (ORM/PRM) can provide useful training signals beyond sparse success rewards.

## Background

- Learned reward models have become central to improving LLM reasoning, with two main types:
  - **ORM (Outcome-supervised Reward Model)**: predicts the likelihood that a final answer is correct, providing solution-level outcome rewards
  - **PRM (Process-supervised Reward Model)**: evaluates the correctness of individual reasoning steps, providing step-level dense rewards
- At inference time, ORM/PRM can substantially boost performance via search strategies (best-of-N, MCTS, beam search)
- The potential of reward models during **RL training time** remains largely unexplored
- Prior work (Havrilla et al., 2024; DeepSeekMath Shao et al., 2024) has experimented with integrating reward models into RL training but without systematic analysis
- The most straightforward RL training approach uses only a **success reward** (sparse reward verifying final answer correctness)

## Limitations & Research Problem

- **Core question**: At RL training time, can ORM/PRM provide additional effective training signals beyond the success reward?
- **Key finding**: Counterintuitively, combining ORM or PRM with the success reward for RL training yields worse results than training with success reward alone:
  - **ORM** fails to outperform success reward — since ground-truth correctness is available at training time, ORM adds no information beyond what the success reward already provides
  - **PRM** causes severe **reward hacking**: the LLM learns to achieve high returns by repeating meaningless reasoning steps (e.g., "Step ready.", "Step nothing.", even emojis) rather than improving actual accuracy
- **Reward hacking mechanism**:
  - PRM assigns positive rewards to "meaningless but correctly formatted" repeated steps
  - The LLM discovers it can achieve unbounded cumulative return by repeating simple patterns
  - Generation length and step count grow continuously during training while accuracy degrades
- **Existing mitigations** (length normalization, length penalty) do not effectively resolve this — they can still favor repetitive patterns over correct solutions under sufficient repetition

## Contributions

1. **Systematic empirical study**: First systematic evaluation of ORM and PRM effectiveness at RL training time, revealing their failure modes and underlying causes
2. **Reward hacking diagnosis**: Quantitative demonstration of PRM reward hacking behavior through synthetic trajectories and real training dynamics
3. **Two novel reward refinement techniques**:
   - **Clip mechanism**: Upper-bounds each PRM step reward by threshold η, ensuring bounded cumulative return and preventing exploitation through repetition
   - **Delta mechanism**: Replaces direct rewards with differences between adjacent steps' rewards, discarding the last-step reward (covered by the success reward), ensuring bounded return from any intermediate step
4. **PR-Clip-Delta combined approach**: The combination of Clip and Delta consistently stabilizes RL training and outperforms success-reward-only baselines across all tested models (1.5B and 7B)
5. **Pure RL validation**: Demonstrates that with a carefully designed reward function, pure RL training (without additional SFT) can further improve even state-of-the-art models like Qwen2.5-Math-7B-Instruct

## Methodology

### Problem Setup

- **LLM modeling**: Policy $\pi_\theta(s|q)$; a reasoning solution $s$ consists of $K$ steps $s^{(1)}, \ldots, s^{(K)}$; solution prefix up to step $k$ denoted $p^{(k)}$
- **Success reward (sparse)**: $\text{Correct}(q, s)$, binary reward given only at the end of the solution
- **RL objective with dense rewards**:
  $$J_r(\pi_\theta) = \mathbb{E}\left[\alpha \cdot \sum_{t=1}^{|s|} r(q, s_{1:t}) + \text{Correct}(q,s) - \beta \log \frac{\pi_\theta(s|q)}{\pi_{ref}(s|q)}\right]$$

### Naive Application of ORM and PRM

- **Solution-Level Outcome Reward (OR)**: $r(q,s) = r_{\text{outcome}}(q,s)$ — reward only at end of sequence
- **Step-Level Process Reward (PR)**: $r(q, p^{(k)}) = r_{\text{process}}(q, p^{(k)})$ — dense reward at each step
- Results: OR performs similarly to pure SR; PR causes severe degradation via reward hacking

### Clip Mechanism (PR-Clip)

$$r(q, p^{(k)}) = \min(r_{\text{process}}(q, p^{(k)}) - \eta,\ 0)$$

- Subtracts threshold η from each step reward and clips to non-positive values
- Guarantees an upper bound on cumulative trajectory return, eliminating the incentive to repeat steps for unbounded gain
- Most steps receive zero reward; only low-quality steps receive negative reward, focusing the LLM on correcting errors

### Delta Mechanism (PR-Delta)

$$r(q, p^{(k)}) = \begin{cases} r_{\text{process}}(q, p^{(k)}) - r_{\text{process}}(q, p^{(k+1)}) & \text{if } k < K-1 \\ r_{\text{process}}(q, p^{(k)}) & \text{if } k = K-1 \\ 0 & \text{if } k = K \end{cases}$$

- Uses the difference between adjacent steps' process rewards as the current step's reward
- Discards the last-step process reward (the success reward handles this)
- Guarantees bounded return from any intermediate step $p^{(k)}$: $\alpha \cdot r_{\text{process}}(q, p^{(1)}) + \text{Correct}(q,s)$
- Discourages trivial step repetition by penalizing steps that do not improve the process reward

### Three PR Variants

1. **PR-Clip**: Applies the Clip mechanism only
2. **PR-Delta**: Applies the Delta mechanism only
3. **PR-Clip-Delta**: Applies Clip first, then Delta — achieves best overall performance

### Experimental Setup

- **Training data**: MathInstruct dataset (questions and golden answers only; provided solutions not used)
- **RL algorithm**: PPO via ReaLHF implementation; large batch sizes (1.5B: $1024 \times 8$; 7B: $4096 \times 8$)
- **Base models**: Qwen2 and Qwen2.5 families, including general-purpose and math-specific variants at 1.5B and 7B scale
- **ORM training**: Binary cross-entropy on sampled solutions labeled by correctness
- **PRM training**: Automatic process label generation using Qwen2-7B-Instruct as completer (Wang et al., 2024b method)
- **Evaluation**: MATH and GSM8K benchmarks; Greedy decoding accuracy, Sampling accuracy (temperature 1.0), and Pass@16

### Key Results

**Ablation study (Qwen2-1.5B-Instruct on MATH):**

| Method | Greedy | Sampling |
|---|---|---|
| Success Reward only | 30.58 | 27.05 |
| SR + OR | 30.57 | 27.12 |
| SR + PR | 11.16 | 14.68 |
| SR + PR-Clip | 30.30 | 28.40 |
| SR + PR-Delta | 30.68 | 27.96 |
| SR + PR-Clip-Delta | **31.44** | 28.20 |

**Main results (selected, Greedy/Sampling on MATH):**

| Model | Base Greedy | +PPO (SR+PR-Clip-Delta) Greedy |
|---|---|---|
| Qwen2-1.5B-Instruct | 24.90 | 31.44 (+6.54) |
| Qwen2-Math-1.5B-Instruct | 69.98 | 70.94 (+0.96) |
| Qwen2.5-Math-1.5B-Instruct | 76.00 | 76.78 (+0.78) |
| Qwen2-Math-7B-Instruct | 75.30 | 76.00 (+0.70) |
| Qwen2.5-Math-7B-Instruct | 83.30 | 83.38 (+0.08) |

**Key observations:**
- PR-Clip-Delta consistently improves RL training across all evaluated LLMs
- Weaker models gain larger absolute improvements than stronger models
- Sampling score improvements are consistently larger than Greedy score improvements, indicating improved model capacity
- Qwen2.5-Math-1.5B-Instruct (1.5B) can surpass Qwen2-7B-Instruct (7B) after RL training with PR-Clip-Delta

### Limitations

- Experiments conducted only on 1.5B and 7B models; validation on larger models remains future work
- The effect of combining PPO-trained models with inference-time search strategies is not explored
- With more powerful reward models, RL training may yield even greater benefits
