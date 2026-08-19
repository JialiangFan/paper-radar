---
title: "Learning Contextual Runtime Monitors for Safe AI-Based Autonomy"
year: 2026
authors:
  - "Yuan"
  - "et al."
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2026_Yuan_ContextualRuntimeMonitors.pdf"
url: "https://arxiv.org/abs/2601.20666"
code: ""
project: ""
tags:
  - "controller-ensembles"
  - "robotics"
  - "runtime-assurance"
  - "runtime-monitoring"
  - "safe-autonomy"
  - "safe-vla"
---
# Learning Contextual Runtime Monitors for Safe AI-Based Autonomy

## One-sentence Summary

This paper formulates monitor selection for AI controller ensembles as a contextual monitoring problem.

## Problem Setting

Category: Runtime Monitoring Assurance. The paper studies how an embodied or learning-enabled robot
system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Runtime
Monitoring]], [[Runtime Assurance]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper formulates monitor selection for AI controller ensembles as a contextual monitoring problem.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: State-space, Task / Plan.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

It uses contextual bandit ideas to learn which controller or monitor should be trusted under current
operating conditions.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: State-space, Task / Plan.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Runtime Assurance]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Validated in simulated autonomous-driving scenarios with safety and performance trade-offs.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Runtime Monitoring]], [[Runtime Assurance]].

## Strengths

- Treats safety as a deployment-time problem rather than only a training objective.
- Provides monitor signals that can trigger stopping, replanning, shielding, or human intervention.
- Fits the review theme through [[Runtime Monitoring]], [[Runtime Assurance]].

## Limitations

- Not a VLA manipulation paper; assumes an ensemble/controller structure.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use contextual monitor selection to route VLA actions through different shield types depending on hazard context.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper formulates monitor selection for AI controller ensembles as a contextual monitoring problem.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Monitoring]], [[Runtime Assurance]].

## Related Papers

- [[2021_Chen_SimplexDrive]]
- [[2023_Hsu_SafetyFilterUnified]]
- [[2024_Agia_Sentinel]]

## My Notes

- Relevance rank in this workspace: 76.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: State-space, Task / Plan.
