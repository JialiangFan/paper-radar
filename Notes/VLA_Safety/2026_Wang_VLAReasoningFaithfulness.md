---
title: "Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation"
year: 2026
authors:
  - "Wang"
  - "et al."
venue: "arXiv"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2026_Wang_VLAReasoningFaithfulness.pdf"
url: "https://arxiv.org/abs/2605.17268"
code: ""
project: ""
tags:
  - "benchmarks-and-evaluation"
  - "embodied-reasoning"
  - "faithfulness"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
---
# Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation

## One-sentence Summary

This paper probes whether VLA driving-model reasoning faithfully reflects entities and actions relevant to safety.

## Problem Setting

Category: VLA Safety. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Runtime
Monitoring]], [[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This paper probes whether VLA driving-model reasoning faithfully reflects entities and actions relevant to safety.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

It formalizes reasoning faithfulness with entity and action fidelity criteria over chain-of-
causation inferences.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Analyzes hundreds of inferences over PhysicalAI-AV driving scenarios and proposes a safety
architecture informed by failures.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: indirect.
- Runtime monitoring: yes.
- Action shielding: indirect.
- Human-in-the-loop safety: indirect.
- Low-level robot safety: indirect.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Strengths

- Directly targets VLA-specific safety rather than generic text-only alignment.
- Highlights evaluation or mitigation mechanisms relevant to runtime Safe VLA systems.
- Fits the review theme through [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Limitations

- Driving-specific and reasoning-focused; manipulation control constraints are not central.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Port entity/action fidelity checks to manipulation: did the VLA mention the hazard, and did the action respect it?
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This paper probes whether VLA driving-model reasoning faithfully reflects entities and actions relevant to safety.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2026_Li_VLASafetySurvey]]
- [[2026_Chen_HazardArena]]
- [[2025_Ying_AGENTSAFE]]

## My Notes

- Relevance rank in this workspace: 59.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
