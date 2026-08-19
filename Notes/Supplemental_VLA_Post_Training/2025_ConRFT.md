---
title: "ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy"
year: 2025
authors: "ConRFT authors"
venue: "arXiv"
category: "Supplemental_VLA_Post_Training"
pdf: "../../PDFs/Supplemental_VLA_Post_Training/2025_ConRFT.pdf"
url: "https://arxiv.org/abs/2502.05450"
code: ""
project: ""
tags:
  - human-intervention
  - reinforcement-fine-tuning
  - safe-vla
  - supplemental-recent
  - vla-post-training
---

# ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy

## Why This Was Added

Directly supports VLA post-training with online fine-tuning and human intervention for safe exploration.

## Relevance To Safe VLA

Strong fit for a real-robot safety-correction training proposal because unsafe or low-quality rollouts can be converted into improvement signals.

## Method / Contribution

Uses reinforced fine-tuning via a consistency policy, with online interaction and human interventions to improve VLA manipulation performance.

## Limitations

The safety role is mostly mediated through intervention and reward design rather than formal safety guarantees.

## How To Use In Proposal

- Use this paper to support: vla-post-training, reinforcement-fine-tuning, human-intervention.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the method provides training data, safety labels, correction targets, evaluation metrics, or a deployable monitor.

## PDF Status

Downloaded.
