# cplint: A Suite for Probabilistic Logic Programming

## Research Problem
How to provide a comprehensive, unified probabilistic logic programming toolkit supporting exact/approximate inference, parameter/structure learning, and causal reasoning on SWI-Prolog.

> Riguzzi, F., & Azzolini, D. (2025). *cplint (4.5) - software for probabilistic logic programming*. Software documentation, Sep 12, 2025.

## Topic
Probabilistic Logic Programming Software

## Background
Probabilistic logic programming (PLP) unifies probabilistic reasoning with logic programming, providing a coherent framework for knowledge representation and reasoning under uncertainty. The foundational formalisms underlying cplint are LPADs (Logic Programs with Annotated Disjunctions) and CP-logic, which define probability distributions over possible worlds by attaching probability annotations to disjunctive clause heads. cplint is a comprehensive software suite built on SWI-Prolog that provides an end-to-end pipeline from probabilistic inference to both parameter and structure learning, while maintaining compatibility with multiple PLP syntax standards including ProbLog, PRISM, and Distributional Clauses.

## Limitations & Research Problem
- **Limitation:** Traditional logic programming systems cannot natively handle probabilistic uncertainty. Earlier PLP systems (e.g., PRISM, ProbLog) typically supported only discrete distributions or provided only inference capabilities, lacking a unified inference-and-learning framework and offering limited support for continuous random variables.
- **Problem:** How to provide a single software framework that simultaneously supports both discrete and continuous probability distributions, multiple inference strategies (exact and approximate), causal inference via do-calculus, decision theory, and both parameter and structure learning -- all while remaining compatible with multiple PLP syntax standards?

## Contributions
- Provides a unified PLP software suite integrating exact inference (BDD-based PITA program transformation) with multiple approximate inference methods (Monte Carlo sampling, rejection sampling, Metropolis-Hastings MCMC, Gibbs sampling, likelihood weighting, and particle filtering)
- Supports both discrete probability distributions and continuous probability densities, including over a dozen built-in distributions (Gaussian, Beta, Gamma, Dirichlet, Poisson, Binomial, Geometric, Exponential, Negative Binomial, Multinomial, and user-defined densities)
- Maintains compatibility with four PLP syntaxes: native LPAD/CP-logic, ProbLog, PRISM, and Distributional Clauses (DC)
- Offers MPE (Most Probable Explanation), MAP (Maximum A Posteriori), and Viterbi inference via branch-and-bound meta-interpretation
- Supports causal inference based on Pearl's do-calculus
- Supports decision-theoretic reasoning following DTProbLog syntax
- Integrates three learning algorithms: EMBLEM (EM-based parameter learning over BDDs), SLIPCOVER (structure learning by searching clause and theory spaces), and LEMUR (structure learning via Monte Carlo tree search)
- Provides cplint on SWISH, a web application for interactive online use with built-in result visualization (C3.js and R)

## Methodology
- **Exact Inference (PITA):** Compiles LPAD programs via program transformation into Prolog programs augmented with BDD (Binary Decision Diagram) operations, using the bddem foreign library to efficiently compute probabilities over the compiled representation. Variant systems PITA(IND,IND) and PITA(IND,EXC) accelerate computation by assuming independence and exclusivity of atoms in conjunctions and disjunctions, respectively.
- **Approximate Inference (mcintyre):** Employs a sampling-based program transformation technique where a meta-interpreter randomly samples possible worlds and estimates query probabilities from success rates. This is the only inference module capable of handling continuous random variables.
- **Conditional Inference Strategies:** For discrete variables, supports rejection sampling, Metropolis-Hastings MCMC (with configurable lag and mixing parameters), and Gibbs sampling (with blocked sampling). For continuous variables, additionally supports likelihood weighting (which assigns importance weights based on evidence likelihood) and particle filtering (sequential Monte Carlo with resampling after each evidence element).
- **Semantics:** Based on LPAD possible worlds semantics -- a world is obtained by grounding the program and selecting exactly one head atom per ground clause; the probability of a world is the product of selected head probabilities, and query probability is the sum over all worlds where the query holds. For programs with continuous random variables, the semantics is extended via the Borel sigma-algebra over R^N with Lebesgue measure as the probability measure, lifted to the full program using least model semantics of constraint logic programs.
- **Parameter Learning (EMBLEM):** Runs Expectation Maximization directly on BDD representations, exploiting the compact BDD structure to efficiently compute expectations. Parameters can be initialized via truncated Dirichlet processes or symmetric Dirichlet distributions.
- **Structure Learning (SLIPCOVER / LEMUR):** SLIPCOVER searches the clause space and theory space separately to learn probabilistic logic program structure, using Progol-style language bias (mode declarations with modeh/modeb). LEMUR performs structure learning by searching the clause space using Monte Carlo tree search. Both algorithms support bottom clause construction and refinement-based specialization modes.
