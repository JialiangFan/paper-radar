# Logical Neural Networks

## Research Problem
How to create a neural architecture where every neuron has a 1:1 correspondence to a logical formula, enabling fully interpretable bidirectional inference while maintaining learning capability.

> Riegel, R., Gray, A., Luus, F., Khan, N., Makondo, N., Akhalwaya, I., ... & Srivastava, S. (2020). Logical Neural Networks. *arXiv preprint arXiv:2006.13155*.

## Topic

Neuro-Symbolic AI Integration Framework

## Background

The long-standing divide between neural networks (strong learning but opaque) and symbolic logic (rigorous reasoning but brittle learning) has been a fundamental challenge in AI. Existing neuro-symbolic approaches such as Markov Logic Networks (MLNs), probabilistic soft logic, and Logic Tensor Networks (LTNs) have attempted to bridge this gap but suffer from limited expressivity, incomplete reasoning, or loss of interpretability. Logical Neural Networks (LNNs) are proposed as a framework that seamlessly unifies neural learning with symbolic reasoning by establishing a 1-to-1 correspondence between neurons and components of logical formulae in a weighted real-valued logic.

## Limitations & Research Problem

- **Limitation 1:** MRF-based approaches (e.g., MLNs) treat logical clauses as atomic units, concealing internal logical structure and precluding full theorem proving. Their probabilistic inference via MCMC is computationally expensive and non-deterministic in convergence.
- **Limitation 2:** Most neuro-symbolic methods adopt a closed-world assumption (absent statements are false) and fix inference direction toward predefined target variables, lacking the ability to handle incomplete knowledge or perform omnidirectional reasoning.
- **Limitation 3:** Prior approaches that convert logic into neural networks (e.g., KBANN) do not preserve logical gate behavior in the final model's neurons, sacrificing interpretability and the correspondence between network structure and logical semantics.
- **Problem:** How to design a framework where every neuron maintains a 1-to-1 correspondence with elements of logical formulae, while simultaneously supporting end-to-end differentiable learning, bidirectional inference, and the open-world assumption?

## Contributions

- Proposes the Logical Neural Networks (LNN) framework, establishing a 1-to-1 correspondence between neurons and components of weighted real-valued logical formulae, yielding a highly interpretable, disentangled representation where every neuron has a clear logical meaning.
- Introduces weighted nonlinear logic as a weighted generalization of Lukasiewicz-like logics, with learnable operand importance weights and bias terms enabling parameterized conjunction, disjunction, and implication operators.
- Designs the upward-downward inference algorithm that alternates upward passes (leaves to root) and downward passes (root to leaves) over formula syntax trees, achieving omnidirectional, bidirectional inference with provable convergence in finite steps (Theorem 1).
- Proposes a truth value bounds mechanism using lower and upper bounds on [0,1] to support the open-world assumption and probabilistic semantics, with Theorem 2 proving that LNN-computed bounds constitute valid bounds on the true probability.
- Introduces a novel loss function incorporating contradiction loss (penalizing cases where lower bound exceeds upper bound), providing resilience to inconsistent knowledge while supporting constrained optimization.
- Develops tailored activation functions via piecewise-linear interpolation that guarantee classical outputs for classical inputs without requiring explicit constraints, while maintaining favorable gradient properties.

## Methodology

- **Model Structure:** An LNN is a recurrent neural network whose graph structure mirrors the syntax trees of represented logical formulae in a 1-to-1 correspondence. Each neuron outputs a pair of truth value bounds (lower, upper) in [0,1]. A threshold alpha distinguishes four primary states: True, False, Unknown, and Contradiction (when lower > upper).
- **Activation Functions for Connectives:** Logical connectives (AND, OR, NOT, implication) are implemented via parameterized activation functions. The n-ary weighted nonlinear conjunction is defined as beta(cross_i x_i^{w_i}) = f(beta - sum w_i(1-x_i)); disjunction is defined dually. The bias term beta unifies implication as a residuum of conjunction.
- **Weighted Nonlinear Logic:** Learnable operand weights w_i and bias beta generalize standard real-valued logics to weighted variants supporting importance weighting. The activation function f may be chosen as ReLU-clamped (yielding Lukasiewicz t-/s-norms), logistic, or a tailored piecewise-linear function.
- **Inference (Upward-Downward Algorithm):** Inference proceeds via Algorithm 3: iteratively visiting all formula roots, executing an upward pass (Algorithm 1 -- computing parent bounds from subformula bounds) followed by a downward pass (Algorithm 2 -- tightening leaf bounds using formula-level bounds via real-valued generalizations of modus ponens, modus tollens, conjunctive syllogism, and disjunctive syllogism). Convergence within epsilon is guaranteed by monotonic bound tightening (Theorem 1).
- **Probability Bounds Interpretation:** By employing different activation functions (max/min aggregation) for lower and upper bound computations respectively, truth value bounds can be interpreted as bounds on the probability that a subformula is True. Theorem 2 formalizes this: L_sigma <= inf p(S_sigma) and U_sigma >= sup p(S_sigma) over all consistent probability models.
- **Learning:** The model is end-to-end differentiable, optimizing operand weights, bias terms, and atom truth value bounds via backpropagation. The loss function combines standard error terms with a contradiction loss term (sum of max{0, L_k - U_k}) penalizing logical inconsistency. The tailored activation function (Eq. 8) uses piecewise-linear interpolation through four critical points to ensure classical correctness and eliminate the need for constrained optimization, while providing large and reliable gradients.
- **Empirical Evaluation:** On the Smokers-and-Friends experiment, LNN correctly resolves contradictions and infers all logical consequences, outperforming both MLN (which produces contradictions) and LTN (which cannot infer friendship symmetry). On the LUBM ontology reasoning benchmark, LNN achieves 100% precision and 100% recall (matching only Stardog among symbolic reasoners). On the TPTP theorem proving benchmark (Common Sense Reasoning subset), LNN successfully proves all 25 eligible problems within seconds, a capability not demonstrated by recent neural theorem provers.
