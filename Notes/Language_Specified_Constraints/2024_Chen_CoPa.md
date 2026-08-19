---
title: "CoPa: General Robotic Manipulation through Spatial Constraints of Parts with Foundation Models"
year: 2024
authors:
  - "Chen"
  - "et al."
venue: "arXiv"
category: "Language Specified Constraints"
pdf: "../../PDFs/Language_Specified_Constraints/2024_Chen_CoPa.pdf"
url: "https://arxiv.org/abs/2403.08248"
code: ""
project: "https://copa-2024.github.io/"
tags:
  - "constraint-grounding"
  - "foundation-models"
  - "manipulation"
  - "robotics"
  - "safe-vla"
  - "semantic-safety"
  - "spatial-constraints"
  - "spatial-safety"
---
# CoPa: General Robotic Manipulation through Spatial Constraints of Parts with Foundation Models

## One-sentence Summary

CoPa uses foundation models to infer spatial constraints between object parts and solve open-world manipulation tasks.

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

- CoPa uses foundation models to infer spatial constraints between object parts and solve open-world manipulation tasks.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor, Controller.
- Covers safety scope: Semantic, Embodied / Spatial, State-space.
- Provides a mechanism for converting language, perception, or object relations into executable structure.

## Methodology

A VLM identifies relevant object parts and commonsense spatial relations; an optimization pipeline
generates 6-DoF end-effector poses satisfying the constraints.

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

Shows general manipulation performance on tasks requiring object-part reasoning.

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

- The constraints are not explicitly safety-certified and may be brittle when perception or commonsense relations are wrong.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Add a safety-specific relation vocabulary: avoid, keep away, do not contact, maintain clearance, approach slowly.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: CoPa uses foundation models to infer spatial constraints between object parts and solve open-world manipulation tasks.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Constraint Grounding]], [[Spatial Safety]], [[Semantic Safety]].

## Related Papers

- [[2025_Tang_GeoManip]]
- [[2025_Su_ReSem3D]]
- [[2023_Huang_VoxPoser]]

## My Notes

- Relevance rank in this workspace: 40.
- Use this paper when arguing for the layer: Agent / Monitor, Controller.
- Use this paper when arguing for the safety scope: Semantic, Embodied / Spatial, State-space.
