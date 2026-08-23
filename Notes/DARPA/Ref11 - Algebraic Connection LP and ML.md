# Algebraic Connection between Logic Programming and Machine Learning

## Research Problem
How to unify logic programming and machine learning through a common algebraic (matrix/tensor) foundation, enabling GPU-accelerated symbolic reasoning and differentiable logic programming.

> Inoue, K. (2024). Algebraic connection between logic programming and Machine Learning. In *FLOPS 2024*, LNCS 14659, pp. 3-9. Springer.

## 主题
Algebraic Neurosymbolic Logic Programming

## 背景
推理(reasoning)与学习(learning)是AI的两大基本能力，二者互补且可相互增强。Neurosymbolic AI 领域致力于连接深度学习与符号推理，但多数方法仅提供神经网络低层感知与高层符号推理之间的接口，缺乏统一的数学基础。本文提出一种基于代数方法(algebraic methods)的原创途径，利用 matrices 和 tensors 等代数数据结构表示逻辑公式，从而在共同的数值空间(numeric field)中实现 symbolic reasoning 与 machine learning 的深层整合。

## 现有局限与研究问题
- **Limitation:** 当前 LLMs 在正确推理方面存在固有缺陷；传统 neurosymbolic AI 方法多为神经网络与符号系统之间的"接口式"集成，缺少在统一数学框架下同时实现识别、学习与推理的能力。
- **Problem:** 如何在共同的代数框架下将 logic programming 的符号推理转化为数值计算，使其既具备对噪声的鲁棒性(robustness)，又可利用 GPU 并行实现可扩展计算(scalable computation)，并进一步与神经学习系统无缝整合？

## 贡献
- 提出了 algebraic logic programming 的系统性框架，将逻辑公式编码为 vectors/matrices/tensors，通过 linear algebra 运算实现逻辑推理。
- 定义了 program matrix M_P，使得 immediate consequence operator T_P 可表示为 matrix-vector product：v_J = theta(M_P * v_I)，其中 theta 为 binary thresholding function。
- 利用 program matrix 的稀疏性(sparsity)，通过 sparse representation 和 GPU 并行计算，实现了比 state-of-the-art solvers 快一个数量级的 logic program model computation。
- 提出 partial evaluation 的矩阵化方法：通过程序矩阵自乘 M_P^2, M_P^4, ..., M_P^32 实现指数级加速。
- 将 linear algebraic method 扩展到 abduction（利用 abductive matrix，即 program matrix 的转置）和 first-order Datalog programs。
- 提出 differentiable logic programming 方法：定义连续域上的 loss function L(x)，通过 gradient descent 求解 stable/supported models，具备噪声鲁棒性和 GPU 可扩展性。
- 实现了 differentiable answer set programming (ASP)，将 stable model 约束嵌入 loss function。
- 提出 differentiable LFIT (D-LFIT)：从 interpretation transition 对 (I, J) 中通过 cost minimization 学习 program matrix，成功构建了含 10^4 个基因的 Boolean network。
- 将 differentiable ILP 扩展到 first-order rule learning，支持从含噪声和错误标注的数据中进行可扩展规则学习。

## 方法论
- **Linear Algebraic Approach (Section 2):** 将 propositional logic program P 编码为 program matrix M_P（行对应 head atom 的 if-and-only-if 规则，列对应 body literal）。Interpretation I 编码为 binary vector v_I。T_P operator 通过 matrix-vector product + thresholding 实现。Fixpoint computation 通过迭代 v_{k+1} = theta(M_P * v_k) 求 least model。Stable models 通过同时提供多个 guess 向量作为 initial matrix 计算。Abduction 通过 abductive matrix（M_P 的转置）实现反向推理。First-order 场景下，binary predicate 用矩阵表示，linear recursion 转化为 linear matrix equations。
- **Differentiable Approach (Section 3):** 将 interpretation vector 从 Boolean domain 放松到 continuous domain。定义 loss function L(x) 使得 L(x)=0 当且仅当 x 为目标模型。通过 stochastic gradient descent 或 Newton's method 最小化 L，最终 thresholding 得到逻辑解。对 ASP，supported model 条件和 stability 约束均嵌入 loss function。对 SAT，构造 clause matrix M_S 并通过 local search 最小化 loss。对 ILP，给定 (I, J) 对，通过最小化 theta(M_P * x_I) 与 x_J 之间的距离学习 program matrix M_P。进一步利用 LSTM 和 Transformer 架构实现 differentiable LFIT 变体（delta-LFIT, delta-LFIT+）。
- **未来方向:** 深度融合 linear algebraic 与 differentiable 两种方法；将代数方法与 LLMs 结合以实现 commonsense reasoning。
