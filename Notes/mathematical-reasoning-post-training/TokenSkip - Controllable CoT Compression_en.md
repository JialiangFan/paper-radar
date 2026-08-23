# TokenSkip - Controllable CoT Compression

## Topic
Controllable Chain-of-Thought (CoT) compression via token skipping — enabling LLMs to selectively skip less semantically important tokens within CoT sequences, thereby reducing inference cost while preserving strong reasoning performance.

## Background
Chain-of-Thought (CoT) prompting has emerged as a cornerstone strategy for enhancing LLM reasoning in complex tasks. Frontier models such as OpenAI o1 and DeepSeek-R1 demonstrate that scaling up CoT length at inference time can continuously improve reasoning performance. However, the autoregressive nature of LLM decoding means that longer CoT outputs lead to proportional increases in both inference latency and key-value cache memory footprint. The quadratic computational cost of attention layers further exacerbates this overhead, making extended CoT sequences (beyond 10,000 tokens) practically costly in terms of computation and user-facing response time.

## Limitations & Research Problem
**Central research question:** Does every token in a CoT output contribute equally to deriving the final answer?

**Limitations of existing approaches:**
- **Token-efficient prompts** (BeConcise, OnlyNumbers, AbbreWords): Achieve only 0.94–0.97 actual compression ratios on MATH-500, with negligible efficiency gains.
- **Length-control prompts** (LC-Prompt): Even when the target ratio is set to 0.5, the actual ratio exceeds 0.89; the model cannot reliably adhere to specified compression targets.
- **Truncation**: While it adheres to the specified ratio, it causes severe reasoning degradation — a 79% accuracy drop on GSM8K and a 21% drop on MATH-500 at a compression ratio of 0.5.
- Existing token importance metrics (e.g., Selective Context based on unidirectional LM perplexity) suffer from positional dependency bias, as the intrinsic decreasing perplexity across a sentence conflates position with importance. Unidirectional causal attention also fails to capture full contextual information for each token.
- Prior work suggested that skipping reasoning steps may conflict with test-time scaling, potentially impairing reasoning performance.

**Key empirical findings:**
1. Token semantic importance within CoT outputs varies substantially. Mathematical expressions and key numerical values contribute more to the final answer, while semantic connectors (e.g., "so", "since") contribute less.
2. LLMs are capable of recovering the full CoT process from compressed outputs (CoT Recovery), demonstrating that compressed CoTs retain sufficient semantic information and that interpretability can be maintained.

## Contributions
1. **First work to explore CoT efficiency enhancement through token skipping**, motivated by the observed variation in semantic importance across tokens in LLM CoT trajectories.
2. **TokenSkip**: A simple yet effective approach enabling LLMs to skip redundant tokens within CoTs and learn shortcuts between critical reasoning tokens, supporting controllable CoT compression with adjustable ratios.
3. **Empirical validation**: On Qwen2.5-14B-Instruct, TokenSkip reduces reasoning tokens by 40% (313 → 181) on GSM8K with less than 0.4% performance drop. On MATH-500, LLaMA-3.1-8B-Instruct achieves 30% token reduction with under 4% performance decline and a 1.4× inference speedup.
4. **Low training cost**: Only 0.2% of model parameters are fine-tuned via LoRA; training data is no larger than the original dataset (7,473 examples for GSM8K, 7,500 for MATH); training completes in ~2 hours for 7B and ~2.5 hours for 14B models on two NVIDIA RTX 3090 GPUs.
5. **Generalizability**: TokenSkip maintains strong out-of-domain performance on GSM8K and MMLU-STEM when trained only on MATH, and reduces CoT length by 50% on CommonsenseQA without any performance degradation, demonstrating applicability beyond mathematical reasoning.

## Methodology

### Core Insight
The key insight behind TokenSkip is that **each reasoning token contributes differently to deriving the answer**. By pruning low-importance tokens from LLM-generated CoT trajectories and fine-tuning the model on these compressed trajectories, TokenSkip enables LLMs to autonomously skip redundant tokens and identify shortcuts between critical reasoning tokens during inference.

### Token Importance Measurement
TokenSkip employs **LLMLingua-2** — a small bidirectional BERT-like language model trained with GPT-4 compression annotations — as the token importance metric. The importance of token $x_i$ is defined as:

$$I_2(x_i) = P(x_i \mid \boldsymbol{x}_{\leq n}; \boldsymbol{\theta}_{\mathcal{M}_B})$$

This is the predicted probability of the token given the full bidirectional context, rather than a unidirectional perplexity measure. The bidirectional attention mechanism avoids the positional dependency bias inherent in causal LMs and better captures the global semantic role of each token.

### Three-Stage Pipeline

**Stage 1: Token Pruning**

Given a target LLM $\mathcal{M}$, a CoT trajectory $\boldsymbol{c} = \{c_i\}_{i=1}^m$, and a specified compression ratio $\gamma \in [0, 1]$:
1. Compute token importance scores $\{I(c_i)\}_{i=1}^m$ using LLMLingua-2.
2. Rank scores in descending order and compute the $\gamma$-quantile pruning threshold:
$$I_\gamma = Q_\gamma(I(c_1), \ldots, I(c_m))$$
3. Retain only tokens whose importance meets or exceeds the threshold:
$$\tilde{\boldsymbol{c}} = \{c_i \mid I(c_i) \geq I_\gamma,\ 1 \leq i \leq m\}$$

Importantly, compression is applied solely to the CoT sequences; the final answer tokens are kept unchanged to preserve correctness.

**Stage 2: Training (Supervised Fine-Tuning)**

Given a training dataset $\mathcal{D}$ with $N$ samples:
1. Generate $N$ CoT trajectories using the target LLM $\mathcal{M}$; filter out trajectories with incorrect answers.
2. For each trajectory, sample a compression ratio $\gamma$ from the ratio set $\{\gamma_0, \ldots, \gamma_z\}$ (default: $\{0.5, 0.6, 0.7, 0.8, 0.9, 1.0\}$) and prune accordingly.
3. Format each training sample as: $\mathcal{Q}\ [\text{EOS}]\ \gamma\ [\text{EOS}]\ \tilde{\boldsymbol{c}}\ \boldsymbol{a}$, where $\gamma$ is inserted after the question as a controllable signal.
4. A portion of original (uncompressed) CoT trajectories ($\gamma = 1$) is included to preserve base reasoning capability.
5. Fine-tune $\mathcal{M}$ using LoRA by minimizing the negative log-likelihood over the compressed CoT and answer tokens:
$$\mathcal{L} = \sum_{i=1}^{l} \log P(y_i \mid \boldsymbol{x}, \gamma, \boldsymbol{y}_{<i}; \boldsymbol{\theta}_\mathcal{M})$$

**Stage 3: Inference**

The input prompt at inference follows the same format as training: $\mathcal{Q}\ [\text{EOS}]\ \gamma\ [\text{EOS}]$. The user specifies a desired compression ratio $\gamma \in \{\gamma_0, \ldots, \gamma_z\}$ to control the degree of CoT compression. The model autoregressively generates the compressed CoT $\hat{\boldsymbol{c}}$ and answer $\hat{\boldsymbol{a}}$, having learned to skip unimportant tokens and find shortcuts between critical reasoning tokens.

### Key Experimental Results

| Model | Benchmark | Compression Ratio | Token Reduction | Accuracy Drop |
|---|---|---|---|---|
| Qwen2.5-14B-Instruct | GSM8K | 0.6 | ~40% (313→181) | <0.4% |
| LLaMA-3.1-8B-Instruct | MATH-500 | 0.5 | ~30% | <4% |
| Qwen2.5-7B/14B-Instruct | CommonsenseQA | 0.5 | ~50% | ~0% |

**Ratio adherence**: TokenSkip's actual compression ratio closely tracks the specified $\gamma$, unlike More Ratio and prompting-based baselines which fail to achieve tight adherence.

**Token importance distribution**: Skipped tokens skew toward lower importance scores while retained tokens predominantly exhibit high importance, confirming that the model learns to discard semantically redundant tokens.

**Importance metric comparison**: LLMLingua-2-based TokenSkip outperforms Selective Context. GPT-4o as an upper-bound metric further improves performance, suggesting headroom for gains with more powerful importance metrics.

**Length budget analysis**: Under a fixed length budget equal to the original LLM, TokenSkip with $\gamma \in \{0.7, 0.8, 0.9\}$ surpasses the original LLM by 1.3–2.6 absolute percentage points on MATH-500, indicating that the compressed CoT format enables more efficient use of reasoning tokens within the same budget.

### Limitations
- Experiments with larger models (Qwen2.5-32B/72B-Instruct) were not conducted due to computational constraints; TokenSkip may achieve an even more favorable efficiency–accuracy trade-off at larger scales.
- The token importance metric (LLMLingua-2) was not specifically trained on mathematical data, potentially limiting its ability to handle numerical tokens and mathematical expressions optimally.
- Long-CoT models such as QwQ-32B-Preview were excluded from experiments due to computational constraints.
