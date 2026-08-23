# VLSA/AEGIS: Vision-Language-Action Models with Plug-and-Play Safety Constraint Layer

- **Authors**: Tsinghua University (THU-RCSCT)
- **Year/Venue**: 2025
- **ArXiv**: [2512.11891](https://arxiv.org/abs/2512.11891)
- **GitHub**: [THU-RCSCT/vlsa-aegis](https://github.com/THU-RCSCT/vlsa-aegis)
- **Tags**: #VLA #CBF #formal-guarantee #plug-and-play #manipulation

## Problem
VLA 模型生成的动作可能导致碰撞或不安全行为。需要一种不修改 VLA 模型本身、但能保证动作安全的方法。

## Method: AEGIS Architecture
1. **Vision-Language Safety Assessment Module**: 从视觉和语言输入评估当前安全状态
2. **Action-Driven Safety-Guaranteed Control Module**: 基于 **Control Barrier Functions (CBFs)** 动态调整 VLA 输出动作
   - 如果动作安全 → 原样输出（不影响正常性能）
   - 如果动作不安全 → CBF 修正到最近的安全动作
3. **Plug-and-play**: 不需要重新训练 VLA，直接叠加在任何 VLA 上

## Formal Guarantee?
**YES — CBF 提供理论安全保证**。Control Barrier Function 保证系统状态始终在安全集合内（forward invariance）。

## Key Results
- Obstacle avoidance ↑59.16%
- Task success ↑17.25%
- 引入 **SafeLIBERO** benchmark（两级难度的安全操作评测）

## Relevance
**形式化保证最强的 VLA 安全方法**。CBF 作为 plug-and-play 层的设计很优雅——不需要重新训练模型就能添加安全保证。但这是 inference-time 的，不是 post-training。

## Limitation & Opportunity
- 不是 post-training（inference-time 修正）
- **核心机会**: 将 CBF 约束集成到 VLA 的 RL post-training loss 中（CBF-constrained GRPO/PPO），同时获得 post-training 的性能提升和 CBF 的形式化保证

## Related Papers
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — post-training 方法（CMDP, 无 CBF）
- [[robotics-safety-post-training/papers/SECURE|SECURE]] — 也用 CBF，但从 demonstration 学习
- [[robotics-safety-post-training/papers/SafeDiffuser|SafeDiffuser]] — CBF 嵌入 diffusion denoising
