# SECURE: Enhancing Safety in Learning from Demonstration via CBF Shielding

- **Authors**: Letian Chen et al.
- **Year/Venue**: 2024 / HRI 2024
- **ACM**: [10.1145/3610977.3635002](https://dl.acm.org/doi/10.1145/3610977.3635002)
- **Tags**: #CBF #formal-guarantee #learning-from-demonstration #manipulation #safety-shield

## Problem
从人类示范学习的 robot policy 可能在部署时产生不安全的动作（如刀具操作时碰到障碍物）。

## Method
1. 从 end-user demonstrations 中学习 **customized CBF**
2. CBF 作为 safety shield 层叠加在 LfD policy 上
3. 当 policy 输出不安全动作时，CBF shield 将其修正为最近的安全动作

## Formal Guarantee?
**YES — CBF 提供形式化安全保证**（forward invariance of safe set）。

## Key Results
- 真实世界 knife-cutting 任务
- Task completion ↑12.5%
- **Safety violations → ZERO**

## Relevance
**CBF + post-hoc safety** 的经典范例。与 VLSA/AEGIS 类似但从 demonstration 学 CBF。在真实机器人刀具操作上达到 zero violation——这是形式化方法的力量。

## Related Papers
- [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]] — 同样 CBF plug-and-play，但用于 VLA
- [[robotics-safety-post-training/papers/SafeDiffuser|SafeDiffuser]] — CBF 嵌入 diffusion
- [[robotics-safety-post-training/papers/Neural-Lyapunov-Barrier|Neural Lyapunov Barrier]] — Lyapunov 方法的形式化验证
