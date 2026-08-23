# Tensor Logic: The Language of AI

## Research Problem
How to create a single programming language based on tensor equations that unifies neural networks, symbolic AI, kernel methods, and probabilistic graphical models.

> Domingos, P. (2025). Tensor Logic: The Language of AI. arXiv:2510.12269v3.

## Topic

Unifying Neural-Symbolic AI Languages

## Background

AI currently lacks a dedicated programming language that simultaneously provides all requisite features: automatic differentiation, GPU acceleration, automated reasoning, knowledge acquisition, scalability, learnability, and transparency. Python, the de facto AI language, was never designed for AI; libraries like PyTorch and TensorFlow add differentiation and GPU support but offer no help for reasoning or knowledge representation. Traditional AI languages such as LISP and Prolog support symbolic reasoning but lack scalability and learning capabilities. Neurosymbolic AI attempts to bridge this gap by coupling deep learning modules with symbolic components, but often inherits the shortcomings of both rather than their strengths. A fundamentally unified language is needed.

## Limitations & Research Problem

- **Limitation 1:** The AI programming ecosystem is fragmented. Python/PyTorch excels at neural computation but provides no support for formal reasoning; Datalog/Prolog excels at symbolic reasoning but lacks scalability and gradient-based learning; probabilistic graphical models offer principled uncertainty handling but suffer from expensive inference.
- **Limitation 2:** Neurosymbolic approaches combine deep learning and symbolic modules at the system level without a shared mathematical foundation, frequently producing hybrid systems that inherit both paradigms' weaknesses.
- **Problem:** Can a programming language be designed that unifies neural networks (tensor algebra) and symbolic AI (logic programming) at the mathematical level, simultaneously achieving scalability, learnability, transparency, and sound reasoning?

## Contributions

- Proposes **Tensor Logic**, a programming language whose sole construct is the tensor equation, grounded in the observation that logical rules and Einstein summation are essentially the same operation.
- Establishes a formal correspondence between logic programming and tensor algebra: a relation is a compact representation of a sparse Boolean tensor, and a Datalog rule is an einsum over Boolean tensors followed by a Heaviside step function.
- Defines tensor projection and tensor join as operations that directly correspond to database projection and database join, unifying relational algebra with tensor algebra.
- Demonstrates that tensor logic elegantly implements major AI paradigms: neural networks (MLPs, CNNs, RNNs, GNNs, Transformers), symbolic AI (Datalog programs), kernel machines, and probabilistic graphical models (Bayesian networks, belief propagation, sampling).
- Introduces **reasoning in embedding space** -- sound and transparent inference over embedded objects, relations, and rules using tensor product representations, where the error probability decreases with increasing embedding dimension (analogous to Bloom filters).
- Proposes a temperature-controlled sigmoid mechanism: setting T toward 0 yields purely deductive reasoning, while increasing T enables analogical reasoning that borrows inferences across similar objects, combining compositionality with similarity-based generalization.
- Presents two scaling strategies: (1) separation of concerns, where dense subtensors are processed on GPUs and sparse subtensors are handled by a database query engine; (2) Tucker decomposition of sparse tensors into dense form for unified GPU execution, with controllable approximation error.
- Proves that tensor logic is Turing-complete (via RNN implementation) and that automatic differentiation is exceptionally simple -- the gradient of a tensor logic program is itself a tensor logic program.

## Methodology

- **Core Representation:** The tensor equation is the sole language construct. The left-hand side (LHS) specifies the tensor being computed; the right-hand side (RHS) is a series of tensor joins followed by tensor projection onto the LHS indices, with an optional elementwise univariate nonlinearity. Tensors are denoted by name followed by a comma-separated list of indices in square brackets. Join signs are implicit, and equations with the same LHS are implicitly summed.
- **Inference Engine:** Supports forward chaining (executing tensor equations sequentially as linear code until a fixpoint is reached or a stopping criterion is met) and backward chaining (treating each tensor equation as a function and recursively calling equations for RHS tensors). These generalize the corresponding symbolic AI inference procedures to arbitrary tensor types.
- **Learning Engine:** Automatic differentiation is particularly simple due to the uniform structure of tensor equations -- the derivative of the LHS with respect to any RHS tensor is the product of the remaining tensors. The gradient is itself a tensor logic program. Learning supports backpropagation through structure, allowing different examples to follow different derivation paths. Tensor decomposition (e.g., Tucker decomposition) generalizes predicate invention from inductive logic programming.
- **Implementing AI Paradigms:** An MLP is implemented by a single equation `X[i,j] = sig(W[i,j,k] X[i-1,k])`; a Transformer requires approximately twelve tensor equations (covering embedding, positional encoding, multi-head attention, layer normalization, MLP layers, and output); GNNs use a neighborhood relation tensor for message passing; kernel machines are expressed via Gram matrix equations; graphical models map factors to tensors, marginalization to projection, pointwise products to joins, belief propagation to forward chaining, and sampling to backward chaining with selective projection.
- **Embedding Space Reasoning:** Objects are embedded as random unit vectors. A relation R(x,y) is embedded as `EmbR[i,j] = R(x,y) Emb[x,i] Emb[y,j]` (tensor product representation). Rules are embedded by replacing their antecedents and consequents with their corresponding embedded relation tensors. Forward or backward chaining over embedded rules yields approximate inference, with error decreasing as embedding dimension grows. Periodic extract-threshold-re-embed cycles further control error accumulation. A temperature parameter controls the deductive-analogical spectrum.
- **Scaling Approaches:** (1) A hybrid architecture where dense subtensors are computed on GPUs and sparse subtensors are managed by a database query engine with full query optimization; (2) converting all sparse tensors to dense form via Tucker decomposition for unified GPU execution, leveraging the fact that even random decompositions suffice for approximate correctness, with error controllable via embedding dimension and step-function denoising.
