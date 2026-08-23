# Learning Dynamic Rope Manipulation Using Task-Level Iterative Learning Control

- **Title:** Learning Dynamic Rope Manipulation Using Task-Level Iterative Learning Control
- **Authors:** Krishna Suresh, Chris Atkeson
- **Venue:** arXiv preprint (arXiv:2602.21302)
- **Year:** 2026
- **Affiliations:** Carnegie Mellon University

## Topic
Task-level ILC for rope manipulation

## Background
Dynamic manipulation of deformable objects (ropes, cloth) is hard for both robots and humans due to their many unactuated degrees of freedom and the difficulty of accurate modeling. This work studies the non-planar "flying knot" task (tying an overhand knot with a single one-handed whip-and-twist motion) and shows how a robot can learn it with very few real-world trials, without large demonstration datasets or massive simulation.

## Limitations & Research Problem
- **Limitation:** Typical ILC is designed for robot trajectory tracking and weights errors equally along the whole trajectory; this equal weighting causes learning to fail for deformable-object manipulation.
- **Limitation:** Simulation-based policy learning needs large amounts of simulated data and suffers from the sim-to-real gap; domain randomization is a worst-case robust design that degrades nominal performance.
- **Problem:** Can a robot learn a dynamic rope-manipulation task directly on hardware in fewer than 10 trials, from a single human demonstration plus a simplified rope model, and transfer across different ropes?

## Contributions
- Extends ILC from refining robot state trajectories to refining the trajectories of the **manipulated object's unactuated degrees of freedom**.
- Introduces **Task-Level ILC** for dynamic rope manipulation, tying a flying knot from a single demonstration in <10 real trials and transferring across ropes.
- Introduces a **critical-point objective** that focuses learning on a single key moment of the error history (the rope-rope collision) rather than weighting the whole trajectory equally; shown to be essential for success.
- Achieves 100% success across 7 rope types (chain, latex surgical tubing, braided/twisted ropes; 7–25 mm thick, 0.013–0.5 kg/m) and transfers across most rope types in 2–5 trials.

## Methodology
- **Overall pipeline:** A Task-Level ILC loop — execute initial command u(t) on hardware → measure task state x(t) → compute task error at the critical point → map it through an inverse model M⁻¹ into a command correction Δu(t) → update the command.
- **Critical-point objective:** Pick a key time t_c (here the rope-rope collision) and minimize only the weighted error ‖x(t_c) − x^demo(t_c)‖²_Q at that instant, rather than the integral of tracking error, avoiding interference from free-rope errors before/after collision.
- **Command parameterization:** The feedforward command is represented by 10 Bézier curves (7 joints + 3 base-translation dims) with 8 knot points each, strongly reducing dimensionality; a base-translation constraint enforces translation invariance of the task objective.
- **Optimization-based inverse model:** A QP minimizes a quadratic task objective subject to linearized dynamics Δx=MΔκ and joint position/velocity/acceleration/torque limits; solved with Drake + the Clarabel solver to return the command correction Δκ*.
- **Models:** The robot is a kinematic chain (100:1 gearing makes the rope's effect on robot dynamics negligible); the rope is a 3D serial chain of point masses (11 links, weighted end), simulated with a maximal-coordinate variational integrator.
- **Experimental setup:** xArm 7 arm at 250 Hz; Vicon Vantage 16 motion capture tracking 11 rope markers; compared against two baselines — directly tracking the human hand motion, and equally-weighted ILC on rope motion; 40 trials for success rate; evaluated for cross-rope transfer and robustness to model parameters (stiffness, end mass).
