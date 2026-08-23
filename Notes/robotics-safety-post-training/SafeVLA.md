# SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning

- **Authors**: Borong Zhang, Yuhao Zhang, Jiaming Ji, Yingshan Lei, Josef Dai, Yuanpei Chen, Yaodong Yang
- **Year/Venue**: 2025 / NeurIPS 2025 Spotlight
- **ArXiv**: [2503.03480](https://arxiv.org/abs/2503.03480)
- **Affiliation**: PKU-Alignment, Peking University
- **GitHub**: [PKU-Alignment/SafeVLA](https://github.com/PKU-Alignment/SafeVLA)
- **Tags**: #VLA #safe-RL #CMDP #post-training #manipulation

## Problem
VLA 模型在真实世界部署时面临安全风险（碰撞、损坏物体、危险操作），现有 VLA 训练只优化任务完成率，不考虑安全约束。

## Method: Integrated Safety Approach (ISA)
1. **Safety Requirement Modeling**: 系统定义 VLA 的安全需求（物体安全、机器人安全）
2. **Unsafe Behavior Elicitation**: 主动诱发多样的不安全行为（对抗性场景生成）
3. **CMDP-based Safe RL**: 用 Constrained MDP 框架做 post-training
   - Reward model: 任务完成度
   - **Cost model**: 安全违规程度
   - Min-max optimization: 在满足安全约束的前提下最大化任务 reward
4. **Safety-CHORES Benchmark**: 程序化生成的安全评测场景

## Formal Guarantee?
**无严格形式化保证**。使用 CMDP 约束优化，提供统计安全保证但非 formal verification。

## Key Results
- Safety violation cost ↓83.58%
- Task success rate ↑3.85%（安全和性能不矛盾！）
- 跨 12 个 OOD 任务组合泛化（500+ 场景）
- Sim-to-real transfer 成功

## Relevance
**最直接相关的论文**——首次将 CMDP-based safe RL 作为 post-training 应用到 VLA。是 [[robotics-safety-post-training/papers/Safe-RLHF|Safe RLHF]] 方法论在 robotics 的直接延伸。

## Limitation & Opportunity
- Cost model 是 learned 的，无形式化保证
- **机会**: 将 cost model 替换为 CBF（如 [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]]），获得形式化安全保证

## Related Papers
- [[robotics-safety-post-training/papers/Safe-RLHF|Safe RLHF]] — 方法论来源（CMDP + Lagrangian）
- [[robotics-safety-post-training/papers/VLSA-AEGIS|VLSA/AEGIS]] — 互补方法：CBF plug-and-play（有形式化保证）
- [[robotics-safety-post-training/papers/VLA-RFT|VLA-RFT]] — 另一种 VLA post-training（GRPO, 无安全焦点）
- [[reasoning-fine-tuning/papers/SafeGen-LLM - Safety Generalization in Planning|SafeGen-LLM]] — Plan-level 对比（GRPO + reward machine）
