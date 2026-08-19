---
title: "Learning Robot Safety from Sparse Human Feedback using Conformal Prediction"
year: 2025
authors:
  - "Bajcsy"
  - "et al."
venue: "arXiv"
category: "Human in the Loop"
pdf: "../../PDFs/Human_in_the_Loop/2025_Bajcsy_SparseHumanSafety.pdf"
url: "https://arxiv.org/abs/2501.04823"
code: ""
project: ""
tags:
  - "conformal-prediction"
  - "human-feedback"
  - "human-in-the-loop-safety"
  - "robot-safety"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "state-space-safety"
---
# Learning Robot Safety from Sparse Human Feedback using Conformal Prediction

## One-sentence Summary

The paper uses sparse human feedback and conformal prediction to learn when robot behavior should be considered unsafe.

## Problem Setting

Category: Human in the Loop. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Human-in-the-loop Safety]],
[[Runtime Monitoring]], [[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- The paper uses sparse human feedback and conformal prediction to learn when robot behavior should be considered unsafe.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Controller.
- Covers safety scope: Semantic, Embodied / Spatial, State-space.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

Human feedback calibrates safety predictions so the robot can quantify uncertainty and maintain
coverage guarantees under limited labels.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Controller.
- Safety scope: Semantic, Embodied / Spatial, State-space.
- Main interface to Safe VLA: [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[State-Space Safety]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Focuses on robot safety cases where constraints are subjective, incomplete, or missed by predefined
rules.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[State-Space Safety]].

## Strengths

- Acknowledges uncertainty and subjectivity in safety requirements.
- Provides practical mechanisms for intervention, approval, clarification, or correction.
- Fits the review theme through [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[State-Space Safety]].

## Limitations

- Coverage guarantees depend on calibration assumptions and the feedback distribution; physical action correction is a separate step.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use calibrated human safety models as a semantic monitor feeding a formal action shield.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: The paper uses sparse human feedback and conformal prediction to learn when robot behavior should be considered unsafe.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[State-Space Safety]].

## Related Papers

- [[2023_Ren_KnowNo]]
- [[2024_Xie_SafeMPCFeedback]]
- [[2024_Santos_LanguageSafetyFeedback]]

## My Notes

- Relevance rank in this workspace: 27.
- Use this paper when arguing for the layer: Agent / Monitor, Controller.
- Use this paper when arguing for the safety scope: Semantic, Embodied / Spatial, State-space.
