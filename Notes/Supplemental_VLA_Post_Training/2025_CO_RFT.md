---
title: "CO-RFT: Efficient Fine-Tuning of Vision-Language-Action Models through Chunked Offline Reinforcement Learning"
year: 2025
authors: "CO-RFT authors"
venue: "arXiv"
category: "Supplemental_VLA_Post_Training"
pdf: "../../PDFs/Supplemental_VLA_Post_Training/2025_CO_RFT.pdf"
url: "https://arxiv.org/abs/2508.02219"
code: ""
project: ""
tags:
  - fine-tuning
  - offline-rl
  - safe-vla
  - supplemental-recent
  - vla-post-training
---

# CO-RFT: Efficient Fine-Tuning of Vision-Language-Action Models through Chunked Offline Reinforcement Learning

## Why This Was Added

Adds an offline RL fine-tuning option that may be practical when real-robot online exploration is limited.

## Relevance To Safe VLA

Relevant for using logged safe/unsafe/corrected trajectories without risky online training.

## Method / Contribution

Fine-tunes VLA models with chunked offline reinforcement learning after imitation-learning initialization.

## Limitations

Offline reward quality and dataset coverage can limit safety generalization.

## How To Use In Proposal

- Use this paper to support: offline-rl, vla-post-training, fine-tuning.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the method provides training data, safety labels, correction targets, evaluation metrics, or a deployable monitor.

## PDF Status

Downloaded.
