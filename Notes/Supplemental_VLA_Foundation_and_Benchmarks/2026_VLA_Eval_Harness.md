---
title: "vla-eval: A Unified Evaluation Harness for Vision-Language-Action Models"
year: 2026
authors: "Allen Institute for AI authors"
venue: "ICLR 2026"
category: "Supplemental_VLA_Foundation_and_Benchmarks"
pdf: "../../PDFs/Supplemental_VLA_Foundation_and_Benchmarks/2026_VLA_Eval_Harness.pdf"
url: "https://openreview.net/forum?id=IpKQsHWaYS"
code: "https://github.com/allenai/vla-evaluation-harness"
project: ""
tags:
  - benchmark
  - evaluation-harness
  - safe-vla
  - supplemental-recent
  - vla-evaluation
---

# vla-eval: A Unified Evaluation Harness for Vision-Language-Action Models

## Why This Was Added

Evaluation harness for running many VLA models on many robot simulation benchmarks.

## Relevance To Safe VLA

Useful if the project needs standardized evaluation rather than one-off scripts.

## Method / Contribution

Decouples model integration from benchmark integration so cross-evaluation matrices can be filled systematically.

## Limitations

It is evaluation infrastructure, not a safety method; safety metrics must be added.

## How To Use In Proposal

- Use this paper to support: benchmark, evaluation-harness, vla-evaluation.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the method provides training data, safety labels, correction targets, evaluation metrics, or a deployable monitor.

## PDF Status

Downloaded.
