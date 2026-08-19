---
title: "CLAP: Contrastive Latent Action Pretraining for Learning Vision-Language-Action Models from Human Videos"
year: 2026
authors: "Chubin Zhang, Jianan Wang, Zifeng Gao, Yue Su, Tianru Dai, Cai Zhou, Jiwen Lu, Yansong Tang"
venue: "arXiv"
category: "Supplemental_VLA_Foundation_and_Benchmarks"
pdf: "../../PDFs/Supplemental_VLA_Foundation_and_Benchmarks/2026_Zhang_CLAP.pdf"
url: "https://arxiv.org/abs/2601.04061"
code: ""
project: "https://lin-shan.com/CLAP/"
tags:
  - contrastive-learning
  - human-video-pretraining
  - latent-action-models
  - safe-vla
  - supplemental-recent
  - vla-foundation-model
---

# CLAP: Contrastive Latent Action Pretraining for Learning Vision-Language-Action Models from Human Videos

## Why This Was Added

Adds a recent human-video pretraining route for VLA models by learning executable latent actions from video transitions.

## Relevance To Safe VLA

Relevant to action representation, data scaling, and transfer from human demonstrations to robot execution. For the Safe VLA project, the useful question is whether safety monitors or shields can operate over CLAP's learned latent action codebook or the downstream flow policy.

## Method / Contribution

CLAP aligns visual latent actions from human videos with proprioceptive latent actions from robot trajectories through contrastive learning and a quantized executable codebook. The paper builds two VLA formulations on top of the representation: CLAP-NTP for autoregressive instruction following and object generalization, and CLAP-RF for faster Rectified Flow-based continuous control. It also introduces Knowledge Matching regularization to reduce catastrophic forgetting during fine-tuning.

## Limitations

The work is capability-oriented rather than safety-oriented. It still requires robotic grounding for entirely new tasks, faces ambiguity between human hand motions and robot gripper actions, uses a multi-stage training pipeline, and does not provide explicit runtime safety constraints or formal safety guarantees.

## How To Use In Proposal

- Use this paper to support: vla-foundation-model, latent-action-models, human-video-pretraining, contrastive-learning.
- Connect it to the two proposal directions: inherent VLA safety training and safety-agent/runtime monitoring.
- For the real-robot project, ask whether the learned latent action codebook can expose safety-relevant intervention points for correction targets, action shielding, or monitor-conditioned policy heads.

## PDF Status

Downloaded.
