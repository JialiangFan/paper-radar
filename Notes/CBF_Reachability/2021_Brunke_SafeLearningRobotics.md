---
title: "Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning"
year: 2021
authors:
  - "Lukas Brunke"
  - "Melissa Greeff"
  - "Adam W. Hall"
  - "Zhaocong Yuan"
  - "Siqi Zhou"
  - "Jacopo Panerati"
  - "Angela P. Schoellig"
venue: "Annual Review of Control, Robotics, and Autonomous Systems"
category: "CBF Reachability"
pdf: "../../PDFs/CBF_Reachability/2021_Brunke_SafeLearningRobotics.pdf"
url: "https://arxiv.org/abs/2108.06266"
code: ""
project: ""
tags:
  - "action-shielding"
  - "control-barrier-functions"
  - "robotics"
  - "runtime-assurance"
  - "safe-learning"
  - "safe-vla"
  - "survey"
---
# Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning

## One-sentence Summary

This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification.

## Problem Setting

Category: CBF Reachability. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Runtime Assurance]], [[Action
Shielding]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Inference / Action, Controller.
- Covers safety scope: State-space, Low-level Robot, Embodied / Spatial.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

It reviews robust/adaptive control, Gaussian processes, CBFs, reachability, model predictive safety,
constrained RL, and policy certification.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Inference / Action, Controller.
- Safety scope: State-space, Low-level Robot, Embodied / Spatial.
- Main interface to Safe VLA: [[Runtime Assurance]], [[Action Shielding]], [[Control Barrier Functions]], [[Reachability Analysis]].

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

Survey paper focused on realistic robotics safety and benchmark needs.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Runtime Assurance]], [[Action Shielding]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Strengths

- Offers formal language for state-space safety and forward invariance.
- Connects high-level constraints to controller-level guarantees when dynamics and safe sets are available.
- Fits the review theme through [[Runtime Assurance]], [[Action Shielding]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Limitations

- It predates the recent VLA wave and does not address semantic safety or multimodal foundation models directly.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use it as the classical robotics safety backbone for Safe VLA runtime assurance.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Assurance]], [[Action Shielding]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Related Papers

- [[2017_Fisac_GeneralSafetyFramework]]
- [[2018_Wabersich_PredictiveSafetyFilter]]
- [[2023_Hsu_SafetyFilterUnified]]

## My Notes

- Relevance rank in this workspace: 37.
- Use this paper when arguing for the layer: Training / Model, Inference / Action, Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot, Embodied / Spatial.
