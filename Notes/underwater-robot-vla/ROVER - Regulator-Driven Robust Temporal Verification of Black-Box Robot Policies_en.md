# ROVER: Regulator-Driven Robust Temporal Verification of Black-Box Robot Policies

## Topic
Post-hoc safety evaluation and iterative improvement of black-box robot policies using Signal Temporal Logic (STL) specifications and quantitative robustness metrics.

## Background
Deep reinforcement learning policies for robotics are typically black boxes, making it difficult for external regulators or certification bodies to verify their safety properties. Traditional testing approaches (e.g., counting failures) lack the temporal expressiveness needed to capture complex safety requirements like "if the robot deviates, it must correct within T timesteps." Signal Temporal Logic provides quantitative robustness semantics that can measure not just whether a safety property is satisfied, but by how much -- enabling graded, actionable feedback for policy improvement.

## Limitations & Research Problem
- **Limitation:** Existing safety evaluation methods either require white-box access to the policy internals (impractical for proprietary or complex neural network policies) or rely on binary pass/fail metrics that provide no guidance for improvement.
- **Limitation:** Standard reward shaping for safety is typically ad-hoc and does not systematically address temporal safety requirements that span multiple timesteps.
- **Problem:** How to provide a principled, quantitative, black-box safety evaluation framework that (1) formalizes temporal safety rules, (2) measures policy compliance with graded metrics, and (3) generates actionable feedback to iteratively improve policy safety?

## Contributions
- A regulator-in-the-loop iterative framework (ROVER) for black-box policy evaluation using STL specifications over execution traces
- Three complementary robustness metrics: Total Robustness Value (TRV) for average compliance, Largest Robustness Value (LRV) for worst-case analysis, and Average Violation Robustness Value (AVRV) for violation severity
- Decision rules for classifying policy safety profiles into actionable categories (no action needed, policy improvement, edge-case analysis)
- A weighted safety scoring system S(pi) that incorporates domain-informed specification priorities
- Cross-domain validation on virtual racing (Mario Kart SNES) and mobile robot navigation (TurtleBot3), including real-world deployment

## Methodology
- **STL Specification Formalization**: Domain experts translate human-readable temporal safety rules into STL formulas. For virtual racing: global speed limits, track boundary compliance with recovery time bounds, and turn-conditional acceleration delays. For navigation: smooth turning constraints, timed goal completion, and obstacle proximity escape requirements.
- **Trace Collection & Robustness Computation**: N=100 rollout traces are collected from the black-box policy. For each trace and each STL specification, the quantitative robustness value rho(phi, tau) is computed, yielding a distribution of robustness scores per specification.
- **Metric Aggregation**:
  - TRV = sum of robustness values across all traces (overall compliance)
  - LRV = minimum robustness value across all traces (worst-case)
  - AVRV = mean of negative robustness values only (violation severity)
- **Regulator Decision Framework**: Based on metric combinations, regulators issue recommendations: "No action" (metrics near zero, low dispersion), "Policy improvement" (all metrics strongly negative), or "Edge-case analysis" (LRV much worse than AVRV, indicating rare catastrophic failures).
- **STL-Guided Reward Reshaping**: Regulator feedback is translated into reward function modifications -- e.g., increasing road-departure penalties, adding explicit speed limit reward terms, or adding action smoothness rewards. The policy is then retrained with the modified reward.
- **Iterative Refinement**: The evaluate-feedback-retrain loop repeats until the regulator is satisfied with the safety profile.
- **Experimental Setup**: Virtual racing domain uses PPO-trained agents in Mario Kart SNES with 3 STL specifications evaluated over 100 traces. Navigation domain uses SAC-trained TurtleBot3 agents in Gazebo simulation with 3 STL specifications, also validated on physical TurtleBot3 hardware. Pre- and post-verification satisfaction rates, TRV, and LRV changes are compared.

## Key Results
- Average satisfaction rate improvement of 43.8% across six STL specifications and two domains
- Virtual racing: "Stay on Track" improved from 8% to 99% satisfaction; "Speed Limit" from 30% to 83%
- Navigation simulation: "Timed Completion" improved from 18% to 54%; "Don't Linger" from 45% to 67%
- Real-world TurtleBot3: 27% improvement in smooth-navigation satisfaction rate
- Sim-to-real gap observed: real-world policies exhibited more frequent turns than in simulation
- TRV improvements confirmed consistent average-case improvement; LRV improvements in 3 of 6 specifications indicated reduced worst-case severity
