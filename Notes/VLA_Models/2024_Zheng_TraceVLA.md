---
title: "TraceVLA: Visual Trace Prompting Enhances Spatial-Temporal Awareness for Generalist Robotic Policies"
year: 2024
authors:
  - "Ruijie Zheng"
  - "Yongyuan Liang"
  - "Shuaiyi Huang"
  - "Jianfeng Gao"
  - "Hal Daumé"
  - "Andrey Kolobov"
  - "Furong Huang"
  - "Jianwei Yang"
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2024_Zheng_TraceVLA.pdf"
url: "https://arxiv.org/abs/2412.10345"
code: ""
project: "https://tracevla.github.io/"
tags:
  - "robotics"
  - "safe-vla"
  - "spatial-safety"
  - "spatial-temporal"
  - "vision-language-action-models"
  - "visual-traces"
  - "vla"
---
# TraceVLA: Visual Trace Prompting Enhances Spatial-Temporal Awareness for Generalist Robotic Policies

## One-sentence Summary

TraceVLA encodes state-action history as visual traces to improve spatial-temporal awareness in VLA policies.

## Problem Setting

Category: VLA Models. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Vision-Language-Action Models]],
[[Spatial Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- TraceVLA encodes state-action history as visual traces to improve spatial-temporal awareness in VLA policies.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Embodied / Spatial, Task / Plan.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The model fine-tunes OpenVLA with visual trace prompting over 150K collected manipulation
trajectories, and also studies a compact Phi-3-Vision VLA variant.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Embodied / Spatial, Task / Plan.
- Main interface to Safe VLA: [[Vision-Language-Action Models]], [[Spatial Safety]].

## Key Equations or Formalisms

VLA policies are commonly represented as conditional action models:

```math
a_t \sim \pi_\theta(a_t \mid I_t, q, x_t, h_t)
```

where `I_t` is visual observation, `q` is the language instruction, `x_t` is robot state,
and `h_t` is history. Some models tokenize actions into language-like tokens; others
generate continuous action chunks through diffusion or flow matching.

## Experiments

Evaluates across SimplerEnv configurations and real WidowX tasks, reporting improvements over
OpenVLA.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Spatial Safety]].

## Strengths

- Important reference point for modern VLA capability and action representation.
- Useful nominal policy or dataset context for safety-layer experiments.
- Fits the review theme through [[Vision-Language-Action Models]], [[Spatial Safety]].

## Limitations

- Better spatial awareness may reduce errors but does not equal explicit safety enforcement.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use visual traces as monitor features for detecting near-collisions, unstable progress, or repeated unsafe corrections.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: TraceVLA encodes state-action history as visual traces to improve spatial-temporal awareness in VLA policies.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Spatial Safety]].

## Related Papers

- [[2024_Kim_OpenVLA]]
- [[2024_Agia_Sentinel]]
- [[2024_Black_Pi0]]

## My Notes

- Relevance rank in this workspace: 53.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Embodied / Spatial, Task / Plan.
