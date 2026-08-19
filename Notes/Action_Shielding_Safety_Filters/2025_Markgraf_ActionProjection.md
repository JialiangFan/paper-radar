---
title: "Safe Reinforcement Learning using Action Projection: Safeguard the Policy or the Environment?"
year: 2025
authors:
  - "Markgraf"
  - "et al."
venue: "arXiv"
category: "Action Shielding Safety Filters"
pdf: "../../PDFs/Action_Shielding_Safety_Filters/2025_Markgraf_ActionProjection.pdf"
url: "https://arxiv.org/abs/2509.12833"
code: ""
project: ""
tags:
  - "action-projection"
  - "action-shielding"
  - "robotics"
  - "safe-rl"
  - "safe-vla"
  - "safety-filter"
  - "state-space-safety"
---
# Safe Reinforcement Learning using Action Projection: Safeguard the Policy or the Environment?

## One-sentence Summary

This paper analyzes projection-based safety filters and clarifies when to treat projection as part of the policy or the environment.

## Problem Setting

Category: Action Shielding Safety Filters. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Action
Shielding]], [[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper analyzes projection-based safety filters and clarifies when to treat projection as part of the policy or the environment.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Inference / Action.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

It formalizes safe-environment RL and safe-policy RL under actor-critic learning and analyzes action
aliasing caused by many unsafe actions projecting to the same safe action.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Inference / Action.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Action Shielding]], [[State-Space Safety]].

## Key Equations or Formalisms

A generic safety filter can be expressed as:

```math
a_{safe}=\Pi_{\mathcal{A}_{safe}(s)}(a_{vla})
```

where the projection or replacement operator keeps the action close to the VLA proposal
while satisfying a state-dependent admissible-action set. The open Safe VLA problem is
constructing `A_safe(s)` from semantic and spatial observations.

## Experiments

Empirical comparisons validate the theoretical differences and mitigation strategies across
continuous-control environments.

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

For the preferred research framing, the paper contributes most to: [[Action Shielding]], [[State-Space Safety]].

## Strengths

- Separates nominal policy performance from safety enforcement.
- Naturally supports plug-and-play deployment around existing learned policies.
- Fits the review theme through [[Action Shielding]], [[State-Space Safety]].

## Limitations

- The focus is RL training dynamics rather than semantic VLA grounding.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use its action-aliasing analysis to design learning-compatible VLA shields and logging metrics.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper analyzes projection-based safety filters and clarifies when to treat projection as part of the policy or the environment.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Action Shielding]], [[State-Space Safety]].

## Related Papers

- [[2018_Dalal_SafeExploration]]
- [[2025_Hu_VLSA_AEGIS]]
- [[2017_Alshiekh_Shielding]]

## My Notes

- Relevance rank in this workspace: 43.
- Use this paper when arguing for the layer: Training / Model, Inference / Action.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
