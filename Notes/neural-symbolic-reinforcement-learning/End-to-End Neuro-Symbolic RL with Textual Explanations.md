# End-to-End Neuro-Symbolic RL with Textual Explanations

**论文:** Luo et al., ICML 2024 (PMLR 235)
**框架名称:** INSIGHT

## 主题
Explainable Neuro-Symbolic Reinforcement Learning

## 背景
Neuro-symbolic reinforcement learning (NS-RL) 通过使用 symbolic policies 来实现可解释的决策，是 deep RL 透明化的重要范式。然而，现有方法在处理视觉观测任务时，需要从像素中提取 structured state representations，早期方法（如基于 SPACE 模型）在 policy learning 阶段无法利用 reward signals 来优化状态表示，导致性能显著下降。此外，symbolic policies 本身虽然具有内在可解释性，但对于非专业用户而言仍然难以理解（需要一阶逻辑或特定语法知识），可访问性（accessibility）不足。

## 现有局限与研究问题
- **Limitation 1 (效率与性能):** 以往的 NS-RL 方法（如 Diffses/SPACE-Neural）使用图像重建目标提取 structured states，计算开销大且状态表示在 policy learning 期间固定不变，无法通过 reward signals 进行端到端优化，导致严重的性能退化。
- **Limitation 2 (可访问性):** Symbolic policies 虽然透明，但需要用户具备 first-order logic 或特定编程语法的专业知识才能解读，NS-RL 领域几乎没有面向非专业用户生成自然语言解释的工作。
- **Problem:** 如何设计一个既能端到端联合学习 structured states 和 symbolic policies、又能为非专业用户提供自然语言解释的高效 NS-RL 框架？

## 贡献
1. 提出 INSIGHT 框架：通过将 vision foundation models（FastSAM + DeAoT）蒸馏为高效的 perception module，实现 structured states 与 symbolic policies 的端到端联合学习，perception module 可在 policy learning 阶段通过 reward signals 持续优化。
2. 设计了基于 GPT-4 的 textual explanation pipeline：包含 concept grounding、policy interpretation 和 decision explanation 三个阶段，将 symbolic policies 转化为自然语言解释，显著降低用户理解门槛。
3. 在 9 个 Atari 游戏和 MetaDrive 自动驾驶任务上验证了框架有效性，INSIGHT 在所有任务上超越现有 NS-RL 方法，性能匹配甚至超过纯神经网络基线。

## 方法论

### 整体架构
INSIGHT 由三个模块组成：Visual Perception Module、Policy Learning Module、Policy Explanation Module。

### 3.1 Visual Perception Module
- **Frame-Symbol Dataset 构建:** 利用预训练神经 agent 采集约 10,000 帧图像，通过 FastSAM（分割）和 DeAoT（追踪）提取目标物体的 bounding boxes，得到 frame-symbol 数据集 D_symbol，包含物体的存在性、坐标（归一化到 [0,1]）和形状信息。
- **多任务感知模型:** 使用 CNN encoder 提取隐藏表示，三个 FCN heads 分别预测物体的 existence（用 distribution-balanced focal loss）、coordinates（L1 loss）和 size。
- **端到端优化:** Perception module 先在 D_symbol 上预训练，再在 policy learning 阶段通过 reward signals 继续微调（fine-tune），使其能捕获预训练阶段遗漏但对任务关键的特征。

### 3.2 Policy Learning Module（EQL + Neural Guidance）
- **EQL (Equation Learner) Network:** 以物体坐标为输入，通过包含多种激活函数（平方、立方、常数、恒等、乘法、加法）的网络层生成 symbolic expressions 作为 policy，辅以 sparsity regularization 保证表达式简洁。
- **Neural Guidance 机制:** 由于 EQL 表达力有限（坐标是 non-distributed representations），直接用 EQL 探索环境效果差。因此引入 neural actor (π_neural) 使用 encoder 的隐藏表示与环境交互，同时训练 EQL actor (π_EQL) 去逼近 π_neural 的动作分布（通过最小化 cross entropy L_ng）。两者同步训练（PPO + neural guidance + sparsity reg + CNN loss），显著提升采样效率。
- **训练策略:** 仅在最后一轮迭代中联合优化全部目标 L，其余迭代仅优化 L_ppo，避免对 perception module 施加过大的变化。

### 3.3 Policy Explanation Module（基于 GPT-4）
- **Concept Grounding:** 向 LLM 提供 task description（游戏目标、动作效果）和 policy description（坐标系、符号表达式含义），让 LLM 将符号量与语义关联。
- **Policy Interpretation:** 采用 chain-of-thought 策略，分三步分析 symbolic policy：输入变量 -> 中间变量 -> 动作 logits，并用预定义规则（如解释须基于 policy 表达式、概率须基于 logits）约束输出质量。
- **Decision Explanation:** 向 LLM 提供具体状态下的坐标值和动作 log-likelihood 的梯度信息，利用 sensitivity 分析解释特定决策的原因。

## 实验结果
- **任务性能:** 在 9 个 Atari 任务上，INSIGHT 全面超越所有 NS-RL baseline（CGP、Diffses、DSP、NUDGE），性能匹配纯 Neural baseline（Table 1）。在 MetaDrive 上同样优于 Neural 和 Coor-Neural baseline（Table 2）。
- **推理效率:** 推理速度（2ms/step on Pong）与纯 Neural 方法持平，比 SPACE-Neural 和 SA-Neural 快一个数量级（Table 3）。
- **消融实验:** End-to-end 微调（vs. Fixed）、预训练（vs. w/o Pretrain）、neural guidance（vs. w/o NG）均对性能有显著贡献（Figure 3）；对超参数具有较强鲁棒性（Figure 4）。
- **可解释性:** GPT-4 生成的 policy interpretation 和 decision explanation 对非专业用户友好，能正确识别关键变量和触发模式（Figure 5）。

## 局限性
- EQL 网络目前无法表达某些推理任务所需的逻辑运算。
- 缺乏对生成的 textual explanations 的定量评估方法。
