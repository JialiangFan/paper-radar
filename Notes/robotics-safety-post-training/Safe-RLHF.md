# Safe RLHF: Safe Reinforcement Learning from Human Feedback

- **Authors**: Josef Dai et al. (PKU-Alignment, Peking University)
- **Year/Venue**: 2024 / ICLR 2024 Spotlight
- **ArXiv**: [2310.12773](https://arxiv.org/abs/2310.12773)
- **GitHub**: [PKU-Alignment/safe-rlhf](https://github.com/PKU-Alignment/safe-rlhf)
- **Tags**: #CMDP #Lagrangian #safe-RLHF #foundation

## Problem
标准 RLHF 将 helpfulness 和 harmlessness 混在一个 reward 中，导致安全和能力的 trade-off 不可控。

## Method
1. **Decoupled preferences**: 分别训练 reward model (helpfulness) 和 cost model (harmlessness)
2. **Lagrangian CMDP optimization**: 用 Lagrange multiplier 动态平衡两个目标
3. **PKU-SafeRLHF dataset**: 双重标注的偏好数据

## Formal Guarantee?
**No strict formal guarantee**，但 CMDP 提供约束满足的理论保证（在 perfect optimization 下）。

## Relevance
**SafeVLA 的方法论来源**。SafeVLA 直接将 Safe RLHF 的 CMDP 框架从 LLM 迁移到 VLA。理解 Safe RLHF 是理解整个 safe post-training pipeline 的基础。

## Related Papers
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — 在 VLA 上的应用
- [[robotics-safety-post-training/papers/Safe-RLHF-V|Safe RLHF-V]] — 多模态扩展
- [[robotics-safety-post-training/papers/HC-RLHF|HC-RLHF]] — 加入高置信安全保证
- [[robotics-safety-post-training/papers/PE-RLHF|PE-RLHF]] — 加入物理知识
