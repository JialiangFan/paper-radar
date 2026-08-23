# MOSAIC: Learning When to Act or Refuse — Guarding Agentic Reasoning Models

**arXiv:** [2603.03205v1](http://arxiv.org/abs/2603.03205v1)
**Date:** 2026-03-03
**Authors:** Aradhye Agarwal, Gurdit Siyan, et al.
**Keywords:** safe reinforcement learning, agentic safety

---

## 相关主题
- [[literature_review]] — Theme 3: LLM 推理与规划的安全性
- 将安全对齐扩展到**多步工具使用**场景

## 核心创新点
提出 MOSAIC 后训练对齐框架，将安全决策显式化为 **plan → check → act/refuse** 循环中的一等公民决策，提升多步骤工具使用中的代理安全性。

## 主要方法
- 推理结构化为 plan-check-act/refuse 循环
- 显式安全推理和拒绝作为 first-class actions
- **偏好型强化学习**：基于轨迹对比训练，不依赖轨迹级标签
- 零-shot 跨模型评估：Qwen2.5-7B, Qwen3-4B-Thinking, Phi-4

## 结论/性能
- 有害行为最多降低 **~50%**
- 对注入攻击的拒绝率提升 **>20%**
- 降低隐私泄露
- 保持或提升良性任务性能

## 独特价值
相比 IPO/ThinkSafe（聚焦推理安全）和 SafePlan（聚焦机器人任务），MOSAIC 将安全对齐扩展到 **agentic 多步工具使用**场景，这是一个新兴且重要的安全前沿。
