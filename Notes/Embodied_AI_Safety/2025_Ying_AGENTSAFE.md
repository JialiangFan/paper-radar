---
title: "AGENTSAFE: Benchmarking the Safety of Embodied Agents on Hazardous Instructions"
year: 2025
authors:
  - "Zonghao Ying"
  - "Le Wang"
  - "Yisong Xiao"
  - "Jiakai Wang"
  - "Yuqing Ma"
  - "Jinyang Guo"
  - "Zhenfei Yin"
  - "Mingchuan Zhang"
  - "Aishan Liu"
  - "Xianglong Liu"
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2025_Ying_AGENTSAFE.pdf"
url: "https://arxiv.org/abs/2506.14697"
code: ""
project: ""
tags:
  - "benchmark"
  - "benchmarks-and-evaluation"
  - "embodied-ai-safety"
  - "hazardous-instructions"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
---
# AGENTSAFE: Benchmarking the Safety of Embodied Agents on Hazardous Instructions

## One-sentence Summary

AGENTSAFE benchmarks whether embodied VLM agents comply with or refuse hazardous instructions across perception, planning, and execution.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]],
[[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- AGENTSAFE benchmarks whether embodied VLM agents comply with or refuse hazardous instructions across perception, planning, and execution.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The benchmark combines a simulation sandbox, an adapter from high-level VLM outputs to low-level
embodied actions, and a risk-aware instruction suite inspired by human, environment, and agent
harms.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Includes 45 adversarial scenarios, 1,350 hazardous tasks, and thousands of hazardous instructions,
including jailbroken variants.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Strengths

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Limitations

- The benchmark is stronger on semantic and task-level risk than on low-level robot dynamics, joint limits, contact forces, and formal safety guarantees.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Add state/action traces and shieldable constraints so each hazardous instruction can be scored by semantic refusal, trajectory safety, and controller-level violation.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: AGENTSAFE benchmarks whether embodied VLM agents comply with or refuse hazardous instructions across perception, planning, and execution.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Vision-Language-Action Models]].

## Related Papers

- [[2026_Chen_HazardArena]]
- [[2025_Lu_ISBench]]
- [[2024_Xie_BadRobot]]
- [[2024_Robey_RoboPAIR]]

## My Notes

- Relevance rank in this workspace: 5.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
