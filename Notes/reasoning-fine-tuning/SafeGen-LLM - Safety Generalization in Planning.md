# SafeGen-LLM: Enhancing Safety Generalization in Task Planning for Robotic Systems

**arXiv:** [2602.24235v1](http://arxiv.org/abs/2602.24235v1)
**Date:** 2026-02-27
**Authors:** Jialiang Fan, Weizhe Xu, Mengyu Liu, et al.
**Keywords:** LLM planning, safety, PDDL

---

## 相关主题
- [[literature_review]] — Theme 2 + Theme 3 交叉
- 与 [[SafePlan]], [[PDDL-Instruct]] 直接相关

## 核心创新点
提出 SafeGen-LLM，通过**形式化安全约束驱动的两阶段后训练**和基于**奖励机器（reward machines）**的 GRPO 策略优化，在多域规划中实现安全性泛化。

## 主要方法
1. 构建包含**显式安全约束的多域 PDDL3 基准**
2. **阶段 1 (SFT)**：在符合约束的规划数据集上学习规划语法与语义
3. **阶段 2 (GRPO)**：基于形式化验证的细粒度奖励机器指导安全对齐 + 课程学习
4. 支持 PDDL 与自然语言多种输入格式

## 与现有工作对比
| 方法 | 安全保障机制 | 规划形式化 | 训练/推理时 |
|------|-----------|----------|-----------|
| SafePlan | LTL 验证 | AI2-THOR | 推理时 |
| PDDL-Instruct | VAL 验证器 | PDDL | 训练时 |
| **SafeGen-LLM** | 奖励机器 + GRPO | PDDL3 | 训练时 |

## 结论/性能
在多域规划任务和多输入格式下显著优于前沿专有基线，展现出强大的安全性泛化能力。

## 关键启发
SafeGen-LLM 是 SafePlan 和 PDDL-Instruct 的"交集"——同时解决安全性和规划能力，且通过 GRPO + 奖励机器实现了训练时的安全泛化。
