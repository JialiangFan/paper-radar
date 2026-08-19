---
title: "HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models"
year: 2026
authors:
  - "Chen"
  - "et al."
venue: "arXiv"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2026_Chen_HazardArena.pdf"
url: "https://arxiv.org/abs/2604.12447"
code: ""
project: ""
tags:
  - "action-shielding"
  - "benchmark"
  - "benchmarks-and-evaluation"
  - "robotics"
  - "runtime-safety"
  - "safe-vla"
  - "semantic-safety"
---
# HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models

## One-sentence Summary

HazardArena exposes semantic safety failures where the same physical action is safe or unsafe depending on context.

## Problem Setting

Category: VLA Safety. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Benchmarks and
Evaluation]], [[Action Shielding]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- HazardArena exposes semantic safety failures where the same physical action is safe or unsafe depending on context.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Inference / Action.
- Covers safety scope: Semantic, Embodied / Spatial, Task / Plan.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The benchmark constructs safe/unsafe twin scenarios with matched objects and layouts but different
risk-bearing semantics, then evaluates VLA policies and a training-free Safety Option Layer based on
semantic attributes or VLM judging.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Inference / Action.
- Safety scope: Semantic, Embodied / Spatial, Task / Plan.
- Main interface to Safe VLA: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Action Shielding]].

## Key Equations or Formalisms

A generic safety filter can be expressed as:

```math
a_{safe}=\Pi_{\mathcal{A}_{safe}(s)}(a_{vla})
```

where the projection or replacement operator keeps the action close to the VLA proposal
while satisfying a state-dependent admissible-action set. The open Safe VLA problem is
constructing `A_safe(s)` from semantic and spatial observations.

## Experiments

Reports results across more than 2,000 assets and 40 risk-sensitive tasks in seven risk categories,
showing that policies trained on safe scenarios often fail in semantically unsafe counterparts.

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

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Action Shielding]].

## Strengths

- Directly targets VLA-specific safety rather than generic text-only alignment.
- Highlights evaluation or mitigation mechanisms relevant to runtime Safe VLA systems.
- Fits the review theme through [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Action Shielding]].

## Limitations

- The mitigation layer is semantic and task-level; it still needs grounded state/action constraints for hard robot safety guarantees.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use the twin-scenario design to build a benchmark where semantic labels compile into CBF, velocity, force, or workspace constraints.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: HazardArena exposes semantic safety failures where the same physical action is safe or unsafe depending on context.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Action Shielding]].

## Related Papers

- [[2025_Zhang_SafeVLA]]
- [[2025_Hu_VLSA_AEGIS]]
- [[2025_Ying_AGENTSAFE]]
- [[2025_Lu_ISBench]]

## My Notes

- Relevance rank in this workspace: 3.
- Use this paper when arguing for the layer: Agent / Monitor, Inference / Action.
- Use this paper when arguing for the safety scope: Semantic, Embodied / Spatial, Task / Plan.
