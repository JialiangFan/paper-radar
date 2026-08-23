# ARES - Adaptive Reasoning Effort Selection

## Topic: Adaptive reasoning effort

**Full Title**: ARES: Adaptive Reasoning Effort Selection for Efficient LLM Agents
**Authors**: Jingbo Yang, Bairu Hou, Wei Wei, Yujia Bao, Shiyu Chang
**Institutions**: UC Santa Barbara; Accenture Center for Advanced AI
**ArXiv**: 2603.07915v1 [cs.AI], March 9, 2026
**Code**: https://github.com/UCSB-NLP-Chang/Ares

---

## Background

Modern LLM agents powered by thinking LLMs achieve high task accuracy through extended chain-of-thought (CoT) reasoning, but this comes at a substantial inference cost due to the accumulation of large numbers of reasoning tokens across multi-step trajectories. State-of-the-art LLMs (e.g., GPT-5, Gemini-3) now expose configurable reasoning effort levels—such as high/medium/low or thinking/fast modes—enabling users to trade off reasoning depth against computational cost.

A straightforward cost-reduction strategy is to configure agents to always reason at a lower effort level. However, not all steps in an agent task require the same depth of reasoning: simple navigation steps (e.g., opening a landing page) need little deliberation, while complex planning or error-correction steps demand intensive reasoning. A fixed, static effort strategy therefore fails to balance performance and cost effectively across the heterogeneous demands of a multi-step trajectory.

Prior model routing approaches—which route different tasks to models of varying sizes—are also ill-suited to this problem: they incur extra inference costs from redundant context re-encoding, cannot reuse KV cache across model switches, and face non-monotonic performance-cost relationships that are difficult to optimize.

---

## Limitations & Research Problem

**Key limitations of existing approaches**:

1. **Static effort policies are suboptimal**: Consistently applying low effort causes severe performance degradation (nearly 20% accuracy drop observed on gpt-oss-20b when switching from high to low effort at every step). Consistently applying high effort wastes tokens on simple steps.
2. **Random effort selection is ineffective**: Uniform random sampling across effort levels cannot meaningfully balance performance and cost.
3. **Model routing incurs overhead**: Traditional routing across heterogeneous models requires re-encoding context, prevents KV cache reuse, and adds latency—particularly costly for long multi-turn trajectories.
4. **Single-turn adaptive reasoning methods do not transfer**: Existing approaches that dynamically truncate or adjust reasoning trace length are designed for single-turn settings and do not account for error propagation across turns. A suboptimal effort allocation at an early step can cascade into failures at later steps, making global optimization significantly harder.
5. **Overthinking degrades performance**: In some domains (e.g., WebArena web navigation), excessive reasoning causes the agent to become overly divergent, producing incorrect action formats or losing task focus—the medium effort strategy actually outperforms high effort on TAU-Bench Airline.

**Core research question**: How can an LLM agent automatically select the most appropriate reasoning effort level at each individual decision step in a multi-step task, minimizing inference token consumption while preserving task success rate?

---

## Contributions

1. **ARES framework**: A plug-and-play, model-agnostic framework for per-step dynamic reasoning effort selection in multi-step LLM agent tasks. A lightweight router model (Qwen3-1.7B) is introduced alongside the agent to predict the minimum sufficient reasoning effort level (low/medium/high) for each upcoming step based on the current interaction history.

2. **Automated multi-phase data generation pipeline**: A three-phase pipeline that produces high-quality supervision for effort labels without manual annotation: (1) Trajectory Collection—collect successful trajectories with minimal steps; (2) Reasoning Effort Annotation—automatically identify the minimum sufficient effort for each step via multi-trial LLM verification; (3) Rationale Generation—synthesize semantic justifications from a teacher LLM to serve as chain-of-thought supervision for the router.

3. **Two-stage training: SFT + RL (GRPO)**: The router is first supervised-fine-tuned on the synthesized dataset to predict minimum sufficient effort labels. It is then further optimized via Group Relative Policy Optimization (GRPO) with a composite reward capturing task success, per-step reasoning cost, and output format compliance. The RL stage enables the router to learn globally optimal effort allocation strategies that account for multi-turn dynamics and error recovery.

4. **Empirical validation across three agent domains**:
   - TAU-Bench (tool-use agents): reasoning token consumption reduced by **35.2%**, task performance matches high-effort baseline (54.8%)
   - BrowseComp-Plus (deep-research agents): token consumption reduced by **41.8%**, accuracy 41.3% (vs. high-effort ceiling 42.7%)
   - WebArena (web navigation agents): token consumption reduced by **45.3%**, task success rate 46.5% (exceeds high-effort baseline 45.0%)
   - RL further improves: TAU-Bench Retail success rate rises to 58.5%; total tokens reduced by an additional 176k vs. SFT

5. **Cross-scale generalization**: ARES trained on gpt-oss-20b trajectories generalizes to gpt-oss-120b (6x larger backbone), achieving 65.2% accuracy (vs. 67.8% high-effort ceiling) with ~23% fewer tokens—demonstrating scale-invariant transferability of learned reasoning patterns.

---

## Methodology

### Problem Formulation

Agent task as sequential decision-making: at each turn $t$, the LLM agent $\mathcal{M}_\text{agent}$ (parameters $\phi$) takes action $a_t \sim P_\phi(a_t \mid h_t, o_t, e_t)$ given interaction history $h_t = (x, o_1, a_1, \ldots, o_{t-1}, a_{t-1})$, current observation $o_t$, and reasoning effort level $e_t \in \mathcal{E} = \{e_\text{low}, e_\text{mid}, e_\text{high}\}$.

The router $\mathcal{M}_\text{router}$ (parameters $\theta$) receives the same context as the agent and directly predicts the optimal $e_t$. The optimization objective is:

$$\max_\theta \mathbb{E}_{x, \mathcal{X}, \tau \sim \mathcal{T}(\theta, \phi)} \left[ \mathcal{V}(\tau, x) - \lambda \sum_{t=1}^T \text{cost}(e_t) \right]$$

where $\mathcal{V}(\tau, x) \in \{0,1\}$ is task success and $\text{cost}(e_t)$ is the total tokens generated at turn $t$.

### Three-Phase Data Generation Pipeline

**Phase 1 - Trajectory Collection**: For each training task $x$, sample $N$ successful trajectories using the agent at maximum effort $e_\text{high}$. Select the most concise trajectory $\tau^* = (o_1, a_1^*, \ldots, o_T, a_T^*)$ (fewest steps) as the reference path. Concise trajectories (i) minimize total reasoning cost inflation and (ii) isolate the step-wise minimum effort requirement by fixing the action sequence.

**Phase 2 - Reasoning Effort Annotation**: For each step $t$ in $\tau^*$, determine the minimum sufficient effort level. For each candidate $e \in \{e_\text{low}, e_\text{mid}, e_\text{high}\}$, sample $K=3$ agent responses and apply a verification function $\mathcal{V}(\hat{a}, a_t^*)$. An effort level is "sufficient" if it reliably reproduces the correct action $a_t^*$ in a majority of trials. The effort label $y_t$ is the lowest sufficient level. Steps where no effort level passes verification are discarded to maintain data quality. Verification criteria are domain-specific: tool-use agents require exact tool name and parameter matching; web agents require exact environmental interaction; deep-research agents use LLM-as-judge for semantic equivalence of search queries.

**Phase 3 - Rationale Generation**: A powerful teacher LLM (GPT-5) is given the interaction history, current observation, and ground-truth effort label $y_t$, and tasked with generating a brief reasoning rationale $r_t$ (3–5 sentences) that: (1) tracks current task progress, (2) analyzes the complexity of the next sub-task, and (3) justifies why $y_t$ is the appropriate effort level. A strict length constraint ensures the router's own reasoning does not introduce significant latency overhead.

**Supervised Fine-tuning (SFT)**: Fine-tune the lightweight router (Qwen3-1.7B) on the augmented dataset $\mathcal{D} = \{(h_t, o_t, r_t, y_t)\}$ using standard next-token prediction loss. The model is trained to first generate the rationale $r_t$ (within `<think>` tags) and then output the discrete effort label $y_t$. SFT hyperparameters: 3 epochs, learning rate 5e-6, batch size 64, warmup ratio 0.1, max prompt/response lengths 4,096/512 tokens.

### Reinforcement Learning Stage (GRPO)

**Motivation**: SFT has two shortcomings: (1) it assumes all preceding steps were assigned optimal effort (no training signal for recovery from sub-optimal prior selections); (2) it provides only a single effort label per query, lacking contrastive signals across different selection sequences at the trajectory level.

**Router Rollout**: During RL, the router interacts with the agent and environment over full trajectories. At each turn $t$, the router takes history $h_t$ and observation $o_t$ as input to produce: (a) a rationale $r_t$ and (b) an effort prediction $e_t$. The agent then executes its action at effort level $e_t$.

**Composite Reward Function** $R(\tau)$:

- **Outcome Reward** $R_\text{out}$: +5.0 if task is successful, 0.0 otherwise. Cost penalties apply only to successful trajectories to prevent the router from learning to fail quickly.
- **Reasoning Cost Reward** $R_\text{cost}$: per-step penalty $c(e_t) = -0.2$ (low), $-0.5$ (mid), $-1.0$ (high); trajectory-averaged and normalized. Normalization is critical: it correctly incentivizes reliance on medium effort when that is the optimal strategy for the domain.
- **Format Reward** $R_\text{form}$: $-1.0$ if the prescribed output format is violated; rollout is immediately terminated and marked as failure.

**RL Data Filtering** (two-stage):
1. Zero-Success Filtering: discard prompts with 0% success rate across N=8 rollouts (task is unsolvable regardless of effort).
2. Variance-Based Efficiency Selection: for prompts with 100% success rate, retain only those whose reward variance falls in the top 30%—these are prompts where multiple effort strategies succeed but with substantially different costs, providing the strongest learning signal for efficiency optimization.

**RL Training**: GRPO with G=16 outputs per prompt; base model initialized from SFT checkpoint; 5 epochs, batch size 32, learning rate 1.5e-6, KL coefficient 0.01.

### Key Design Insights

- **Rationale generation improves accuracy**: Ablating the rationale (direct label prediction without chain-of-thought) causes a 3.5% accuracy drop, confirming that explicit analysis of task difficulty functions as a necessary cognitive bridge between context and effort label.
- **Reward normalization is critical**: Normalized cost reward reduces high-effort selection ratio from ~30% to ~15% during RL training on TAU-Bench Airline, while simultaneously improving task accuracy—outperforming the unnormalized variant on both dimensions.
- **RL corrects overthinking bias**: On TAU-Bench Airline (where high effort yields lower accuracy than medium), the SFT-initialized router initially selects high effort for >50% of steps. GRPO training rapidly suppresses this to <20% while raising low-effort selection to ~70%, autonomously discovering and correcting the suboptimal over-deliberation behavior.
- **Effort correlates with action semantics**: Analysis of effort distribution by action type on WebArena reveals that `go_back` (strategic recovery from incorrect navigation path) and `branch` (substantive modification of navigation plan) actions require the highest proportion of high reasoning effort—consistent with their role as high-stakes error-correction decision points in the task trajectory.
- **KV cache advantage**: Because ARES operates within a single model's reasoning modes rather than routing across different models, KV cache can be preserved and reused across turns regardless of the selected effort level, eliminating the re-encoding overhead that burdens multi-model routing approaches.
