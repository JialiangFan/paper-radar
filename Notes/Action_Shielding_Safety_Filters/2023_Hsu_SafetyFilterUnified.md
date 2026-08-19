---
title: "The Safety Filter: A Unified View of Safety-Critical Control in Autonomous Systems"
year: 2023
authors:
  - "Hsu"
  - "et al."
venue: "arXiv"
category: "Action Shielding Safety Filters"
pdf: "../../PDFs/Action_Shielding_Safety_Filters/2023_Hsu_SafetyFilterUnified.pdf"
url: "https://arxiv.org/abs/2309.05837"
code: ""
project: ""
tags:
  - "action-shielding"
  - "control-barrier-functions"
  - "robotics"
  - "runtime-assurance"
  - "safe-vla"
  - "safety-filter"
  - "survey"
---
# The Safety Filter: A Unified View of Safety-Critical Control in Autonomous Systems

## One-sentence Summary

This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families.

## Problem Setting

Category: Action Shielding Safety Filters. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Action
Shielding]], [[Runtime Assurance]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families.
- Clarifies or exercises the safety-enforcement layer: Inference / Action, Controller.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

It abstracts safety filters into monitor, intervention, model, and admissible-set components,
comparing guarantees and scalability trade-offs.

Implementation-level interpretation for this review:

- Safety enforcement layer: Inference / Action, Controller.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Action Shielding]], [[Runtime Assurance]], [[Control Barrier Functions]], [[Reachability Analysis]].

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

Survey/unification paper rather than a single benchmark.

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

For the preferred research framing, the paper contributes most to: [[Action Shielding]], [[Runtime Assurance]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Strengths

- Separates nominal policy performance from safety enforcement.
- Naturally supports plug-and-play deployment around existing learned policies.
- Fits the review theme through [[Action Shielding]], [[Runtime Assurance]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Limitations

- The paper does not solve semantic constraint grounding, but it offers the right architecture vocabulary.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use its modular decomposition as the design template for the VLA runtime safety layer.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Action Shielding]], [[Runtime Assurance]], [[Control Barrier Functions]], [[Reachability Analysis]].

## Related Papers

- [[2018_Wabersich_PredictiveSafetyFilter]]
- [[2019_Ames_CBFTheory]]
- [[2021_Brunke_SafeLearningRobotics]]

## My Notes

- Relevance rank in this workspace: 45.
- Use this paper when arguing for the layer: Inference / Action, Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
