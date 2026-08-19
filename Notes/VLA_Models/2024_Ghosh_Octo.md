---
title: "Octo: An Open-Source Generalist Robot Policy"
year: 2024
authors:
  - "Ghosh"
  - "et al."
venue: "RSS 2024"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2024_Ghosh_Octo.pdf"
url: "https://arxiv.org/abs/2405.12213"
code: "https://github.com/octo-models/octo"
project: "https://octo-models.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "generalist-policy"
  - "open-source"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
  - "vla"
---
# Octo: An Open-Source Generalist Robot Policy

## One-sentence Summary

Octo is an open generalist robot policy trained on large-scale robot trajectories and designed for broad manipulation research.

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

- Octo is an open generalist robot policy trained on large-scale robot trajectories and designed for broad manipulation research.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The policy uses a transformer architecture with flexible observation/action tokenization and
pretraining over Open X-Embodiment-style datasets.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Task / Plan, Embodied / Spatial.
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

Includes architecture and data ablations, with tests on multiple robot manipulation tasks and
embodiments.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
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

- Like other capability-oriented generalist policies, safety is not a first-class objective.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use Octo as a second base policy to test whether a safety layer transfers across VLA architectures.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Octo is an open generalist robot policy trained on large-scale robot trajectories and designed for broad manipulation research.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2023_ONeill_OpenXEmbodiment]]
- [[2024_Kim_OpenVLA]]
- [[2022_Brohan_RT1]]

## My Notes

- Relevance rank in this workspace: 24.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial.
