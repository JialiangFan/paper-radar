---
title: "GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation"
year: 2024
authors:
  - "Chi-Lam Cheang"
  - "Guangzeng Chen"
  - "Ya Jing"
  - "Tao Kong"
  - "Hang Li"
  - "Yifeng Li"
  - "Yuxiao Liu"
  - "Hongtao Wu"
  - "Jiafeng Xu"
  - "Yichu Yang"
  - "Hanbo Zhang"
  - "Minzhao Zhu"
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2024_Cheang_GR2.pdf"
url: "https://arxiv.org/abs/2410.06158"
code: ""
project: "https://gr2-manipulation.github.io/"
tags:
  - "robot-manipulation"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "video-language-action"
  - "vision-language-action-models"
  - "vla"
---
# GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation

## One-sentence Summary

GR-2 pretrains on web-scale video and fine-tunes for video generation and action prediction in robot manipulation.

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

- GR-2 pretrains on web-scale video and fine-tunes for video generation and action prediction in robot manipulation.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The model learns dynamics from millions of videos, then adapts to robot trajectories for both
future-video and action prediction.

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

Reports high multi-task success and generalization to new objects, environments, and tasks.

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

- Web-scale dynamics do not ensure physical safety or hard constraints during execution.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use predicted video futures as a monitor input for forecasting semantic and spatial safety violations.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: GR-2 pretrains on web-scale video and fine-tunes for video generation and action prediction in robot manipulation.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Semantic Safety]].

## Related Papers

- [[2024_Black_Pi0]]
- [[2024_Liu_RDT1B]]
- [[2024_Zheng_TraceVLA]]

## My Notes

- Relevance rank in this workspace: 52.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
