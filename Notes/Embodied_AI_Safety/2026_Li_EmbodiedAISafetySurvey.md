---
title: "Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses"
year: 2026
authors:
  - "Li"
  - "et al."
venue: "arXiv"
category: "Embodied AI Safety"
pdf: "../../PDFs/Embodied_AI_Safety/2026_Li_EmbodiedAISafetySurvey.pdf"
url: "https://arxiv.org/abs/2605.02900"
code: "https://github.com/x-zheng16/Awesome-Embodied-AI-Safety"
project: ""
tags:
  - "action-shielding"
  - "attacks-defenses"
  - "embodied-ai-safety"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "semantic-safety"
  - "survey"
---
# Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses

## One-sentence Summary

This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems.

## Problem Setting

Category: Embodied AI Safety. The paper studies how an embodied or learning-enabled robot system
should represent, learn, evaluate, monitor, or enforce behavior under language, vision, state, and
action uncertainty. In the Safe VLA pipeline, it is most relevant to [[Semantic Safety]], [[Runtime
Monitoring]], [[Action Shielding]], [[Human-in-the-loop Safety]], [[Benchmarks and Evaluation]].

## Motivation

VLA and embodied agents are increasingly capable of mapping instructions and observations into
actions, but unsafe behavior can arise from semantic misunderstanding, poor spatial grounding,
distribution shift, adversarial prompts, or low-level controller constraints. This paper matters
because it either defines the nominal capability that must be safeguarded or supplies a mechanism
for monitoring, grounding, filtering, or evaluating safety.

## Main Contributions

- This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems.
- Clarifies or exercises the safety-enforcement layer: Training / Model, Agent / Monitor, Inference / Action, Controller.
- Covers safety scope: Semantic, Task / Plan, Embodied / Spatial, State-space, Low-level Robot.
- Provides evidence that task success alone is insufficient for evaluating embodied agents.

## Methodology

It synthesizes hundreds of papers and connects adversarial, backdoor, jailbreak, hardware,
detection, safe-training, robust-inference, and human-agent interaction work.

Implementation-level interpretation for this review:

- Safety enforcement layer: Training / Model, Agent / Monitor, Inference / Action, Controller.
- Safety scope: Semantic, Task / Plan, Embodied / Spatial, State-space, Low-level Robot.
- Main interface to Safe VLA: [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Human-in-the-loop Safety]], [[Benchmarks and Evaluation]].

## Key Equations or Formalisms

A generic safety filter can be expressed as:

```math
a_{safe}=\Pi_{\mathcal{A}_{safe}(s)}(a_{vla})
```

where the projection or replacement operator keeps the action close to the VLA proposal
while satisfying a state-dependent admissible-action set. The open Safe VLA problem is
constructing `A_safe(s)` from semantic and spatial observations.

## Experiments

Survey paper; no single experimental benchmark, but useful as a map of attack surfaces and defense
families.

## Safety Relevance to My Project

This paper is relevant to:

- Semantic safety: yes.
- Embodied / spatial safety: yes.
- State-space safety: yes.
- Runtime monitoring: yes.
- Action shielding: yes.
- Human-in-the-loop safety: yes.
- Low-level robot safety: yes.
- Benchmark design: yes.

For the preferred research framing, the paper contributes most to: [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Human-in-the-loop Safety]], [[Benchmarks and Evaluation]].

## Strengths

- Makes physical or interactive hazards explicit.
- Useful for adversarial evaluation and safety taxonomy construction.
- Fits the review theme through [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Human-in-the-loop Safety]], [[Benchmarks and Evaluation]].

## Limitations

- Breadth makes it less specific about VLA action shielding implementation details.
- From a Safe VLA perspective, the main missing piece is a robust link from open-world semantic interpretation to enforceable state/action constraints unless the paper explicitly supplies that link.

## Possible Extensions

- Use its pipeline taxonomy to ensure the Safe VLA project does not ignore perception, cognition, controller, or human-interaction failure modes.
- Evaluate the idea using a common VLA policy, a shared simulator, explicit safety violation metrics, and separate reporting of task success versus safety success.

## Useful Quotes / Concepts

- Key concept: This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems.
- Useful framing: safety should be measured independently from task success, especially when the robot can complete a task through unsafe intermediate states.
- Related concepts: [[Semantic Safety]], [[Runtime Monitoring]], [[Action Shielding]], [[Human-in-the-loop Safety]], [[Benchmarks and Evaluation]].

## Related Papers

- [[2026_Li_VLASafetySurvey]]
- [[2024_Xie_BadRobot]]
- [[2024_Robey_RoboPAIR]]
- [[2025_Ying_AGENTSAFE]]

## My Notes

- Relevance rank in this workspace: 28.
- Use this paper when arguing for the layer: Training / Model, Agent / Monitor, Inference / Action, Controller.
- Use this paper when arguing for the safety scope: Semantic, Task / Plan, Embodied / Spatial, State-space, Low-level Robot.
