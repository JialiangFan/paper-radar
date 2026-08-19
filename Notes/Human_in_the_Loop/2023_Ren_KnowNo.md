---
title: "Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners"
year: 2023
authors:
  - "Allen Z. Ren"
  - "Anushri Dixit"
  - "Alexandra Bodrova"
  - "Sumeet Singh"
  - "Stephen Tu"
  - "Noah Brown"
  - "Peng Xu"
  - "Leila Takayama"
  - "Fei Xia"
  - "Jake Varley"
  - "Zhenjia Xu"
  - "Dorsa Sadigh"
  - "Andy Zeng"
  - "Anirudha Majumdar"
venue: "arXiv"
category: "Human in the Loop"
pdf: "../../PDFs/Human_in_the_Loop/2023_Ren_KnowNo.pdf"
url: "https://arxiv.org/abs/2307.01928"
code: ""
project: "https://robot-help.github.io/"
tags:
  - "conformal-prediction"
  - "human-in-the-loop"
  - "human-in-the-loop-safety"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "uncertainty"
---
# Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners

## One-sentence Summary

KnowNo uses conformal prediction to calibrate when an LLM-based robot planner should ask for human help under ambiguity.

## Problem Setting

Category: Human in the Loop. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Human-in-the-loop Safety]],
[[Runtime Monitoring]], [[Semantic Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- KnowNo uses conformal prediction to calibrate when an LLM-based robot planner should ask for human help under ambiguity.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

The planner forms prediction sets over candidate actions or plans, calibrates uncertainty with
conformal prediction, and requests help when the set is too ambiguous to act confidently.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan.
- Main interface to Safe VLA: [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[Semantic Safety]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Tested across simulated and real robot tasks with spatial, numerical, preference, and commonsense
ambiguity, with formal task-completion assurances under calibration assumptions.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: indirect.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[Semantic Safety]].

## Strengths

- Acknowledges uncertainty and subjectivity in safety requirements.
- Provides practical mechanisms for intervention, approval, clarification, or correction.
- Fits the review theme through [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[Semantic Safety]].

## Limitations

- The guarantee concerns uncertainty over symbolic choices, not low-level physical safety after an action is selected.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use the same ask-for-help trigger when a semantic-to-state grounding module cannot confidently instantiate safety constraints.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: KnowNo uses conformal prediction to calibrate when an LLM-based robot planner should ask for human help under ambiguity.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Human-in-the-loop Safety]], [[Runtime Monitoring]], [[Semantic Safety]].

## Related Papers

- [[2024_Santos_LanguageSafetyFeedback]]
- [[2024_Xie_SafeMPCFeedback]]
- [[2025_Bajcsy_SparseHumanSafety]]

## My Notes

- Relevance rank in this workspace: 11.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan.
