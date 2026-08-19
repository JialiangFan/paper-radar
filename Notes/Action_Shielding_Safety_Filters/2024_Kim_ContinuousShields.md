---
title: "Realizable Continuous-Space Shields for Safe Reinforcement Learning"
year: 2024
authors:
  - "Kyungmin Kim"
  - "Davide Corsi"
  - "Andoni Rodriguez"
  - "JB Lanier"
  - "Benjami Parellada"
  - "Pierre Baldi"
  - "Cesar Sanchez"
  - "Roy Fox"
venue: "arXiv"
category: "Action Shielding Safety Filters"
pdf: "../../PDFs/Action_Shielding_Safety_Filters/2024_Kim_ContinuousShields.pdf"
url: "https://arxiv.org/abs/2410.02038"
code: ""
project: ""
tags:
  - "action-shielding"
  - "continuous-control"
  - "robotics"
  - "runtime-assurance"
  - "safe-rl"
  - "safe-vla"
  - "shielding"
  - "state-space-safety"
---
# Realizable Continuous-Space Shields for Safe Reinforcement Learning

## One-sentence Summary

This paper extends shielding toward continuous state and action spaces with realizability checks.

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

- This paper extends shielding toward continuous state and action spaces with realizability checks.
- Clarifies or exercises the safety-enforcement layer: Inference / Action, Agent / Monitor.
- Covers safety scope: State-space, Task / Plan.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

It defines shields that validate and adjust continuous actions while satisfying safety
specifications, including stateful and non-Markovian requirements.

Implementation-level interpretation for this review:

- Safety enforcement layer: Inference / Action, Agent / Monitor.
- Safety scope: State-space, Task / Plan.
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

Demonstrates safety preservation without severe success-rate loss in navigation and multi-agent
particle environments.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Strengths

- Separates nominal policy performance from safety enforcement.
- Naturally supports plug-and-play deployment around existing learned policies.
- Fits the review theme through [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Limitations

- The examples are not VLA manipulation systems and still require explicit specifications.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use continuous shields for VLA action spaces where actions are end-effector deltas or joint commands.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper extends shielding toward continuous state and action spaces with realizability checks.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Action Shielding]], [[Runtime Assurance]], [[State-Space Safety]].

## Related Papers

- [[2017_Alshiekh_Shielding]]
- [[2025_Markgraf_ActionProjection]]
- [[2025_Hu_VLSA_AEGIS]]

## My Notes

- Relevance rank in this workspace: 44.
- Use this paper when arguing for the layer: Inference / Action, Agent / Monitor.
- Use this paper when arguing for the safety scope: State-space, Task / Plan.
