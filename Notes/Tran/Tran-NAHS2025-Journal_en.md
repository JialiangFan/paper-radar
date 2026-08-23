# Quantitative Verification of Learning-Enabled Systems Using ProbStar Reachability

## Topic
Probabilistic Neural Network Verification

## Background
Formal verification of deep neural networks (DNNs) is essential for ensuring the safety of learning-enabled safety-critical autonomous systems. Existing DNN verification methods primarily focus on qualitative verification, returning SAT/UNSAT results to determine whether a network violates safety or robustness properties. However, in practice, sensor inputs inherently contain noise modeled as multivariate Gaussian distributions, necessitating quantitative verification that computes the probability of property violation.

## Limitations & Research Problem
- **Limitation:** Most existing quantitative verification methods target binary neural networks or quantized finite discrete input spaces; only one method addresses continuous input spaces for ReLU networks, and it is restricted to ellipsoidal inputs. Furthermore, system-level verification for Learning-Enabled Cyber-Physical Systems (Le-CPS) provides only qualitative results (Safe/Unsafe/Unknown) without probabilistic quantification.
- **Problem:** How to perform quantitative verification on FFNNs with diverse piecewise linear activation functions (ReLU, LeakyReLU, SatLin, SatLins) over continuous input spaces, and extend this to closed-loop Le-CPS to compute exact probabilities of safety property violations?

## Contributions
- Introduces the Probabilistic Star (ProbStar) set representation, extending the star set with truncated multivariate Gaussian distributions for quantitative reasoning about networks with diverse piecewise linear activations
- Develops two verification strategies: exact verification (computing precise violation probabilities) and over-approximate verification (reducing computation by filtering low-probability paths)
- Proposes the first unified system-level approach for both qualitative and quantitative verification of closed-loop Le-CPS
- Solves ProbStar probability computation under rank-deficient constraint matrices via SVD decomposition and Gaussian approximation of Dirac Delta distributions
- Implements the framework in the open-source StarV tool and evaluates on HorizontalCAS, ACASXu, rocket landing, AEBS, and adaptive cruise control benchmarks

## Methodology
- **ProbStar definition:** Combines star sets with truncated Gaussian distributions, defined as a tuple ⟨c, V, N, P, l, u⟩ where predicate variables follow a Gaussian distribution N(μ, Σ) subject to linear constraints P(α) ≜ Cα ≤ d and element-wise bounds l ≤ α ≤ u
- **Probability computation:** Uses SVD decomposition to project rank-deficient constraint matrices from high-dimensional to low-dimensional spaces, applies Gaussian approximation for singular distributions, and invokes Genz/Botev methods for truncated normal probability computation
- **Layer-by-layer reachability:** For each FFNN layer, performs affine mapping followed by neuron-by-neuron activation handling (stepReLU/stepSatLin/stepLeakyReLU/stepSatLins), splitting input ProbStars into multiple sub-ProbStars with associated probabilities
- **Optimization:** Uses estimated bounds (Proposition 6) to quickly determine whether LP solving is needed for tight bounds, and applies domain contraction to update predicate variable bounds after adding new constraints
- **Le-CPS system-level verification:** Couples the FFNN controller F with a linear plant model x(k+1) = Ax(k) + Bu(k), iteratively propagating ProbStar reachable sets over a bounded time horizon k_max to verify safety properties S and compute satisfaction probabilities P_i at each step
