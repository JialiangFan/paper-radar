---
title: "CBF-RL: Safety Filtering Reinforcement Learning in Training with Control Barrier Functions"
year: 2025
authors:
  - "Lizhi Yang"
  - "Blake Werner"
  - "Massimiliano de Sa"
  - "Aaron D. Ames"
venue: "arXiv"
category: "CBF Reachability"
pdf: "../../PDFs/CBF_Reachability/2025_Yang_CBFRL.pdf"
url: "https://arxiv.org/abs/2510.14959"
code: ""
project: ""
tags:
  - "action-shielding"
  - "control-barrier-functions"
  - "humanoid"
  - "low-level-robot-safety"
  - "robotics"
  - "safe-rl"
  - "safe-vla"
---
# CBF-RL: Safety Filtering Reinforcement Learning in Training with Control Barrier Functions

## One-sentence Summary

CBF-RL uses CBF filtering during training so policies internalize safety and may deploy without an online filter.

## Problem Setting

Category: CBF Reachability. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Control Barrier Functions]],
[[Action Shielding]], [[Low-level Robot Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- CBF-RL uses CBF filtering during training so policies internalize safety and may deploy without an online filter.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Controller.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

The algorithm minimally modifies nominal RL policy rollouts using CBF terms and safety filtering,
with theory connecting continuous-time filters to discrete-time rollouts.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Controller.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Control Barrier Functions]], [[Action Shielding]], [[Low-level Robot Safety]].

## Key Equations or Formalisms

The standard CBF safe set is:

```math
\mathcal{C}=\{x\mid h(x)\ge 0\}
```

A controller keeps the system forward invariant by choosing actions that satisfy:

```math
\dot h(x,u)+\alpha(h(x))\ge 0
```

Runtime shielding is often written as a minimally invasive quadratic program:

```math
u^* = \arg\min_u \|u-u_{nom}\|^2 \quad
\text{s.t.}\quad \dot h(x,u)+\alpha(h(x))\ge 0
```

## Experiments

Ablates navigation tasks and demonstrates safe behavior on a Unitree G1 humanoid robot.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Control Barrier Functions]], [[Action Shielding]], [[Low-level Robot Safety]].

## Strengths

- Offers formal language for state-space safety and forward invariance.
- Connects high-level constraints to controller-level guarantees when dynamics and safe sets are available.
- Fits the review theme through [[Control Barrier Functions]], [[Action Shielding]], [[Low-level Robot Safety]].

## Limitations

- Training-time internalization is useful but less plug-and-play than an external VLA shield for existing policies.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Compare training-time CBF internalization against runtime VLA shielding in the same benchmark.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: CBF-RL uses CBF filtering during training so policies internalize safety and may deploy without an online filter.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Control Barrier Functions]], [[Action Shielding]], [[Low-level Robot Safety]].

## Related Papers

- [[2025_Hu_VLSA_AEGIS]]
- [[2017_Ames_CBF_QP]]
- [[2025_Zhang_SafeVLA]]

## My Notes

- Relevance rank in this workspace: 49.
- Use this paper when arguing for the layer: Training / Model, Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
