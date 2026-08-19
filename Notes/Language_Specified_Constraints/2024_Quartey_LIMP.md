---
title: "Verifiably Following Complex Robot Instructions with Foundation Models"
year: 2024
authors:
  - "Quartey"
  - "et al."
venue: "arXiv"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2024_Quartey_LIMP.pdf"
url: "https://arxiv.org/abs/2402.11498"
code: "https://github.com/robotlimp"
project: "https://robotlimp.github.io/"
tags:
  - "constraint-grounding"
  - "language-instructions"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "spatial-safety"
  - "verification"
---
# Verifiably Following Complex Robot Instructions with Foundation Models

## One-sentence Summary

LIMP grounds complex natural-language robot instructions into symbolic specifications and motion-planning behavior that can be checked before execution.

## Problem Setting

Category: Language Specified Constraints. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Constraint
Grounding]], [[Semantic Safety]], [[Spatial Safety]], [[Runtime Assurance]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- LIMP grounds complex natural-language robot instructions into symbolic specifications and motion-planning behavior that can be checked before execution.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Controller.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

Foundation models parse open-ended language, ground referents in observations, construct symbolic
instruction representations, and synthesize motion plans that satisfy spatiotemporal constraints.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Controller.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Constraint Grounding]], [[Semantic Safety]], [[Spatial Safety]], [[Runtime Assurance]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Evaluated on 150 real-world instructions in five environments; outperforms LLM task and code-writing
planners on complex spatiotemporal instructions.

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

For the preferred research framing, the paper contributes most to: [[Constraint Grounding]], [[Semantic Safety]], [[Spatial Safety]], [[Runtime Assurance]].

## Strengths

- Addresses the central semantic-to-physical grounding challenge.
- Provides intermediate representations that can be converted into monitors or controller constraints.
- Fits the review theme through [[Constraint Grounding]], [[Semantic Safety]], [[Spatial Safety]], [[Runtime Assurance]].

## Limitations

- The focus is navigation and motion-planning correctness; it does not fully address manipulator dynamics or actuator-level limits.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use LIMP-style symbolic grounding as the semantic front-end for a VLA action shield.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: LIMP grounds complex natural-language robot instructions into symbolic specifications and motion-planning behavior that can be checked before execution.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[Semantic Safety]], [[Spatial Safety]], [[Runtime Assurance]].

## Related Papers

- [[2024_Santos_LanguageSafetyFeedback]]
- [[2023_Huang_VoxPoser]]
- [[2022_Liang_CodeAsPolicies]]
- [[2025_Tang_GeoManip]]

## My Notes

- Relevance rank in this workspace: 12.
- Use this paper when arguing for the layer: Agent / Monitor, Controller.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
