# THINKSAFE: Self-Generated Safety Alignment for Reasoning Models

**arXiv:** [2601.23143v1](http://arxiv.org/abs/2601.23143v1)
**Date:** 2026-01-30
**Authors:** Seanie Lee, Sangwoo Park, Yumin Choi, et al.
**Keywords:** GRPO, safety alignment, reasoning models

---

## 相关主题
- [[literature_review]] — Theme 3: LLM 推理与规划的安全性
- 与 [[IPO - Intervened Preference Optimization]], [[SafeThink - Safety Recovery in Reasoning Models]] 互补

## 核心创新点
提出自生成安全对齐框架 ThinkSafe，通过轻量级的**拒绝引导（refusal steering）**让模型在自身分布内生成安全推理痕迹，从而在**无需外部教师**的情况下恢复安全对齐。

## 关键 Insight
> 虽然 compliance 抑制了安全机制，但模型通常保留了识别有害内容的潜在知识。ThinkSafe 通过 refusal steering 解锁这种能力。

## 主要方法
1. 利用 refusal steering 引导模型产生**在分布内**的安全推理轨迹
2. 以这些自生成的安全响应对模型进行微调
3. 避免外部教师蒸馏带来的分布差异

## 结论/性能
- 在 DeepSeek-R1-Distill 与 Qwen3 上显著提升安全性并保持推理能力
- 安全性**优于 GRPO**，计算成本显著更低

## 与同主题论文对比
| 方法 | 类型 | 需要外部教师？ | 推理时开销？ |
|------|------|--------------|------------|
| IPO | 训练时 | 否（自我分析） | 无 |
| SafeThink | 推理时 | 安全奖励模型 | 有 |
| **ThinkSafe** | 训练时 | 否（自生成） | 无 |
| SafePlan | 推理时 | 形式化规则 | 有 |
