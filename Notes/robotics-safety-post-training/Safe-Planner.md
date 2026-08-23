# Safe Planner: Empowering Safety Awareness in Large Pre-Trained Models for Robot Task Planning

- **Authors**: Multiple
- **Year/Venue**: 2025 / AAAI 2025
- **ArXiv**: [2411.06920](https://arxiv.org/abs/2411.06920)
- **Tags**: #planning #safety-module #sim-to-real #VLM

## Problem
预训练的 VLM/LLM 缺乏真实场景的安全知识（从互联网数据学习，不了解物理世界的危险）。

## Method
1. 训练独立的 **safety prediction module**（在仿真中训练）
2. 在 VLM 做高层规划时，safety module 评估每个计划的风险
3. 拒绝高风险计划，引导 VLM 选择安全替代方案
4. Sim-to-real transfer

## Formal Guarantee?
**No**（learned safety predictor，无形式化保证）。

## Key Results
- SOTA task success + improved safety
- Sim-to-real 安全模块迁移成功

## Relevance
与 SafeGen-LLM 在同一层级（planning），但用 learned safety module 而非 formal specification。两者可互补。

## Related Papers
- [[robotics-safety-post-training/papers/SafeGen-LLM|SafeGen-LLM]] — formal specification + GRPO
- [[robotics-safety-post-training/papers/SELP|SELP]] — LTL formal constraint
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — VLA-level safety
