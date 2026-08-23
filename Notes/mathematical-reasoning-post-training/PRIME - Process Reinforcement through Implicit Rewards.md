# PRIME - Process Reinforcement through Implicit Rewards

## 主题/Topic: Implicit process reward RL

## 背景/Background

大型语言模型（LLM）在复杂多步推理任务中，inference-time scaling 依赖 dense process rewards（过程奖励）比 sparse outcome rewards（结果奖励）更为有效。在强化学习（RL）训练侧，dense rewards 理论上可以改善训练效率和 credit assignment 问题，但实际应用中收效甚微。核心挑战在于：在线训练 process reward model（PRM）时，获取高质量的 step-level 标注极为昂贵，既难以扩展，又容易导致 reward hacking。

## 现有局限与研究问题/Limitations & Research Problem

**现有方法的三大局限：**

1. **C1：Process rewards 难以定义。** 推理步骤在序列中没有自然边界，逐 token 标注代价高昂，且中间过程的正确性本身具有歧义性（错误步骤有时仍能引导出正确答案）。

2. **C2：PRM 在线更新不可扩展。** 防止 reward overoptimization 和 reward hacking 要求 reward model 与 policy model 同步在线更新，但传统 PRM 的在线更新需要大量 step-level 标注，既不高效也不可扩展。

3. **C3：显式 reward modeling 引入额外开销。** 训练专门的 reward model 需要大量标注数据和广泛的数据覆盖，还引入额外的训练阶段，成本极高。

**核心研究问题：** 如何以可扩展的方式获取并利用高质量 dense rewards，同时实现高效的在线 PRM 更新？

## 贡献/Contributions

1. **提出 PRIME 框架**：一种可扩展的在线 RL 方法，利用 implicit process rewards 实现 dense reward 的高效集成，无需单独训练专用 PRM。

2. **Implicit PRM 在线更新**：PRIME 仅用 outcome labels 和 policy rollouts 即可在线更新 Implicit PRM（Cross-Entropy loss），无需任何 step-level 标注，从根本上解决了 C1、C2。

3. **消除专用 reward modeling 阶段**：直接用 SFT 模型或 base 模型初始化 Implicit PRM，绕过了传统方法所需的专门 PRM 训练阶段（解决 C3），且实验显示直接从 SFT 初始化的 PRM 优于专门训练的 EurusPRM。

4. **通用性强**：PRIME 与多种 RL 算法兼容（RLOO、REINFORCE、PPO、GRPO），作为通用 plug-in 均能提升效率和性能。

5. **强劲实验结果**：从 Qwen2.5-Math-7B-Base 出发，PRIME 相比 SFT 模型在多项推理 benchmark 上平均提升 15.1%；最终模型 Eurus-2-7B-PRIME 仅用 Qwen-Math 10% 的训练数据即超越 Qwen2.5-Math-7B-Instruct。

## 方法论/Methodology

### 核心思想：Implicit Process Rewards

Implicit PRM 将 outcome reward model（ORM）在推理时复用为 PRM，其 token-level process reward 定义为：

$$r_\phi(y_t) := \beta \log \frac{\pi_\phi(y_t | \mathbf{y}_{<t})}{\pi_{\text{ref}}(y_t | \mathbf{y}_{<t})}$$

其中 $\pi_\phi$ 为 reward model（即 Implicit PRM），$\pi_{\text{ref}}$ 为参考模型。训练阶段与标准 ORM pipeline 相同，仅在推理时以此公式提取 token-level dense rewards，无需任何 step-level 标注。

### 训练流程（Algorithm 1）

1. 用 SFT 模型初始化 policy model $\pi_\theta$ 和 Implicit PRM $\pi_\phi$，reference model $\pi_{\text{ref}}$ 固定。
2. 每次迭代：从数据集采样 prompts，policy 对每个 prompt 生成 $K$ 个 responses。
3. 用 rule-based outcome verifier 计算 outcome rewards $r_o$。
4. 用 online prompt filtering（准确率范围过滤）筛选中等难度 prompts，平衡数据分布。
5. 用筛选后的数据对 Implicit PRM 进行 CE loss 在线更新：$\mathcal{L}_{CE}(\phi) = -\mathbb{E}[r_o(\mathbf{y}) \cdot \log \sigma(r_\phi(\mathbf{y})) + (1 - r_o(\mathbf{y})) \cdot \log(1 - \sigma(r_\phi(\mathbf{y})))]$
6. 计算 advantage：将 implicit process rewards 与 outcome rewards 的 returns 分别计算后相加（RLOO with LOO baseline）。
7. 用 PPO clip loss 更新 policy model。

### Advantage Estimation

结合 implicit process rewards 和 outcome rewards 分别计算 RLOO（leave-one-out）advantage 后求和：

$$A_t^i = \underbrace{\sum_{s=t}^{|\mathbf{y}^i|} \gamma^{s-t} \left[ r_\phi(y_s^i) - \frac{1}{K-1} \sum_{j \neq i} r_\phi(\mathbf{y}^j) \right]}_{\text{RLOO with implicit process rewards}} + \underbrace{r_o(\mathbf{y}^i) - \frac{1}{K-1} \sum_{j \neq i} r_o(\mathbf{y}^j)}_{\text{RLOO with outcome rewards}}$$

### 关键设计选择

- **SFT 初始化 PRM**：直接用策略模型的 SFT checkpoint 初始化 Implicit PRM，无需额外训练，且能缓解 distribution shift 问题（PRM 只在 policy 的 on-policy rollouts 上更新）。
- **Online vs. Offline PRM**：实验表明 offline PRM 因 distribution shift 逐渐过优化，而 online PRM 持续提升准确率，验证在线更新的必要性。
- **PRM as reward model vs. value model**：实验表明将 Implicit PRM 用作 reward model（计算 returns）优于用作 value model（计算 baseline），且优于线性头 value model（PPO）。
- **Online Prompt Filtering**：过滤掉极易和极难的 prompts，保留中等难度样本，降低训练方差并平衡 Implicit PRM 的训练数据分布。

### 实验结果

- Eurus-2-7B-PRIME 在 7 项推理 benchmark（AIME 2024、AMC、MATH-500、MinervaM ath、OlympiadBench、LeetCode、LiveCodeBench）上平均得分 41.0，超越 GPT-4o（45.6 avg 但在 AMC/AIME 上不及）和 Qwen2.5-Math-7B-Instruct。
- 相比仅用 outcome rewards 的 RLOO，PRIME 实现 2.5× 样本效率提升和 6.9% 性能提升。
- PRIME 对 REINFORCE、GRPO、PPO 均有一致性提升，证明其通用性。
