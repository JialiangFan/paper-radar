# Logic Tensor Networks

## Research Problem
How to design a unified differentiable framework that grounds first-order logic into tensor computation graphs for end-to-end neurosymbolic learning.

## 主题
Neurosymbolic AI via Differentiable Logic

## 背景
近年来，将 logic 与 neural networks 结合的 neurosymbolic AI 研究日益受到关注。传统 deep learning 采用纯 sub-symbolic 方法，虽然在 computer vision、natural language processing 等领域取得了显著成果，但存在 data inefficiency 和 out-of-distribution generalization 能力不足的问题。与此同时，symbolic AI 擅长 theorem proving 和 logical inference，却难以处理 incomplete knowledge 和高维复杂数据。Neurosymbolic AI 试图融合两者优势，将 knowledge representation（知识库、ontology、semantic network）与 data-driven learning 相结合，而其核心挑战在于如何将 symbolic 元素（constants、functions、predicates）grounding 到实数域数据中，即经典的 symbol grounding problem。

## 现有局限与研究问题
- **Limitation 1:** 纯 sub-symbolic 模型缺乏 comprehensibility，无法显式表达和利用 rich knowledge（first-order logic 层面的关系、规则与约束），导致 data inefficiency 和泛化困难。
- **Limitation 2:** 纯 symbolic AI 系统计算复杂度高，对 incomplete/noisy data 缺乏鲁棒性，难以从高维原始数据中学习 latent structures。
- **Limitation 3:** 已有的 neurosymbolic 方法缺少一个统一的、fully differentiable 的逻辑语言，无法在同一框架下同时支持 classification、regression、clustering、relational learning、semi-supervised learning、query answering 等多种任务。
- **Problem:** 如何设计一个通用的 neurosymbolic 框架，使得 first-order logic 的语法与语义能够完全嵌入可微分的计算图中，从而在保留逻辑表达力的同时实现端到端的 gradient-based learning？

## 贡献
- 提出 **Logic Tensor Networks (LTN)**，一个基于 **Real Logic** 的 neurosymbolic 框架。Real Logic 是一种 fully differentiable first-order logic language，其 truth-values 取值于连续区间 [0,1]（fuzzy semantics），logic signature 中的所有元素均通过 neural computational graphs grounding 到 real-valued tensors。
- 引入 **Stable Product Real Logic** 配置：采用 product t-norm 及其对偶 t-conorm 作为 connectives 的 fuzzy 近似，并通过 projection functions 将 truth-values 映射至开区间以解决 vanishing/exploding gradients 问题，提升训练数值稳定性。
- 提出 **generalized mean aggregator** 作为 quantifier（universal/existential）的可微近似，通过超参数 p 控制 smooth min/max 的严格程度，兼顾灵活性与可微性。
- 扩展 LTN 支持 **explicit domain declaration**（typed constants、variables、predicates）、**guarded quantifiers**（条件量化）和 **diagonal quantification**（对齐样本-标签对的高效量化）。
- 形式化定义 Real Logic 中的 **learning**（最大化 satisfiability）、**reasoning**（logical consequence 与 refutation-based reasoning）和 **query answering**（truth/value/generalization queries）三大任务。
- 在统一框架下演示 LTN 可处理 binary/multi-class/multi-label classification、regression、clustering、semi-supervised learning、relational learning、embedding learning 以及 logical reasoning 等多种任务，并基于 TensorFlow 2 提供开源实现。

## 方法论
- **Real Logic 语法与语义：** 定义 first-order language L，包含 constant symbols C、function symbols F、predicate symbols P 和 variable symbols X，所有符号通过 domain typing 函数 D 进行类型约束。语义层面，采用 **grounding** G（替代传统 FOL 的 interpretation）将每个 constant 映射为 tensor、variable 映射为 tensor sequence、function 映射为 tensor-to-tensor 函数、predicate 映射为输出 [0,1] 值的函数（通常由 neural network 实现）。
- **Connectives 与 Quantifiers 的模糊语义：** Conjunction (∧)、disjunction (∨)、implication (→)、negation (¬) 分别由 t-norm T、t-conorm S、fuzzy implication I、fuzzy negation N 近似。Quantifiers ∀ 和 ∃ 由 aggregation operators（generalized mean w.r.t. error 和 generalized mean）近似，参数 p 越大越接近 strict min/max。
- **Stable Product 配置：** 为解决 product t-norm 在边界值（0 或 1）处的 vanishing gradients，引入 projection π₀ 和 π₁ 将 [0,1] 映射至开区间 ]0,1] 和 [0,1[，确保梯度始终非零。
- **Knowledge Base 表示：** 通过 symbol grounding（固定或参数化）、factual propositions、generalized propositions（含 quantified variables 的 first-order formulas）以及 fuzzy semantics operators 的选择，构建 Real Logic theory T = (K, G(·|θ), Θ)。
- **Learning（学习）：** 定义 satisfiability 为所有公式 truth-values 的聚合，学习即通过 gradient-based optimization 搜索使 satisfiability 最大化的参数 θ*，支持 L1/L2 regularization。Learning constants → embeddings，learning functions → generative/regression models，learning predicates → classifiers。
- **Reasoning（推理）：** 定义 fuzzy logical consequence；提出两种推理方式：(1) Querying after learning——在最优 grounding 上直接查询公式真值；(2) Proof by refutation——通过搜索满足 knowledge base 但违反目标公式的 counter-example grounding 来验证 logical consequence，使用 elu-based penalty 函数实现可微优化。
- **Query Answering（查询）：** 支持 truth queries（公式真值）、value queries（term 的 tensor 值）、generalization truth queries（新数据上的公式真值）和 generalization value queries（新数据上的 regression 输出）。
- **实现：** 基于 TensorFlow 2，每个 logical operator 直接 grounding 为 TensorFlow 计算图节点，利用自动微分进行端到端优化，使用 Adam optimizer，学习率 0.001，结果取 10 次运行的均值（95% confidence interval）。
