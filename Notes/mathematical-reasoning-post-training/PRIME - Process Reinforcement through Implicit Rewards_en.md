# PRIME - Process Reinforcement through Implicit Rewards

## Topic: Implicit Process Reward RL

## Background

Dense process rewards — feedback provided at each intermediate reasoning step rather than only at the end of a trajectory — have proven more effective than sparse outcome rewards for inference-time scaling of large language models (LLMs) on complex multi-step reasoning tasks. On the training side, dense rewards are theoretically appealing for reinforcement learning (RL) of LLMs because fine-grained token-level feedback can improve sample efficiency and address the credit assignment problem inherent in sparse outcome rewards. However, successful large-scale applications of dense rewards in RL for LLMs have remained elusive, primarily because collecting the high-quality process labels required to train process reward models (PRMs) online is prohibitively expensive and not scalable, making these models particularly vulnerable to reward hacking under distribution shift.

## Limitations & Research Problem

The incorporation of dense rewards into online RL for LLMs faces three fundamental challenges:

**C1. Process rewards are hard to define.** Reasoning steps do not occur at natural boundaries in token sequences, making it too costly to annotate labels for every token. Furthermore, the absolute correctness of intermediate steps is inherently ambiguous — some incorrect reasoning steps can still guide the model toward a correct final answer.

**C2. Online PRM updates are not scalable.** Preventing reward overoptimization and reward hacking requires the reward model to be updated online alongside the policy. However, updating PRMs online demands extensive step-level annotations on the latest policy rollouts, which is neither efficient nor scalable during RL training.

**C3. Explicit reward modeling introduces significant overhead.** Training a dedicated reward model requires broad annotated data coverage to balance adaptability to the evolving policy distribution and generalization. This necessitates an additional, costly data collection and training stage beyond the standard RL pipeline, which existing industry-leading models cite as a primary reason for not incorporating PRMs into large-scale RL training.

**Core Research Question:** How can high-quality dense rewards be obtained and utilized at scale to enable efficient online PRM updates in RL for LLMs, without the prohibitive cost of step-level annotation?

## Contributions

1. **PRIME framework:** A scalable online RL method that integrates dense token-level rewards into the policy optimization loop via implicit process reward modeling, requiring no step-level annotations and no dedicated PRM training stage.

2. **Implicit PRM online update with only outcome supervision:** PRIME updates the Implicit PRM online using only policy rollouts and outcome labels (binary correctness) via a cross-entropy loss. This is feasible because the Implicit PRM — trained as an outcome reward model — produces token-level process rewards at inference through its log-probability ratio relative to a reference model, addressing C1 and C2 simultaneously.

3. **Elimination of the dedicated reward modeling stage:** By initializing the Implicit PRM directly from the SFT model (or even the base model), PRIME bypasses the explicit PRM training stage required by existing approaches (addressing C3). Empirically, SFT-initialized Implicit PRMs outperform dedicated PRMs trained on additional step-level data, attributed to the mitigation of distribution shift when the PRM shares initialization with the policy.

4. **Algorithm generality:** PRIME is compatible with diverse RL algorithms (RLOO, REINFORCE, PPO, GRPO) as a plug-in modification to the advantage estimation function, consistently improving both sample efficiency and final performance across all tested algorithms.

5. **Strong empirical results:** Starting from Qwen2.5-Math-7B-Base with a lightweight SFT warmup, PRIME achieves a 15.1% average improvement across seven key reasoning benchmarks over the SFT model. The resulting model, Eurus-2-7B-PRIME, surpasses Qwen2.5-Math-7B-Instruct on seven reasoning benchmarks using only 10% of its training data, and achieves 26.7% pass@1 on AIME 2024, surpassing GPT-4o and Llama-3.1-70B-Instruct.

## Methodology

### Implicit Process Reward Modeling

The Implicit PRM repurposes a standard outcome reward model (ORM) as a process reward model at inference time. During training, the Implicit PRM $\pi_\phi$ is trained identically to a standard ORM using only outcome-level labels. At inference, token-level process rewards are extracted via the log-probability ratio:

$$r_\phi(y_t) := \beta \log \frac{\pi_\phi(y_t \mid \mathbf{y}_{<t})}{\pi_{\text{ref}}(y_t \mid \mathbf{y}_{<t})}$$

where $\pi_{\text{ref}}$ is a fixed reference model. This formulation derives from the implicit Q-function interpretation of reward-model training: optimizing the ORM objective implicitly learns a Q-function, from which token-level process rewards can be extracted without any step-level supervision.

### Online RL Training Loop (Algorithm 1)

**Initialization:** Both the policy model $\pi_\theta$ and the Implicit PRM $\pi_\phi$ are initialized from the same SFT model checkpoint. The reference model $\pi_{\text{ref}}$ is fixed at this checkpoint.

**Per-iteration procedure:**
1. Sample a batch of prompts $\mathcal{B}$ from the dataset.
2. Generate $K$ responses per prompt using the current policy $\pi_\theta$.
3. Compute outcome rewards $r_o$ using a rule-based outcome verifier (exact match for math; pass rate for code).
4. Apply **online prompt filtering**: retain only prompts where the accuracy across $K$ rollouts falls within a specified range, preserving medium-difficulty prompts. This reduces training variance and balances the data distribution for PRM updates.
5. **Update the Implicit PRM** $\pi_\phi$ via cross-entropy loss on the filtered data:
   $$\mathcal{L}_{\text{CE}}(\phi) = -\mathbb{E}_{(\mathbf{x}, \mathbf{y}, r_o(\mathbf{y}))} \left[ r_o(\mathbf{y}) \cdot \log \sigma(r_\phi(\mathbf{y})) + (1 - r_o(\mathbf{y})) \cdot \log(1 - \sigma(r_\phi(\mathbf{y}))) \right]$$
6. **Compute advantages** by combining implicit process reward returns and outcome reward returns.
7. **Update the policy** $\pi_\theta$ via PPO clip surrogate loss.

### Advantage Estimation

PRIME calculates returns from implicit process rewards and outcome rewards separately to avoid numerical instability from directly mixing their scales, then sums them as the final advantage:

$$A_t^i = \underbrace{\sum_{s=t}^{|\mathbf{y}^i|} \gamma^{s-t} \left[ r_\phi(y_s^i) - \frac{1}{K-1} \sum_{j \neq i} r_\phi(\mathbf{y}^j) \right]}_{\text{RLOO with implicit process rewards}} + \underbrace{r_o(\mathbf{y}^i) - \frac{1}{K-1} \sum_{j \neq i} r_o(\mathbf{y}^j)}_{\text{RLOO with outcome rewards}}$$

The leave-one-out (LOO) baseline is applied to both components to reduce variance. A three-step normalization procedure is applied to the process reward component: (1) subtract the LOO baseline; (2) normalize the process reward at each step by subtracting the mean; (3) compute discounted returns.

### Policy Update

Policy updates use the PPO clip surrogate loss:

$$L_{\text{CLIP}}(\theta) = \mathbb{E}_t \left[ \min\left( \frac{\pi_\theta(y_t | \mathbf{y}_{<t})}{\pi_{\theta_{\text{old}}}(y_t | \mathbf{y}_{<t})} A_t,\ \text{clip}\left(\frac{\pi_\theta(y_t | \mathbf{y}_{<t})}{\pi_{\theta_{\text{old}}}(y_t | \mathbf{y}_{<t})}, 1 - \epsilon, 1 + \epsilon\right) A_t \right) \right]$$

The KL coefficient is set to 0 in all experiments, as the clip loss suffices to constrain policy drift.

### Key Design Findings

- **SFT initialization outperforms dedicated PRMs:** Initializing both policy and PRM from the same SFT checkpoint largely mitigates distribution shift, as the PRM is trained exclusively on on-policy rollouts from that initialization. Counterintuitively, this simple initialization outperforms a PRM (EurusPRM) trained on substantially more step-level data.

- **Online update is essential to prevent reward hacking:** Offline PRMs — even those starting with higher initial accuracy — gradually suffer from reward overoptimization as the policy distribution shifts during RL training. Online PRMs trained on current policy rollouts maintain and improve accuracy throughout training.

- **PRMs as reward models outperform PRMs as value models:** Empirical comparison across four advantage estimation variants (REINFORCE, PPO with linear-head value model, Implicit PRM as value model, Implicit PRM as reward model) shows that using implicit process rewards to calculate discounted returns (reward model usage) consistently outperforms all value-model-based approaches, including standard PPO. This suggests that the inductive biases of PRMs are better suited to reward computation than to value estimation in LLM RL.

- **PRIME generalizes across RL algorithms:** Applied as a drop-in modification to REINFORCE, GRPO, and PPO (in addition to RLOO), PRIME consistently improves both sample efficiency and downstream task performance, demonstrating that its benefits are algorithm-agnostic.

### Experimental Setup

- **Base model:** Qwen2.5-Math-7B-Base with a lightweight SFT warmup stage.
- **Infrastructure:** 8×A800 GPUs using the veRL framework.
- **Hyperparameters:** AdamW optimizer with learning rate $5 \times 10^{-7}$ for policy, $10^{-6}$ for PRM; batch size 256; $K=4$ rollouts per prompt; $\beta=0.05$; KL coefficient 0.
- **Benchmarks:** AIME 2024, AMC, MATH-500, MinervaM ath, OlympiadBench, LeetCode, LiveCodeBench (v2).
- **Key results:** Eurus-2-7B-PRIME achieves an average of 41.0 across benchmarks at step 240, compared to 28.8 for the SFT baseline and 36.9 for RLOO with outcome verifier only. PRIME requires only 40% of the training steps of RLOO to achieve equivalent outcome training rewards, yielding an overall 2× training efficiency advantage when accounting for the 24% per-step overhead of PRM updates.
