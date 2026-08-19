---
title: "SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning"
year: 2025
authors:
  - "Zhang"
  - "et al."
venue: "NeurIPS 2025"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2025_Zhang_SafeVLA.pdf"
url: "https://arxiv.org/abs/2503.03480"
code: "https://github.com/PKU-Alignment/SafeVLA"
project: "https://pku-safevla.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "robotics"
  - "safe-rl"
  - "safe-vla"
  - "safety-alignment"
  - "semantic-safety"
  - "vision-language-action-models"
  - "vla"
---
# SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning

## One-sentence Summary

SafeVLA treats safety alignment for VLA policies as a constrained learning problem rather than relying on inherited LLM/VLM harmlessness.

## Problem Setting

Category: VLA Safety. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Vision-
Language-Action Models]], [[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- SafeVLA treats safety alignment for VLA policies as a constrained learning problem rather than relying on inherited LLM/VLM harmlessness.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The paper models VLA safety with a constrained Markov decision process, actively elicits unsafe
behaviors, and optimizes a safety-performance trade-off with safe reinforcement learning over
embodied tasks.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Semantic Safety]], [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Evaluates aligned and baseline VLA policies on Safety-CHORES-style scenarios with hazards to humans,
objects, and the robot; emphasizes safety improvement while preserving task performance.

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

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Strengths

- Directly targets VLA-specific safety rather than generic text-only alignment.
- Highlights evaluation or mitigation mechanisms relevant to runtime Safe VLA systems.
- Fits the review theme through [[Semantic Safety]], [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Limitations

- The method requires training or fine-tuning access and a benchmark distribution of hazards; it does not by itself provide hard runtime guarantees for unseen physical constraints.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Combine SafeVLA-style elicitation data with an external monitor that converts detected hazard classes into runtime shields.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: SafeVLA treats safety alignment for VLA policies as a constrained learning problem rather than relying on inherited LLM/VLM harmlessness.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Vision-Language-Action Models]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2025_Hu_VLSA_AEGIS]]
- [[2026_Chen_HazardArena]]
- [[2023_Ji_SafetyGymnasium]]
- [[2023_Brohan_RT2]]

## My Notes

- Relevance rank in this workspace: 2.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
