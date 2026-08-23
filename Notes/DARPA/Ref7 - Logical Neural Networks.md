# Logical Neural Networks

## Research Problem
How to create a neural architecture where every neuron has a 1:1 correspondence to a logical formula, enabling fully interpretable bidirectional inference while maintaining learning capability.

> Riegel, R., Gray, A., Luus, F., Khan, N., Makondo, N., Akhalwaya, I., ... & Srivastava, S. (2020). Logical Neural Networks. *arXiv preprint arXiv:2006.13155*.

## 主题

Neuro-Symbolic AI Integration Framework

## 背景

传统 AI 研究长期面临 neural networks (学习能力强但缺乏可解释性) 与 symbolic logic (推理严谨但难以从数据中学习) 之间的根本性割裂。现有的 neuro-symbolic 方法，如 Markov Logic Networks (MLNs) 和 Logic Tensor Networks (LTNs)，试图弥合这一鸿沟，但均在表达能力、推理完备性或可解释性方面存在显著不足。LNN 的提出旨在构建一个真正将 neural network 的学习能力与 symbolic logic 的推理能力无缝统一的框架，使每个 neuron 都具有明确的逻辑语义。

## 现有局限与研究问题

- **Limitation 1:** 基于 Markov Random Fields 的方法（如 MLNs）将逻辑子句视为原子单元，隐藏了内部逻辑结构，无法实现完整的 theorem proving；其概率推断需要 MCMC 采样，计算代价高且不确定收敛。
- **Limitation 2:** 现有 neuro-symbolic 方法（如基于 embedding 的方法）通常采用 closed-world assumption，将知识库中未出现的命题视为假，无法处理 incomplete knowledge；且推理方向固定于预定义的 target variables，缺乏 omnidirectional inference 能力。
- **Limitation 3:** 已有的将逻辑转化为神经网络的方法（如 KBANN）在转化后神经元不再保持逻辑门行为，丧失了可解释性和逻辑对应关系。
- **Problem:** 如何设计一个框架，使得每个 neuron 与逻辑公式中的元素保持 1-to-1 correspondence，同时支持 end-to-end differentiable learning、bidirectional inference 以及 open-world assumption？

## 贡献

- 提出 Logical Neural Networks (LNNs) 框架，实现 neuron 与 weighted real-valued logic 中公式组件的一一对应，每个 neuron 具有明确的逻辑含义，表示为 disentangled representation。
- 引入 weighted nonlinear logic，作为 Lukasiewicz-like logic 的加权推广，通过 importance weighting 使不同输入对逻辑运算的贡献可微调，支持 conjunction、disjunction 和 implication 的参数化表达。
- 设计 upward-downward inference algorithm，在公式语法树上交替执行 upward pass（从叶到根）和 downward pass（从根到叶），实现 omnidirectional、bidirectional inference，并证明该算法在有限步内收敛（Theorem 1）。
- 提出基于 truth value bounds（上下界）的推理机制，支持 open-world assumption 和 probabilistic semantics（Theorem 2 证明 LNN 计算的上下界构成真实概率的有效界）。
- 设计包含 contradiction loss 的 novel loss function，通过惩罚逻辑矛盾（lower bound > upper bound）实现对 inconsistent knowledge 的鲁棒性，同时支持 constrained optimization。
- 提出 tailored activation function，通过分段线性插值保证 classical inputs 产生 classical outputs，无需额外约束即可保持逻辑正确性，并提供良好的 gradient 性质。

## 方法论

- **Model Structure:** LNN 为一种 recurrent neural network，其图结构与所表示的逻辑公式的 syntax tree 一一对应。每个 neuron 输出 [0,1] 上的 truth value bounds（lower bound, upper bound）对，通过阈值 alpha 区分 True、False、Unknown 和 Contradiction 四种状态。
- **Activation Functions for Connectives:** 逻辑连接词（AND, OR, NOT, implication）由参数化的 activation functions 实现。n-ary weighted nonlinear conjunction 定义为 beta(cross_i x_i^{w_i}) = f(beta - sum w_i(1-x_i))；disjunction 类似地定义。Bias term beta 使 implication 可通过调整 beta 统一表示。
- **Weighted Nonlinear Logic:** 引入 operand weights w_i 和 bias beta 作为可学习参数，将标准 real-valued logic 推广为加权版本，支持 importance weighting。Activation function f 可选择 ReLU-clamped（对应 Lukasiewicz t-/s-norms）、logistic function 或 tailored piecewise-linear function。
- **Inference (Upward-Downward Algorithm):** 推理通过 Algorithm 3 实现：反复遍历所有公式根节点，对每个公式执行 upward pass（Algorithm 1，利用子公式 bounds 计算父公式 bounds）和 downward pass（Algorithm 2，利用公式和已计算的子公式 bounds 通过 inference rules 收紧叶节点 bounds）。支持 modus ponens、modus tollens、conjunctive/disjunctive syllogism 等经典推理规则的实值推广。
- **Probability Bounds:** 通过对 lower/upper bound 计算分别使用不同的 activation functions（max/min 聚合），使 truth value bounds 可解释为子公式为 True 的概率的上下界，形式化为 Theorem 2。
- **Learning:** 模型 end-to-end differentiable，通过 backpropagation 优化 operand weights、bias 和 atom truth value bounds。Loss function 包含标准误差项和 contradiction loss（sum of max{0, L_k - U_k}）。Tailored activation function (Eq. 8) 通过四个 critical points 的线性插值确保 classical correctness 并消除约束优化的需要。
- **Empirical Evaluation:** 在 Smokers-and-Friends 实验中，LNN 在处理矛盾公理时优于 MLN 和 LTN；在 LUBM benchmark 上实现 100% precision 和 100% recall；在 TPTP theorem proving benchmark 的 Common Sense Reasoning 子集上成功证明所有 25 个可处理问题。
