---
title: "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control"
year: 2023
authors:
  - "Brohan"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2023_Brohan_RT2.pdf"
url: "https://arxiv.org/abs/2307.15818"
code: ""
project: "https://robotics-transformer2.github.io/"
tags:
  - "action-tokenization"
  - "robot-foundation-model"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
  - "vla"
---
# RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control

## One-sentence Summary

RT-2 popularized the VLA formulation by co-training web-scale vision-language models and robotic action prediction through action tokenization.

## Problem Setting

Category: VLA Models. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Vision-Language-Action Models]],
[[Semantic Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- RT-2 popularized the VLA formulation by co-training web-scale vision-language models and robotic action prediction through action tokenization.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

Robot actions are discretized and represented as tokens in the same sequence space as language,
allowing VLM co-fine-tuning on web VQA/captioning and robot trajectories.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Vision-Language-Action Models]], [[Semantic Safety]].

## Key Equations or Formalisms

VLA policies are commonly represented as conditional action models:

```math
a_t \sim \pi_\theta(a_t \mid I_t, q, x_t, h_t)
```

where `I_t` is visual observation, `q` is the language instruction, `x_t` is robot state,
and `h_t` is history. Some models tokenize actions into language-like tokens; others
generate continuous action chunks through diffusion or flow matching.

## Experiments

Reports thousands of real-robot trials showing improved generalization to novel objects, symbols,
and simple semantic reasoning tasks.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Semantic Safety]].

## Strengths

- Important reference point for modern VLA capability and action representation.
- Useful nominal policy or dataset context for safety-layer experiments.
- Fits the review theme through [[Vision-Language-Action Models]], [[Semantic Safety]].

## Limitations

- The model optimizes task execution but lacks a native runtime safety layer for collision, speed, force, or semantic hazards.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use RT-2-like policies as the nominal action generator in a safety-layer study that compares prompt-only safety, monitor-only safety, and formal action shielding.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: RT-2 popularized the VLA formulation by co-training web-scale vision-language models and robotic action prediction through action tokenization.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Semantic Safety]].

## Related Papers

- [[2022_Brohan_RT1]]
- [[2023_Driess_PaLME]]
- [[2024_Kim_OpenVLA]]
- [[2025_Zhang_SafeVLA]]

## My Notes

- Relevance rank in this workspace: 6.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
