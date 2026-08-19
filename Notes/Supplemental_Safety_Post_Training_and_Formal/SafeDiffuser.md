---
imported_title: "SafeDiffuser: Safe Planning with Diffusion Probabilistic Models"
imported_from: "/Users/jfan/ND/看论文/robotics-safety-post-training/papers/SafeDiffuser.md"
imported_reason: "Diffusion planning safety background for action-generation models."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# SafeDiffuser: Safe Planning with Diffusion Probabilistic Models

- **Authors**: Multiple
- **Year/Venue**: 2025 / ICLR 2025
- **ArXiv**: [2306.00148](https://arxiv.org/abs/2306.00148)
- **Tags**: #CBF #diffusion #safe-planning #formal-guarantee

## Problem
Diffusion-based planners/policies 生成的轨迹不保证满足安全约束。

## Method
将 **CBF 约束嵌入 diffusion denoising 过程**：
- 每步 denoising 时，检查 CBF 约束
- 如果违反，将 denoised sample 投影到安全集合
- 理论上保证最终生成的轨迹满足 CBF 安全约束

## Formal Guarantee?
**YES — CBF safety guarantee integrated into generation process**。

## Key Results
- 在 planning/control 任务上验证
- 保持生成质量的同时满足安全约束

## Relevance
**DPPO + SafeDiffuser = Safe Diffusion Policy Post-Training**。DPPO 提供了 diffusion policy 的 RL fine-tuning 框架，SafeDiffuser 提供了 CBF 安全约束的嵌入方法。两者结合是一个自然的研究方向。

## Related Papers
- [[robotics-safety-post-training/papers/DPPO|DPPO]] — diffusion policy 的 RL post-training
- [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]] — CBF for VLA
- [[robotics-safety-post-training/papers/SECURE|SECURE]] — CBF from demonstrations
