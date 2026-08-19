---
title: "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances"
year: 2022
authors:
  - "Ahn"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2022_Ahn_SayCan.pdf"
url: "https://arxiv.org/abs/2204.01691"
code: ""
project: "https://say-can.github.io/"
tags:
  - "affordances"
  - "constraint-grounding"
  - "language-grounding"
  - "robot-planning"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
---
# Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

## One-sentence Summary

SayCan combines language-model planning scores with learned affordance scores so plans are both semantically plausible and executable.

## Problem Setting

Category: VLA Models. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Vision-Language-Action Models]],
[[Constraint Grounding]], [[Semantic Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- SayCan combines language-model planning scores with learned affordance scores so plans are both semantically plausible and executable.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The planner evaluates candidate skills by multiplying LLM likelihood with value-function affordance
estimates, selecting skill sequences that the robot can actually perform.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Vision-Language-Action Models]], [[Constraint Grounding]], [[Semantic Safety]].

## Key Equations or Formalisms

VLA policies are commonly represented as conditional action models:

```math
a_t \sim \pi_\theta(a_t \mid I_t, q, x_t, h_t)
```

where `I_t` is visual observation, `q` is the language instruction, `x_t` is robot state,
and `h_t` is history. Some models tokenize actions into language-like tokens; others
generate continuous action chunks through diffusion or flow matching.

## Experiments

Demonstrates long-horizon mobile manipulation tasks in kitchen-like settings.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Constraint Grounding]], [[Semantic Safety]].

## Strengths

- Important reference point for modern VLA capability and action representation.
- Useful nominal policy or dataset context for safety-layer experiments.
- Fits the review theme through [[Vision-Language-Action Models]], [[Constraint Grounding]], [[Semantic Safety]].

## Limitations

- Affordance feasibility is not the same as safety; explicit hazards, constraints, and low-level limits are not formally enforced.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Replace or augment affordance scores with safety scores and formal constraint feasibility checks.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: SayCan combines language-model planning scores with learned affordance scores so plans are both semantically plausible and executable.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Constraint Grounding]], [[Semantic Safety]].

## Related Papers

- [[2023_Driess_PaLME]]
- [[2023_Huang_GroundedDecoding]]
- [[2022_Liang_CodeAsPolicies]]

## My Notes

- Relevance rank in this workspace: 32.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
