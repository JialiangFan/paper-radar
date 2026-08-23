# LLM 后训练：推理、规划与安全

> 文献综述 — 适用于学术汇报 PPT

| Research Topic | Paper Number | PDF Files |
|---|---|---|
| 过程奖励建模 (Process Reward Modeling) | 4 | 2502.01456v2.pdf (PRIME), 2510.11457v1.pdf (DRM), 2506.18896v2.pdf (ReasonFlux-PRM), 2024.emnlp-main.20.pdf (Jiao et al.) |
| 基于搜索的 LLM 规划 (Search-Based LLM Planning) | 3 | 2023.emnlp-main.507.pdf (RAP), 2512.23167v1.pdf (SPIRAL), 2410.20007v1.pdf (CoPlanner) |
| LLM 推理与规划的安全性 (Safety in LLM Reasoning & Planning) | 2 | 2503.06892v1 (1).pdf (SafePlan), 4405_Towards_Safe_Reasoning_in.pdf (IPO) |
| CoT 推理的有效性分析与改进 (CoT Effectiveness & Improvement) | 2 | NeurIPS-2024-chain-of-thoughtlessness-...pdf (Chain of Thoughtlessness), 20208_Teaching_LLMs_to_Plan_Lo.pdf (PDDL-Instruct) |
| **总计** | **11** | |

---

# Part 1. 文献分类 (Literature Taxonomy)

---

## Theme 1: 过程奖励建模 (Process Reward Modeling)

**Papers:**
- PRIME — Process Reinforcement through Implicit Rewards (2025)
- DRM — From \<Answer\> to \<Think\>: Multidimensional Supervision of Reasoning Process (2025)
- ReasonFlux-PRM — Trajectory-Aware PRMs for Long CoT Reasoning (2025)
- Jiao et al. — Learning Planning-based Reasoning via Trajectories Collection and Process Reward Synthesizing (EMNLP 2024)

**主题概述：**
这一类工作关注如何为 LLM 推理过程提供细粒度的步骤级反馈信号，而无需昂贵的人工标注。四篇论文提出了不同的自动化过程监督方案：从结果标注合成（Jiao et al.）、模型 logprob 隐式推导（PRIME）、多维度评估（DRM）到轨迹级上下文建模（ReasonFlux-PRM）。它们的共同结论是：过程监督显著优于结果监督，但标注瓶颈必须通过自动化解决。

---

## Theme 2: 基于搜索的 LLM 规划 (Search-Based LLM Planning)

**Papers:**
- RAP — Reasoning with Language Model is Planning with World Model (EMNLP 2023)
- SPIRAL — Symbolic LLM Planning via Grounded and Reflective Search (AAAI 2025)
- CoPlanner — Cooperative Strategic Planning Enhances Reasoning Capabilities in LLMs (2024)

**主题概述：**
这一类工作探索如何在 LLM 中实现真正的多步规划，超越自回归生成的局限。RAP 奠定了"LLM 即世界模型 + MCTS"的范式；SPIRAL 通过三智能体认知架构和反思驱动奖励塑造进一步推进；CoPlanner 则通过分离规划智能体与推理智能体实现协作。核心思路都是：通过结构化搜索弥补 LLM 缺乏前瞻和回溯能力的不足。

---

## Theme 3: LLM 推理与规划的安全性 (Safety in LLM Reasoning & Planning)

**Papers:**
- SafePlan — Leveraging Formal Logic and CoT Reasoning for Enhanced Safety in LLM-based Robotic Task Planning (2025)
- IPO — Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention (ICLR 2026)

**主题概述：**
这两篇论文分别从推理时和训练时两个角度解决 LLM 推理的安全性问题。SafePlan 在推理阶段通过形式化逻辑（LTL）和结构化 CoT 进行多层安全验证；IPO 在训练阶段通过识别推理轨迹中的"安全触发点"和"顺从线索"，利用 DPO 进行对齐。两者互补：理想情况下应同时部署训练时和推理时的安全保障。

---

## Theme 4: CoT 推理的有效性分析与改进 (CoT Effectiveness & Improvement)

**Papers:**
- Chain of Thoughtlessness — An Analysis of CoT in Planning (NeurIPS 2024)
- PDDL-Instruct — Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning (ICLR 2026, under review)

**主题概述：**
这两篇论文构成一组"问题—解决方案"的对话。Chain of Thoughtlessness 提供了严谨的负面结论：CoT 不能诱导真正的算法推理，本质是模式匹配。PDDL-Instruct 则给出了回应：通过结合形式化验证器（VAL）的指令微调，CoT 可以有效提升符号规划能力。二者共同说明：原始 CoT 不够，但结构化 CoT + 验证反馈可以奏效。

---

# Part 2. 代表性论文深度解读 (Representative Paper Deep Dive)

---

## Theme 1: 过程奖励建模

### 代表性论文
**PRIME: Process Reinforcement through Implicit Rewards**

### 发表信息
- **标题:** Process Reinforcement through Implicit Rewards
- **作者:** Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Wenjie Li, Bingxiang He, Quanquan Gu, Huishuai Zhang, Ningyu Zhang, et al.
- **发表:** arXiv 2502.01456v2, 2025
- **类型:** Preprint

### 建议截图材料

- **Screenshot 1:** 论文首页（标题 + 作者列表）
  - 用途：介绍论文基本信息
  - 位置：第 1 页

- **Screenshot 2:** Implicit PRM 与 Explicit PRM 的对比框架图
  - 用途：直观展示隐式奖励 vs 显式奖励的区别，以及在线更新机制
  - 位置：约第 3-4 页（方法部分）

- **Screenshot 3:** 各 benchmark 的性能对比表
  - 用途：展示 15.1% 平均提升的实验结果
  - 位置：约第 6-7 页（实验部分）

---

### 背景

传统的过程奖励模型（PRM）需要大量步骤级标注数据来训练，这些标注通常由人工完成，成本高昂且存在噪声。即使使用 Monte Carlo 采样等自动化方法，PRM 仍然需要单独训练，且存在策略模型更新后 PRM 过时（reward hacking）的问题。

此外，已有的结果奖励模型（ORM）只提供最终答案的对/错反馈，无法指导推理过程中间步骤的改进，这导致 RL 训练效率低下。

---

### 研究问题

> 能否在不训练独立 PRM 的情况下，从策略模型自身获取密集的过程级奖励信号，从而实现高效的推理 RL 训练？

---

### 核心贡献

- **Contribution 1:** 提出隐式过程奖励——直接从策略模型和参考模型的 token 级 logprob 比值推导步骤级奖励，无需任何标注
- **Contribution 2:** 实现在线 PRM 更新——隐式奖励随策略模型同步更新，天然避免 reward hacking
- **Contribution 3:** 即插即用设计——可无缝集成到 REINFORCE、GRPO、PPO 等任意策略梯度算法中
- **Contribution 4:** 在数学和编程 benchmark 上平均提升 15.1%

---

### 方法

#### 整体思路

PRIME 的核心洞察是：策略模型在每个推理步骤上的 logprob 变化本身就编码了该步骤的"奖励"信息。通过计算策略模型与参考模型之间的 token 级 logprob 比值，可以得到隐式过程奖励，用于 RL 训练。

#### 核心组件

- **Implicit PRM:** 利用 $\log \frac{\pi_\theta(a|s)}{\pi_{ref}(a|s)}$ 计算每步隐式奖励，无需额外模型
- **Online Update:** 隐式奖励与策略模型同步更新，不存在 PRM 滞后问题
- **KL-Regularized Reward:** 在奖励中加入 KL 正则项，平衡探索与利用

#### 训练 / 优化

- **Training Objective:** 策略梯度 + 隐式过程奖励（RLOO 变体）
- **Reward Signal:** Token 级 logprob 比值的步骤级聚合
- **Inference Workflow:** 推理时不需要额外的 PRM，直接使用策略模型生成

---

### 关键要点

- 最重要的 insight：过程奖励可以"免费"获取，不需要任何额外标注或模型训练
- 相比同主题论文（DRM、ReasonFlux-PRM），PRIME 最轻量——不需要训练任何额外模型
- 在线更新机制天然解决了 reward hacking 问题，这是显式 PRM 的常见痛点
- 局限：隐式奖励假设可加性可能不适用于所有推理场景；评估集中在数学/代码领域

---

## Theme 2: 基于搜索的 LLM 规划

### 代表性论文
**SPIRAL: Symbolic LLM Planning via Grounded and Reflective Search**

### 发表信息
- **标题:** SPIRAL: Symbolic LLM Planning via Grounded and Reflective Search
- **作者:** Wenhan Luo, Zhengyi Lu, Weichuan Liu, et al.
- **发表:** AAAI 2025
- **类型:** Conference Paper

### 建议截图材料

- **Screenshot 1:** 论文首页（标题 + AAAI 2025）
  - 用途：介绍论文基本信息
  - 位置：第 1 页

- **Screenshot 2:** 三智能体（Planner-Simulator-Critic）+ MCTS 的整体框架图
  - 用途：这是论文最核心的贡献可视化，清晰展示认知架构
  - 位置：约第 3-4 页

- **Screenshot 3:** DailyLifeAPIs 和 HuggingFace benchmark 的性能对比表
  - 用途：展示 83.6% 准确率和超越 LATS 16pp 的结果
  - 位置：约第 6-7 页

---

### 背景

已有的 LLM 规划方法（如 RAP、LATS、ToT）虽然利用了树搜索，但存在两个关键缺陷：(1) 搜索过程缺乏接地（grounding），无法准确模拟动作的实际效果；(2) 奖励信号稀疏，仅依赖最终结果反馈，导致搜索效率低下。

---

### 研究问题

> 如何通过接地模拟和反思反馈，让 LLM 在 MCTS 规划中获得更准确的状态转移和更密集的奖励信号？

---

### 核心贡献

- **Contribution 1:** 提出三智能体认知架构（Planner + Simulator + Critic）嵌入 MCTS
- **Contribution 2:** Simulator 作为世界模型，提供接地的状态转移模拟
- **Contribution 3:** Reflection-Driven Reward Shaping：$R_t = \alpha R_{base}(a_t) + (1-\alpha)\rho_{ref}$，结合基础奖励和反思评分

---

### 方法

#### 整体思路

SPIRAL 将 MCTS 中的每个搜索步骤分配给三个专门的智能体：Planner 提出候选动作，Simulator 模拟执行后的状态转移（世界模型），Critic 提供战略级反思反馈。

#### 核心组件

- **Planner Agent:** 基于当前状态提出候选动作
- **Simulator Agent:** 模拟动作执行后的环境状态变化，提供接地验证
- **Critic Agent:** 评估当前规划质量，生成反思评分 $\rho_{ref}$

#### 训练 / 优化

- **Training Objective:** 无需训练——纯推理时框架
- **Reward Signal:** Reflection-Driven Reward Shaping 结合 base reward 和 critic reflection score
- **Inference Workflow:** MCTS 搜索，每个节点扩展由三个 LLM 调用完成

---

### 关键要点

- 核心 insight：在 MCTS 中引入接地模拟（Simulator）和密集反思反馈（Critic）可以显著提升搜索质量
- 相比 RAP 和 LATS：SPIRAL 在 DailyLifeAPIs 上领先 16 个百分点，且 token 效率更优
- 三智能体架构的思想与认知科学中的系统 1/2 思维框架相呼应
- 局限：每步需要 3 次 LLM 调用，计算开销大；仅在 API 调用域上评估

---

## Theme 3: LLM 推理与规划的安全性

### 代表性论文
**IPO: Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention**

### 发表信息
- **标题:** Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention
- **作者:** Yuntao Liu, Zhangchen Xu, Jianwei Yin, et al.
- **发表:** ICLR 2026
- **类型:** Conference Paper

### 建议截图材料

- **Screenshot 1:** 论文首页（标题 + ICLR 2026）
  - 用途：介绍论文基本信息
  - 位置：第 1 页

- **Screenshot 2:** Safety Trigger 和 Compliance Cue 的推理轨迹分析图
  - 用途：这是论文最核心的发现的可视化——展示推理轨迹中安全相关的关键节点
  - 位置：约第 4-5 页

- **Screenshot 3:** IPO 方法流程图（识别→替换→DPO 训练）
  - 用途：展示 Corrective Intervention 的完整 pipeline
  - 位置：约第 5-6 页

---

### 背景

大推理模型（Large Reasoning Models, LRMs）如 DeepSeek-R1 通过扩展推理链（extended thinking）显著提升了推理能力，但也带来了新的安全风险：更长的推理过程中可能出现"顺从线索"（compliance cues），引导模型逐步偏向不安全输出。传统的安全对齐方法（如 RLHF/DPO）主要针对最终输出，无法干预推理过程本身。

---

### 研究问题

> 如何在不损害推理能力的前提下，通过干预推理轨迹中的关键节点来提升大推理模型的安全性？

---

### 核心贡献

- **Contribution 1:** 发现推理轨迹中存在"安全触发点"（safety triggers）和"顺从线索"（compliance cues）两类关键结构
- **Contribution 2:** 提出 Continuation Safety Ratio (CSR) 指标量化推理轨迹的安全性
- **Contribution 3:** 提出 Intervened Preference Optimization (IPO)——通过替换 compliance cues 为 safety triggers 构造偏好对，再用 DPO 训练

---

### 方法

#### 整体思路

IPO 首先分析推理轨迹，识别两类关键推理步骤：safety triggers（使 CSR 上升到 100% 的步骤）和 compliance cues（与不安全转折点高度相关的步骤，Pearson R=0.853）。然后将 compliance cues 替换为 safety triggers，构造偏好数据对，最后用 DPO 在部分轨迹上进行训练。

#### 核心组件

- **Safety Trigger Identification:** 找到推理轨迹中巩固安全推理的关键步骤
- **Compliance Cue Detection:** 找到信号顺从（导向不安全输出）的推理步骤
- **Corrective Intervention:** 将不安全轨迹中的 compliance cues 替换为 safety triggers

#### 训练 / 优化

- **Training Objective:** DPO loss on partial trajectory preference pairs
- **Reward Signal:** 偏好对来自 corrective intervention 构造（无需额外奖励模型）
- **Inference Workflow:** 训练后直接使用，无额外推理时开销

---

### 关键要点

- 最重要的 insight：推理轨迹不是"黑盒"——其中存在可识别的安全关键结构，可以精准干预
- 相比 SafePlan（推理时验证），IPO 是训练时方案，无推理时延开销
- >30% 有害性降低的同时保持甚至提升推理能力，证明安全与能力不必矛盾
- 局限：安全触发点的识别方法可能不适用于所有攻击类型；仅在 7B-8B 模型上验证

---

## Theme 4: CoT 推理的有效性分析与改进

### 代表性论文
**PDDL-Instruct: Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning**

### 发表信息
- **标题:** Teaching LLMs to Plan: Logical Chain-of-Thought Instruction Tuning for Symbolic Planning
- **作者:** Anonymous (under review)
- **发表:** ICLR 2026 (under review)
- **类型:** Conference Paper (under review)

### 建议截图材料

- **Screenshot 1:** 论文首页
  - 用途：介绍论文基本信息
  - 位置：第 1 页

- **Screenshot 2:** 两阶段指令微调流程图（Phase 1 + Phase 2 with VAL verifier）
  - 用途：这是论文的核心方法可视化
  - 位置：约第 3-5 页

- **Screenshot 3:** Blocksworld 上 94% 准确率的对比实验图
  - 用途：展示 +66% 提升的核心结果
  - 位置：约第 6-8 页

---

### 背景

Chain of Thoughtlessness (NeurIPS 2024) 已经证明：标准 CoT 提示不能诱导 LLM 真正的算法推理——改进仅在高度特定的提示下出现，且随问题规模增大而衰减。这意味着 LLM 在符号规划任务上需要更根本的训练方法，而非仅靠提示工程。

---

### 研究问题

> 如何通过结合形式化验证器反馈的指令微调，教会 LLM 真正的符号规划能力？

---

### 核心贡献

- **Contribution 1:** 两阶段指令微调框架——Phase 1（正确/错误规划 + 解释）+ Phase 2（CoT + VAL 验证器反馈循环）
- **Contribution 2:** 在 Blocksworld 上达到 94% 规划准确率（基线 Llama-3-8B 提升 66%）
- **Contribution 3:** 跨域泛化——无需域特定重训练即可迁移到 Mystery Blocksworld、Logistics

---

### 方法

#### 整体思路

PDDL-Instruct 将形式化规划验证器（VAL）引入 LLM 的指令微调过程。Phase 1 让模型学习区分正确和错误的规划并理解原因；Phase 2 让模型在迭代验证反馈循环中从自身错误中学习。

#### 核心组件

- **Phase 1 (Initial IT):** 在正确/错误规划对上训练，附带自然语言解释
- **Phase 2 (CoT IT):** 迭代式 CoT 微调，每轮通过 VAL 验证器检查规划正确性并提供反馈
- **VAL Verifier:** 形式化规划验证器，提供 binary 或 detailed 反馈（detailed 效果更好）

#### 训练 / 优化

- **Training Objective:** 标准语言模型微调 loss（两个阶段）
- **Reward Signal:** VAL 验证器提供的正确性反馈（作为训练数据而非显式奖励）
- **Inference Workflow:** 微调后直接生成规划，可选择性使用 VAL 做后验证

---

### 关键要点

- 核心 insight：形式化验证器反馈是让 CoT 在规划任务上真正有效的关键——回应了 Chain of Thoughtlessness 的负面结论
- 详细反馈（detailed feedback）一致优于二元反馈（binary feedback），说明信息丰富的误差信号对规划学习至关重要
- 跨域泛化能力说明模型学到的是规划推理的一般能力，而非特定域的模式
- 局限：需要 PDDL 形式化表示；仅在符号规划域上验证；模型规模较小

---

# Part 3. 跨论文综合分析 (Cross-Paper Insights)

---

## 整体研究趋势

- **从结果监督到过程监督：** 领域正在从 ORM 向 PRM 转移（PRIME, DRM, ReasonFlux-PRM, Jiao et al.），提供更密集、更有指导性的训练信号
- **从单体推理到多智能体协作：** CoPlanner 和 SPIRAL 表明，将推理分解为专门角色（规划者/执行者/批评者）能提升性能
- **从提示工程到训练内化：** Chain of Thoughtlessness 证明 CoT 提示的局限性，推动了 PDDL-Instruct 等通过训练内化推理能力的方法
- **安全对齐深入推理过程：** IPO 开创了对推理轨迹本身进行安全对齐的范式，而非仅对齐最终输出
- **经典 AI 方法的回归：** MCTS（RAP, SPIRAL）、LTL（SafePlan）、PDDL（PDDL-Instruct）等经典形式化方法与神经网络 LLM 的融合日益紧密

---

## 共同模式

### 常见方法框架
- **DPO 作为对齐基础设施：** Jiao et al.、DRM、IPO 都使用 DPO 但构造偏好对的方式各异
- **MCTS 作为推理搜索框架：** RAP → SPIRAL 构成了搜索式规划的演进链
- **形式化验证器在循环中：** VAL（PDDL-Instruct）、Simulator（SPIRAL）、LTL（SafePlan）——验证反馈是提升推理质量的共同模式

### 常见训练方式
- **RL 训练：** PRIME (RLOO), CoPlanner (PPO), DRM (GRPO), ReasonFlux-PRM (GRPO)
- **偏好优化：** Jiao et al. (DPO), DRM (DPO), IPO (DPO)
- **指令微调：** PDDL-Instruct（两阶段 IT）

### 常见实验设计
- **数学推理 benchmark：** MATH-500, AIME 2024, GSM8K（PRIME, DRM, ReasonFlux-PRM, Jiao et al., IPO）
- **规划 benchmark：** Blocksworld（RAP, Chain of Thoughtlessness, PDDL-Instruct）
- **小模型 vs 大模型对比：** 多篇论文展示 7-8B 模型超越 GPT-3.5/GPT-4

---

## 主题间差异

| 维度 | 过程奖励建模 | 搜索式规划 | 安全对齐 | CoT 分析与改进 |
|------|-------------|-----------|---------|---------------|
| **问题定义** | 如何获取步骤级奖励 | 如何实现多步规划 | 如何保证安全性 | CoT 是否/如何有效 |
| **方法类型** | 奖励模型设计 + RL | 搜索算法 + 多智能体 | 形式逻辑 / 偏好优化 | 实证分析 / 指令微调 |
| **训练信号** | 隐式/合成过程奖励 | 搜索启发式 | 安全偏好对 / 形式逻辑 | 验证器反馈 |
| **应用场景** | 数学、代码推理 | API 调用、逻辑推理 | 机器人任务、通用安全 | 符号规划 |
| **评估重点** | 推理准确率 | 规划成功率 | 有害性降低率 | 泛化性分析 |

---

## 启发与思考

- **过程奖励的"免费午餐"：** PRIME 证明了隐式奖励可以无标注获取，这一思路是否可以推广到安全对齐领域？例如，是否存在安全相关的隐式信号？
- **验证驱动的推理改进：** PDDL-Instruct、SPIRAL、SafePlan 都依赖某种形式的验证。这暗示了一个通用范式：**生成-验证-修正**循环可能是提升 LLM 推理的核心机制。
- **安全与能力的解耦：** IPO 表明安全对齐可以精准作用于推理轨迹中的特定节点而不损害整体能力。这为"对齐税"问题提供了新的解决思路。
- **小模型的逆袭：** RAP（33B > GPT-4）、Jiao et al.（7B > GPT-3.5）、PDDL-Instruct（8B 达 94%）——结构化推理支持可以替代模型规模，这对资源受限场景意义重大。
- **CoT 的正确打开方式：** Chain of Thoughtlessness 否定了原始 CoT，PDDL-Instruct 给出了修正方案——CoT 需要配合训练和验证才能发挥作用。

---

## 开放问题

1. **跨域过程奖励模型：** 当前 PRM（PRIME, DRM, ReasonFlux-PRM）主要在数学/代码上验证，能否迁移到开放域推理（如常识推理、伦理判断）？

2. **搜索效率与实用性：** SPIRAL 和 RAP 的搜索方法效果好但计算开销大，如何在保持质量的前提下降低推理时搜索成本？

3. **安全对齐的鲁棒性：** IPO 的 safety trigger/compliance cue 识别方法是否能应对新型攻击？安全触发点的分布在更大模型上是否一致？

4. **形式化方法的可扩展性：** SafePlan（LTL）和 PDDL-Instruct（PDDL）都依赖形式化表示，如何将其扩展到无法轻易形式化的现实世界任务？

5. **过程监督 + 搜索 + 安全的统一框架：** 目前三个主题相对独立，是否可能设计一个统一框架，同时提供密集过程奖励、结构化搜索和安全保障？

6. **推理长度与质量的关系：** IPO 发现更长的推理链可能引入安全风险，Chain of Thoughtlessness 发现更长的 CoT 不一定更好——推理链的"最优长度"如何确定？
