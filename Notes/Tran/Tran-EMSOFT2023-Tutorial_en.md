# Tutorial: Neural Network and Autonomous Cyber-Physical Systems Formal Verification for Trustworthy AI and Safe Autonomy

## Topic
Neural Network CPS Verification

## Background
The increasing use of deep learning models in safety-critical applications demands formal analysis of system behavior, including reasoning about individual components (e.g., controller robustness) and their interactions and effects on the system as a whole. NNV (Neural Network Verification) is a software tool supporting verification of multiple deep learning models, centered on reachability algorithms and various set representations such as star sets, polytopes, zonotopes, and ImageStars. The field has matured with competitions like VNN-COMP and ARCH-COMP AINNCS, as well as standard formats including ONNX and VNN-LIB.

## Limitations & Research Problem
- **Limitation:** Safety-critical CPS increasingly incorporate ML components but lack formal safety guarantees for these components and overall system behavior; existing verification methods have limitations in scalability and supported network types.
- **Problem:** How to formally verify diverse types of neural networks (CNN, RNN, SSNN, BNN, Neural ODE, etc.) and neural network control systems (NNCS) to ensure trustworthy AI and safe autonomy?

## Contributions
- Provides a half-day interactive tutorial systematically demonstrating NNV tool capabilities for neural network and autonomous CPS verification
- Covers verification of a broad range of network types: FFNN, CNN, RNN, Semantic Segmentation NN, Binary NN, Neural ODE, and NNCS
- Demonstrates safety-critical application verification examples from aerospace, automotive, and maritime domains
- NNV tool has been adopted by industry organizations including AFRL, Collins Aerospace, Northrop Grumman, General Motors, and Toyota
- Supports in-browser execution via platforms like CodeOcean for interactive demonstrations

## Methodology
- Reachability analysis-based verification using set representations including star sets, polytopes, zonotopes, and ImageStars to compute exact and over-approximate reachable sets
- Open-loop neural network safety and robustness verification, evaluating model behavior under targeted and random adversarial attacks
- Closed-loop NNCS verification: step-by-step demonstration of loading/creating NNCS models, defining specifications, computing reachable sets, and presenting verification proofs or counterexamples
- Integration with Matlab/Simulink model-based design flow, fitting the typical embedded systems and CPS development workflow
- Demonstrated effectiveness through real use cases from programs such as DARPA Assured Autonomy, ANSR, and NSF Safe Learning-Enabled Systems
