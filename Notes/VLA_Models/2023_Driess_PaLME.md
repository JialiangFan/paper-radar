---
title: "PaLM-E: An Embodied Multimodal Language Model"
year: 2023
authors:
  - "Driess"
  - "et al."
venue: "arXiv"
category: "VLA Models"
pdf: "../../PDFs/VLA_Models/2023_Driess_PaLME.pdf"
url: "https://arxiv.org/abs/2303.03378"
code: ""
project: "https://palm-e.github.io/"
tags:
  - "embodied-ai"
  - "multimodal"
  - "robot-foundation-model"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
---
# PaLM-E: An Embodied Multimodal Language Model

## One-sentence Summary

PaLM-E injects embodied visual and state observations into a large language model for multimodal embodied reasoning.

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

- PaLM-E injects embodied visual and state observations into a large language model for multimodal embodied reasoning.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

Continuous sensor modalities are encoded into token-like embeddings interleaved with text and
trained end-to-end with a pretrained LLM across robotics, VQA, and captioning tasks.

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

Shows positive transfer across multiple robot embodiments and vision-language tasks, including
embodied planning and manipulation.

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

- PaLM-E improves embodied reasoning but still relies on downstream controllers and lacks a formal runtime safety layer.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use PaLM-E-like representations for semantic hazard recognition while enforcing physical constraints in a separate controller.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: PaLM-E injects embodied visual and state observations into a large language model for multimodal embodied reasoning.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Vision-Language-Action Models]], [[Semantic Safety]].

## Related Papers

- [[2022_Ahn_SayCan]]
- [[2023_Brohan_RT2]]
- [[2023_Huang_GroundedDecoding]]

## My Notes

- Relevance rank in this workspace: 17.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
