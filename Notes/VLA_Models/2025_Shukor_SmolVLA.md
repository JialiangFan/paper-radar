---
title: "SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics"
year: 2025
authors:
  - "Shukor"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2025_Shukor_SmolVLA.pdf"
url: "https://arxiv.org/abs/2506.01844"
code: ""
project: ""
tags:
  - "efficient-models"
  - "low-level-robot-safety"
  - "open-source"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
  - "vla"
---
# SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics

## One-sentence Summary

SmolVLA explores smaller, efficient VLA models trained on community robotics data.

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

- SmolVLA explores smaller, efficient VLA models trained on community robotics data.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The work emphasizes affordable training and deployment by using compact multimodal backbones and
standardized robot data pipelines.

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

Reports manipulation evaluations in the LeRobot ecosystem and compatibility with accessible
hardware.

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

- Efficiency helps deployment but does not solve semantic or physical safety assurance.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use SmolVLA for low-cost Safe VLA experiments where the safety layer is the main research contribution.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: SmolVLA explores smaller, efficient VLA models trained on community robotics data.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Low-level Robot Safety]].

## Related Papers

- [[2024_Kim_OpenVLA]]
- [[2024_Ghosh_Octo]]
- [[2023_Liu_LIBERO]]

## My Notes

- Relevance rank in this workspace: 55.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
