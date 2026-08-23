# SafeThink: Safety Recovery in Reasoning Models Is Only a Few Early Steering Steps Away

**arXiv:** [2602.11096v1](http://arxiv.org/abs/2602.11096v1)
**Date:** 2026-02-11
**Authors:** Soumya Suvra Ghosal, Souradip Chakraborty, et al.
**Keywords:** safe reinforcement learning, reasoning safety

---

## 相关主题
- [[literature_review]] — Theme 3: LLM 推理与规划的安全性
- 与 [[IPO - Intervened Preference Optimization]] 互补（推理时 vs 训练时）

## 核心创新点
将安全恢复视为**满足约束（satisficing）**而非最大化目标，在推理过程中仅在安全阈值被触发时注入经优化的短前缀 **"Wait, think safely"** 以引导模型走向安全完成。

## 主要方法
- **推理时防护**：用安全奖励模型监控推理轨迹
- 条件性插入短纠错前缀
- 在 6 个开源多模态大模型和 4 个越狱基准上评估

## 关键发现
> 安全恢复通常只需前 **1-3 步**干预即可实现安全纠偏

## 结论/性能
- 攻击成功率降低 **30-60%**
- LlamaV-o1: JailbreakV-28K 63.33% → 5.74%
- R1-Onevision: Hades 69.07% → 5.65%
- MathVista 准确率几乎无损：65.20% → 65.00%

## 与 IPO 的互补性
| 维度 | IPO | SafeThink |
|------|-----|-----------|
| 阶段 | 训练时 | 推理时 |
| 机制 | DPO 偏好优化 | 条件前缀注入 |
| 开销 | 一次性训练 | 每次推理监控 |
| 发现 | safety triggers / compliance cues | 前 1-3 步即可纠偏 |
