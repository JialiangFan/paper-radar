---
title: "RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic"
year: 2025
authors:
  - "Zhang"
  - "et al."
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2025_Zhang_RoboSafe.pdf"
url: "https://arxiv.org/abs/2512.21220"
code: ""
project: ""
tags:
  - "embodied-ai-safety"
  - "robotics"
  - "runtime-assurance"
  - "runtime-monitoring"
  - "safe-vla"
  - "safety-logic"
  - "semantic-safety"
---
# RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic

## One-sentence Summary

RoboSafe proposes executable safety logic and predictive reasoning for embodied agents facing hazardous instructions.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Runtime
Monitoring]], [[Runtime Assurance]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- RoboSafe proposes executable safety logic and predictive reasoning for embodied agents facing hazardous instructions.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The system builds safety memory, generates context-aware safety predicates, anticipates risks, and
uses executable logic to govern embodied decisions.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Semantic Safety]], [[Runtime Monitoring]], [[Runtime Assurance]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Evaluates embodied-agent safety on hazardous instruction scenarios.

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

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Runtime Monitoring]], [[Runtime Assurance]].

## Strengths

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Semantic Safety]], [[Runtime Monitoring]], [[Runtime Assurance]].

## Limitations

- Executable semantic logic still needs a mapping to continuous robot state/action constraints for hard physical safety.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use executable safety predicates as an intermediate representation before compiling to CBF/reachability constraints.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: RoboSafe proposes executable safety logic and predictive reasoning for embodied agents facing hazardous instructions.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Runtime Monitoring]], [[Runtime Assurance]].

## Related Papers

- [[2025_Ying_AGENTSAFE]]
- [[2026_Chen_HazardArena]]
- [[2024_Quartey_LIMP]]

## My Notes

- Relevance rank in this workspace: 60.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
