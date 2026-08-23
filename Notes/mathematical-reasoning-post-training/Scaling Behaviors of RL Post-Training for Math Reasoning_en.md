# Scaling Behaviors of RL Post-Training for Math Reasoning

> Tan et al., arXiv:2509.25300, December 2025
> Institutions: USTC, Shanghai AI Laboratory, University of Oxford, Imperial College London, University of Georgia, CUHK, Chinese Academy of Sciences, Dalian University of Technology, NUS, Wuhan University
> Code: github.com/tanzelin430/Mathematical-Reasoning-RL-Scaling-Law
> Dataset: huggingface.co/datasets/Artemis0430/GURU-MATH-CL

## Topic: RL post-training scaling laws

A systematic empirical investigation into how model scale, data volume, and computational budget jointly govern performance during reinforcement learning (RL) post-training of large language models (LLMs), with a focus on mathematical reasoning.

---

## Background

- Pre-training scaling laws (Kaplan et al. 2020; Hoffmann et al. 2022) are well-established: loss follows power-law relationships with model size N, data D, and compute C, enabling compute-optimal training strategies (Chinchilla).
- RL post-training has become the dominant approach for improving LLM reasoning capabilities in mathematics (DeepSeek-R1, Kimi k1.5, GRPO-based methods), but its scaling behavior remains largely uncharacterized.
- Prior work (Hilton et al. 2023) demonstrated power-law scaling in single-agent RL for CNNs, but systematic empirical study of LLM RL fine-tuning scaling is absent.
- Three critical resource regimes are identified: (1) **compute-constrained** — minimize test loss under a fixed FLOPs budget; (2) **data-constrained** — identify the optimal model size given limited unique training samples; (3) **data reuse** — investigate the trade-off between unique data volume and repeated optimization steps under a fixed compute budget.

---

## Limitations & Research Problem

- **Gap**: Pre-training scaling laws do not directly apply to RL post-training because the optimization objective, reward structure, and training dynamics differ fundamentally.
- **Open questions**:
  1. Does RL post-training loss follow a predictive power-law as a function of compute C, data D, and model size N?
  2. Under a fixed compute budget, should one prefer a larger model or more training steps?
  3. Does learning efficiency k(N) grow indefinitely with model scale, or does it saturate?
  4. In data-limited regimes, is repeated reuse of high-quality data an effective substitute for larger corpora?
  5. Do RL post-training gains transfer to out-of-domain tasks?
- **Limitation of existing approaches**: No unified quantitative framework characterizes the interplay between N, C, and D in RL fine-tuning, leaving practitioners without principled guidelines for resource allocation.

---

## Contributions

Four key empirical findings, supported by 63 fine-tuned LLMs across the Qwen2.5 family (0.5B–72B):

1. **Larger models exhibit consistently higher learning efficiency** on both compute and data metrics, but efficiency gains follow a saturation trend — diminishing marginal returns appear beyond 32B parameters.

2. **A predictive power-law formulation** characterizes the relationship between test loss L, model size N, and resource budget X (compute C or data D), robust across both base and instruction-tuned models:
   $$\log L(N, X) = -k(N) \cdot \log X + E(N)$$
   where learning efficiency saturates as:
   $$k(N) = \frac{K_{\max}}{1 + \frac{N_0}{N}}$$
   This shows k(N) asymptotically approaches an upper bound $K_{\max}$ rather than growing indefinitely.

3. **Latent saturation in learning efficiency**: The analytical term k(N) reveals that scaling up models beyond a certain point yields diminishing returns in efficiency, introducing a practical trade-off between model scale and training steps in compute-constrained settings.

4. **Data reuse is highly effective in data-constrained regimes**: Final performance is primarily governed by the total number of optimization steps (D_total) rather than sample uniqueness. Performance remains nearly unchanged for reuse factor τ ≤ 25, with degradation appearing only at τ = 100.

---

## Methodology

### Experimental Setup

- **Model family**: Qwen2.5 dense series (0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B); parameter count is the sole varying architectural factor.
- **Training framework**: VeRL (large-scale RL platform for LLMs), ensuring reproducibility across all experiments.
- **Training data**: Mathematics subset of the guru-RL-92k dataset from the Reasoning360 project, curated via deduplication and difficulty filtering. Problems are sorted by increasing difficulty (decreasing pass rate on Qwen2.5-7B-Instruct) to enable curriculum learning.
- **Evaluation set**: 500 held-out math problems for fitting scaling laws; generalization evaluated across mathematics (AIME2024, AMC2023, GSM8K, MATH-500), code (HumanEval), logic (Zebra Puzzle), and science (SuperGPQA).
- **RL algorithm**: Group Relative Policy Optimization (GRPO; Shao et al. 2024), which estimates advantages by normalizing rewards across responses sampled from the same prompt:
  $$\mathcal{L}_{\text{GRPO}} = \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t=1}^{|o_i|}\left\{\min\left[\rho(\theta)\hat{A}_{i,t},\,\text{clip}(\rho(\theta), 1-\varepsilon, 1+\varepsilon)\hat{A}_{i,t}\right] - \beta D_{\text{KL}}\right\}$$
- **Reward signal**: Binary rule-based reward (Pass@1) — a script extracts the final answer from the model output (\\boxed{} format) and compares it to the ground truth.
- **Primary metric**: Test loss $L = 1 - R/R_{\max}$, a proxy for reward-based performance aligned with the neural scaling law literature; maximizing reward is equivalent to minimizing L.

### Fitting and Prediction Protocols

- **Inter-model Extrapolation**: Fit scaling law parameters on smaller models (0.5B–32B) to predict 72B model performance; validated against actual 72B results.
- **Intra-model Prediction**: Fit scaling law using only early training steps to forecast the remaining loss trajectory for a specific model.
- Each configuration is repeated **three times** for both base and instruct model variants; statistical uncertainty is reported via Average Standard Deviation and Standard Error of the Mean (SEM).

### Three Scaling Regimes

| Regime | Definition | Core Formula |
|--------|-----------|--------------|
| Compute-Constrained | Fixed FLOPs C; find optimal N and data D | $\log L(N,C) = -k_C(N)\cdot\log C + E_C(N)$ |
| Data-Constrained | Fixed unique samples D; find optimal N | $\log L(N,D) = -k_D(N)\cdot\log D + E_D(N)$ |
| Data Reuse | Fixed D_total; vary reuse factor τ | $\arg\min_\tau L(\tau)$ s.t. $D_{\text{unique}} \times \tau = D_{\text{total}}$ |

Both compute and data efficiency coefficients share the same saturation form: $k_C(N) = K_{C\max}/(1 + N_C/N)$ and $k_D(N) = K_{D\max}/(1 + N_D/N)$.

### Key Empirical Observations

- **Observation 1 (Compute scaling)**: Within 0.5B–32B, a fixed compute budget is best spent on larger models rather than extended training of smaller ones. Between 32B and 72B, learning efficiency saturation introduces a trade-off between model scale and training steps.
- **Observation 2 (Data scaling)**: For a fixed volume of unique training data D, larger models consistently achieve lower test loss, demonstrating superior sample efficiency throughout the 0.5B–72B range.
- **Observation 3 (Model size scaling)**: When trained to convergence on sufficiently large datasets, test loss decreases monotonically with model size, though the trend deviates from a strict power law (smaller models show weaker returns, likely due to richer pre-trained representations in larger models benefiting more from RL fine-tuning).
- **Observation 4 (Data reuse)**: Performance for τ ≤ 25 is nearly indistinguishable from τ = 1; overfitting becomes apparent at τ = 100. This confirms that total optimization steps, not sample uniqueness, are the primary driver of final performance.
- **Observation 5 (Domain transfer)**: RL post-training on mathematics reliably improves in-domain generalization (unseen math benchmarks: GSM8K, MATH-500, AMC2023, AIME2024) but shows negligible or negative transfer to out-of-domain tasks (code generation: HumanEval; science: SuperGPQA; logic: Zebra Puzzle — the largest models show performance degradation on logical reasoning).

### Hyperparameter Configuration (GRPO)

| Hyperparameter | Value |
|----------------|-------|
| Learning Rate | 1.0 × 10⁻⁶ |
| Batch Size | 512 |
| KL Loss Coefficient | 0.001 |
| Rollout Temperature (Training) | 1.0 |
| Rollout Temperature (Evaluation) | 0.7 |
| Clip Ratio | 0.2 |
| Input Sequence Length | 2048 |
| Output Sequence Length | 4096 |

### Discussion and Limitations

- **Evaluation dependence**: Test loss as a proxy metric is monotonic and convergent but heavily task-dependent; absolute scaling coefficients k(N) and E are not universally interpretable across datasets (e.g., GSM8K vs. AIME show distinct convergence rates).
- **Algorithm dependence**: All results are based on GRPO; whether more advanced RL algorithms can improve sample efficiency or reshape the scaling frontier remains open.
- **Future direction**: Integration of agentic mechanisms (tool use, long-term memory) is anticipated to improve scaling behavior by offloading deterministic computations and shifting the performance frontier upward for a given compute or data budget.
