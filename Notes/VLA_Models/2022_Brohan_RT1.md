---
title: "RT-1: Robotics Transformer for Real-World Control at Scale"
year: 2022
authors:
  - "Anthony Brohan"
  - "Noah Brown"
  - "Justice Carbajal"
  - "Yevgen Chebotar"
  - "Joseph Dabis"
  - "Chelsea Finn"
  - "Keerthana Gopalakrishnan"
  - "Karol Hausman"
  - "Alex Herzog"
  - "Jasmine Hsu"
  - "Julian Ibarz"
  - "Brian Ichter"
  - "Alex Irpan"
  - "Tomas Jackson"
  - "Sally Jesmonth"
  - "Nikhil J Joshi"
  - "Ryan Julian"
  - "Dmitry Kalashnikov"
  - "Yuheng Kuang"
  - "Isabel Leal"
  - "Kuang-Huei Lee"
  - "Sergey Levine"
  - "Yao Lu"
  - "Utsav Malla"
  - "Deeksha Manjunath"
  - "Igor Mordatch"
  - "Ofir Nachum"
  - "Carolina Parada"
  - "Jodilyn Peralta"
  - "Emily Perez"
  - "Karl Pertsch"
  - "Jornell Quiambao"
  - "Kanishka Rao"
  - "Michael Ryoo"
  - "Grecia Salazar"
  - "Pannag Sanketi"
  - "Kevin Sayed"
  - "Jaspiar Singh"
  - "Sumedh Sontakke"
  - "Austin Stone"
  - "Clayton Tan"
  - "Huong Tran"
  - "Vincent Vanhoucke"
  - "Steve Vega"
  - "Quan Vuong"
  - "Fei Xia"
  - "Ted Xiao"
  - "Peng Xu"
  - "Sichun Xu"
  - "Tianhe Yu"
  - "Brianna Zitkovich"
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2022_Brohan_RT1.pdf"
url: "https://arxiv.org/abs/2212.06817"
code: ""
project: "https://robotics-transformer1.github.io/"
tags:
  - "behavior-cloning"
  - "benchmarks-and-evaluation"
  - "robotics"
  - "robotics-transformer"
  - "safe-vla"
  - "vision-language-action-models"
  - "vla"
---
# RT-1: Robotics Transformer for Real-World Control at Scale

## One-sentence Summary

RT-1 scales language-conditioned real-robot behavior cloning with a transformer policy over tokenized actions.

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

- RT-1 scales language-conditioned real-robot behavior cloning with a transformer policy over tokenized actions.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The model trains on a large real-robot dataset with image and language inputs, tokenizes robot
actions, and uses a transformer to predict action tokens for closed-loop control.

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

Reports broad real-world task performance across many instructions and objects on Google robots.

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

- Safety is largely implicit in demonstrations and deployment setup, not a runtime assurance mechanism.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use RT-1 as a historical baseline showing why capability scaling needs independent safety monitors.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: RT-1 scales language-conditioned real-robot behavior cloning with a transformer policy over tokenized actions.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2023_Brohan_RT2]]
- [[2023_ONeill_OpenXEmbodiment]]
- [[2024_Ghosh_Octo]]

## My Notes

- Relevance rank in this workspace: 31.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
