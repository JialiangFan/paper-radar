---
title: "LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning"
year: 2023
authors:
  - "Liu"
  - "et al."
venue: "arXiv"
category: "Benchmarks Evaluation"
pdf: "../../PDFs/Benchmarks_Evaluation/2023_Liu_LIBERO.pdf"
url: "https://arxiv.org/abs/2306.03310"
code: "https://github.com/Lifelong-Robot-Learning/LIBERO"
project: "https://libero-project.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "language-conditioned"
  - "manipulation"
  - "robot-benchmark"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
---
# LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning

## One-sentence Summary

LIBERO provides language-conditioned manipulation task suites for evaluating lifelong robot learning and VLA policies.

## Problem Setting

Category: Benchmarks Evaluation. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Benchmarks and Evaluation]],
[[Vision-Language-Action Models]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- LIBERO provides language-conditioned manipulation task suites for evaluating lifelong robot learning and VLA policies.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides reusable infrastructure or metrics that can be adapted for Safe VLA evaluation.

## Methodology

The benchmark uses procedural generation to create task suites that vary objects, goals, spatial
relations, and long-horizon transfer requirements.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Includes 130 tasks and human demonstrations, with studies of transfer, task ordering, and
pretraining.

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

For the preferred research framing, the paper contributes most to: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Strengths

- Provides reusable environments, tasks, or metrics for systematic comparison.
- Can support repeatable Safe VLA experiments with controlled violations.
- Fits the review theme through [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Limitations

- Safety violations are not the main metric, but LIBERO is a convenient substrate for Safe VLA benchmarks.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Create SafeLIBERO-style extensions with semantic hazards, obstacles, forbidden regions, and state-space constraints.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: LIBERO provides language-conditioned manipulation task suites for evaluating lifelong robot learning and VLA policies.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Related Papers

- [[2025_Hu_VLSA_AEGIS]]
- [[2024_Kim_OpenVLA]]
- [[2023_Gu_ManiSkill2]]

## My Notes

- Relevance rank in this workspace: 68.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
