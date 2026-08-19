---
title: "Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts"
year: 2026
authors:
  - "Sun"
  - "et al."
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2026_Sun_PreVLA.pdf"
url: "https://arxiv.org/abs/2605.22446"
code: ""
project: ""
tags:
  - "action-verification"
  - "preemptive-verification"
  - "robotics"
  - "runtime-monitoring"
  - "runtime-safety"
  - "safe-vla"
  - "vision-language-action-models"
  - "world-models"
---
# Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts

## One-sentence Summary

Pre-VLA performs pre-execution verification of VLA action chunks, filtering low-quality actions before they are executed or used in world-model rollouts.

## Problem Setting

Category: Runtime Monitoring Assurance. The paper studies runtime verification for VLA-generated action chunks under uncertainty, with the goal of reducing physical failures and world-model error accumulation.

## Motivation

Generative VLA policies can produce low-quality action chunks that cause downstream execution failures. A runtime harness should assess candidate actions before execution, especially when action errors compound over long horizons.

## Main Contributions

- Proposes a preemptive runtime verification architecture for VLA action chunks.
- Predicts both safety confidence and critic-derived advantage scores.
- Uses a dual-mode resampling scheduler to filter or resample low-quality actions under limited compute.
- Applies the same verification idea to physical execution and world-model imagination.

## Methodology

Pre-VLA uses an efficient multimodal verifier with modality-aware pooling and a lightweight dual-branch head. The verifier scores candidate action chunks, and the scheduler decides whether to accept, filter, or resample actions before execution.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Inference / Action.
- Safety scope: Embodied / Spatial, Task / Plan.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Runtime Assurance]], [[Benchmarks and Evaluation]].

## Experiments

Evaluates on LIBERO, reporting improved closed-loop success rate over RynnVLA-002, fewer task execution steps, and fast forward verification latency per action chunk.

## Safety Relevance to My Project

Pre-VLA is a direct prior for the pre-execution verification part of a VLA harness. It supports the idea that action chunks should be treated as proposals, not commands.

## Strengths

- Operates before action execution, which is preferable to detecting failures only after they occur.
- Fits a model-agnostic harness design because it can sit between a VLA and the robot controller.
- Explicitly considers runtime compute constraints.

## Limitations

- The verifier is learned, so its safety confidence is not a hard physical guarantee.
- It filters quality and safety risk, but does not by itself construct formal safe sets or semantic hazard constraints.
- Needs to be combined with an action shield for hard constraint enforcement.

## Possible Extensions

- Use Pre-VLA as the predictive risk scorer feeding an intervention manager.
- Combine verifier scores with CBF-QP feasibility and semantic safety gates.
- Log rejected action chunks as safety data for regression evaluation.

## Related Papers

- [[2024_Agia_Sentinel]]
- [[2025_Yang_FPCVLA]]
- [[2025_Hu_VLSA_AEGIS]]
- [[2026_Chen_HazardArena]]

## My Notes

- Good citation for "runtime verification before execution."
- In the proposal, frame it as a narrow verifier module rather than a complete safety harness.
