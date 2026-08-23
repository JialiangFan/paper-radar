# FOSP: Fine-tuning Offline Safe Policy through World Models

- **Authors**: Multiple
- **Year/Venue**: 2024
- **ArXiv**: [2407.04942](https://arxiv.org/abs/2407.04942)
- **Tags**: #offline-to-online #safe-RL #reachability #world-model #manipulation

## Problem
Offline pre-trained 策略在新环境中 fine-tuning 时，online 探索可能导致不安全行为。

## Method
1. **Offline pre-training**: 在 offline 数据上训练策略
2. **World model**: 学习环境动力学
3. **Online fine-tuning with reachability guidance**: 用 reachability analysis 引导 online RL，确保探索过程中的安全
4. **In-sample optimization**: 约束策略更新在 offline 数据支撑范围内

## Formal Guarantee?
**Partial — Reachability guidance** 提供 reachable set 的安全分析，但基于 learned world model（近似）。

## Key Results
- Vision-based manipulation 任务上有效
- Real-world deployment 验证

## Relevance
**Offline→online safe fine-tuning** 的范式与 VLA post-training 高度相关。VLA 通常先 offline 训练，再 online fine-tune。FOSP 的 reachability guidance 可以为这个过程提供安全保障。

## Related Papers
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — 也是 VLA safe post-training，但用 CMDP
- [[robotics-safety-post-training/papers/Neural-Lyapunov-Barrier|Neural Lyapunov Barrier]] — 更强的形式化验证
