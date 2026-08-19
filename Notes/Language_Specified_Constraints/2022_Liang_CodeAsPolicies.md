---
title: "Code as Policies: Language Model Programs for Embodied Control"
year: 2022
authors:
  - "Liang"
  - "et al."
venue: "arXiv"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2022_Liang_CodeAsPolicies.pdf"
url: "https://arxiv.org/abs/2209.07753"
code: ""
project: "https://code-as-policies.github.io/"
tags:
  - "constraint-grounding"
  - "language-grounding"
  - "llm-robotics"
  - "programmatic-policies"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
---
# Code as Policies: Language Model Programs for Embodied Control

## One-sentence Summary

Code as Policies shows that LLM-generated programs can compose perception and control APIs for embodied tasks.

## Problem Setting

Category: Language Specified Constraints. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Constraint
Grounding]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- Code as Policies shows that LLM-generated programs can compose perception and control APIs for embodied tasks.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

Few-shot prompts map language comments to policy code, enabling generated programs with loops,
conditionals, spatial parsing, and calls to robot-control primitives.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Constraint Grounding]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Demonstrates tabletop manipulation and mobile manipulation across multiple robot platforms.

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

For the preferred research framing, the paper contributes most to: [[Constraint Grounding]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Strengths

- Addresses the central semantic-to-physical grounding challenge.
- Provides intermediate representations that can be converted into monitors or controller constraints.
- Fits the review theme through [[Constraint Grounding]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Limitations

- Generated code is flexible but unsafe without sandboxing, formal checks, and controller-level constraints.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Compile generated code through a safety API that requires every actuation call to include monitorable preconditions and shield constraints.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: Code as Policies shows that LLM-generated programs can compose perception and control APIs for embodied tasks.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[Semantic Safety]], [[Vision-Language-Action Models]].

## Related Papers

- [[2022_Ahn_SayCan]]
- [[2023_Huang_GroundedDecoding]]
- [[2024_Quartey_LIMP]]

## My Notes

- Relevance rank in this workspace: 41.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
