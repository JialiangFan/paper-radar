# ARES - Adaptive Reasoning Effort Selection

## 主题/Topic: Adaptive reasoning effort

**论文全名**: ARES: Adaptive Reasoning Effort Selection for Efficient LLM Agents
**作者**: Jingbo Yang, Bairu Hou, Wei Wei, Yujia Bao, Shiyu Chang
**机构**: UC Santa Barbara; Accenture Center for Advanced AI
**ArXiv**: 2603.07915v1 [cs.AI], 2026年3月9日
**代码**: https://github.com/UCSB-NLP-Chang/Ares

---

## 背景/Background

现代基于 thinking LLM 的 agent 通过长链式思维 (chain-of-thought, CoT) reasoning 实现高准确率，但产生大量 inference cost。许多前沿 LLM（如 GPT-5、Gemini-3）支持可配置的 reasoning effort（如 high/medium/low 或 thinking/fast 模式），允许用户按需调节推理深度与成本。

然而，主流做法是为 agent 的每个决策步骤统一设置固定的 reasoning effort level，这种静态策略无法适应不同步骤的实际复杂度。在多步骤 agent 任务中，不同步骤本质上具有不同的难度：简单的导航步骤（如打开某个页面）不需要深度推理，而复杂的规划或纠错步骤则需要高强度思考。此外，现有的 model routing 方法（将不同任务路由到不同规模模型）在多轮 agent 场景下面临 KV cache 无法复用、推理成本增加等问题。

---

## 现有局限与研究问题/Limitations & Research Problem

**现有局限**:

1. **静态 effort 策略失效**: 全程使用 low effort 导致性能严重下降（实验中 gpt-oss-20b 在每步从 high 切换为 low 时准确率下降近 20%）；全程 high effort 则产生大量不必要的 token 消耗。
2. **Random 策略无效**: 随机选择 effort level 无法有效平衡性能与成本。
3. **Model routing 的局限**: 传统 model routing 将任务路由到不同规模/架构的模型，需要重新编码上下文，无法复用 KV cache，引入额外推理开销；且不同模型间性能-成本关系非单调，难以优化。
4. **单轮自适应 reasoning 方法不适用**: 现有自适应 reasoning 方法（动态调整 reasoning trace 长度或截断中间思考）主要针对单轮任务，无法处理多轮 agent 任务中的误差传播问题——早期步骤的次优 effort 分配会影响后续步骤，使全局优化更为复杂。
5. **"Overthinking"问题**: 在部分任务（如 WebArena 网页导航）中，过度推理反而导致性能下降，agent 的思考过程变得过于发散，产生格式错误或任务偏移。

**核心研究问题**: 如何为多步骤 LLM agent 在每个决策步骤自动选择最合适的 reasoning effort level，在维持任务成功率的同时最小化推理 token 消耗？

---

## 贡献/Contributions

1. **提出 ARES 框架**: 一个针对多步骤 agent 任务的逐步动态 reasoning effort 选择框架，通过轻量级 router 模型（Qwen3-1.7B）为每个步骤预测最低充分的 reasoning effort level（low/medium/high）。

2. **多阶段自动数据生成 pipeline**: 设计了三阶段数据合成流程——(1) Trajectory Collection（收集高质量成功轨迹）、(2) Reasoning Effort Annotation（自动标注每步所需最低 effort）、(3) Rationale Generation（生成语义化推理依据），解决了 effort 标签难以直接获取的核心问题。

3. **SFT + RL 双阶段训练**: 先通过有监督微调 (SFT) 训练 router 预测最低充分 effort，再通过 GRPO 强化学习进一步优化，使 router 能捕捉多轮决策的全局动态，避免贪心 SFT 目标的局限性。

4. **实验验证**: 在 TAU-Bench（工具使用）、BrowseComp-Plus（深度研究）、WebArena（网页导航）三类 benchmark 上验证有效性：
   - TAU-Bench Retail: reasoning token 消耗减少 **35.2%**，性能持平 high effort 基线（54.8%）
   - BrowseComp-Plus: token 消耗减少 **41.8%**，准确率 41.3%（接近 high effort 的 42.7%）
   - WebArena: token 消耗减少 **45.3%**，成功率 46.5%（超越 high effort 基线 45.0%）
   - RL 进一步提升：TAU-Bench Retail 成功率提升至 58.5%，token 消耗相比 SFT 减少 176k

5. **跨模型泛化**: 在 gpt-oss-120b（训练于 gpt-oss-20b 轨迹）上验证了 scale-invariant 泛化能力，准确率 65.2%，接近 high effort 基线（67.8%），token 消耗减少约 23%。

---

## 方法论/Methodology

### 问题形式化

将 agent 任务形式化为序列决策过程：agent $\mathcal{M}_\text{agent}$（参数 $\phi$）在每个时刻 $t$ 根据交互历史 $h_t = (x, o_1, a_1, \ldots, o_{t-1}, a_{t-1})$ 和当前观测 $o_t$ 生成动作 $a_t$。LLM 的 reasoning level $e_t \in \mathcal{E} = \{e_\text{low}, e_\text{mid}, e_\text{high}\}$ 可配置。

Router $\mathcal{M}_\text{router}$（参数 $\theta$）接收与 agent 相同的上下文输入，预测最优 effort level $e_t$。优化目标为在确保任务成功的前提下最小化累积 inference cost：

$$\max_\theta \mathbb{E}_{x, \mathcal{X}, \tau \sim \mathcal{T}(\theta, \phi)} \left[ \mathcal{V}(\tau, x) - \lambda \sum_{t=1}^T \text{cost}(e_t) \right]$$

### 三阶段数据生成 Pipeline

**Phase 1 - Trajectory Collection**: 以最高 effort level $e_\text{high}$ 对每个训练任务采样 $N$ 条成功轨迹，筛选步骤数最少的轨迹 $\tau^* = (o_1, a_1^*, \ldots, o_T, a_T^*)$ 作为参考路径。最短轨迹可以降低总 reasoning cost 并隔离每步的最低需求。

**Phase 2 - Reasoning Effort Annotation**: 对参考轨迹中每个步骤 $t$，逐一测试三个 effort level。对每个 effort level $e \in \mathcal{E}$，采样 $K=3$ 次响应，通过验证函数 $\mathcal{V}(\hat{a}, a_t^*)$ 判断是否能可靠复现正确动作（多数正确即为充分）。选取最低充分 effort level 作为标签 $y_t$。验证标准针对不同 agent 类型（工具使用、网页浏览、深度研究）定制：工具使用 agent 要求 tool name 和关键参数完全匹配，网页 agent 要求与环境交互完全一致，深度研究 agent 使用 LLM judge 判断语义等价性。

**Phase 3 - Rationale Generation**: 使用教师 LLM（GPT-5）对标注好的轨迹生成推理依据 $r_t$（3-5句话），内容涵盖：当前任务进度追踪、当前步骤复杂度分析、下一子任务预测。依据长度严格限制以保持 router 轻量。

**Supervised Fine-tuning (SFT)**: 在增强数据集 $\mathcal{D} = \{(h_t, o_t, r_t, y_t)\}$ 上使用标准 next-token prediction 目标微调轻量级 router（Qwen3-1.7B），训练其先生成推理依据 $r_t$，再输出 effort label $y_t$。

### 强化学习阶段 (RL via GRPO)

SFT 的局限：(1) 假设所有前序步骤的 effort 选择均为最优，无法学习从次优状态恢复；(2) 每个 query 仅提供单个 effort 选择信号，缺乏跨序列对比信号。

GRPO 训练中，router 在 agent 与环境交互的完整轨迹上进行优化。复合奖励函数 $R(\tau)$ 包含三部分：

- **Outcome Reward $R_\text{out}$**: 任务完成得 +5.0，失败得 0.0（仅成功轨迹施加 cost penalty）
- **Reasoning Cost Reward $R_\text{cost}$**: 逐步惩罚，$c(e_t) = -0.2$（low）、$-0.5$（mid）、$-1.0$（high），归一化为轨迹均值
- **Format Reward $R_\text{form}$**: 违反输出格式（如 `<think>` 标签）得 -1.0，立即终止

**RL 数据过滤**: 丢弃成功率为 0 的 prompt（任务本身不可解）；保留成功率 100% 且奖励方差在 top 30% 的 prompt（多种 reasoning 策略均可成功但成本差异大，提供最强的效率优化信号）。

### 关键设计分析

- **Rationale 的作用**: 消融实验表明，移除 rationale 生成使准确率下降 3.5%，说明显式分析任务难度是提升 effort 预测精度的关键认知桥梁。
- **RL reward normalization 的作用**: 归一化 cost reward 使高 effort 使用率从 ~30% 降至 ~15%，同时提升任务准确率，效果显著优于非归一化设置。
- **Overthinking 的纠正**: 在 TAU-Bench Airline domain，SFT router 初始化后超过 50% 步骤选择 high effort，RL 训练快速将此比例压缩至 20% 以下，同时将 low effort 比例提升至约 70%，完全纠正了过度推理偏差。
- **Step 类型与 effort 分布**: 分析显示 `go_back`（从错误路径恢复）和 `branch`（实质性修改导航计划）类动作需要最高比例的 high effort，符合直觉——这些是任务中的高风险纠错节点。
