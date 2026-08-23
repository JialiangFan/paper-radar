# P2S: Probabilistic Process Supervision for General-Domain Reasoning QA

**arXiv:** [2601.20649v1](http://arxiv.org/abs/2601.20649v1)
**Date:** 2026-01-28
**Authors:** Wenlin Zhong, Chengyuan Liu, Yiquan Wu, et al.
**Keywords:** reinforcement learning reasoning, process reward

---

## 相关主题
- [[literature_review]] — Theme 1: 过程奖励建模
- 与 [[PRIME]], [[DRM]], [[ReasonFlux-PRM]] 互补

## 核心创新点
提出 Probabilistic Process Supervision（P2S），在强化学习中通过对推理过程每一步的**路径保真性奖赏（Path Faithfulness Reward, PFR）**提供细粒度的过程监督，并与结果奖赏结合，缓解奖励稀疏问题。

## 主要方法
- 在自监督框架下**无需额外奖励模型或人工标注推理步骤**
- RL 过程中对高质量参考推理链（gold-CoT）进行合成与筛选
- 针对每一步推理计算 PFR：基于在当前前缀下生成 gold-CoT 后缀的条件概率
- PFR 可与任意结果奖赏灵活结合，提供密集学习信号

## 与现有工作的关系
| 方法 | 过程奖励来源 | 需要额外模型？ |
|------|-------------|--------------|
| PRIME | logprob 比值（隐式） | 否 |
| DRM | 多维度评分（显式训练） | 是 |
| ReasonFlux-PRM | 轨迹+步骤评分 | 是 |
| **P2S** | 条件概率（自监督） | 否 |

## 结论/性能
在阅读理解和医学问答基准上显著优于强基线，证明 PFR + 结果奖赏的组合能有效提升通用领域推理。

## 关键启发
- 与 PRIME 类似，P2S 也是"免费"过程监督的路线，但机制不同（条件概率 vs logprob 比值）
- 将过程奖励扩展到**通用领域推理**（非数学/代码），填补了现有 PRM 工作的空白
