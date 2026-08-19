---
title: "CaStL: Constraints as Specifications through LLM Translation for Long-Horizon Task and Motion Planning"
year: 2025
authors:
  - "Weihang Guo"
  - "Zachary Kingston"
  - "Lydia E. Kavraki"
venue: "ICRA 2025"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2025_Guo_CaStL.pdf"
url: "https://arxiv.org/abs/2410.22225"
code: ""
project: ""
tags:
  - "constraint-grounding"
  - "formal-specification"
  - "language-constraints"
  - "planning"
  - "robotics"
  - "runtime-assurance"
  - "safe-vla"
  - "semantic-safety"
---
# CaStL: Constraints as Specifications through LLM Translation for Long-Horizon Task and Motion Planning

## One-sentence Summary

CaStL translates natural-language constraints into formal planning specifications.

## Problem Setting

Category: Language Specified Constraints. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Constraint
Grounding]], [[Semantic Safety]], [[Runtime Assurance]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- CaStL translates natural-language constraints into formal planning specifications.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, State-space.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

An LLM converts user constraints into formal representations such as PDDL-style predicates and
temporal/task constraints that a planner can solve against.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, State-space.
- Main interface to Safe VLA: [[Constraint Grounding]], [[Semantic Safety]], [[Runtime Assurance]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Evaluates on planning domains with richer natural-language constraints than standard benchmark
specifications.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Constraint Grounding]], [[Semantic Safety]], [[Runtime Assurance]].

## Strengths

- Addresses the central semantic-to-physical grounding challenge.
- Provides intermediate representations that can be converted into monitors or controller constraints.
- Fits the review theme through [[Constraint Grounding]], [[Semantic Safety]], [[Runtime Assurance]].

## Limitations

- Planner-level constraints still need refinement to continuous robot state and low-level actuation limits.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use CaStL-like formalization as the semantic middle layer between VLA instructions and controller shields.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: CaStL translates natural-language constraints into formal planning specifications.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[Semantic Safety]], [[Runtime Assurance]].

## Related Papers

- [[2024_Quartey_LIMP]]
- [[2022_Liang_CodeAsPolicies]]
- [[2024_Santos_LanguageSafetyFeedback]]

## My Notes

- Relevance rank in this workspace: 75.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, State-space.
