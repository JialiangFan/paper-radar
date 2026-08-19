---
title: "IS-Bench: Evaluating Interactive Safety of VLM-Driven Embodied Agents in Daily Household Tasks"
year: 2025
authors:
  - "Lu"
  - "et al."
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2025_Lu_ISBench.pdf"
url: "https://arxiv.org/abs/2506.16402"
code: ""
project: ""
tags:
  - "benchmark"
  - "benchmarks-and-evaluation"
  - "embodied-ai-safety"
  - "interactive-safety"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
---
# IS-Bench: Evaluating Interactive Safety of VLM-Driven Embodied Agents in Daily Household Tasks

## One-sentence Summary

IS-Bench evaluates interactive safety, including risks that emerge from an agent's own intermediate actions rather than only from the initial instruction.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Benchmarks and Evaluation]],
[[Semantic Safety]], [[Runtime Monitoring]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- IS-Bench evaluates interactive safety, including risks that emerge from an agent's own intermediate actions rather than only from the initial instruction.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The benchmark instantiates dynamic household safety risks in a high-fidelity simulator and scores
whether VLM agents perceive, reason about, and mitigate hazards during execution.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Main interface to Safe VLA: [[Benchmarks and Evaluation]], [[Semantic Safety]], [[Runtime Monitoring]].

## Key Equations or Formalisms

Runtime monitors usually estimate a risk or failure score:

```math
r_t = M(o_{1:t}, a_{1:t}, x_{1:t})
```

An intervention policy then triggers when `r_t` crosses a threshold. The important design
choice is whether the monitor only warns, switches to a fallback, asks a human, or passes a
formal constraint set to an action shield.

## Experiments

Includes 161 scenarios and 388 safety risks; evaluates leading VLM agents and safety-aware
prompting.

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

For the preferred research framing, the paper contributes most to: [[Benchmarks and Evaluation]], [[Semantic Safety]], [[Runtime Monitoring]].

## Strengths

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Benchmarks and Evaluation]], [[Semantic Safety]], [[Runtime Monitoring]].

## Limitations

- The benchmark highlights process safety but does not yet expose low-level robot state traces needed for formal shielding.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Add action-level logs, state constraints, and intervention points so monitors can be compared on prevention time and shield effectiveness.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: IS-Bench evaluates interactive safety, including risks that emerge from an agent's own intermediate actions rather than only from the initial instruction.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Benchmarks and Evaluation]], [[Semantic Safety]], [[Runtime Monitoring]].

## Related Papers

- [[2025_Ying_AGENTSAFE]]
- [[2026_Chen_HazardArena]]
- [[2023_Ji_SafetyGymnasium]]

## My Notes

- Relevance rank in this workspace: 16.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
