---
title: "BadRobot: Jailbreaking Embodied LLMs in the Physical World"
year: 2024
authors:
  - "Xie"
  - "et al."
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2024_Xie_BadRobot.pdf"
url: "https://arxiv.org/abs/2407.20242"
code: ""
project: "https://embodied-ai-safety.github.io/"
tags:
  - "benchmarks-and-evaluation"
  - "embodied-ai-safety"
  - "jailbreak"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "unsafe-instructions"
---
# BadRobot: Jailbreaking Embodied LLMs in the Physical World

## One-sentence Summary

BadRobot shows that language-level jailbreaks can produce physically unsafe embodied behavior, including mismatches between verbal refusal and executed action.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Runtime
Monitoring]], [[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- BadRobot shows that language-level jailbreaks can produce physically unsafe embodied behavior, including mismatches between verbal refusal and executed action.
- Clarifies or exercises the safety-enforcement layer: Agent / Monitor.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

The work designs voice/user interaction attacks against embodied LLM systems and analyzes
vulnerabilities such as cascading jailbreaks, language-action misalignment, and deceptive
instructions.

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

Tests multiple LLM/VLM-based embodied systems and frameworks across physical-world scenarios.

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

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Limitations

- It is primarily an attack/evaluation paper; it does not provide formal runtime shields.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use BadRobot scenarios as adversarial inputs to evaluate whether semantic monitors and action filters jointly prevent unsafe execution.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: BadRobot shows that language-level jailbreaks can produce physically unsafe embodied behavior, including mismatches between verbal refusal and executed action.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Runtime Monitoring]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2024_Robey_RoboPAIR]]
- [[2025_Ying_AGENTSAFE]]
- [[2026_Li_EmbodiedAISafetySurvey]]

## My Notes

- Relevance rank in this workspace: 20.
- Use this paper when arguing for the layer: Agent / Monitor.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial.
