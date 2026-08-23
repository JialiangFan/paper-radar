# Three Pathways to Neurosymbolic RL

> Graf & Emami, 2024 | Neurosymbolic Artificial Intelligence, IOS Press | NREL

## 主题

Interpretable Neurosymbolic Reinforcement Learning

## 背景

纯数据驱动的 deep RL 方法（如基于 neural network 的 policy）虽然在多种控制任务中取得了成功，但缺乏 interpretability 和 reliability。Neurosymbolic AI (NSAI) 试图将 symbolic reasoning 的可解释性与 neural network 的可学习性相结合，但如何在 RL 框架中实现这种结合仍是开放问题。建筑能源管理（Building Energy Management, BEM）领域天然依赖基于规则的控制策略（如 "温度 > 20C 则开空调"），是研究 neurosymbolic RL 的理想应用场景。

## 现有局限与研究问题

- **Limitation 1:** 传统 deep RL policy 是黑箱模型，无法提供人类可理解的决策解释，在 safety-critical 的 BEM 等领域难以被信任和部署。
- **Limitation 2:** 经典 symbolic logic 是离散且不可微的，无法直接用于基于 gradient descent 的学习框架，导致 symbolic 方法与 neural 方法难以无缝融合。
- **Limitation 3:** 现有 neurosymbolic RL 工作多局限于 toy problem，缺乏在实际（real-world simulation）控制任务中的系统性探索。
- **Problem:** 如何设计同时具备 differentiability（可学习）和 interpretability（可解释）的 policy/model 架构，并将其系统性地融入不同 RL paradigm？

## 贡献

- 提出三条将 differentiable interpretable model 融入 RL 的路径：**Model-free RL**（用 DDT 替代 neural policy）、**Model-based RL**（用 LNN 学习 symbolic world model + classical planning）、**Differentiable Predictive Control (DPC)**（LNN policy + 可微仿真的端到端优化）。
- 将两种 neurosymbolic 架构——**Differentiable Decision Tree (DDT)** 和 **Logical Neural Network (LNN)**——集成到标准 RL 框架中，并在建筑能源管理仿真环境 OCHRE/ochre_gym 中进行实验验证。
- 系统性地揭示了 differentiability 与 interpretability 之间的根本张力：模型越可微/可学习，其离散可解释性越难保持（sigmoid 越平滑越好学，但离 crisp rule 越远）。
- 讨论了 scalability、discrete-to-continuous relaxation、warm start 策略等关键开放问题。

## 方法论

### 核心架构

- **Differentiable Decision Tree (DDT):** 将标准 decision tree 的 hard split 替换为 sigmoid-based soft split，decision node 对所有 attribute 的 linear combination 做阈值比较，leaf node 输出 action probability。所有参数（权重、阈值、sigmoid 强度、leaf probability）均可通过 SGD 学习。通过 "soft action"（离散 action value 的加权组合）生成连续动作。
- **Logical Neural Network (LNN):** 基于 real-valued logic，将 AND/OR 等逻辑连接词实现为带权重约束的 differentiable gate（y = f(w * x - theta)）。权重约束保证了逻辑语义。LNN 可从数据中学习逻辑规则，自动将无关 predicate 的权重置零。

### 三条路径

1. **Pathway 1 -- Model-free RL + DDT:**
   - 将 DDT 作为 SAC (Soft Actor-Critic) 的 actor network，集成到 stablebaselines3 框架。
   - 在 ochre_gym 的 time-of-use (TOU) pricing 场景中测试 HVAC 控制。
   - 支持 "warm start"：用已知的 rule-based controller (RBC) 初始化 DDT。
   - **结果：** RBC 整体优于 DDT 和 DRL；warm-start DDT 接近 RBC 性能但非 warm-start 的 DDT 不稳定；DDT 的 sigmoid cascade 给 SGD 带来数值困难；DDT 具有自适应能力（在 RBC 表现差的凉爽月份更好）。

2. **Pathway 2 -- Model-based RL + LNN + Classical Planning:**
   - 用 LNN 从仿真数据中学习 action 的 pre-/post-condition（STRIPS 格式的 symbolic world model）。
   - 定义 vocabulary 将连续仿真状态映射为 logical predicate。
   - 将学到的 LNN model 转换为 PDDL planning problem，用 classical planner 求解 optimal action sequence。
   - **结果：** LNN 权重收敛到 0/1 整数值，学到的规则完全可解释；成功发现了"若 cold 则 pull_switch 使之 not cold"的控制规则。

3. **Pathway 3 -- DPC + LNN + Differentiable Simulation:**
   - 在 PyTorch 中实现可微的温度调节仿真，LNN 作为 policy network。
   - 整个 episode 展开为一个计算图，通过 backpropagation 端到端优化 LNN 参数（dL/d_theta）。
   - 使用 smoothness parameter scheduling：初始 sigmoid 平滑便于梯度优化，逐步增强至接近 crisp logic。
   - **结果：** LNN 成功学到可解释的规则（如 "if Hot then TurnACOn"，"if Hot AND PowerCheap then TurnACOn"），spurious predicate 权重归零。

### 关键发现与 Trade-off

- **Differentiability vs. Interpretability:** sigmoid 越平滑越利于学习，但离 discrete interpretable rule 越远；DDT 的 relaxation 是 "uncontrolled" 的（不像 integer programming 中 relaxation 有理论保证），discretization 困难。
- **LNN 优于 DDT 的可解释性：** LNN 的权重几乎总收敛到 0/1，天然产生可解释的逻辑表达式；DDT 的 real-valued weight 难以直接"snap"为整数。
- **Scalability 挑战：** DDT 在 stochastic gradient descent 环境下 scale 困难；DPC 方法需要完全可微的仿真器（实践中罕见）；Model-based 方法面临规则数量爆炸问题。
