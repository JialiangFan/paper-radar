# VLA-RFT: Vision-Language-Action Reinforcement Fine-Tuning with Verified Rewards

- **Authors**: Multiple institutions
- **Year/Venue**: 2025
- **ArXiv**: [2510.00406](https://arxiv.org/abs/2510.00406)
- **Tags**: #VLA #GRPO #post-training #world-model #manipulation

## Problem
VLA 模型需要大量标注数据进行监督训练，且难以在部署环境中持续改进。

## Method
1. **Data-driven World Model**: 训练世界模型作为模拟器
2. **GRPO Optimization**: 在世界模型中用 GRPO 做 VLA 的 reinforcement fine-tuning
3. **Verified Rewards**: 世界模型提供可验证的 reward 信号

## Formal Guarantee?
**Partial** — 在世界模型中训练避免了真实世界安全风险，但世界模型本身的准确性无保证。

## Key Results
- 仅 0.4K iterations 达到 150K SFT baseline 的性能
- 更好的环境扰动鲁棒性

## Relevance
展示了 **GRPO 可以用于 VLA post-training**。与 SafeGen-LLM 的 GRPO for planning 互补，VLA-RFT 是 GRPO for control。但缺少安全约束——如果加入 SafeVLA 的 CMDP 或 VLSA 的 CBF，就是理想的组合。

## Related Papers
- [[robotics-safety-post-training/papers/SafeVLA|SafeVLA]] — 有安全约束的 VLA post-training
- [[robotics-safety-post-training/papers/DPPO|DPPO]] — 另一种 VLA RL fine-tuning（PPO + diffusion）
- [[robotics-safety-post-training/papers/SafeGen-LLM|SafeGen-LLM]] — GRPO for planning（同一 RL 算法，不同层级）
