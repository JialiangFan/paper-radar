# Radial Restraint: Bounded Rationality for Logic Programs

## Research Problem
How to guarantee termination and decidability of logic program evaluation under non-monotonic negation while soundly approximating the well-founded model with minimal overhead.

## Topic
Bounded rationality in logic programs

## Background
Declarative logic programs (LP) based on the well-founded semantics (WFS) are widely used for knowledge representation (KR) in databases, business rules, and the semantic web. Logical functions are expressively desirable in KR -- particularly in Rulelog, the logical extension of LP developed within the SILK project, where functions support HiLog, defeasibility via argumentation theories, and existentials in omniform rules. However, when functions are present, the Herbrand universe becomes infinite, rendering LP inferencing undecidable: models may be infinite and a single query may yield infinitely many answers.

## Limitations & Research Problem
- **Limitation:** The dominant practical approach to mitigating undecidability caused by functions is to set engine-level parameters (e.g., timeouts or term-depth bounds in Prolog) and treat any atom not inferred within the bound as false. This introduces unsoundness when an atom A is incomplete and another atom A' depends negatively on A. Moreover, inference outcomes become implementation-dependent and lack declarative semantic grounding.
- **Problem:** How can functions be permitted in LP while guaranteeing finiteness of models, decidability of inferencing, and soundness in the presence of non-monotonicity?

## Contributions
- Introduces **radial restraint**, a novel bounded rationality approach for LP parameterized by a norm (measuring syntactic complexity of terms) and an associated abstraction function. Terms exceeding the norm bound are assigned the WFS third truth value of *undefined* rather than false, thereby preserving soundness even under non-monotonic negation.
- Defines a **fixed-point semantics for radially restrained well-founded models** (Definition 4) and proves they soundly approximate the standard well-founded model (Theorem 2, Corollary 1). Weaker abstraction functions yield tighter approximations, forming a monotone chain of successively more informative finite models.
- Establishes that finitary abstraction functions guarantee finiteness of the true-atom set (Proposition 1) and that the restrained model reaches its fixed point at a finite ordinal (Theorem 1), ensuring decidability and termination.
- Proposes **SLG_ABS**, an extension of tabled SLG resolution that incorporates abstraction at both the subgoal creation and answer derivation stages. SLG_ABS is proven correct with respect to radially restrained models (Theorem 4) and terminates under finitary abstraction (Theorem 3).
- Provides a complexity analysis showing SLG_ABS achieves O(|subgoals(F_fin)| x size(P_Q(E))), matching the best known bound for well-founded semantics computation (Theorem 5).
- Implements SLG_ABS with depth-k abstraction in XSB Prolog (v3.3.7), with answer abstraction overhead of only 0-4%, scaling to knowledge bases exceeding 10^8 rules and facts.

## Methodology
- **Norm and Abstraction Function Framework:** A norm N(.) maps terms to non-negative integers satisfying N(t)=0 iff t is the empty term, and subsumption monotonicity. An abstraction function abs(.) replaces subterms exceeding the norm bound with position variables, ensuring abs(t) subsumes t. The canonical instance is depth-k abstraction, which replaces all subterms at depth greater than k with fresh variables. Norms and abstractions are finitary when the set of distinct abstracted terms over the Herbrand universe is finite.
- **Radially Restrained Well-Founded Model Construction:** The standard dynamic stratification iterated fixed-point construction is modified (Definition 4) by augmenting the True_I^P and False_I^P operators with the constraint abs(B*theta) = B*theta. Only ground instances invariant under abstraction can be classified as true or false; all others default to undefined. This yields a three-valued model that is a subset of (i.e., sound with respect to) the standard well-founded model.
- **SLG_ABS Resolution:** Extends SLG with two abstraction mechanisms: (1) Subgoal Abstraction (Definition 7) applies abs(.) when creating a new tree for a subgoal in the evaluation forest; (2) Answer Abstraction (Definition 8) applies abs(.) during the POSITIVE RETURN operation -- when an answer Ans differs from abs(Ans), a reserved atom undefined_abs is appended to the Delays, permanently marking the answer as undefined. NEGATIVE RETURN is generalized to resolve non-ground failed subgoals.
- **Implementation in XSB:** Answer abstraction is performed within the SLG-WAM's answer check/insert step by maintaining a depth counter during answer traversal. When depth exceeds k, the current subterm is replaced by a free position variable and undefined_abs is added to Delays. Depth-k abstraction is configurable on a per-predicate basis, enabling fine-grained control over restraint granularity.
