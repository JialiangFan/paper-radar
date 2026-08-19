---
title: "Unpacking Failure Modes of Generative Policies: Runtime Monitoring of Consistency and Progress"
year: 2024
authors:
  - "Christopher Agia"
  - "Rohan Sinha"
  - "Jingyun Yang"
  - "Zi-ang Cao"
  - "Rika Antonova"
  - "Marco Pavone"
  - "Jeannette Bohg"
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2024_Agia_Sentinel.pdf"
url: "https://arxiv.org/abs/2410.04640"
code: ""
project: "https://sites.google.com/stanford.edu/sentinel"
tags:
  - "failure-detection"
  - "generative-policies"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
---
# Unpacking Failure Modes of Generative Policies: Runtime Monitoring of Consistency and Progress

## One-sentence Summary

Sentinel separates fast action-consistency failures from slower task-progress failures for runtime monitoring of generative robot policies.

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

- Sentinel separates fast action-consistency failures from slower task-progress failures for runtime monitoring of generative robot policies.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The monitor applies statistical temporal consistency checks to action chunks and uses VLM progress
assessment when a policy is confidently moving but not making task progress.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Task / Plan, Embodied / Spatial.
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

Evaluated on diffusion-policy mobile manipulation in simulation and real-world settings, detecting
more failures than either monitor alone.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
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

- The monitor warns about failure but does not by itself compute a safe replacement action or formal constraint set.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Connect Sentinel detections to recovery options: stop, ask human, replan, or invoke a CBF/reachability shield.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Sentinel separates fast action-consistency failures from slower task-progress failures for runtime monitoring of generative robot policies.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Monitoring]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Related Papers

- [[2024_Duan_AHA]]
- [[2023_Liu_SiriusMonitor]]
- [[2026_Ahmed_TAILSafe]]
- [[2025_Peng_FailSafeVLA]]

## My Notes

- Relevance rank in this workspace: 14.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial.
