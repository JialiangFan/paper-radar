---
title: "Human-in-the-Loop Imitation Learning using Remote Teleoperation"
year: 2020
authors:
  - "Ajay Mandlekar"
  - "Danfei Xu"
  - "Roberto Martín-Martín"
  - "Yuke Zhu"
  - "Li Fei-Fei"
  - "Silvio Savarese"
venue: "arXiv"
category: "Human in the Loop"
pdf: "../../PDFs/Human_in_the_Loop/2020_Mandlekar_HITLTeleoperation.pdf"
url: "https://arxiv.org/abs/2012.06733"
code: ""
project: ""
tags:
  - "human-in-the-loop"
  - "human-in-the-loop-safety"
  - "imitation-learning"
  - "intervention"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
---
# Human-in-the-Loop Imitation Learning using Remote Teleoperation

## One-sentence Summary

This work uses remote human interventions to collect corrective demonstrations for safer and more efficient imitation learning.

## Problem Setting

Category: Human in the Loop. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Human-in-the-loop Safety]],
[[Runtime Monitoring]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This work uses remote human interventions to collect corrective demonstrations for safer and more efficient imitation learning.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Training / Model.
- Covers safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

A human supervisor intervenes during policy execution through teleoperation; intervention data are
incorporated to improve future policy behavior.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Training / Model.
- Safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
- Main interface to Safe VLA: [[Human-in-the-loop Safety]], [[Runtime Monitoring]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Demonstrates gains on robot threading and coffee-making tasks compared with non-interventional data
collection.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: yes.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Human-in-the-loop Safety]], [[Runtime Monitoring]].

## Strengths

- Acknowledges uncertainty and subjectivity in safety requirements.
- Provides practical mechanisms for intervention, approval, clarification, or correction.
- Fits the review theme through [[Human-in-the-loop Safety]], [[Runtime Monitoring]].

## Limitations

- Requires human availability and does not define formal safety constraints.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use interventions not only for retraining but also to label which semantic or state constraints were violated.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This work uses remote human interventions to collect corrective demonstrations for safer and more efficient imitation learning.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Human-in-the-loop Safety]], [[Runtime Monitoring]].

## Related Papers

- [[2023_Liu_SiriusMonitor]]
- [[2023_Ren_KnowNo]]
- [[2024_Xie_SafeMPCFeedback]]

## My Notes

- Relevance rank in this workspace: 66.
- Use this paper when arguing for the layer: Agent / Monitor, Training / Model.
- Use this paper when arguing for the safety scope: Task / Plan, Embodied / Spatial, Low-level Robot.
