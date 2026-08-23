# Inductive Logic Programming at 30

## Research Problem
How to learn interpretable, general logic programs from small numbers of examples by leveraging background knowledge, meta-level search, and predicate invention.

## Topic
ILP Advances and Future Directions

## Background
Inductive Logic Programming (ILP) is a form of logic-based machine learning that aims to induce a hypothesis (a logic program) that generalises given training examples and background knowledge (BK). Unlike most ML approaches that use vectors or tensors to represent data and learn functions, ILP uses logic programs to represent data and learns relations. Since its introduction by Muggleton in 1991, ILP has reached its 30th anniversary. This survey by Cropper, Dumancic, Evans, and Muggleton (2022) reviews the last decade of ILP research, focusing on four major areas of progress: meta-level search methods, techniques for learning recursive programs, new approaches for predicate invention, and the integration of diverse technologies.

## Limitations & Research Problem
- **Limitation 1:** Classical top-down and bottom-up search methods are inefficient over large hypothesis spaces. Top-down approaches may generate many hypotheses that fail to cover examples, while bottom-up approaches tend to produce unnecessarily long clauses and struggle to learn recursive hypotheses or support predicate invention.
- **Limitation 2:** Most ILP systems do not support predicate invention (PI), and those that do heavily depend on user-provided metarules or predefined symbol spaces, making it difficult to automatically invent high-level concepts.
- **Limitation 3:** ILP has traditionally relied on hand-crafted background knowledge designed by domain experts. Obtaining suitable BK is both difficult and expensive, and over-reliance on hand-crafted BK is a widely acknowledged criticism of the field.
- **Limitation 4:** Classical systems such as FOIL and Progol struggle to learn recursive programs from small numbers of training examples, limiting generalisation to inputs of arbitrary length.
- **Problem:** How can meta-level search, recursion, predicate invention, and emerging technologies (ASP solvers, neural networks) overcome these bottlenecks to achieve more efficient, expressive, and scalable inductive logic programming?

## Contributions
- Provides a systematic survey of four core advances in ILP over the past decade: (i) meta-level search methods, (ii) recursive program learning, (iii) predicate invention, and (iv) integration of diverse technologies.
- Presents a clear comparative framework (Table 1) contrasting old ILP (top-down/bottom-up search, limited recursion, no predicate invention, first-order hypotheses, Prolog-based) with new ILP (meta-level search, full recursion support, limited predicate invention, ASP/higher-order/probabilistic hypotheses, Prolog + ASP + neural networks).
- Articulates the distinctive advantages of ILP over mainstream ML: data efficiency (learning from very few examples, often a single one), use of background knowledge for complex relational reasoning, expressivity (learning cellular automata, Petri nets, answer set programs, general algorithms), and explainability (logic programs are human-readable and support ultra-strong ML).
- Identifies current limitations and proposes directions for future research.

## Methodology
- **Meta-level search:** The ILP learning problem is encoded as a meta-level logic program, and the hypothesis search is delegated to off-the-shelf solvers (e.g., ASP solvers). Representative systems include ASPAL, ILASP3, Metagol, and Popper. ILASP3 employs a counter-example-driven select-and-constrain loop, using an ASP solver to find the best hypothesis at each iteration and generating constraints from failures. Popper operates in three repeating stages -- generate, test, and constrain -- translating hypotheses (rather than individual examples) into constraints that prune the search space.
- **Recursion:** Meta-Interpretive Learning (MIL) introduces metarules (higher-order clause templates) to restrict the form of inducible programs, enabling systems such as Metagol to learn recursive programs. Key metarules include the *chain* metarule (P(A,B) <- Q(A,C), R(C,B)) and the *tailrec* metarule (P(A,B) <- Q(A,C), P(C,B)). This allows generalisation from small numbers of examples to inputs of arbitrary length, opening ILP to applications in string transformations, answer set grammars, and general algorithm synthesis.
- **Predicate invention:** Automatic invention of new auxiliary predicate symbols to reduce sample complexity, improve predictive accuracy, and enable knowledge reuse. Approaches include: (a) placeholders (predefining invented symbols via mode declarations, though requiring user-specified arity); (b) metarule-driven PI (MIL systems use metarules to chain invented predicates automatically); (c) pre/post-processing PI (CUR2LED clusters BK relations into new predicates, ALPs learn latent predicates via auto-encoding logic programs, Knorf refactors programs to compress and remove redundancy, reducing BK program size by 50% or more).
- **Lifelong learning:** Metagol_DF tackles multi-task learning by adding solved-task solutions to BK for reuse in subsequent tasks. Forgetgol introduces a forgetting mechanism to dynamically grow and shrink BK, reducing hypothesis space size and sample complexity.
- **Hypothesis representations:** The field has expanded beyond traditional Prolog to Datalog (guaranteed termination, encodable as SAT/SMT satisfiability problems), as well as ASP, higher-order, and probabilistic representations, enabling integration with modern constraint-solving and statistical reasoning technologies.
