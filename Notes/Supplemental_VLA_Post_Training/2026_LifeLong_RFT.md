---
title: "Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning"
year: 2026
authors: "Yuan Liu, Haoran Li, Shuai Tian, Yuxing Qin, Yuhui Chen, Yupeng Zheng, Yongzhen Huang, Dongbin Zhao"
venue: "arXiv"
category: "Supplemental_VLA_Post_Training"
pdf: "../../PDFs/Supplemental_VLA_Post_Training/2026_LifeLong_RFT.pdf"
url: "https://arxiv.org/abs/2602.10503"
code: ""
project: ""
tags:
  - continual-learning
  - reinforcement-fine-tuning
  - safe-vla
  - supplemental-recent
  - vla-post-training
---

# Towards Long-Lived Robots: Continual Learning VLA Models via Reinforcement Fine-Tuning

## Why This Was Added

Directly supports continual VLA improvement with reinforcement fine-tuning.

## Relevance To Safe VLA

Relevant to a real-robot project where deployment data, corrections, and new tasks arrive over time.

## Method / Contribution

Introduces LifeLong-RFT with chunk-level on-policy RL and multi-dimensional process rewards to reduce forgetting and improve adaptation.

## Limitations

Mostly evaluates structured benchmarks and selected real-world tasks; safety-specific violations are not the central metric.

## How To Use In Proposal

- Use this paper to support: continual-learning, vla-post-training, reinforcement-fine-tuning.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the method provides training data, safety labels, correction targets, evaluation metrics, or a deployable monitor.

## PDF Status

Downloaded.
