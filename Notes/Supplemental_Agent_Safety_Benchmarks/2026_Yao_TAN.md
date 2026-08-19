---
title: "Trustworthy Agent Network: Trust in Agent Networks Must Be Baked In, Not Bolted On"
year: 2026
authors: "Yixiang Yao, Yuhang Yao, Xinyi Fan, Jiechao Gao, Jie Wang, Minjia Zhang, Srivatsan Ravi, Carlee Joe-Wong"
venue: "arXiv"
category: "Supplemental_Agent_Safety_Benchmarks"
pdf: "../../PDFs/Supplemental_Agent_Safety_Benchmarks/2026_Yao_TAN.pdf"
url: "https://arxiv.org/abs/2605.19035"
code: ""
project: ""
tags:
  - agent-safety
  - multi-agent-systems
  - runtime-monitoring
  - safe-vla
  - semantic-safety
  - supplemental-recent
  - trustworthy-agents
---

# Trustworthy Agent Network: Trust in Agent Networks Must Be Baked In, Not Bolted On

## Why This Was Added

This vision paper argues that trust in agent-to-agent networks must be embedded into the coordination architecture itself, because local guardrails, voting, sandboxing, and post-hoc monitors do not prevent unsafe global states from becoming reachable.

## Relevance To Safe VLA

Useful for the safety-agent/runtime-monitoring branch of Safe VLA: it gives a systems argument for constraining multi-agent state transitions and semantic contracts, not merely adding an external judge after a VLA or agent proposes an action.

## Method / Contribution

Introduces the Trustworthy Agent Network (TAN) framing with four design pillars: compositional robustness, semantic containment, accountability and attributability, and cross-boundary reliability. The paper contrasts bolted-on safeguards with baked-in constraints over the global transition function of an agent network.

## Limitations

The paper is a conceptual/vision work rather than an implemented robotics benchmark. Its TAN principles still need concrete mappings to VLA action interfaces, robot-state constraints, formal monitors, and real-time execution budgets.

## How To Use In Proposal

- Use this paper to support: agent-safety, multi-agent-systems, trustworthy-agents.
- Connect it to a Safe VLA harness where planner, VLA policy, monitor, verifier, and controller are separate agents or modules sharing state.
- Treat "unsafe states should be unreachable by construction" as a design target for runtime assurance, while being careful not to claim the paper provides a deployable robot safety mechanism.

## PDF Status

Downloaded.
