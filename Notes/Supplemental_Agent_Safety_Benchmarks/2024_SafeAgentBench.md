---
title: "SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents"
year: 2024
authors: "Sheng Yin et al."
venue: "arXiv"
category: "Supplemental_Agent_Safety_Benchmarks"
pdf: "../../PDFs/Supplemental_Agent_Safety_Benchmarks/2024_SafeAgentBench.pdf"
url: "https://arxiv.org/abs/2412.13178"
code: "https://github.com/shengyin1224/SafeAgentBench"
project: ""
tags:
  - agent-safety
  - benchmark
  - embodied-agents
  - safe-vla
  - supplemental-recent
---

# SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents

## Why This Was Added

Foundational embodied-agent safety benchmark for task planning.

## Relevance To Safe VLA

Useful for demonstrating that agent-level planning safety is a separate failure surface from action control.

## Method / Contribution

Provides hazardous/safe task datasets, SafeAgentEnv, low-level controller support, and semantic/execution evaluation.

## Limitations

It targets embodied LLM agents, not necessarily end-to-end VLA robot controllers.

## How To Use In Proposal

- Use this paper to support: agent-safety, benchmark, embodied-agents.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the method provides training data, safety labels, correction targets, evaluation metrics, or a deployable monitor.

## PDF Status

Downloaded.
