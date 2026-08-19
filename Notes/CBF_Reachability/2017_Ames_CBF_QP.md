---
title: "Control Barrier Function Based Quadratic Programs for Safety Critical Systems"
year: 2017
authors:
  - "Aaron D. Ames"
  - "Xu"
  - "Grizzle"
  - "Tabuada"
venue: "IEEE TAC"
category: "CBF Reachability"
pdf: "../../PDFs/CBF_Reachability/2017_Ames_CBF_QP.pdf"
url: "https://ieeexplore.ieee.org/document/7782377"
code: ""
project: ""
tags:
  - "action-shielding"
  - "control-barrier-functions"
  - "controller-safety"
  - "robotics"
  - "safe-vla"
  - "safety-filter"
  - "state-space-safety"
---
# Control Barrier Function Based Quadratic Programs for Safety Critical Systems

## One-sentence Summary

This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller.

## Problem Setting

Category: CBF Reachability. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Control Barrier Functions]],
[[Action Shielding]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller.
- Clarifies or exercises the safety-enforcement layer: Controller.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

Defines safety by a superlevel set of a barrier function and solves a quadratic program that
minimally modifies the nominal control subject to CBF derivative constraints.

Implementation-level interpretation for this review:

- Safety enforcement layer: Controller.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Control Barrier Functions]], [[Action Shielding]], [[State-Space Safety]], [[Low-level Robot Safety]].

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

Demonstrates the method on safety-critical control examples, establishing the basis for many
robotics safety filters.

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

For the preferred research framing, the paper contributes most to: [[Control Barrier Functions]], [[Action Shielding]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Strengths

- Offers formal language for state-space safety and forward invariance.
- Connects high-level constraints to controller-level guarantees when dynamics and safe sets are available.
- Fits the review theme through [[Control Barrier Functions]], [[Action Shielding]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Limitations

- The user must provide a valid barrier function and sufficiently accurate dynamics; perception and semantic grounding are outside the formulation.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Treat grounded semantic constraints as generators of barrier functions and use CBF-QPs as the final action shield for VLA outputs.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Control Barrier Functions]], [[Action Shielding]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Related Papers

- [[2025_Hu_VLSA_AEGIS]]
- [[2019_Ames_CBFTheory]]
- [[2022_Lederer_ElasticJointCBF]]

## My Notes

- Relevance rank in this workspace: 10.
- Use this paper when arguing for the layer: Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
