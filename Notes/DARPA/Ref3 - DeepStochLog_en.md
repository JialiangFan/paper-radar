# DeepStochLog: Neural Stochastic Logic Programming

## Research Problem
How to build a scalable neural-symbolic framework using stochastic definite clause grammars instead of possible-world semantics, achieving orders-of-magnitude faster inference than PLP-based approaches.

> Winters, T., Marra, G., Manhaeve, R., & De Raedt, L. (2022). DeepStochLog: Neural Stochastic Logic Programming. *The Thirty-Sixth AAAI Conference on Artificial Intelligence (AAAI-22)*.

## Topic
Neural Stochastic Logic Programming

## Background
Neural-symbolic learning methods such as DeepProbLog extend probabilistic logic programs (PLPs) with neural predicates, enabling end-to-end training. However, PLP-based approaches rely on distribution (possible world) semantics, requiring summation over all possible worlds to compute query probabilities — an inference process that is computationally expensive and limits scalability. Stochastic logic programs (SLPs), by contrast, are based on stochastic grammar semantics and treat inference as a random walk process rather than world enumeration, yielding substantially more efficient computation. DeepStochLog proposes a neural-symbolic framework based on stochastic definite clause grammars (SDCGs) as a scalable alternative to neural PLP methods.

## Limitations & Research Problem
- **Limitation 1:** Neural PLP methods based on possible world semantics (e.g., DeepProbLog, NeurASP) require weighted model counting over exponentially many possible worlds; inference cost grows rapidly with program size, causing timeouts on large-scale problems (multi-digit addition, long expressions).
- **Limitation 2:** Existing SLP-based methods (e.g., Tensorlog) are computationally efficient but limited to Datalog with binary predicates, lacking expressiveness for context-sensitive grammars and subsymbolic data processing.
- **Limitation 3:** Neural Grammar approaches (e.g., Neural Grammars) are restricted to context-free grammars (CFGs), do not support unification-based context-sensitive grammars, and do not handle subsymbolic inputs such as images.
- **Problem:** How to design a neural-symbolic framework based on stochastic grammar semantics (rather than possible world semantics) that maintains expressiveness (supporting context-sensitive grammars and general logic programs) while achieving significantly better inference and learning scalability than PLP-based methods?

## Contributions
- Introduces DeepStochLog, which extends stochastic definite clause grammars (SDCGs) with **neural definite clause grammar rules** that encapsulate neural networks as probabilistic generators within grammar rules.
- Inference is based on **SLG resolution (tabling)** to construct AND-OR circuits, which are then evaluated bottom-up using the (+, ×) semiring. SLG resolution — a generalization of the CYK algorithm for CFGs — memoizes subgoal answers, converting AND-OR trees into AND-OR forests and dramatically improving efficiency.
- Learning uses **gradient descent** directly on the AND-OR circuit via backpropagation, which is equivalent to the inside-outside EM algorithm but does not require designing a separate outside algorithm for each grammar formalism.
- Achieves state-of-the-art or competitive results on 6 tasks: MNIST addition (T1), handwritten formulas (T2), well-formed parentheses (T3), context-sensitive grammar (T4), semi-supervised citation network classification (T5), and word algebra problems (T6).
- Orders of magnitude faster than DeepProbLog and NeurASP: on 4-digit MNIST addition, DeepStochLog inference takes only 5.7ms while both competitors timeout.

## Methodology
- **Language Design:** A DeepStochLog program is an extended SDCG that additionally supports neural definite clause grammar rules of the form `nn(m, I, O, D) :: nt → g₁, ..., gₙ`, where `m` identifies a neural network, I are input variables, O is the output variable, and D is the output domain. The neural network defines a conditional probability distribution over output variables given inputs, akin to conditional PCFGs. Empty (ε) productions allow probabilistic decisions without consuming sequence elements, enabling DCGs to express general logic programs beyond pure grammars.
- **Logical Inference:** Given a goal G and terminal sequence T, SLD resolution (or SLG resolution with tabling) finds all derivations and constructs a compact AND-OR circuit. SLG resolution memoizes subgoal answers, avoiding redundant proof of identical subgoals and converting SLD derivation trees into AND-OR forests.
- **Probabilistic Inference:** The AND-OR circuit is compiled into an arithmetic circuit (AND nodes → multiplication, OR nodes → addition) and evaluated bottom-up using the (+, ×) semiring to compute P(derives(G,T)). The most probable derivation is found using the (max, ×) semiring.
- **Learning:** The objective is to minimize a differentiable loss function L(P(derives(G_iθ_i, T_i)), t_i). The arithmetic circuit's computational graph is inherently differentiable, and gradients are computed via automatic backpropagation. When the loss is negative log-likelihood, gradient descent is equivalent to the EM inside-outside algorithm. The Adam optimizer is used for training.
- **Experimental Evaluation:**
  - **T1 (MNIST Addition):** Digit lengths 1–4. DeepStochLog achieves 92.7% at length 4 (DeepProbLog and NeurASP timeout). Inference time at length 4: DSL 5.7ms vs. DPL/NA timeout.
  - **T2 (Handwritten Formulas, HWF):** Mathematical expressions of lengths 1–7 with handwritten digits and operators. DSL achieves 94.8% at length 7 (DPL timeout, NGS 20.4%).
  - **T3 (Well-formed Parentheses):** Both DSL and DPL achieve ~100%; DSL maintains higher accuracy on longer sequences.
  - **T4 (Context-Sensitive Grammar aⁿbⁿcⁿ):** DCGs naturally support context-sensitive grammars. DSL achieves 98.8% at length 3–18 (DPL timeouts at length 3–15+).
  - **T5 (Semi-supervised Citation Classification):** Cora/Citeseer datasets. DSL achieves 69.4%/65.0% (DPL timeouts); competitive with specialized methods despite being a general framework.
  - **T6 (Word Algebra Problems):** 300 training examples. Both DSL and DPL achieve ~94–95%.
  - Tabling is critical for efficiency: on HWF length 11, inference without tabling takes 1996s vs. 132s with tabling.
