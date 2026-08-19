---
title: "Experiences from Benchmarking Vision-Language-Action Models for Robotic Manipulation"
year: 2025
authors: "Yihao Zhang, Yuankai Qi, Xi Zheng"
venue: "arXiv"
category: "Supplemental_VLA_Foundation_and_Benchmarks"
pdf: "../../PDFs/Supplemental_VLA_Foundation_and_Benchmarks/2025_Benchmarking_VLAs.pdf"
url: "https://arxiv.org/abs/2511.11298"
code: ""
project: ""
tags:
  - benchmark
  - real-robot
  - safe-vla
  - supplemental-recent
  - vla-evaluation
---

# Experiences from Benchmarking Vision-Language-Action Models for Robotic Manipulation

## Why This Was Added

Directly supports the evaluation slide for real-world VLA manipulation.

## Relevance To Safe VLA

Useful for metrics beyond success rate: efficiency, OOD adaptability, language following, failure modes.

## Method / Contribution

Benchmarks ACT, OpenVLA-OFT, RDT-1B, and pi0 across simulation and ALOHA Mobile manipulation tasks.

## Limitations

Benchmark is not specifically safety-oriented, so safety metrics still need to be added.

## How To Use In Proposal

- Use this paper to support: benchmark, vla-evaluation, real-robot.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the method provides training data, safety labels, correction targets, evaluation metrics, or a deployable monitor.

## PDF Status

Downloaded.
