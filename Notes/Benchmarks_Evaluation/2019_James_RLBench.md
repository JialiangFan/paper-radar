---
title: "RLBench: The Robot Learning Benchmark & Learning Environment"
year: 2019
authors:
  - "Stephen James"
  - "Zicong Ma"
  - "David Rovick Arrojo"
  - "Andrew J. Davison"
venue: "arXiv"
category: "Benchmarks Evaluation"
pdf: "../../PDFs/Benchmarks_Evaluation/2019_James_RLBench.pdf"
url: "https://arxiv.org/abs/1909.12271"
code: ""
project: ""
tags:
  - "benchmarks-and-evaluation"
  - "few-shot-learning"
  - "manipulation"
  - "robot-benchmark"
  - "robotics"
  - "safe-vla"
  - "vision-language-action-models"
---
# RLBench: The Robot Learning Benchmark & Learning Environment

## One-sentence Summary

RLBench offers a large suite of vision-guided manipulation tasks with generated demonstrations.

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

- RLBench offers a large suite of vision-guided manipulation tasks with generated demonstrations.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Provides reusable infrastructure or metrics that can be adapted for Safe VLA evaluation.

## Methodology

Tasks are hand-designed with waypoints and motion planners that can generate demonstrations,
supporting RL, imitation, multi-task, and few-shot learning.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Main interface to Safe VLA: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Includes 100 unique tasks with multiple observation modalities.

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

- It emphasizes task learning, not safety violation taxonomies.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Instrument RLBench tasks with safety predicates and action shields to evaluate runtime assurance.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: RLBench offers a large suite of vision-guided manipulation tasks with generated demonstrations.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Related Papers

- [[2023_Liu_LIBERO]]
- [[2020_Zhu_robosuite]]
- [[2023_Gu_ManiSkill2]]

## My Notes

- Relevance rank in this workspace: 69.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
