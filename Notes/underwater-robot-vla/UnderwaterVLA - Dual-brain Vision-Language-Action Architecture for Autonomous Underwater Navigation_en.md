# UnderwaterVLA: Dual-brain Vision-Language-Action Architecture for Autonomous Underwater Navigation

## Topic
First Vision-Language-Action framework for autonomous underwater vehicle (AUV) navigation, using a dual-brain hierarchical architecture that separates high-level mission reasoning from low-level reactive control.

## Background
Autonomous underwater vehicles face unique challenges including degraded visual conditions (turbidity, poor lighting), limited communication bandwidth at depth, and complex hydrodynamics. While VLA models have shown promise in terrestrial robotics, their application to underwater domains remained unexplored. Traditional underwater navigation systems rely heavily on task-specific training data (e.g., ~262K demonstration images) and lack interpretable decision-making, making them difficult to deploy in novel underwater scenarios.

## Limitations & Research Problem
- **Limitation:** Existing underwater autonomy approaches require large amounts of costly underwater demonstration data for training
- **Limitation:** End-to-end single-brain models fail under degraded visual conditions -- they continue executing stale commands without replanning, causing overshoot and safety violations
- **Limitation:** Conventional methods lack interpretable decision-making, making real-time monitoring and debugging difficult
- **Problem:** How to achieve robust, interpretable autonomous underwater navigation that generalizes to degraded conditions without requiring underwater-specific training data

## Contributions
- First application of Vision-Language-Action models to the AUV domain, demonstrating feasibility of zero-shot underwater navigation
- Dual-brain architecture separating cloud-based mission planning (QVQmax) from on-device reactive control (Qwen 2.5-VL-7B), enabling operation under bandwidth-limited conditions
- Hydrodynamics-aware Model Predictive Control with online drag coefficient estimation from IMU data, requiring no pre-training
- Chain-of-thought reasoning for interpretable decision-making with structured JSON outputs
- 19-27% higher task completion rates over baselines in real-world degraded visual conditions (up to 18 NTU turbidity)

## Methodology
- **Cloud Brain (QVQmax)**: Operates during AUV surfacing events. Uses chain-of-thought prompting to decompose high-level missions into ordered sub-task sequences (e.g., "Navigate to coral reef avoiding shipwrecks" becomes sonar localization, path planning, waypoint transmission). Generates long-horizon plans transmitted to the local brain before descent.
- **Local Brain (Qwen 2.5-VL-7B)**: On-device model running closed-loop perception-action cycles. Outputs structured JSON containing explicit reasoning, decision, velocity commands, and task completion flags. Operates independently during deep deployments without cloud communication.
- **Hydrodynamics-Aware MPC**: Three-phase velocity profile (acceleration 0-0.2s, constant 0.2-0.5s, deceleration 0.5-1.0s) running at 50Hz. Cost function minimizes tracking error, control effort, and drag compensation. Quadratic drag model F_drag = D_v * v|v| with coefficients estimated online via IMU without pre-training.
- **Zero-Shot Paradigm**: Leverages pre-trained foundation models directly -- requires 0 underwater training samples, in contrast to baselines needing ~262K demonstration images.
- **Experimental Setup**: Real-world testing in controlled tank with cylindrical obstacles. Degraded condition testing with illumination reduction and diatomaceous earth injection (turbidity 0.5 to 18 NTU). Baselines compared against QUAR-VLA simulation results. Four task types evaluated: letter distinction (easy), object navigation (medium), tunnel traversal (hard), obstacle avoidance (hard). Results: 85% (letter), 80% (navigation), 80% (tunnel), 60% (obstacle avoidance), representing +19% to +27% improvements over baselines.
