# Safe RLHF-V: Safe Reinforcement Learning from Multi-modal Human Feedback

- **Authors**: PKU-Alignment team
- **Year/Venue**: 2025 / NeurIPS 2025
- **ArXiv**: [2503.17682](https://arxiv.org/abs/2503.17682)
- **Tags**: #multimodal #safe-RLHF #VLM #foundation

## Problem
多模态 LLM (VLM) 缺乏安全对齐方法。文本域的 Safe RLHF 不能直接迁移到视觉+语言。

## Method
1. **BeaverTails-V**: 多模态双重偏好标注（helpfulness + safety，多级安全标签）
2. **Beaver-Guard-V**: 多级 guardrail 系统
3. **Multimodal CMDP**: 分别训练多模态 reward 和 cost models

## Key Results
- Safety + helpfulness 双赢：34%+ win-rate over RLHF baselines

## Relevance
VLM 安全对齐的基础方法。VLA 是 VLM + action head，Safe RLHF-V 的多模态安全方法可以自然扩展到 VLA。

## Related Papers
- [[robotics-safety-post-training/papers/Safe-RLHF|Safe RLHF]] — 文本版本
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — VLA 上的安全 post-training
