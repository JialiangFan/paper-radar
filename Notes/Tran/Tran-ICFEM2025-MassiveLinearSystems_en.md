# Quantitative Verification for Temporal Properties of Massive Linear Systems

## Topic
Massive linear systems quantitative verification

## Background
Verification of linear time-invariant (LTI) systems is critical for ensuring safety and reliability of engineered systems in fields like aerospace, automotive control, and signal processing. Traditional reachability analysis methods focus on qualitative verification, providing binary YES/NO results, but cannot quantify the probability that a system satisfies temporal properties. For large-scale discrete-time LTI systems, computing the matrix exponential becomes intractable in high dimensions due to exponential growth in computation and memory costs.

## Limitations & Research Problem
- **Limitation:** Existing tools like Hylaa only support qualitative verification (invariant property checking) and cannot compute satisfaction probabilities. Direct matrix exponential computation (Taylor series / Pade approximation) is infeasible for large-scale systems. There is no formal framework that can express complex temporal properties with nested operators and compute their satisfaction probabilities.
- **Problem:** How to perform efficient quantitative verification of large-scale (up to 10,000 dimensions) discrete-time LTI systems, supporting both complex temporal property verification and exact or bounded satisfaction probability computation?

## Contributions
- Proposed a simulation-based probabilistic reachability method using Krylov subspace methods (Arnoldi and Lanczos iterations) to efficiently construct reachable sets for high-dimensional discrete-time LTI systems, combined with initial/output space projections to reduce simulation count
- Leveraged ProbStar representation and ProbStarTL to quantitatively analyze and verify complex temporal properties over ProbStar signals
- Demonstrated scalability and effectiveness on nine large-scale linear system benchmarks (dimensions ranging from Motor to MNA5 at 10,922 dimensions), compared against the Hylaa tool

## Methodology
- **Problem Formulation:** Focuses on discrete-time LTI systems with piecewise-constant inputs. Initial states are represented as ProbStars (probabilistic star sets incorporating Gaussian distributions). Defines two core problems: probabilistic reachability analysis and quantitative verification
- **ProbStar Temporal Logic (ProbStarTL):** Based on discrete-time Signal Temporal Logic (DT-STL) syntax, interprets temporal formulas over ProbStar signals (sequences of reachable ProbStar sets). Recursively constructs constraint sets and supports always, eventually, and next temporal operators
- **DNF Transformation:** Converts ProbStarTL specifications into Abstract DNF (ADNF) then realizes into Computable DNF (CDNF). Computes exact satisfaction probability via inclusion-exclusion principle when CDNF length is 11 or fewer; otherwise computes approximate upper and lower bounds
- **Krylov Subspace Acceleration:** Uses Arnoldi (general matrices) and Lanczos (symmetric matrices) iterations to project the n-dimensional system into a k-dimensional subspace (k much less than n), approximating matrix exponentials with a posteriori error bounds for accuracy control
- **Initial/Output Space Projection:** Defines output space O and initial space I projection matrices, reducing simulation count from n dimensions to min(o, i) dimensions. When output dimension is lower than initial dimension, uses transposed dynamics to further reduce computation
- **Evaluation:** Verified three types of ProbStarTL specifications across nine benchmarks, with system dimensions ranging from Motor (small-scale) to MNA5 (10,922 dimensions) and Heat3D (8,000 dimensions). All models successfully completed both qualitative and quantitative verification. Hylaa could only perform qualitative verification on a subset of models for the first specification type
