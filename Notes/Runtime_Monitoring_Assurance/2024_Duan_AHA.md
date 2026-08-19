---
title: "AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation"
year: 2024
authors:
  - "Jiafei Duan"
  - "Wilbert Pumacay"
  - "Nishanth Kumar"
  - "Yi Ru Wang"
  - "Shulin Tian"
  - "Wentao Yuan"
  - "Ranjay Krishna"
  - "Dieter Fox"
  - "Ajay Mandlekar"
  - "Yijie Guo"
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2024_Duan_AHA.pdf"
url: "https://arxiv.org/abs/2410.00371"
code: ""
project: ""
tags:
  - "failure-detection"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
  - "vlm"
---
# AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation

## One-sentence Summary

AHA fine-tunes a VLM to detect and explain manipulation failures, turning failure recognition into a reusable monitor signal.

## Problem Setting

Category: Runtime Monitoring Assurance. The paper studies how an embodied or learning-enabled robot
system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Runtime
Monitoring]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- AHA fine-tunes a VLM to detect and explain manipulation failures, turning failure recognition into a reusable monitor signal.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

FailGen procedurally perturbs successful demonstrations to create failure trajectories, then trains
a VLM to classify and explain failures in natural language.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Generalizes from generated failure data to real-world failure datasets and improves downstream RL,
planning, and trajectory generation when used as feedback.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Runtime Monitoring]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Strengths

- Treats safety as a deployment-time problem rather than only a training objective.
- Provides monitor signals that can trigger stopping, replanning, shielding, or human intervention.
- Fits the review theme through [[Runtime Monitoring]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Limitations

- Failure detection is post hoc or near-runtime; it still needs an intervention/shield policy to prevent damage.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use AHA explanations to ground failure causes into constraints, such as occlusion, wrong object, blocked path, or unstable grasp.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: AHA fine-tunes a VLM to detect and explain manipulation failures, turning failure recognition into a reusable monitor signal.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Monitoring]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Related Papers

- [[2024_Agia_Sentinel]]
- [[2025_Peng_FailSafeVLA]]
- [[2026_Ahmed_TAILSafe]]

## My Notes

- Relevance rank in this workspace: 22.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
