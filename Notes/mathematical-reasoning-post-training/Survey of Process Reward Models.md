# Survey of Process Reward Models

## 主题 / Topic
Process reward model (PRM) survey — 从 outcome signals 到 process supervision，系统综述大型语言模型（LLM）推理对齐中的过程奖励模型。

原文标题：*A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for Large Language Models*
作者：Congmin Zheng, Jiachen Zhu, Zhuoying Ou 等（上海交通大学、UCL、CMU、University of Bristol）
arXiv: 2510.08049v2，2025年10月21日

---

## 背景 / Background

- 大型语言模型（LLM）在推理任务上表现出色，但传统 alignment 方法主要依赖 outcome reward model（ORM），只判断最终答案的对错，提供粗粒度信号。
- 随着推理链（chain-of-thought）变长变复杂，ORM 无法诊断中间步骤错误、无法自适应分配计算资源。
- Process Reward Model（PRM）在步骤或轨迹层面评估推理过程，提供更细粒度的监督信号。
- PRM 形成闭环：**生成过程数据（generate process data）→ 训练 PRM（train PRMs）→ 使用 PRM 改进策略（use PRMs）→ 产生新数据**，循环迭代。
- 与 ORM 相比，PRM 可评估部分解和轨迹，支持 "reason-then-rate" 验证，整合推理时控制器和强化学习（RL）目标；supervision 从被动评估变为主动引导。

---

## 现有局限与研究问题 / Limitations & Research Problem

**现有局限：**
- 现有综述要么聚焦于 test-time scaling 范式（Zhang et al., 2025f），要么关注通用 reward modeling 分类（Zhong et al., 2025），或通用深度 RL 奖励设计（Yu et al., 2025）——均未系统覆盖 PRM 全闭环。
- 人工标注数据（如 PRM800K）成本高、规模受限，自动化方法存在误差传播和 verifier 局限性。
- Discriminative PRM 依赖显式步骤标签，在跨域泛化和抗 reward hacking 上存在挑战。
- Implicit PRM 无需步骤标签但精度较弱；Generative PRM 计算开销更大。
- 标准化评测 benchmark 尚不成熟，跨域泛化与鲁棒性验证仍是开放问题。

**核心研究问题：**
1. 如何生成高质量过程监督数据（fidelity vs. scalability 权衡）？
2. 如何构建 PRM（建模范式选择）？
3. 如何使用 PRM（test-time scaling 与 RL for policy learning）？

---

## 贡献 / Contributions

1. **系统分类框架**：围绕完整 PRM 闭环组织全文——数据生成（Sec. 2）、PRM 构建（Sec. 3）、PRM 使用（Sec. 4）、应用（Sec. 5）、Benchmark（Sec. 6）、讨论（Sec. 7）。
2. **数据生成分类**：将过程监督数据生成分为三类——人工标注（Human Annotation）、自动化监督（Automated Supervision）、半自动化方法（Semi-automated Approaches），分析各类 fidelity–scalability 权衡。
3. **PRM 训练范式分类**：归纳四类建模方法——Discriminative PRMs、Generative PRMs、Implicit PRMs、Other Architectures。
4. **PRM 使用方式总结**：梳理 test-time scaling（re-ranking、verification-guided decoding/search）和 PRM-guided RL（dense step-wise rewards、credit assignment）两大使用范式。
5. **应用领域综述**：涵盖数学、代码、多模态推理、机器人、Agent 等领域及高风险行业（医疗、金融）。
6. **Benchmark 整理**：梳理 PRMBench、ProcessBench、Socratic-PRMBench、ViLBench、VisualProcessBench、MPBench、WebRewardBench、GSM-DC、UniversalBench 等评测资源。
7. **讨论与展望**：从资源效率、粒度、抗 reward hacking 鲁棒性、泛化性、可解释性、功能性六维度对比 rule-based reward、ORM、PRM 三种机制，指出未来挑战。

---

## 方法论 / Methodology

### 2. 数据生成（How to Generate Data）

**2.1 人工标注（Human Annotation）**
- 代表作：PRM800K（Lightman et al., 2023）——人工验证多跳推理链每一步，高保真但成本高。
- 作用：为其他数据生成方法提供种子数据，建立 benchmark 基准。

**2.2 自动化监督（Automated Supervision）**
- Math-Shepherd（Wang et al., 2023）：用符号工具和一致性检验自动验证数学推理步骤，无需人工标注。
- FOVER（Kamoi et al., 2025）：用 Z3、Isabelle 等形式化验证工具自动生成精确步骤错误标签。
- OmegaPRM（Luo et al., 2024）：用 divide-and-conquer 式 Monte Carlo Tree Search（MCTS）定位推理链第一个错误。
- URSA（Luo et al., 2025）：多模态数学推理的全自动双视角流水线，结合 MCTS 误差定位和错误插入引擎。
- MT-RewardTree（Feng et al., 2025b）：将 MCTS 框架应用于机器翻译的 token 级偏好对生成。
- CodePRM（Li et al., 2025a）：代码推理的执行反馈自动步骤监督。
- AlphaMath（Chen et al., 2024）：从 outcome supervision 直接推导伪过程监督，完全消除步骤标签需求。
- rStar-Math（Guan et al., 2025）、Qwen2.5-Math PRM（Zhang et al., 2025j）：自进化与共识过滤策略生成大规模数据集。

**2.3 半自动化方法（Semi-automated Approaches）**
- VRPRM（Chen et al., 2025f）、Athena（Wang et al., 2025b）：从少量人工标注步骤出发，用自动验证或合成生成扩展，用于多模态推理。
- MedS³（Jiang et al., 2025）：医疗推理"慢思考"范式，约 8000 人工样本 + MCTS 扩展。
- ActPRM（Duan et al., 2025）：主动学习——仅在自动信号不确定时查询人工标注。

---

### 3. 构建 PRM（How to Build PRMs）

**3.1 Discriminative PRMs**
- 学习对中间推理状态的评分函数，输出每步正确性/合理性/进展的标量得分 $r_t = \sigma(f_\theta(x, s_{1:t})) \in (0,1)$。
- 训练目标：pointwise loss（BCE 或 MSE）；pairwise preference loss（类似 DPO 目标）。
- 代表工作：DreamPRM、PQM、ER-PRM、EDU-PRM、Q-RM、BiPRM、BiRM、CoLD、ProgRM 等。

**3.2 Generative PRMs**
- 两阶段：先生成验证链或 critique chain $z_t$（"think"），再基于该链判分（"judge"）。
- 联合训练目标结合验证链的 likelihood loss 和步骤级奖励的监督项：$\mathcal{L}_\text{gen} = -\log p_\phi(z_t^* \mid x, s_{1:t}) + \lambda \text{BCE}(r_t, y_t)$。
- 代表工作：ThinkPRM、GenRM（Zhang et al., 2025e）、GenPRM（Zhao et al., 2025）、GRAM-R²、GM-PRM、rStar-Math。

**3.3 Implicit PRMs**
- 无需显式步骤标签，利用 outcome feedback、模型自评估或一致性约束推断细粒度奖励。
- 代表工作：FreePRM（Sun et al., 2025a）、Self-PRM（Feng et al., 2025a）、SP-PRM（Xie et al., 2025a）、SPARE（Rizvi et al., 2025）、Universal PRM / AURORA（Tan et al., 2025）。

**3.4 其他架构创新（Other Architectural Innovations）**
- GraphPRM：将推理建模为步骤图，学习结构依赖。
- ASPRM（AdaptiveStep）：依据模型置信度动态调整推理步骤粒度。
- RetrievalPRM：整合外部检索以改善跨任务泛化。
- MM-PRM、Multilingual PRM、PathFinder-PRM、HRM（Hierarchical Reward Model）等专项架构。

---

### 4. 使用 PRM（How to Use PRMs）

**4.1 Test-Time Scaling**
- 通过推理时的候选采样、re-ranking 或引导搜索提升性能，而非扩大模型规模。
- Best-of-N re-ranking：用 PRM 得分选择最佳候选（Lightman et al., 2023；Wang et al., 2023）。
- 生成式验证：Gen-PRM（Zhao et al., 2025）在评分前生成推理或代码检查；ThinkPRM 微调长 CoT verifier。
- 搜索整合：PRM-BAS（beam annealing search）、CodePRM（Generate–Verify–Refine 流水线）、Web-Shepherd（过滤 web-agent 轨迹）。
- 自适应粒度：AdaptiveStep 基于置信度动态分割推理步骤；SP-PRM 跨多粒度级别扩展 reward-guided search。

**4.2 强化学习策略学习（RL for Policy Learning）**
- PRM 提供密集步骤级或轨迹级 feedback，替代稀疏 outcome 信号，用于 RL 训练循环。
- 早期探索：Math-Shepherd 训练自动 verifier 为 PPO 提供每步奖励；Dai et al. (2024) 将行级 PRM 信号注入代码生成 RL。
- RL 目标中的 PRM 信号形式化：PAV（Setlur et al., 2024）将步骤级 PRM 输出重构为 advantage-like 进展指标；ER-PRM 嵌入 KL 约束 RL 目标；PURE（Cheng et al., 2025）提出 min-form 目标防止 reward hacking；Q-RM 建模 token 级 Q-value 直接用于 RL。
- CAPO（Xie et al., 2025c）：可验证生成式 credit assignment，产生可靠步骤级奖励替代稀疏 outcome 信号。
- 框架整合：OpenR（Wang et al., 2024）开源基础设施；GraphPRM 用于图推理 preference optimization；AgentPRM 整合进 actor-critic 循环。

---

### 5. 下游应用

| 领域 | 代表应用 |
|------|---------|
| 数学 | 验证代数/逻辑步骤、自动批改、辅导、证明验证 |
| 代码 | 评估部分程序（执行/proxy 测试反馈）、text-to-SQL、软件工程 |
| 多模态 | 视觉-语言一致性检查、多模态推理链重排 |
| 文本 | 部分翻译评估、QA 中间跳跃评分、检索增强推理 |
| 机器人 | 长时域操作/导航分解为子目标奖励，稳定控制策略学习 |
| Agent | 轨迹批评、路径剪枝、安全推理 |
| 高风险行业 | 医疗（MedS³）、金融（Fin-PRM）可验证推理 |

---

### 6. Benchmark

| Benchmark | 特点 |
|-----------|------|
| PRMBench（Song et al., 2025） | 6000+ 题，80000 步骤标注，多维标签（simplicity, soundness, sensitivity） |
| ProcessBench（Zheng et al., 2024） | 竞赛级任务，最早错误检测 |
| Socratic-PRMBench（Li et al., 2025b） | ~3000 缺陷轨迹，六类错误模式 |
| ViLBench（Tu et al., 2025） | 视觉-语言 PRM vs ORM 比较 |
| VisualProcessBench（Wang et al., 2025f） | 人工标注多模态错误 |
| MPBench（Xu et al., 2025） | 多任务覆盖：步骤正确性、答案聚合、推理引导搜索 |
| WebRewardBench（Chae et al., 2025） | 40000 步骤级偏好对，web agent 导航 |
| GSM-DC（Yang et al., 2025b） | 注入干扰项测试鲁棒性 |
| UniversalBench（Tan et al., 2025） | 跨分布泛化与可复现性 |

---

### 7. 讨论：三种奖励机制六维对比

| 维度 | Rule-based | ORM | PRM |
|------|-----------|-----|-----|
| 资源效率 | 最高（无需数据/训练） | 中等 | 较低（需步骤标注+复杂流水线） |
| 粒度 | 中等（规则可调） | 粗（仅最终结果） | 最细（步骤级） |
| 抗 reward hacking | 最强（信号绑定最终正确性） | 强 | 中等（易受步骤标注偏差和人类偏好 artifact 影响） |
| 泛化性 | 差（规则需为每个新环境重新设计） | 强（outcome 原则易迁移） | 中等（step-level 思路可泛化，但模型常需对新任务结构再适应） |
| 可解释性 | 最强（逻辑内嵌于规则） | 弱（仅最终判断，无中间信息） | 中等（步骤级监督比 ORM 更丰富，但内部评分机制仍不透明） |
| 功能性 | 受限（仅适用于原始设计场景） | 中等（适合多任务 outcome 评估） | 最强（无缝整合 RL 和 test-time scaling，支持细粒度优化与引导推理） |

**结论**：PRM 将推理 alignment 从粗粒度 outcome 判断转向细粒度步骤级反馈，形成数据生成→模型训练→使用的闭环，持续改善推理质量。关键挑战：降低标注成本、改善跨域泛化、与 agentic planning 和记忆整合、建立标准化评测协议。
