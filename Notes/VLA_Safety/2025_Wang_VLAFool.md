---
title: "When Alignment Fails: Multimodal Adversarial Attacks on Vision-Language-Action Models"
year: 2025
authors:
  - "Wang"
  - "et al."
venue: "arXiv"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2025_Wang_VLAFool.pdf"
url: "https://arxiv.org/abs/2511.16203"
code: ""
project: ""
tags:
  - "adversarial-attacks"
  - "benchmarks-and-evaluation"
  - "multimodal-safety"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
---
# When Alignment Fails: Multimodal Adversarial Attacks on Vision-Language-Action Models

## One-sentence Summary

VLA-Fool studies multimodal perturbations across text, vision, and grounding that cause unsafe or incorrect VLA behavior.

## Problem Setting

Category: VLA Safety. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Runtime
Monitoring]], [[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- VLA-Fool studies multimodal perturbations across text, vision, and grounding that cause unsafe or incorrect VLA behavior.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Inference / Action.
- Covers safety scope: Semantic, Embodied / Spatial, Task / Plan.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The attack jointly perturbs language and visual inputs to exploit cross-modal grounding weaknesses
in a fine-tuned VLA policy.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Inference / Action.
- Safety scope: Semantic, Embodied / Spatial, Task / Plan.
- Main interface to Safe VLA: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Evaluates on LIBERO-style manipulation with OpenVLA variants, showing significant behavioral
deviations from small perturbations.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Strengths

- Directly targets VLA-specific safety rather than generic text-only alignment.
- Highlights evaluation or mitigation mechanisms relevant to runtime Safe VLA systems.
- Fits the review theme through [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Limitations

- Attack-focused work; defenses require robust perception and action-level constraints.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use VLA-Fool perturbations as stress tests for semantic monitors and shield robustness.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: VLA-Fool studies multimodal perturbations across text, vision, and grounding that cause unsafe or incorrect VLA behavior.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2024_Kim_OpenVLA]]
- [[2024_Xie_BadRobot]]
- [[2026_Li_VLASafetySurvey]]

## My Notes

- Relevance rank in this workspace: 58.
- Use this paper when arguing for the layer: Agent / Monitor, Inference / Action.
- Use this paper when arguing for the safety scope: Semantic, Embodied / Spatial, Task / Plan.
