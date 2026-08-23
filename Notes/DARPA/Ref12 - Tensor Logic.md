# Tensor Logic: The Language of AI

## Research Problem
How to create a single programming language based on tensor equations that unifies neural networks, symbolic AI, kernel methods, and probabilistic graphical models.

> Domingos, P. (2025). Tensor Logic: The Language of AI. arXiv:2510.12269v3.

## 主题

Unifying Neural-Symbolic AI Languages

## 背景

AI领域目前缺乏一种同时具备所有关键特性的专用编程语言。Python虽是事实上的AI语言，但其设计初衷并非面向AI；PyTorch和TensorFlow等库提供了automatic differentiation与GPU加速，却不支持automated reasoning和knowledge acquisition。另一方面，传统AI语言如LISP和Prolog缺乏scalability和learning支持。Neurosymbolic AI尝试将deep learning模块与symbolic AI结合，但往往兼具两者的缺陷而非优势。因此，AI亟需一种能从根本层面统一neural、symbolic和statistical方法的编程语言。

## 现有局限与研究问题

- **Limitation 1:** 当前AI编程生态碎片化严重——Python/PyTorch擅长neural network但不支持formal reasoning；Datalog/Prolog擅长symbolic reasoning但缺乏scalability和gradient-based learning能力；graphical model的inference代价高昂。
- **Limitation 2:** Neurosymbolic AI方法通过拼接deep learning与symbolic模块来弥合鸿沟，但这种组合方式缺乏统一的数学基础，常继承双方的shortcomings。
- **Problem:** 能否设计一种从数学层面统一neural network（tensor algebra）与symbolic AI（logic programming）的编程语言，使其同时具备scalability、learnability、transparency和sound reasoning能力？

## 贡献

- 提出**Tensor Logic**，一种以tensor equation为唯一构造的编程语言，基于logical rules与Einstein summation本质等价的观察，实现neural与symbolic AI的根本统一。
- 证明relation可表示为sparse Boolean tensor，Datalog rule等价于对Boolean tensor施加Heaviside step function的einsum，从而建立logic programming与tensor algebra之间的直接对应关系。
- 定义tensor projection与tensor join操作，分别对应database projection与database join，使关系代数操作与张量操作在同一框架下无缝衔接。
- 展示tensor logic可优雅地实现多种主流AI paradigm：neural network（MLP、CNN、RNN、GNN、Transformer）、symbolic AI（Datalog程序）、kernel machine以及probabilistic graphical model（Bayesian network、belief propagation、sampling）。
- 提出**embedding space reasoning**——在embedding空间中进行sound且transparent的推理，通过将object、relation和rule嵌入为dense tensor，实现类似Bloom filter的近似推理，error probability随embedding dimension增大而降低。
- 引入temperature-controlled sigmoid机制：T→0时推理为纯deductive，T增大时实现analogical reasoning，在compositionality与similarity-based generalization之间灵活切换。
- 提出两种scaling策略：(1) separation of concerns——dense subtensor用GPU，sparse subtensor用database query engine；(2) 通过Tucker decomposition将sparse tensor转化为dense tensor，在GPU上统一执行，且与学习和推理算法无缝结合。
- 证明tensor logic是Turing-complete（通过实现RNN），且自动微分极为简洁——tensor equation的gradient本身也是tensor logic program。

## 方法论

- **核心表示：** 以tensor equation作为唯一语言构造。左侧（LHS）为待计算tensor，右侧（RHS）为一系列tensor join后接tensor projection，并可选施加univariate nonlinearity。Tensor以name加index list表示，join隐式执行，projection投影到LHS的indices上。
- **Inference引擎：** 支持forward chaining（将程序视为linear code逐条执行至fixpoint）和backward chaining（将每条equation视为function递归调用），分别对应symbolic AI中的演绎闭包计算和目标导向查询。
- **Learning引擎：** 利用tensor equation结构的简洁性实现自动微分——对RHS中某tensor求导即为其余tensor的乘积。梯度本身构成一个tensor logic program。支持backpropagation through structure，使不同example可对应不同推导路径。Tensor decomposition（如Tucker decomposition）实现predicate invention的generalization。
- **AI paradigm实现：** MLP用单条equation `X[i,j] = sig(W[i,j,k] X[i-1,k])` 实现；Transformer用约12条tensor equation实现（含embedding、positional encoding、multi-head attention、layer norm、MLP、output）；GNN通过Neig关系tensor实现message passing；kernel machine通过Gram matrix equation实现；graphical model中factor对应tensor，marginalization对应projection，pointwise product对应join，belief propagation对应forward chaining。
- **Embedding space reasoning：** 将object embedding为random unit vector，relation R(x,y)的embedding为 `EmbR[i,j] = R(x,y) Emb[x,i] Emb[y,j]`（tensor product representation）。规则通过替换antecedent和consequent的embedding来嵌入。在embedded rule上执行forward/backward chaining实现近似推理，误差随embedding dimension降低，可通过extract-threshold-re-embed循环进一步控制。
- **Scalability方案：** (1) GPU处理dense subtensor + database engine处理sparse subtensor的混合架构；(2) Tucker decomposition将全部sparse tensor转为dense tensor后统一在GPU上执行，利用random decomposition即可保证近似正确性。
