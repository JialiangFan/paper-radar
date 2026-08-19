---
title: "Jailbreaking LLM-Controlled Robots"
year: 2024
authors:
  - "Alexander Robey"
  - "Zachary Ravichandran"
  - "Vijay Kumar"
  - "Hamed Hassani"
  - "George J. Pappas"
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2024_Robey_RoboPAIR.pdf"
url: "https://arxiv.org/abs/2410.13691"
code: ""
project: "https://robopair.org/"
tags:
  - "embodied-ai"
  - "human-in-the-loop-safety"
  - "jailbreak"
  - "robot-safety"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
---
# Jailbreaking LLM-Controlled Robots

## One-sentence Summary

RoboPAIR adapts jailbreak search to LLM-controlled robots and demonstrates that unsafe physical actions can be elicited across access regimes.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Runtime
Monitoring]], [[Human-in-the-loop Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- RoboPAIR adapts jailbreak search to LLM-controlled robots and demonstrates that unsafe physical actions can be elicited across access regimes.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The attack searches prompts that bypass safety refusals in white-box, gray-box, and black-box
robotic systems, targeting physical actions rather than only text output.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Semantic Safety]], [[Runtime Monitoring]], [[Human-in-the-loop Safety]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Demonstrates harmful physical instruction compliance on autonomous-driving, UGV, and quadruped-style
robot setups.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Runtime Monitoring]], [[Human-in-the-loop Safety]].

## Strengths

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Semantic Safety]], [[Runtime Monitoring]], [[Human-in-the-loop Safety]].

## Limitations

- Defenses are discussed but not fully solved; the results underscore the need for non-language safety interlocks.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Evaluate runtime monitors that ignore linguistic compliance and instead check all proposed actions against explicit physical invariants.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: RoboPAIR adapts jailbreak search to LLM-controlled robots and demonstrates that unsafe physical actions can be elicited across access regimes.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Runtime Monitoring]], [[Human-in-the-loop Safety]].

## Related Papers

- [[2024_Xie_BadRobot]]
- [[2025_Ying_AGENTSAFE]]
- [[2026_Li_VLASafetySurvey]]

## My Notes

- Relevance rank in this workspace: 21.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
