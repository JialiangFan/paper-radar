---
title: "Subtle Risks, Critical Failures: A Framework for Diagnosing Physical Safety of LLMs for Embodied Decision Making"
year: 2025
authors:
  - "Son"
  - "et al."
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2025_Son_PhysicalSafetyLLMs.pdf"
url: "https://arxiv.org/abs/2505.19933"
code: ""
project: ""
tags:
  - "benchmark"
  - "benchmarks-and-evaluation"
  - "embodied-decision-making"
  - "human-in-the-loop-safety"
  - "physical-safety"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
---
# Subtle Risks, Critical Failures: A Framework for Diagnosing Physical Safety of LLMs for Embodied Decision Making

## One-sentence Summary

This paper diagnoses physical safety failures in LLM decision making for embodied contexts.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]],
[[Benchmarks and Evaluation]], [[Human-in-the-loop Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper diagnoses physical safety failures in LLM decision making for embodied contexts.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

It frames physical safety as scenario-level decision diagnosis, testing whether language models
recognize subtle embodied risks.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Human-in-the-loop Safety]].

## Key Equations or Formalisms

The paper is more architectural or empirical than equation-driven; its formal relevance is the interface it creates between semantic decisions, state estimation, and robot actions.

## Experiments

Benchmarks LLMs on physical safety situations where superficially reasonable choices can lead to
critical failures.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: indirect.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Human-in-the-loop Safety]].

## Strengths

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Human-in-the-loop Safety]].

## Limitations

- Text/scenario diagnosis does not automatically transfer to closed-loop robot execution.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use its risk categories to seed semantic safety rules for VLA monitors.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper diagnoses physical safety failures in LLM decision making for embodied contexts.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Benchmarks and Evaluation]], [[Human-in-the-loop Safety]].

## Related Papers

- [[2025_Ying_AGENTSAFE]]
- [[2025_Lu_ISBench]]
- [[2026_Li_EmbodiedAISafetySurvey]]

## My Notes

- Relevance rank in this workspace: 61.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
