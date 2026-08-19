---
title: "Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms"
year: 2026
authors:
  - "Li"
  - "et al."
venue: "arXiv"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2026_Li_VLASafetySurvey.pdf"
url: "https://arxiv.org/abs/2604.23775"
code: "https://github.com/LiQiiiii/Awesome-VLA-Safety"
project: ""
tags:
  - "robotics"
  - "runtime-monitoring"
  - "runtime-safety"
  - "safe-vla"
  - "semantic-safety"
  - "survey"
  - "vision-language-action-models"
---
# Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms

## One-sentence Summary

This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem.

## Problem Setting

Category: VLA Safety. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Vision-Language-Action Models]],
[[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Agent / Monitor, Inference / Action, Controller.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial, State-space, Low-level Robot.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

It reviews VLA foundations, training-time and inference-time threats, runtime and training defenses,
evaluation protocols, and deployment-specific safety risks.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Agent / Monitor, Inference / Action, Controller.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial, State-space, Low-level Robot.
- Main interface to Safe VLA: [[Vision-Language-Action Models]], [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Benchmarks and Evaluation]].

## Key Equations or Formalisms

A generic safety filter can be expressed as:

```math
a_{safe}=\Pi_{\mathcal{A}_{safe}(s)}(a_{vla})
```

where the projection or replacement operator keeps the action close to the VLA proposal
while satisfying a state-dependent admissible-action set. The open Safe VLA problem is
constructing `A_safe(s)` from semantic and spatial observations.

## Experiments

As a survey, it synthesizes existing benchmarks and mechanisms rather than introducing a new
experimental system.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Benchmarks and Evaluation]].

## Strengths

- Directly targets VLA-specific safety rather than generic text-only alignment.
- Highlights evaluation or mitigation mechanisms relevant to runtime Safe VLA systems.
- Fits the review theme through [[Vision-Language-Action Models]], [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Benchmarks and Evaluation]].

## Limitations

- The paper maps the area but does not resolve how to compile semantic hazards into formal state/action constraints.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use its timing taxonomy as the outer structure for a Safe VLA monitor-and-shield architecture.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2026_Li_EmbodiedAISafetySurvey]]
- [[2025_Zhang_SafeVLA]]
- [[2026_Chen_HazardArena]]
- [[2025_Hu_VLSA_AEGIS]]

## My Notes

- Relevance rank in this workspace: 8.
- Use this paper when arguing for the layer: Training / Model, Agent / Monitor, Inference / Action, Controller.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial, State-space, Low-level Robot.
