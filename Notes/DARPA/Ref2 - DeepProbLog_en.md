# DeepProbLog: Neural Probabilistic Logic Programming

## Research Problem
How to fully integrate deep neural networks with probabilistic logic programming through minimal syntactic extension (neural predicates), enabling end-to-end differentiable learning across perception, logic, and probability.

> Manhaeve, R., Dumančić, S., Kimmig, A., Demeester, T., & De Raedt, L. (2019). Neural Probabilistic Logic Programming in DeepProbLog. *arXiv:1907.08194v2*. (Extended version of NeurIPS 2018 spotlight)

## Topic
Neural Probabilistic Logic Programming

## Background
AI tasks can be broadly divided into those requiring low-level perception (e.g., image recognition) and those requiring high-level reasoning (e.g., logical deduction). Deep learning excels at perception but falls short of symbolic reasoning approaches. Probabilistic logic programming (PLP), exemplified by ProbLog, unifies logic and probability, while neuro-symbolic AI seeks to bridge neural networks with symbolic reasoning. However, existing neuro-symbolic approaches either use logic merely as a regularization constraint, are limited to non-recursive acyclic logic programs, or fail to fully integrate neural networks with both logic and probability. The authors argue that neuro-symbolic integration should simultaneously combine neural networks with both major reasoning frameworks — logic and probability — and that pure neural, pure logical, and pure probabilistic methods should emerge as special cases.

## Limitations & Research Problem
- **Limitation 1:** Existing neuro-symbolic reasoning approaches (e.g., Neural Theorem Provers, Logic Tensor Networks) primarily approximate logical reasoning by encoding logical terms in Euclidean space. They do not support probabilistic reasoning or perception and are often limited to non-recursive, acyclic logic programs.
- **Limitation 2:** "Logic as regularization" methods (e.g., Semantic Loss, DL2) encode logical constraints as regularization terms in the loss function, but cannot directly perform logical reasoning or probabilistic inference.
- **Limitation 3:** Neural program induction methods (e.g., ∂4, NPI, TerpreT) use neural networks to fill holes in program templates but lack probabilistic semantics and face scalability issues with long program traces.
- **Problem:** How to design a framework that, through a minimal extension of ProbLog (introducing neural predicates), achieves full integration of neural networks with probabilistic logic programming — retaining ProbLog's complete semantics, inference mechanism, and implementation while supporting end-to-end gradient-based training?

## Contributions
- Introduces DeepProbLog, which integrates deep neural networks into the probabilistic logic programming language ProbLog through two minimal syntactic extensions: **neural annotated disjunctions (nADs)** and **neural facts**. A nAD allows a neural network's softmax output to serve as the probability distribution over the head atoms of an annotated disjunction.
- Semantics are fully inherited from ProbLog: nADs are instantiated into standard annotated disjunctions by replacing probabilities with neural network outputs, preserving ProbLog's distribution semantics (possible worlds) and weighted model counting (WMC) inference.
- Achieves end-to-end learning via **algebraic ProbLog (aProbLog)** and the **gradient semiring**: semiring elements are tuples (p, ∇p), and semiring operations on arithmetic circuits (ACs) simultaneously compute probabilities and their gradients. The chain rule then propagates gradients from the logic layer to neural network parameters: dL/dθ_k = (∂L/∂P(q)) · Σ_i (∂P(q)/∂p̂_i) · (∂p̂_i/∂θ_k).
- Uniquely supports four capabilities within a single framework: (i) both symbolic and subsymbolic representations and inference, (ii) program induction, (iii) probabilistic (logic) programming, and (iv) deep learning from examples.
- Comprehensive experimental validation across 9 tasks (T1–T9) spanning logical reasoning with deep learning, program induction, and combined probabilistic programming with deep learning.

## Methodology
- **Language Design:** A DeepProbLog program consists of ground probabilistic facts F, ground neural ADs and neural facts N, and rules R. A neural AD has the form `nn(m_r, I, O, d) :: r(I, O)`, where `m_r` identifies a neural network model, I is an input variable sequence, O is the output variable, and d is the output domain. Upon grounding, the neural network is evaluated via a forward pass, instantiating the nAD into a standard annotated disjunction with concrete probabilities.
- **Inference:** Follows ProbLog's four-step inference pipeline: (1) grounding via backward chaining to identify relevant ground rules, (2) rewriting into a propositional logic formula, (3) knowledge compilation into Sentential Decision Diagrams (SDDs), and (4) transformation into an arithmetic circuit (AC) for weighted model counting. The only additional step in DeepProbLog is instantiating nADs by evaluating neural networks after grounding.
- **Learning:** Adopts the *learning from entailment* setting, minimizing the loss (typically negative log-likelihood) between predicted and target query success probabilities. The key innovation is the **gradient semiring**: elements are (p, ∇p) tuples; semiring addition ⊕ yields (a₁+b₁, a₂+b₂); semiring multiplication ⊗ yields (a₁b₁, b₁a₂+a₁b₂). Evaluating the AC with gradient semiring labels simultaneously produces P(q) and ∂P(q)/∂p_i. Gradients are then propagated to neural parameters via the chain rule. ACs are cached across training iterations to avoid recompilation, significantly improving efficiency.
- **Experimental Setup:**
  - **T1–T4 (Logical reasoning + deep learning):** MNIST digit addition. T1: single-digit addition (DeepProbLog 97.20% vs. baseline 93.46% at N=30K; 67.19% vs. 23.64% at N=300). T2: multi-digit addition with zero-shot transfer from T1 (93.36%). T3: three-image constraint task requiring entropy regularization (infoloss) to prevent mode collapse. T4: noisy labels with explicit noise modeling (73.22% accuracy at 80% noise).
  - **T5–T7 (Program induction):** Based on differentiable Forth (∂4) program sketching. T5: Forth addition (100% accuracy, matching ∂4). T6: bubble sort (100% accuracy, scaling to length 6 where ∂4 fails at length 4). T7: word algebra problems (96.5% accuracy, matching ∂4).
  - **T8–T9 (Probabilistic programming + deep learning):** T8: coin classification with distant supervision (reliably recovers latent structure with ≥10 labeled examples). T9: simplified poker game simultaneously learning card recognition and probabilistic parameters (learned distribution closely matches true distribution).
  - Implementation integrates ProbLog2 with PyTorch. Adam optimizer for neural parameters; SGD for probabilistic logic parameters.
