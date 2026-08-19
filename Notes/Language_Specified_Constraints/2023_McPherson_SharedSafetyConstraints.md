---
title: "Learning Shared Safety Constraints from Multi-task Demonstrations"
year: 2023
authors:
  - "McPherson"
  - "et al."
venue: "arXiv"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2023_McPherson_SharedSafetyConstraints.pdf"
url: "https://arxiv.org/abs/2309.00711"
code: ""
project: ""
tags:
  - "constraint-grounding"
  - "constraint-learning"
  - "demonstrations"
  - "robotics"
  - "safe-robot-learning"
  - "safe-vla"
  - "state-space-safety"
---
# Learning Shared Safety Constraints from Multi-task Demonstrations

## One-sentence Summary

This paper learns safety constraints shared across tasks from demonstrations, such as avoiding breaking plates regardless of the current goal.

## Problem Setting

Category: Language Specified Constraints. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Constraint
Grounding]], [[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper learns safety constraints shared across tasks from demonstrations, such as avoiding breaking plates regardless of the current goal.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Controller.
- Covers safety scope: State-space, Task / Plan.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

It uses inverse reinforcement or inverse constraint learning ideas to infer constraints that persist
across multiple tasks rather than task-specific rewards.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Controller.
- Safety scope: State-space, Task / Plan.
- Main interface to Safe VLA: [[Constraint Grounding]], [[State-Space Safety]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Evaluates multi-task settings where shared constraints improve safety generalization.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Constraint Grounding]], [[State-Space Safety]].

## Strengths

- Addresses the central semantic-to-physical grounding challenge.
- Provides intermediate representations that can be converted into monitors or controller constraints.
- Fits the review theme through [[Constraint Grounding]], [[State-Space Safety]].

## Limitations

- Demonstrations may not reveal rare hazards; natural-language semantics are not the main input.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Combine shared demonstration-derived constraints with explicit language-specified constraints for VLA policies.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper learns safety constraints shared across tasks from demonstrations, such as avoiding breaking plates regardless of the current goal.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[State-Space Safety]].

## Related Papers

- [[2020_Robey_LearningCBF]]
- [[2023_Yu_LanguageToRewards]]
- [[2025_Zhang_SafeVLA]]

## My Notes

- Relevance rank in this workspace: 74.
- Use this paper when arguing for the layer: Training / Model, Controller.
- Use this paper when arguing for the safety scope: State-space, Task / Plan.
