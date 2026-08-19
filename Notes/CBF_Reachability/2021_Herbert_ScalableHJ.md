---
title: "Scalable Learning of Safety Guarantees for Autonomous Systems using Hamilton-Jacobi Reachability"
year: 2021
authors:
  - "Sylvia Herbert"
  - "Jason J. Choi"
  - "Suvansh Sanjeev"
  - "Marsalis Gibson"
  - "Koushil Sreenath"
  - "Claire J. Tomlin"
venue: "arXiv"
category: "CBF Reachability"
pdf: "../../PDFs/CBF_Reachability/2021_Herbert_ScalableHJ.pdf"
url: "https://arxiv.org/abs/2101.05916"
code: ""
project: ""
tags:
  - "neural-reachability"
  - "reachability"
  - "reachability-analysis"
  - "robotics"
  - "safe-control"
  - "safe-vla"
  - "state-space-safety"
---
# Scalable Learning of Safety Guarantees for Autonomous Systems using Hamilton-Jacobi Reachability

## One-sentence Summary

This paper learns approximations to Hamilton-Jacobi reachability to improve scalability of formal safety guarantees.

## Problem Setting

Category: CBF Reachability. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Reachability Analysis]],
[[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper learns approximations to Hamilton-Jacobi reachability to improve scalability of formal safety guarantees.
- Clarifies or exercises the safety-enforcement layer: Controller.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

It uses neural approximators and learning techniques to represent reachability value functions for
higher-dimensional autonomous systems.

Implementation-level interpretation for this review:

- Safety enforcement layer: Controller.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Reachability Analysis]], [[State-Space Safety]].

## Key Equations or Formalisms

Reachability methods define a value function over states; unsafe states are typically
characterized by the sign of that value function. A runtime safety controller intervenes
near the boundary:

```math
\mathcal{S}=\{x\mid V(x)\ge 0\}
```

Conceptually, Hamilton-Jacobi reachability computes whether there exists a control
strategy that avoids the unsafe set under modeled disturbances. For Safe VLA, the key
question is how semantic rules define the unsafe set used in this equation.

## Experiments

Evaluates learned reachability approximations on autonomous-system safety tasks.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: indirect.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: indirect.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: yes.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Reachability Analysis]], [[State-Space Safety]].

## Strengths

- Offers formal language for state-space safety and forward invariance.
- Connects high-level constraints to controller-level guarantees when dynamics and safe sets are available.
- Fits the review theme through [[Reachability Analysis]], [[State-Space Safety]].

## Limitations

- Approximation quality and certification remain central concerns; semantic constraints must already be state-space encoded.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use learned reachability to make VLA shields fast enough for real-time deployment after semantic grounding.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper learns approximations to Hamilton-Jacobi reachability to improve scalability of formal safety guarantees.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Reachability Analysis]], [[State-Space Safety]].

## Related Papers

- [[2017_Fisac_GeneralSafetyFramework]]
- [[2020_Shao_RTS]]
- [[2024_Santos_LanguageSafetyFeedback]]

## My Notes

- Relevance rank in this workspace: 46.
- Use this paper when arguing for the layer: Controller.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
