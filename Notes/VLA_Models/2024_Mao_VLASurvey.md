---
title: "A Survey on Vision-Language-Action Models for Embodied AI"
year: 2024
authors:
  - "Mao"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2024_Mao_VLASurvey.pdf"
url: "https://arxiv.org/abs/2405.14093"
code: ""
project: ""
tags:
  - "benchmarks-and-evaluation"
  - "embodied-ai"
  - "robotics"
  - "safe-vla"
  - "survey"
  - "vision-language-action-models"
  - "vla"
---
# A Survey on Vision-Language-Action Models for Embodied AI

## One-sentence Summary

This survey maps VLA architectures, datasets, training methods, and embodied applications.

## Problem Setting

Category: VLA Models. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Vision-Language-Action Models]],
[[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This survey maps VLA architectures, datasets, training methods, and embodied applications.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

It categorizes VLA models by perception-language-action integration, action representation, data
sources, and embodied task settings.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Key Equations or Formalisms

VLA policies are commonly represented as conditional action models:

```math
a_t \sim \pi_\theta(a_t \mid I_t, q, x_t, h_t)
```

where `I_t` is visual observation, `q` is the language instruction, `x_t` is robot state,
and `h_t` is history. Some models tokenize actions into language-like tokens; others
generate continuous action chunks through diffusion or flow matching.

## Experiments

Survey paper; useful for orienting the capability side of the literature.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Strengths

- Important reference point for modern VLA capability and action representation.
- Useful nominal policy or dataset context for safety-layer experiments.
- Fits the review theme through [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Limitations

- Safety is not the primary axis and runtime assurance is underdeveloped.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use it to situate Safe VLA work against the broader VLA model landscape.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This survey maps VLA architectures, datasets, training methods, and embodied applications.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2026_Li_VLASafetySurvey]]
- [[2024_Kim_OpenVLA]]
- [[2023_Brohan_RT2]]

## My Notes

- Relevance rank in this workspace: 56.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
