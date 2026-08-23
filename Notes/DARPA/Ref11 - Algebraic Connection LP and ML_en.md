# Algebraic Connection between Logic Programming and Machine Learning

## Research Problem
How to unify logic programming and machine learning through a common algebraic (matrix/tensor) foundation, enabling GPU-accelerated symbolic reasoning and differentiable logic programming.

> Inoue, K. (2024). Algebraic connection between logic programming and Machine Learning. In *FLOPS 2024*, LNCS 14659, pp. 3-9. Springer.

## Topic
Algebraic Neurosymbolic Logic Programming

## Background
Reasoning and learning are two fundamental and complementary components of AI. The neurosymbolic AI field seeks to bridge deep learning and symbolic reasoning, yet most existing approaches merely provide interfaces between low-level neural perception and high-level symbolic inference, lacking a unified mathematical foundation. This paper presents an original approach that uses algebraic methods -- representing logical formulas with matrices and tensors -- to integrate symbolic reasoning and machine learning within a common numeric field, enabling recognition, learning, and inference on shared mathematical ground.

## Limitations & Research Problem
- **Limitation:** Current LLMs exhibit inherent deficiencies in correct reasoning. Existing neurosymbolic AI methods predominantly offer interface-level integration between neural and symbolic systems, without a unified algebraic framework that simultaneously supports recognition, learning, and inference with noise robustness and scalability.
- **Problem:** How can logic programming be reformulated in algebraic terms so that symbolic reasoning becomes numerical computation that is (1) robust against noise, (2) scalable via GPU parallelism through sparse matrix operations, and (3) seamlessly integratable with neural learning systems?

## Contributions
- Established a systematic framework for algebraic logic programming, encoding logical formulas as vectors/matrices/tensors and realizing logical reasoning through linear algebraic operations.
- Defined the program matrix M_P such that the immediate consequence operator T_P is computed as a matrix-vector product: v_J = theta(M_P * v_I), where theta is a binary thresholding function.
- Exploited sparsity of program matrices with sparse representation and GPU parallelism, achieving an order-of-magnitude speedup over state-of-the-art logic program solvers.
- Introduced matrix-based partial evaluation through repeated self-multiplication of the program matrix (M_P^2, M_P^4, ..., M_P^32), yielding exponential speedup in unfolding.
- Extended the linear algebraic method to propositional abduction (via the abductive matrix, i.e., the transpose of the program matrix) and to first-order Datalog programs (representing binary predicates as matrices and converting linear recursion into linear matrix equations).
- Proposed differentiable logic programming: defining a continuous loss function L(x) such that L(x) = 0 iff x is an intended model, then solving via stochastic gradient descent or Newton's method, providing noise robustness and GPU scalability.
- Realized differentiable answer set programming (ASP), embedding both supported-model conditions and stability constraints into the loss function.
- Developed differentiable LFIT (D-LFIT): learning program matrices from interpretation transition pairs (I, J) via cost minimization, successfully constructing AND/OR Boolean networks at unprecedented scale (10^4 genes).
- Extended differentiable ILP to first-order rule learning, supporting scalable rule induction from mislabeled and noisy data via sampling-based methods.

## Methodology
- **Linear Algebraic Approach:** A propositional logic program P is encoded as a program matrix M_P, where each row corresponds to the if-and-only-if rule defining a head atom and each column represents a body literal. An interpretation I is encoded as a binary vector v_I. The T_P operator is realized via matrix-vector product followed by thresholding. Least fixpoint computation iterates v_{k+1} = theta(M_P * v_k). Stable models are computed by supplying multiple guess vectors as an initial matrix. Abduction uses the transpose of M_P (the abductive matrix) for backward reasoning, alternating with minimal hitting set computation. For first-order programs, binary predicates are represented as matrices, and Datalog linear recursion is converted to linear matrix equations.
- **Differentiable Approach:** The interpretation vector is relaxed from the Boolean to the continuous domain. A loss function L(x) is defined such that L(x) = 0 iff x is the target model, and gradient-based optimization (SGD or Newton's method) minimizes L, with final thresholding to obtain a logical solution. For ASP, supported-model and stability constraints are embedded in the loss function. For SAT, a clause matrix M_S is constructed and local search minimizes the associated loss. For ILP, given pairs (I, J), the program matrix M_P is learned by minimizing the distance between theta(M_P * x_I) and x_J. Further variants employ LSTM (delta-LFIT) and Transformer architectures (delta-LFIT+) for differentiable logic program learning, and DNF-based program matrices have been learned via cost minimization corresponding to ReLU neural networks.
- **Future Directions:** Deeply combining the linear algebraic and differentiable approaches into a unified framework; connecting algebraic methods with LLMs for commonsense reasoning.
