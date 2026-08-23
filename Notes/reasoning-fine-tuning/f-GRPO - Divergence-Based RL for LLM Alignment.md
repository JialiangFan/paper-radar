# f-GRPO and Beyond: Divergence-Based RL Algorithms for General LLM Alignment

**arXiv:** [2602.05946v1](http://arxiv.org/abs/2602.05946v1)
**Date:** 2026-02-05
**Authors:** Rajdeep Haldar, Lantao Mei, Guang Lin, et al.
**Keywords:** GRPO, RL theory, alignment

---

## 相关主题
- [[literature_review]] — 新增主题: RL 理论与改进
- 为 PRIME, DRM, ReasonFlux-PRM 等使用 RL 训练的方法提供理论基础

## 核心创新点
基于 **f-散度的变分表示**，提出通用对齐框架 f-GRPO（on-policy）和 f-HAL（混合 on/off-policy），覆盖 RLVR 与偏好对齐，并提供理论收敛保证。

## 主要方法
- **f-GRPO**：基于 f-divergence 变分表示的 on-policy RL
- **f-HAL**：混合 on/off-policy 对齐损失
- 理论证明对齐后平均奖励的改进
- 在 RLVR（数学推理）和 PA（安全对齐）上验证

## 结论/性能
在 Math Reasoning 的 RLVR 和 Safety Alignment 任务中，相较现有方法展示出更好的性能和灵活性。

## 关键价值
f-GRPO 为我们综述中多篇使用 GRPO 的论文（PRIME, DRM, ReasonFlux-PRM）提供了统一的理论视角——不同的 f-divergence 选择对应不同的对齐行为。
