---
title: "ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills"
year: 2023
authors:
  - "Gu"
  - "et al."
venue: "arXiv"
category: "Benchmarks Evaluation"
pdf: "../../PDFs/Benchmarks_Evaluation/2023_Gu_ManiSkill2.pdf"
url: "https://arxiv.org/abs/2302.04659"
code: "https://github.com/haosulab/ManiSkill"
project: "https://maniskill2.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "manipulation-benchmark"
  - "robot-learning"
  - "robotics"
  - "safe-vla"
  - "simulation"
  - "vision-language-action-models"
---
# ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills

## One-sentence Summary

ManiSkill2 provides scalable simulated manipulation tasks with rich object variation, demonstrations, and controller interfaces.

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

- ManiSkill2 provides scalable simulated manipulation tasks with rich object variation, demonstrations, and controller interfaces.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Controller.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Provides reusable infrastructure or metrics that can be adapted for Safe VLA evaluation.

## Methodology

The benchmark supports rigid/soft-body manipulation, mobile/single/dual-arm settings, RGB-D/point-
cloud inputs, and fast parallel sampling.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Controller.
- Safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Main interface to Safe VLA: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Includes 20 task families, 2000+ objects, and millions of demonstration frames.

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

For the preferred research framing, the paper contributes most to: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Strengths

- Provides reusable environments, tasks, or metrics for systematic comparison.
- Can support repeatable Safe VLA experiments with controlled violations.
- Fits the review theme through [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Limitations

- Generalizable skill learning is central; explicit semantic safety scenarios are not.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use ManiSkill2 or ManiSkill3 as the simulator basis for a Safe VLA benchmark with contact and collision metrics.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: ManiSkill2 provides scalable simulated manipulation tasks with rich object variation, demonstrations, and controller interfaces.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Related Papers

- [[2023_Liu_LIBERO]]
- [[2019_James_RLBench]]
- [[2020_Zhu_robosuite]]

## My Notes

- Relevance rank in this workspace: 71.
- Use this paper when arguing for the layer: Training / Model, Controller.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
