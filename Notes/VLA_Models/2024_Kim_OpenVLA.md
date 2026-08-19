---
title: "OpenVLA: An Open-Source Vision-Language-Action Model"
year: 2024
authors:
  - "Kim"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2024_Kim_OpenVLA.pdf"
url: "https://arxiv.org/abs/2406.09246"
code: "https://github.com/openvla/openvla"
project: "https://openvla.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "open-source"
  - "robot-policy"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
  - "vla"
---
# OpenVLA: An Open-Source Vision-Language-Action Model

## One-sentence Summary

OpenVLA provides an accessible 7B VLA pretrained on diverse robot demonstrations, making it a practical base policy for safety-layer research.

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

- OpenVLA provides an accessible 7B VLA pretrained on diverse robot demonstrations, making it a practical base policy for safety-layer research.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The model adapts a pretrained vision-language backbone for action generation and trains on Open
X-Embodiment demonstrations, with fine-tuning recipes for downstream manipulation tasks.

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

Evaluates on multiple robot manipulation settings and shows strong generalization and fine-tuning
performance compared with specialized imitation-learning baselines.

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

- OpenVLA is capability-oriented; safety is largely left to data, prompting, downstream evaluation, or external wrappers.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use OpenVLA as the nominal policy in a plug-and-play monitor/shield benchmark because it is open and reproducible.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: OpenVLA provides an accessible 7B VLA pretrained on diverse robot demonstrations, making it a practical base policy for safety-layer research.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2023_ONeill_OpenXEmbodiment]]
- [[2024_Ghosh_Octo]]
- [[2025_Hu_VLSA_AEGIS]]
- [[2024_Zheng_TraceVLA]]

## My Notes

- Relevance rank in this workspace: 7.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
