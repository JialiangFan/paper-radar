---
title: "A predictive safety filter for learning-based control of constrained nonlinear dynamical systems"
year: 2018
authors:
  - "Kim P. Wabersich"
  - "Melanie N. Zeilinger"
venue: "Automatica"
category: "Action Shielding Safety Filters"
pdf: "../../PDFs/Action_Shielding_Safety_Filters/2018_Wabersich_PredictiveSafetyFilter.pdf"
url: "https://arxiv.org/abs/1812.05506"
code: ""
project: ""
tags:
  - "action-shielding"
  - "learning-based-control"
  - "mpc"
  - "robotics"
  - "runtime-assurance"
  - "safe-vla"
  - "safety-filter"
  - "state-space-safety"
---
# A predictive safety filter for learning-based control of constrained nonlinear dynamical systems

## One-sentence Summary

Predictive safety filters turn an unsafe learning controller into a safe closed-loop system by modifying proposed inputs only when needed.

## Problem Setting

Category: Action Shielding Safety Filters. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Action
Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- Predictive safety filters turn an unsafe learning controller into a safe closed-loop system by modifying proposed inputs only when needed.
- Clarifies or exercises the safety-enforcement layer: Inference / Action, Controller.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

A robust MPC problem checks whether the proposed input admits a future safe trajectory under
uncertain dynamics; otherwise it computes a minimally invasive safe input.

Implementation-level interpretation for this review:

- Safety enforcement layer: Inference / Action, Controller.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Key Equations or Formalisms

A generic safety filter can be expressed as:

```math
a_{safe}=\Pi_{\mathcal{A}_{safe}(s)}(a_{vla})
```

where the projection or replacement operator keeps the action close to the VLA proposal
while satisfying a state-dependent admissible-action set. The open Safe VLA problem is
constructing `A_safe(s)` from semantic and spatial observations.

## Experiments

Developed for nonlinear constrained systems and widely reused in safe learning-based control.

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

For the preferred research framing, the paper contributes most to: [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Strengths

- Separates nominal policy performance from safety enforcement.
- Naturally supports plug-and-play deployment around existing learned policies.
- Fits the review theme through [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Limitations

- Requires model structure, constraint definitions, and feasible backup planning; not directly semantic.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Feed constraints generated from language/vision into a predictive safety filter around VLA actions.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Predictive safety filters turn an unsafe learning controller into a safe closed-loop system by modifying proposed inputs only when needed.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Related Papers

- [[2023_Hsu_SafetyFilterUnified]]
- [[2020_Shao_RTS]]
- [[2018_Dalal_SafeExploration]]

## My Notes

- Relevance rank in this workspace: 23.
- Use this paper when arguing for the layer: Inference / Action, Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
