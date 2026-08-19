---
title: "RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation"
year: 2024
authors:
  - "Liu"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2024_Liu_RDT1B.pdf"
url: "https://arxiv.org/abs/2410.07864"
code: ""
project: "https://rdt-robotics.github.io/rdt-robotics/"
tags:
  - "bimanual-manipulation"
  - "diffusion-policy"
  - "low-level-robot-safety"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
  - "vla"
---
# RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation

## One-sentence Summary

RDT-1B scales diffusion-transformer robot policies to bimanual manipulation with a physically interpretable unified action space.

## Problem Setting

Category: VLA Models. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Vision-Language-Action Models]],
[[Low-level Robot Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- RDT-1B scales diffusion-transformer robot policies to bimanual manipulation with a physically interpretable unified action space.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The architecture handles heterogeneous multimodal inputs and high-frequency robot data through a
scalable diffusion transformer and unified action representation.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Main interface to Safe VLA: [[Vision-Language-Action Models]], [[Low-level Robot Safety]].

## Key Equations or Formalisms

VLA policies are commonly represented as conditional action models:

```math
a_t \sim \pi_\theta(a_t \mid I_t, q, x_t, h_t)
```

where `I_t` is visual observation, `q` is the language instruction, `x_t` is robot state,
and `h_t` is history. Some models tokenize actions into language-like tokens; others
generate continuous action chunks through diffusion or flow matching.

## Experiments

Reports real-robot bimanual task performance, zero-shot generalization, and few-demonstration
adaptation.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Low-level Robot Safety]].

## Strengths

- Important reference point for modern VLA capability and action representation.
- Useful nominal policy or dataset context for safety-layer experiments.
- Fits the review theme through [[Vision-Language-Action Models]], [[Low-level Robot Safety]].

## Limitations

- Bimanual manipulation increases collision and force risks, but safety is not the central mechanism.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Study bimanual VLA shielding where constraints include inter-arm collision, grasp force, and object stability.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: RDT-1B scales diffusion-transformer robot policies to bimanual manipulation with a physically interpretable unified action space.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Low-level Robot Safety]].

## Related Papers

- [[2024_Black_Pi0]]
- [[2024_Cheang_GR2]]
- [[2024_Kim_OpenVLA]]

## My Notes

- Relevance rank in this workspace: 51.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
