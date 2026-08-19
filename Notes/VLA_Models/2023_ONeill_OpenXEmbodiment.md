---
title: "Open X-Embodiment: Robotic Learning Datasets and RT-X Models"
year: 2023
authors:
  - "O'Neill"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2023_ONeill_OpenXEmbodiment.pdf"
url: "https://arxiv.org/abs/2310.08864"
code: ""
project: "https://robotics-transformer-x.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "cross-embodiment"
  - "robot-dataset"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
  - "vla"
---
# Open X-Embodiment: Robotic Learning Datasets and RT-X Models

## One-sentence Summary

Open X-Embodiment standardizes a large multi-robot manipulation dataset and trains RT-X models for cross-embodiment transfer.

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

- Open X-Embodiment standardizes a large multi-robot manipulation dataset and trains RT-X models for cross-embodiment transfer.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The collaboration aggregates demonstrations from many robot embodiments into a shared data format
and trains high-capacity robot policies across heterogeneous action/state spaces.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
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

Shows positive transfer and improved robot performance when leveraging data across embodiments and
institutions.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Strengths

- Important reference point for modern VLA capability and action representation.
- Useful nominal policy or dataset context for safety-layer experiments.
- Fits the review theme through [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Limitations

- Safety labels and unsafe counterexamples are not the organizing principle of the dataset.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Add safety annotations and constraint metadata to Open X-Embodiment-style datasets for training and evaluating Safe VLA monitors.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Open X-Embodiment standardizes a large multi-robot manipulation dataset and trains RT-X models for cross-embodiment transfer.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2024_Kim_OpenVLA]]
- [[2024_Ghosh_Octo]]
- [[2023_Brohan_RT2]]

## My Notes

- Relevance rank in this workspace: 19.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
