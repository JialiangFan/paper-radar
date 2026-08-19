---
title: "Learning Control Barrier Functions from Expert Demonstrations"
year: 2020
authors:
  - "Alexander Robey"
  - "Haimin Hu"
  - "Lars Lindemann"
  - "Hanwen Zhang"
  - "Dimos V. Dimarogonas"
  - "Stephen Tu"
  - "Nikolai Matni"
venue: "arXiv"
category: "CBF Reachability"
pdf: "../../PDFs/CBF_Reachability/2020_Robey_LearningCBF.pdf"
url: "https://arxiv.org/abs/2004.03315"
code: ""
project: ""
tags:
  - "constraint-grounding"
  - "control-barrier-functions"
  - "demonstrations"
  - "learning-constraints"
  - "robotics"
  - "safe-vla"
  - "state-space-safety"
---
# Learning Control Barrier Functions from Expert Demonstrations

## One-sentence Summary

This paper learns CBFs from demonstrations, reducing the need to hand-design safe-set functions.

## Problem Setting

Category: CBF Reachability. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Control Barrier Functions]],
[[State-Space Safety]], [[Constraint Grounding]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper learns CBFs from demonstrations, reducing the need to hand-design safe-set functions.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Controller.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

Expert demonstrations provide evidence for safe behavior; the method infers barrier functions that
separate safe and unsafe regions and can be used for certified control.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Controller.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Control Barrier Functions]], [[State-Space Safety]], [[Constraint Grounding]].

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

Demonstrates learned CBFs on control examples where expert behavior encodes safety.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Control Barrier Functions]], [[State-Space Safety]], [[Constraint Grounding]].

## Strengths

- Offers formal language for state-space safety and forward invariance.
- Connects high-level constraints to controller-level guarantees when dynamics and safe sets are available.
- Fits the review theme through [[Control Barrier Functions]], [[State-Space Safety]], [[Constraint Grounding]].

## Limitations

- Requires representative demonstrations and may not capture rare semantic hazards absent from data.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use language-described unsafe sets as additional supervision for learned CBFs.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper learns CBFs from demonstrations, reducing the need to hand-design safe-set functions.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Control Barrier Functions]], [[State-Space Safety]], [[Constraint Grounding]].

## Related Papers

- [[2017_Ames_CBF_QP]]
- [[2025_Yang_CBFRL]]
- [[2023_McPherson_SharedSafetyConstraints]]

## My Notes

- Relevance rank in this workspace: 48.
- Use this paper when arguing for the layer: Training / Model, Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
