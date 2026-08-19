---
title: "Safe MPC Alignment with Human Directional Feedback"
year: 2024
authors:
  - "Zhixian Xie"
  - "Wenlong Zhang"
  - "Yi Ren"
  - "Zhaoran Wang"
  - "George J. Pappas"
  - "Wanxin Jin"
venue: "arXiv"
category: "Human in the Loop"
pdf: "../../PDFs/Human_in_the_Loop/2024_Xie_SafeMPCFeedback.pdf"
url: "https://arxiv.org/abs/2407.04216"
code: ""
project: ""
tags:
  - "constraint-grounding"
  - "constraint-learning"
  - "human-in-the-loop"
  - "human-in-the-loop-safety"
  - "mpc"
  - "robotics"
  - "safe-vla"
  - "state-space-safety"
---
# Safe MPC Alignment with Human Directional Feedback

## One-sentence Summary

This paper learns implicit safety constraints for MPC from sparse human directional corrections.

## Problem Setting

Category: Human in the Loop. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Human-in-the-loop Safety]],
[[Constraint Grounding]], [[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper learns implicit safety constraints for MPC from sparse human directional corrections.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Controller.
- Covers safety scope: State-space, Embodied / Spatial.
- Defines capabilities and action interfaces that a Safe VLA runtime layer must supervise.

## Methodology

Human feedback is treated as directional evidence pointing toward safer regions; the method updates
a hypothesis space over constraints and provides certificates on feedback complexity or
misspecification.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Controller.
- Safety scope: State-space, Embodied / Spatial.
- Main interface to Safe VLA: [[Human-in-the-loop Safety]], [[Constraint Grounding]], [[State-Space Safety]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Uses numerical examples, user studies, and a Franka mobile water-pouring task.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: yes.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Human-in-the-loop Safety]], [[Constraint Grounding]], [[State-Space Safety]].

## Strengths

- Acknowledges uncertainty and subjectivity in safety requirements.
- Provides practical mechanisms for intervention, approval, clarification, or correction.
- Fits the review theme through [[Human-in-the-loop Safety]], [[Constraint Grounding]], [[State-Space Safety]].

## Limitations

- Human feedback must be available and informative; constraint hypothesis classes may miss real safety preferences.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use human directional feedback to repair semantic-to-state constraint grounding when VLM-derived constraints are wrong.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper learns implicit safety constraints for MPC from sparse human directional corrections.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Human-in-the-loop Safety]], [[Constraint Grounding]], [[State-Space Safety]].

## Related Papers

- [[2023_Ren_KnowNo]]
- [[2025_Bajcsy_SparseHumanSafety]]
- [[2024_Santos_LanguageSafetyFeedback]]

## My Notes

- Relevance rank in this workspace: 25.
- Use this paper when arguing for the layer: Agent / Monitor, Controller.
- Use this paper when arguing for the safety scope: State-space, Embodied / Spatial.
