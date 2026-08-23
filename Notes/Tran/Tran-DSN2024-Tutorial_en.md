# Tutorial: Safe, Secure, and Trustworthy AI via Formal Verification of Neural Networks and Autonomous CPS with NNV

## Topic
Neural Network Formal Verification

## Background
As AI and machine learning components are increasingly deployed in safety-critical systems like autonomous cyber-physical systems (CPS), ensuring their safety, security, and trustworthiness has become critically urgent. Deep neural networks (DNNs) are known to suffer from lack of robustness and susceptibility to adversarial perturbations, where small input changes can lead to drastically different outputs. Neural network verification, which aims to formally prove that neural networks meet certain specifications, represents a key approach toward establishing trustworthy AI.

## Limitations & Research Problem
- **Limitation:** DNNs lack robustness and are vulnerable to adversarial attacks; existing AI systems often do not function as intended and lack formal safety guarantees.
- **Problem:** How to formally verify neural networks and neural network control systems (NNCS) used in autonomous CPS to prove they satisfy safety and security specifications?

## Contributions
- Provides an interactive tutorial based on the NNV tool, systematically introducing formal verification methods for neural networks and autonomous CPS
- Organized in three parts: (1) lecture overview on safe/trustworthy AI and neural network verification, (2) hands-on neural network verification with NNV, (3) hands-on autonomous CPS verification with NNV
- Demonstrates verification examples from security (malware classification), medicine (medical imaging), and CPS (autonomous vehicles) domains
- Introduces emerging standards including the ONNX model format and VNN-LIB specification language

## Methodology
- Reachability analysis-based formal verification: represents a neural network as a function f: R^n -> R^m, computes (exactly or overapproximately) the output set Y = f(X) for an input subset X, then checks whether an undesired behavior set B intersects with f(X)
- Uses the NNV tool for automated verification, supporting multiple network types (FFNN, CNN, semantic segmentation networks, etc.)
- For autonomous CPS, models the neural network as a feedback controller in a closed-loop system, combined with plant models (ODEs or hybrid automata) for reachability analysis
- Evaluates robustness against targeted and random adversarial attacks to verify safety properties
- Provides design guidance such as minimizing the number of ReLU layers and total ReLU neurons to reduce analysis complexity
