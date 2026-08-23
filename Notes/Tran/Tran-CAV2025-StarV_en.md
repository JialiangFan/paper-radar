# StarV: A Qualitative and Quantitative Verification Tool for Learning-Enabled Systems

## Topic
Learning-enabled systems verification tool

## Background
Deep learning models are widely used in safety-critical domains such as autonomous vehicles and robotics, yet they remain vulnerable to adversarial attacks. Formal verification of learning-enabled systems (LES) is therefore crucial. Existing star-based verification tools like NNV and NNENUM focus primarily on qualitative verification (SAT/UNSAT), lacking the ability to quantify safety violation probabilities under probabilistic uncertainties. StarV is a Python-based successor to NNV (MATLAB), and the first verification tool to provide both qualitative and quantitative verification for deep neural networks and learning-enabled cyber-physical systems.

## Limitations & Research Problem
- **Limitation:** Existing tools (NNV, NNENUM, etc.) only support qualitative verification and cannot quantify safety violation probabilities under probabilistic uncertainties. Verifying deep CNNs (e.g., VGG16) suffers from severe memory and scalability issues. There is no existing method for quantitative verification of LES temporal properties.
- **Problem:** How to build a unified verification framework that supports both qualitative and quantitative verification while efficiently handling large-scale neural networks and massive linear systems?

## Contributions
- Introduced SparseImageStar and SparseStar data structures using sparse matrix formats (COO/CSR), enabling robustness verification of VGG16 under up to 3000-pixel attacks on a local computer, achieving up to 18x memory efficiency over ImageStar and NNV
- Introduced ProbStar reachability for quantitative verification, supporting exact probabilistic safety violation computation for piecewise linear activation functions (ReLU, LeakyReLU, Satlin, Satlins)
- Proposed ProbStar Temporal Logic (ProbStarTL), the first set-based formalism enabling quantitative verification of LES temporal properties using reachability analysis, supporting always and eventually temporal operators
- Added LSTM and GRU network architecture support using SparseStar reachability
- Implemented efficient quantitative reachability for massive linear systems (up to 10,000 dimensions) using Krylov subspace methods

## Methodology
- **Architecture:** StarV contains five modules: User Interface, Parser (PyTorch and ONNX support), Specification (Safety, Robustness, ProbStarTL), Modeling (ODEs, Hybrid Automata), and Engine (core verification algorithms)
- **SparseImageStar:** Flattens 3D RGB images into sparse matrix column vectors (COO/CSR format), uses indices-shifting technique to operate at feature map level, implements SpGEMM convolution and average pooling directly on SparseImageStar, avoiding feature extraction overhead
- **ProbStar Reachability:** ProbStar extends traditional star sets with affine mapping of truncated multivariate Gaussian distributions to model probabilistic inputs. Propagates through network layers to construct reachable output sets (unions of ProbStars), with both exact and over-approximate verification modes
- **ProbStarTL Verification:** Based on ProbStar signals (bounded-time sequences of ProbStar reachable sets), transforms user-defined temporal specifications into Abstract Disjunctive Normal Form (ADNF), then realizes into Computable DNF (CDNF), and computes satisfaction probability via the inclusion-exclusion principle
- **Massive Linear Systems:** Uses Krylov subspace methods (Arnoldi/Lanczos iterations) to efficiently approximate matrix exponentials, combined with initial/output space projections to reduce computational dimensions
- **Evaluation:** Verified MNIST LSTM/GRU, VGG16 CNN, ACASXu networks, and Le-ACC control system. SparseImageStar achieves up to 8.45x speedup over NNV on MNIST CNNs. ProbStarTL is significantly faster than the NeuroSymbolic approach on Le-ACC
