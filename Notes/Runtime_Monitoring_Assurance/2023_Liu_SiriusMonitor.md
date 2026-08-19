---
title: "Model-Based Runtime Monitoring with Interactive Imitation Learning"
year: 2023
authors:
  - "Liu"
  - "et al."
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2023_Liu_SiriusMonitor.pdf"
url: "https://arxiv.org/abs/2310.17552"
code: ""
project: "https://ut-austin-rpl.github.io/sirius-runtime-monitor/"
tags:
  - "human-in-the-loop"
  - "human-in-the-loop-safety"
  - "interactive-imitation-learning"
  - "robotics"
  - "runtime-assurance"
  - "runtime-monitoring"
  - "safe-vla"
---
# Model-Based Runtime Monitoring with Interactive Imitation Learning

## One-sentence Summary

This paper learns a runtime monitor from trustworthy deployments to predict future failures and reduce human supervision load.

## Problem Setting

Category: Runtime Monitoring Assurance. The paper studies how an embodied or learning-enabled robot
system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Runtime
Monitoring]], [[Human-in-the-loop Safety]], [[Runtime Assurance]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper learns a runtime monitor from trustworthy deployments to predict future failures and reduce human supervision load.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

A latent dynamics model rolls out future outcomes and a failure classifier detects OOD and high-risk
states before failures occur, integrated with interactive imitation learning.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Human-in-the-loop Safety]], [[Runtime Assurance]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Improves success rates in simulation and physical hardware and reduces human monitoring burden over
deployment.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Runtime Monitoring]], [[Human-in-the-loop Safety]], [[Runtime Assurance]].

## Strengths

- Treats safety as a deployment-time problem rather than only a training objective.
- Provides monitor signals that can trigger stopping, replanning, shielding, or human intervention.
- Fits the review theme through [[Runtime Monitoring]], [[Human-in-the-loop Safety]], [[Runtime Assurance]].

## Limitations

- It predicts risk but does not formalize physical constraints or guarantee corrected actions.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use its monitor as the trigger for stop, replan, ask-human, or shielded-control interventions in VLA deployment.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper learns a runtime monitor from trustworthy deployments to predict future failures and reduce human supervision load.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Monitoring]], [[Human-in-the-loop Safety]], [[Runtime Assurance]].

## Related Papers

- [[2024_Agia_Sentinel]]
- [[2026_Ahmed_TAILSafe]]
- [[2023_Ren_KnowNo]]

## My Notes

- Relevance rank in this workspace: 30.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial.
