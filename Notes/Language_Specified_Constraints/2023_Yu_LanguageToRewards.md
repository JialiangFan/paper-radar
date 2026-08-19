---
title: "Language to Rewards for Robotic Skill Synthesis"
year: 2023
authors:
  - "Yu"
  - "et al."
venue: "arXiv"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2023_Yu_LanguageToRewards.pdf"
url: "https://arxiv.org/abs/2306.08647"
code: ""
project: "https://language-to-reward.github.io/"
tags:
  - "constraint-grounding"
  - "language-to-reward"
  - "robot-skill-synthesis"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "state-space-safety"
---
# Language to Rewards for Robotic Skill Synthesis

## One-sentence Summary

Language to Rewards uses LLMs to translate instructions and corrections into reward functions for low-level skill synthesis.

## Problem Setting

Category: Language Specified Constraints. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Constraint
Grounding]], [[Semantic Safety]], [[State-Space Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- Language to Rewards uses LLMs to translate instructions and corrections into reward functions for low-level skill synthesis.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, State-space.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

The system generates executable reward code from natural language, then optimizes robot behavior
with RL or trajectory optimization using that reward.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Agent / Monitor.
- Safety scope: Semantic, Task / Plan, State-space.
- Main interface to Safe VLA: [[Constraint Grounding]], [[Semantic Safety]], [[State-Space Safety]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Shows that reward functions can bridge high-level language and low-level robot actions across
simulated skill tasks.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: indirect.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Constraint Grounding]], [[Semantic Safety]], [[State-Space Safety]].

## Strengths

- Addresses the central semantic-to-physical grounding challenge.
- Provides intermediate representations that can be converted into monitors or controller constraints.
- Fits the review theme through [[Constraint Grounding]], [[Semantic Safety]], [[State-Space Safety]].

## Limitations

- Rewards are softer than constraints and can be misspecified or exploited; safety-critical rules need hard constraints.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Separate generated objectives from generated safety constraints, enforcing the latter with shields rather than reward shaping.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Language to Rewards uses LLMs to translate instructions and corrections into reward functions for low-level skill synthesis.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[Semantic Safety]], [[State-Space Safety]].

## Related Papers

- [[2022_Liang_CodeAsPolicies]]
- [[2023_Huang_VoxPoser]]
- [[2025_Zhang_SafeVLA]]

## My Notes

- Relevance rank in this workspace: 42.
- Use this paper when arguing for the layer: Training / Model, Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, State-space.
