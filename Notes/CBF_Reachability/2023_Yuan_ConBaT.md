---
title: "ConBaT: Control Barrier Transformer for Safe Policy Learning"
year: 2023
authors:
  - "Yuan"
  - "et al."
venue: "arXiv"
category: "CBF Reachability"
pdf: "../../PDFs/CBF_Reachability/2023_Yuan_ConBaT.pdf"
url: "https://arxiv.org/abs/2303.04212"
code: ""
project: ""
tags:
  - "control-barrier-functions"
  - "robotics"
  - "safe-policy-learning"
  - "safe-vla"
  - "state-space-safety"
  - "transformer"
  - "vision-language-action-models"
---
# ConBaT: Control Barrier Transformer for Safe Policy Learning

## One-sentence Summary

ConBaT brings CBF-inspired safety into transformer policy learning.

## Problem Setting

Category: CBF Reachability. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Control Barrier Functions]],
[[State-Space Safety]], [[Vision-Language-Action Models]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- ConBaT brings CBF-inspired safety into transformer policy learning.
- Clarifies or exercises the safety-enforcement layer: Training / Model.
- Covers safety scope: State-space, Low-level Robot.
- Provides a formal or algorithmic mechanism for intervening on unsafe control actions.

## Methodology

A causal transformer predicts safe actions using a critic and safety-labeled data inspired by
barrier-function reasoning.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model.
- Safety scope: State-space, Low-level Robot.
- Main interface to Safe VLA: [[Control Barrier Functions]], [[State-Space Safety]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

The standard CBF safe set is:

```math
\mathcal{C}=\{x\mid h(x)\ge 0\}
```

A controller keeps the system forward invariant by choosing actions that satisfy:

```math
\dot h(x,u)+\alpha(h(x))\ge 0
```

Runtime shielding is often written as a minimally invasive quadratic program:

```math
u^* = \arg\min_u \|u-u_{nom}\|^2 \quad
\text{s.t.}\quad \dot h(x,u)+\alpha(h(x))\ge 0
```

## Experiments

Evaluates on simulated control tasks against imitation learning, RL, and MPC-style baselines.

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

For the preferred research framing, the paper contributes most to: [[Control Barrier Functions]], [[State-Space Safety]], [[Vision-Language-Action Models]].

## Strengths

- Offers formal language for state-space safety and forward invariance.
- Connects high-level constraints to controller-level guarantees when dynamics and safe sets are available.
- Fits the review theme through [[Control Barrier Functions]], [[State-Space Safety]], [[Vision-Language-Action Models]].

## Limitations

- It is not a VLA model and does not provide a general semantic grounding interface.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Investigate whether barrier-informed transformers can be paired with VLA backbones or used as safety critics.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: ConBaT brings CBF-inspired safety into transformer policy learning.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Control Barrier Functions]], [[State-Space Safety]], [[Vision-Language-Action Models]].

## Related Papers

- [[2025_Yang_CBFRL]]
- [[2025_Zhang_SafeVLA]]
- [[2025_Hu_VLSA_AEGIS]]

## My Notes

- Relevance rank in this workspace: 50.
- Use this paper when arguing for the layer: Training / Model.
- Use this paper when arguing for the safety scope: State-space, Low-level Robot.
