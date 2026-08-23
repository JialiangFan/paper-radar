# Neuro-Symbolic Acceleration of MILP Motion Planning with Temporal Logic and Chance Constraints

- **Title:** Neuro-Symbolic Acceleration of MILP Motion Planning with Temporal Logic and Chance Constraints
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** arXiv preprint
- **Year:** 2025
- **Affiliations:** University of Southern California


## 主题
利用图神经网络加速基于MILP的运动规划求解，处理时序逻辑和概率约束

## 背景
自主系统的运动规划常涉及复杂的时间敏感任务和不确定性。将这些任务形式化为混合整数线性规划（MILP）是标准方法，但MILP求解的计算成本高、可扩展性差，严重限制了实时应用。

## 现有局限与研究问题
- **Limitation:** 传统MILP求解器在处理大规模运动规划问题时效率低下；纯神经网络方法缺乏形式化保证；现有加速方法未针对时序逻辑和概率约束的特殊结构进行优化。
- **Problem:** 如何在保持MILP求解器形式化保证的同时，利用机器学习加速求解过程？

## 贡献
- 提出neuro-symbolic框架，用图神经网络（GNN）引导MILP符号求解器的搜索过程
- 针对两类代表性规划问题：Signal Temporal Logic（STL）规约和基于Conformal Predictive Programming（CPP）的概率约束
- GNN学习分支变量选择（branching variable selection）和求解器参数配置
- 在关键指标上平均性能提升约20%

## 方法论
- **问题建模：** 将STL运动规划和CPP概率约束规划统一建模为MILP问题，包含整数变量（离散决策）和连续变量（轨迹参数）
- **GNN引导：** 将MILP问题的结构编码为图表示，使用GNN预测最优分支变量和求解器参数。GNN捕捉MILP问题中变量与约束之间的关系结构
- **Neuro-Symbolic集成：** 神经网络组件不替代符号求解器，而是在求解过程中引导关键决策点（如branch-and-bound中的分支选择），保持求解器的完备性和正确性保证
- **评估：** 在STL规划和CPP概率约束规划两类问题上验证，与state-of-the-art求解器相比，运行时间和解质量均有显著提升
