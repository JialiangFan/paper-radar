---
title: "SafeAgent: A Runtime Protection Architecture for Agentic Systems"
year: 2026
authors:
  - "Liu"
  - "Ilyushin"
  - "Ni"
  - "Zhu"
venue: "arXiv"
category: "Runtime Monitoring Assurance"
pdf: "../../PDFs/Runtime_Monitoring_Assurance/2026_Liu_SafeAgent.pdf"
url: "https://arxiv.org/abs/2604.17562"
code: ""
project: ""
tags:
  - "agent-safety"
  - "llm-agents"
  - "runtime-monitoring"
  - "runtime-protection"
  - "runtime-safety"
  - "safe-vla"
  - "tool-agents"
---
# SafeAgent: A Runtime Protection Architecture for Agentic Systems

## One-sentence Summary

SafeAgent treats LLM agent safety as a stateful runtime protection problem over evolving trajectories rather than as stateless input-output filtering.

## Problem Setting

Category: Runtime Monitoring Assurance. The paper is not VLA-specific, but it is relevant as a software-agent analogue for Claude-Code-like runtime governance.

## Motivation

LLM agents can accumulate risk through multi-step tool use, persistent context, and prompt injection. A runtime safety harness for VLA agents faces a similar systems problem, except actions are physical and continuous rather than only tool calls.

## Main Contributions

- Separates execution governance from semantic risk reasoning.
- Introduces a runtime controller that mediates actions around the agent loop.
- Maintains persistent session state for context-aware safety decisions.
- Evaluates robustness against agent-security benchmarks and prompt-injection workflows.

## Methodology

SafeAgent uses a runtime controller plus context-aware decision core. The controller mediates actions, while the decision core performs risk encoding, utility-cost evaluation, consequence modeling, policy arbitration, and state synchronization.

Implementation-level interpretation for this review:

- Safety enforcement layer: Agent / Monitor.
- Safety scope: Task / Plan, Semantic.
- Main interface to Safe VLA: [[Runtime Assurance]], [[Runtime Monitoring]], [[Human-in-the-loop Safety]].

## Experiments

Evaluates on Agent Security Bench and InjecAgent, showing improved robustness over baseline and text-level guardrail methods while preserving benign-task performance.

## Safety Relevance to My Project

SafeAgent is useful for the proposal analogy to Claude Code: safety should be a runtime architecture with action mediation, state tracking, risk arbitration, and recovery policies. It does not solve robot-specific issues such as continuous control, collision avoidance, force limits, or perception grounding.

## Strengths

- Strong conceptual prior for separating the agent loop from the runtime safety controller.
- Emphasizes persistent state, which matters for long-horizon VLA tasks and safety logs.
- Helps justify a harness architecture instead of prompt-only safety.

## Limitations

- It targets LLM/tool agents, not physical VLA robot control.
- Does not provide action shielding, CBFs, robot-state monitoring, or semantic-to-physical constraint grounding.
- Needs adaptation for continuous actions and real-time safety constraints.

## Possible Extensions

- Translate its runtime controller and decision core into a VLA harness controller and intervention manager.
- Replace tool-call policy arbitration with robot action gating, shielding, and recovery.
- Use persistent session state as the safety data buffer for failures, interventions, and human corrections.

## Related Papers

- [[2023_Ren_KnowNo]]
- [[2025_Yang_FPCVLA]]
- [[2026_Sun_PreVLA]]
- [[2025_Hu_VLSA_AEGIS]]

## My Notes

- Use this as an LLM-agent runtime architecture analogue, not as a robotics safety solution.
- It supports the phrase "Claude-Code-like safety harness" more directly than the VLA papers do.
