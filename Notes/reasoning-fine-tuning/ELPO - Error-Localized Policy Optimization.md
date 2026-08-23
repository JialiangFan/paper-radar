# ELPO: Error-Localized Policy Optimization for Tool-Integrated LLM Reasoning

**arXiv:** [2602.09598v1](http://arxiv.org/abs/2602.09598v1)
**Date:** 2026-02-10
**Authors:** Qiao Liang, Yuke Zhu, Chao Ge, et al.
**Keywords:** LLM planning, process reward, credit assignment

---

## 相关主题
- [[literature_review]] — Theme 1 + Theme 2 交叉
- 与 [[PRIME]], [[P2S - Probabilistic Process Supervision]] 互补

## 核心创新点
提出 Error-Localized Policy Optimization (ELPO)，在工具集成推理中通过定位**首个不可恢复的错误步骤**来进行细粒度的信用分配与策略更新。

## 主要方法
1. **二分搜索回放树**：在固定预算下定位首个不可恢复步骤
2. **分层优势归因**：将回放树转化为稳定的学习信号
3. **误差局部自适应裁剪**：对关键步骤及其后缀强化修正更新

## 与过程奖励方法的对比
| 方法 | 过程信号来源 | 粒度 | 场景 |
|------|-----------|------|------|
| PRIME | logprob 比值 | 步骤级 | 数学/代码 |
| P2S | 条件概率 | 步骤级 | 通用推理 |
| **ELPO** | 回放树 + 二分搜索 | 首错步骤 | 工具集成推理 |

## 结论/性能
在数学、科学问答和代码执行等 TIR 基准上，ELPO 在可比较采样预算下持续优于强 Agentic RL 基线。

## 关键启发
ELPO 提供了"首个不可恢复错误"这一独特视角——不是对每步均匀评分，而是找到推理链中的**致命转折点**，与 IPO 中 compliance cue 的思路异曲同工。
