---
title: "Runtime Safety Monitoring of Deep Neural Networks for Perception: A Survey"
year: 2025
authors:
  - "Schotschneider"
  - "et al."
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2025_Schotschneider_RuntimePerceptionSurvey.pdf"
url: "https://arxiv.org/abs/2511.05982"
code: ""
project: ""
tags:
  - "perception"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "survey"
---
# Runtime Safety Monitoring of Deep Neural Networks for Perception: A Survey

## One-sentence Summary

This survey categorizes runtime monitors for DNN perception by monitoring inputs, internal representations, and outputs.

## Problem Setting

Category: Runtime Monitoring Assurance. The paper studies how an embodied or learning-enabled robot
system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Runtime
Monitoring]], [[Semantic Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This survey categorizes runtime monitors for DNN perception by monitoring inputs, internal representations, and outputs.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

It maps monitor families to concerns such as generalization errors, OOD inputs, and adversarial
attacks.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Embodied / Spatial.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Semantic Safety]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Survey paper synthesizing perception-monitoring literature for safety-critical autonomy.

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

For the preferred research framing, the paper contributes most to: [[Runtime Monitoring]], [[Semantic Safety]].

## Strengths

- Treats safety as a deployment-time problem rather than only a training objective.
- Provides monitor signals that can trigger stopping, replanning, shielding, or human intervention.
- Fits the review theme through [[Runtime Monitoring]], [[Semantic Safety]].

## Limitations

- Perception safety alone does not enforce robot action safety.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use perception monitors as one tier in a VLA runtime safety stack before semantic grounding and action shielding.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This survey categorizes runtime monitors for DNN perception by monitoring inputs, internal representations, and outputs.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Monitoring]], [[Semantic Safety]].

## Related Papers

- [[2024_Vardal_LearningRuntimeMonitors]]
- [[2024_Duan_AHA]]
- [[2026_Li_VLASafetySurvey]]

## My Notes

- Relevance rank in this workspace: 65.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Embodied / Spatial.
