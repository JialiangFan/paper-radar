---
title: "GUARD: A Safe Reinforcement Learning Benchmark"
year: 2023
authors:
  - "Zhao"
  - "et al."
venue: "arXiv"
category: "Benchmarks Evaluation"
pdf: "../../PDFs/Benchmarks_Evaluation/2023_Zhao_GUARD.pdf"
url: "https://arxiv.org/abs/2305.13681"
code: "https://github.com/intelligent-control-lab/GUARD"
project: ""
tags:
  - "benchmark"
  - "benchmarks-and-evaluation"
  - "constraints"
  - "robotics"
  - "safe-rl"
  - "safe-vla"
  - "state-space-safety"
---
# GUARD: A Safe Reinforcement Learning Benchmark

## One-sentence Summary

GUARD provides a generalized benchmark for comparing SafeRL algorithms under diverse constraints and tasks.

## Problem Setting

Category: Benchmarks Evaluation. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Benchmarks and Evaluation]],
[[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- GUARD provides a generalized benchmark for comparing SafeRL algorithms under diverse constraints and tasks.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Inference / Action.
- Covers safety scope: State-space, Low-level Robot.
- Provides reusable infrastructure or metrics that can be adapted for Safe VLA evaluation.

## Methodology

The benchmark packages agents, tasks, and safety-constraint specifications with implementations of
multiple SafeRL algorithms.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Inference / Action.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Benchmarks and Evaluation]], [[State-Space Safety]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Compares state-of-the-art SafeRL algorithms under varied task settings.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Benchmarks and Evaluation]], [[State-Space Safety]].

## Strengths

- Provides reusable environments, tasks, or metrics for systematic comparison.
- Can support repeatable Safe VLA experiments with controlled violations.
- Fits the review theme through [[Benchmarks and Evaluation]], [[State-Space Safety]].

## Limitations

- It is not designed for multimodal instructions or semantic VLA safety.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Borrow its standardized constraint reporting for Safe VLA evaluation.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: GUARD provides a generalized benchmark for comparing SafeRL algorithms under diverse constraints and tasks.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Benchmarks and Evaluation]], [[State-Space Safety]].

## Related Papers

- [[2023_Ji_SafetyGymnasium]]
- [[2019_Ray_SafetyGym]]
- [[2025_Zhang_SafeVLA]]

## My Notes

- Relevance rank in this workspace: 67.
- Use this paper when arguing for the layer: Training / Model, Inference / Action.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
