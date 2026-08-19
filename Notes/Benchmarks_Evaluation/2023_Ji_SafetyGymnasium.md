---
title: "Safety-Gymnasium: A Unified Safe Reinforcement Learning Benchmark"
year: 2023
authors:
  - "Ji"
  - "et al."
venue: "NeurIPS Datasets and Benchmarks 2023"
category: "Benchmarks Evaluation"
pdf: "../../PDFs/Benchmarks_Evaluation/2023_Ji_SafetyGymnasium.pdf"
url: "https://arxiv.org/abs/2310.12567"
code: "https://github.com/PKU-Alignment/safety-gymnasium"
project: "https://sites.google.com/view/safety-gymnasium"
tags:
  - "benchmark"
  - "benchmarks-and-evaluation"
  - "constraints"
  - "low-level-robot-safety"
  - "robotics"
  - "safe-rl"
  - "safe-vla"
  - "state-space-safety"
---
# Safety-Gymnasium: A Unified Safe Reinforcement Learning Benchmark

## One-sentence Summary

Safety-Gymnasium standardizes SafeRL tasks, constraints, and algorithms for evaluating reward-constraint trade-offs.

## Problem Setting

Category: Benchmarks Evaluation. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Benchmarks and Evaluation]],
[[State-Space Safety]], [[Low-level Robot Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- Safety-Gymnasium standardizes SafeRL tasks, constraints, and algorithms for evaluating reward-constraint trade-offs.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Inference / Action.
- Covers safety scope: State-space, Low-level Robot, Embodied / Spatial.
- Provides reusable infrastructure or metrics that can be adapted for Safe VLA evaluation.

## Methodology

The suite extends Safety Gym-style tasks with single-agent and multi-agent constraints, vector and
vision observations, and a library of safe policy optimization algorithms.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Inference / Action.
- Safety scope: State-space, Low-level Robot, Embodied / Spatial.
- Main interface to Safe VLA: [[Benchmarks and Evaluation]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Benchmarks many SafeRL algorithms under multiple cost constraints and observation modalities.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: yes.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Benchmarks and Evaluation]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Strengths

- Provides reusable environments, tasks, or metrics for systematic comparison.
- Can support repeatable Safe VLA experiments with controlled violations.
- Fits the review theme through [[Benchmarks and Evaluation]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Limitations

- The tasks are generic SafeRL rather than VLA semantic instruction-following tasks.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Adapt its cost-rate and violation metrics to VLA manipulation with semantic hazards and formal state constraints.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Safety-Gymnasium standardizes SafeRL tasks, constraints, and algorithms for evaluating reward-constraint trade-offs.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Benchmarks and Evaluation]], [[State-Space Safety]], [[Low-level Robot Safety]].

## Related Papers

- [[2019_Ray_SafetyGym]]
- [[2023_Zhao_GUARD]]
- [[2025_Zhang_SafeVLA]]

## My Notes

- Relevance rank in this workspace: 29.
- Use this paper when arguing for the layer: Training / Model, Inference / Action.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot, Embodied / Spatial.
