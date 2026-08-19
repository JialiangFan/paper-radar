---
title: "FailSafe: Reasoning and Recovery from Failures in Vision-Language-Action Models"
year: 2025
authors:
  - "Peng"
  - "et al."
venue: "arXiv"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2025_Peng_FailSafeVLA.pdf"
url: "https://arxiv.org/abs/2510.01642"
code: ""
project: ""
tags:
  - "failure-recovery"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "vision-language-action-models"
---
# FailSafe: Reasoning and Recovery from Failures in Vision-Language-Action Models

## One-sentence Summary

FailSafe targets failure detection and recovery for VLA manipulation policies rather than only offline evaluation.

## Problem Setting

Category: VLA Safety. The paper studies how an embodied or learning-enabled robot system should
represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and action
uncertainty. In the Safe VLA pipeline, it is most relevant to [[Runtime Monitoring]], [[Vision-
Language-Action Models]], [[Semantic Safety]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- FailSafe targets failure detection and recovery for VLA manipulation policies rather than only offline evaluation.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

A VLM-based module reasons over potential failures and supplies recovery feedback to VLA policies
during task execution.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Vision-Language-Action Models]], [[Semantic Safety]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Reports improvements for several VLA policies, including OpenVLA and pi0-style models, in
manipulation benchmarks.

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

For the preferred research framing, the paper contributes most to: [[Runtime Monitoring]], [[Vision-Language-Action Models]], [[Semantic Safety]].

## Strengths

- Directly targets VLA-specific safety rather than generic text-only alignment.
- Highlights evaluation or mitigation mechanisms relevant to runtime Safe VLA systems.
- Fits the review theme through [[Runtime Monitoring]], [[Vision-Language-Action Models]], [[Semantic Safety]].

## Limitations

- Recovery decisions are not the same as formal safety constraints and may still rely on heuristic VLM reasoning.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Connect failure explanations to shield constraints and human approval policies.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: FailSafe targets failure detection and recovery for VLA manipulation policies rather than only offline evaluation.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Runtime Monitoring]], [[Vision-Language-Action Models]], [[Semantic Safety]].

## Related Papers

- [[2024_Duan_AHA]]
- [[2024_Agia_Sentinel]]
- [[2024_Kim_OpenVLA]]
- [[2024_Black_Pi0]]

## My Notes

- Relevance rank in this workspace: 57.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
