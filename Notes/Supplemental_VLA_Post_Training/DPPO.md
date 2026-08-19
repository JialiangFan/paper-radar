---
imported_title: "DPPO: Diffusion Policy Policy Optimization"
imported_from: "/Users/jfan/ND/看论文/robotics-safety-post-training/papers/DPPO.md"
imported_reason: "RL optimization background for diffusion robot policies."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# DPPO: Diffusion Policy Policy Optimization

- **Authors**: Allen Z. Ren et al. (Princeton)
- **Year/Venue**: 2025 / ICLR 2025
- **ArXiv**: [2409.00588](https://arxiv.org/abs/2409.00588)
- **Tags**: #diffusion-policy #PPO #post-training #manipulation #sim-to-real

## Problem
预训练的 diffusion policy 如何通过 RL 继续优化？Diffusion 的多步 denoising 使标准 PPO 不直接适用。

## Method
- 定义 **two-layer Diffusion Policy MDP**（outer MDP: environment, inner MDP: denoising）
- 在此 MDP 上做 PPO fine-tuning
- Structured, on-manifold exploration（在 diffusion 的流形上探索，隐式安全）

## Formal Guarantee?
**No**，但 on-manifold exploration 提供隐式安全（动作空间被约束在训练数据分布附近）。

## Key Results
- Long-horizon manipulation 任务显著提升
- Zero-shot sim-to-real transfer

## Relevance
Diffusion policy 正在成为 robot 的主流策略表示。DPPO 证明了 diffusion policy 可以 RL post-training。结合 [[robotics-safety-post-training/papers/SafeDiffuser|SafeDiffuser]] 的 CBF 约束，可以实现 safe diffusion policy post-training。

## Related Papers
- [[robotics-safety-post-training/papers/SafeDiffuser|SafeDiffuser]] — 在 diffusion denoising 中嵌入 CBF（安全版本）
- [[robotics-safety-post-training/papers/VLA-RFT|VLA-RFT]] — GRPO fine-tuning VLA
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — CMDP safe RL for VLA
