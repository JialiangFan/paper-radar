---
title: "ReSem3D: Refinable 3D Spatial Constraints via Fine-Grained Semantic Grounding for Generalizable Robotic Manipulation"
year: 2025
authors:
  - "Su"
  - "et al."
venue: "arXiv"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2025_Su_ReSem3D.pdf"
url: "https://arxiv.org/abs/2507.18262"
code: "https://github.com/scy-v/ReSem3D"
project: "https://resem3d.github.io/"
tags:
  - "3d-grounding"
  - "constraint-grounding"
  - "robot-manipulation"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "spatial-constraints"
  - "spatial-safety"
---
# ReSem3D: Refinable 3D Spatial Constraints via Fine-Grained Semantic Grounding for Generalizable Robotic Manipulation

## One-sentence Summary

ReSem3D uses MLLMs and vision foundation models to build hierarchical 3D spatial constraints from language and RGB-D observations.

## Problem Setting

Category: Language Specified Constraints. The paper studies how an embodied or learning-enabled
robot system should represent, learn, evaluate, monitor, or enforce behavior under language, vision,
state, and action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Constraint
Grounding]], [[Spatial Safety]], [[Semantic Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- ReSem3D uses MLLMs and vision foundation models to build hierarchical 3D spatial constraints from language and RGB-D observations.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Controller.
- Covers safety scope: Semantic, Embodied / Spatial, State-space.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

The system recursively grounds parts and regions, refines 3D constraints, and encodes them as real-
time joint-space optimization objectives for manipulation.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Controller.
- Safety scope: Semantic, Embodied / Spatial, State-space.
- Main interface to Safe VLA: [[Constraint Grounding]], [[Spatial Safety]], [[Semantic Safety]].

## Key Equations or Formalisms

The grounding problem can be written as a compiler:

```math
g_\phi: (\text{language rule}, \text{scene}, \text{robot state})
\rightarrow \{c_i(x,a,t)\le 0\}_{i=1}^m
```

The downstream controller or shield enforces the resulting constraints. The reliability
of `g_phi` is the key bottleneck for semantic-to-state safety.

## Experiments

Evaluates in household and chemical-lab environments under zero-shot conditions, including
simulation and real-robot experiments.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: indirect.

For the preferred research framing, the paper contributes most to: [[Constraint Grounding]], [[Spatial Safety]], [[Semantic Safety]].

## Strengths

- Addresses the central semantic-to-physical grounding challenge.
- Provides intermediate representations that can be converted into monitors or controller constraints.
- Fits the review theme through [[Constraint Grounding]], [[Spatial Safety]], [[Semantic Safety]].

## Limitations

- It focuses on task execution constraints; safety guarantees depend on the optimizer and perception fidelity.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Reuse its fine-grained 3D grounding as the front-end for forbidden-region and clearance constraints in Safe VLA.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: ReSem3D uses MLLMs and vision foundation models to build hierarchical 3D spatial constraints from language and RGB-D observations.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[Spatial Safety]], [[Semantic Safety]].

## Related Papers

- [[2025_Tang_GeoManip]]
- [[2024_Chen_CoPa]]
- [[2023_Huang_VoxPoser]]
- [[2025_Hu_VLSA_AEGIS]]

## My Notes

- Relevance rank in this workspace: 39.
- Use this paper when arguing for the layer: Agent / Monitor, Controller.
- Use this paper when arguing for the safety scope: Semantic, Embodied / Spatial, State-space.
