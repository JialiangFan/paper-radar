---
title: "FPC-VLA: A Vision-Language-Action Framework with a Supervisor for Failure Prediction and Correction"
year: 2025
authors:
  - "Yang"
  - "et al."
venue: "arXiv"
category: "VLA Safety"
pdf: "../../PDFs/VLA_Safety/2025_Yang_FPCVLA.pdf"
url: "https://arxiv.org/abs/2509.04018"
code: ""
project: "https://fpcvla.github.io/"
tags:
  - "failure-correction"
  - "failure-prediction"
  - "robotics"
  - "runtime-monitoring"
  - "safe-vla"
  - "supervisor"
  - "vision-language-action-models"
---
# FPC-VLA: A Vision-Language-Action Framework with a Supervisor for Failure Prediction and Correction

## One-sentence Summary

FPC-VLA wraps a VLA policy with a VLM-based supervisor that predicts failure-prone actions and issues corrective guidance before execution.

## Problem Setting

Category: VLA Safety. The paper studies how an end-to-end VLA policy can be supervised at runtime rather than trusted to execute every proposed action directly.

## Motivation

VLA policies are usually trained on successful demonstrations, so they can struggle after deviation and lack mechanisms for anticipating or correcting failures. This paper is useful evidence that a second supervisory model can improve VLA robustness without replacing the base policy.

## Main Contributions

- Introduces a dual-model framework: base VLA for action generation plus VLM supervisor for failure prediction and correction.
- Uses structured vision-language queries to evaluate action viability at keyframes.
- Generates failure-prediction and correction data automatically from robot datasets rather than relying on manual labels.
- Adds a dual-stream action fusion module that refines actions with historical predictions.

## Methodology

The supervisor is triggered at selected keyframes. Given observation, instruction, and proposed action context, it predicts whether a failure is likely. If risk is detected, it generates a structured directional correction; the system then uses action fusion to refine the original VLA output.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor, Inference / Action.
- Safety scope: Embodied / Spatial, Task / Plan.
- Main interface to Safe VLA: [[Runtime Monitoring]], [[Runtime Assurance]], [[Vision-Language-Action Models]].

## Experiments

Evaluates on simulation platforms including SIMPLER and LIBERO, and reports real-world deployments across multiple robot embodiments such as WidowX, Google Robot, and Franka.

## Safety Relevance to My Project

This is one of the closest examples of a VLA plus runtime supervisor architecture. It supports the proposal claim that VLA safety should be implemented as an external harness layer, but it is narrower than a full safety harness because it focuses on failure prediction and correction rather than semantic gating, formal action shielding, or safety logging.

## Strengths

- Directly wraps VLA execution rather than only benchmarking it.
- Provides a practical supervisor pattern for failure prediction and correction.
- Uses keyframe-triggered supervision to reduce runtime overhead.

## Limitations

- The supervisor is not a formal safety guarantee.
- Corrections still need downstream action shielding before real robot execution.
- The paper is more focused on manipulation robustness than open-world semantic safety or hard physical constraints.

## Possible Extensions

- Route supervisor corrections through an AEGIS-style action shield.
- Combine with Sentinel-style temporal monitoring to trigger the supervisor adaptively.
- Log supervisor interventions into a safety data buffer for later regression tests and fine-tuning.

## Related Papers

- [[2025_Hu_VLSA_AEGIS]]
- [[2024_Agia_Sentinel]]
- [[2025_Peng_FailSafeVLA]]
- [[2026_Sun_PreVLA]]

## My Notes

- Use this paper when arguing that VLA-agent safety harnesses are already emerging as dual-model runtime systems.
- Distinguish it from the proposed harness: FPC-VLA is supervisor plus action refinement; the proposal adds semantic gate, formal shield, monitor, recovery manager, and logging.
