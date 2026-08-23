# BFS-PO: Best-First Search for Large Reasoning Models

**arXiv:** [2602.14917v1](http://arxiv.org/abs/2602.14917v1)
**Date:** 2026-02-16
**Authors:** Fiorenzo Parascandolo, Wenhui Tan, et al.
**Keywords:** GRPO, search-based reasoning

---

## 相关主题
- [[literature_review]] — Theme 2: 基于搜索的 LLM 规划
- 与 [[SPIRAL]], [[RAP]] 的搜索策略形成对比

## 核心创新点
提出基于**最佳优先搜索**的 RL 算法 BFS-PO，结合基于最大熵节点的回溯机制，在训练中引导大规模推理模型生成**更短且正确**的推理链，缓解 overthinking 问题。

## 主要方法
- 在 RL 框架下采用 Best-First Search 探索策略
- 通过最大熵节点的回溯机制寻找最短正确答案
- 训练过程中逐步生成更短的输出

## 与现有搜索方法的对比
| 方法 | 搜索策略 | 阶段 | 目标 |
|------|---------|------|------|
| RAP | MCTS | 推理时 | 探索推理空间 |
| SPIRAL | MCTS + 三智能体 | 推理时 | 接地搜索 |
| **BFS-PO** | Best-First Search | 训练时 | 压缩推理链 |

## 结论/性能
在不同基准和基线 LRM 上，BFS-PO **同时提高准确性并缩短输出长度**。

## 关键启发
BFS-PO 将搜索从推理时引入训练时，与 PRIME/GRPO 等 RL 方法结合使用，解决了 GRPO/DAPO 导致的 overthinking 问题。
