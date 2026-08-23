# A Survey of Constraint Formulations in Safe Reinforcement Learning

## 主题
Safe RL Constraint Formulations

## 背景
安全RL已成为在约束条件下优化策略的基本范式。主流方法基于constrained criterion，即在满足安全约束的前提下最大化期望累积reward。然而，安全约束的多样化表示形式和理论关联缺乏系统性梳理，阻碍了领域的理解和发展。

## 现有局限与研究问题
- **Limitation:** 现有综述侧重于方法（how to solve），而非约束形式化（how to formulate），约束表示的多样性使得理解和比较不同算法变得困难
- **Problem:** 不同约束形式化之间的数学关系是什么？是否存在统一的更一般化的问题形式？

## 贡献
- 首篇从约束形式化角度系统综述安全RL的论文（IJCAI 2024）
- 识别并定义七类主要约束形式化：期望累积安全约束、状态约束、联合chance约束、期望瞬时安全约束、几乎确定累积约束、几乎确定瞬时约束（时不变/时变阈值）
- 引入transformability、generalizability、conservative approximation三个理论概念，揭示各约束形式化之间的数学互联关系
- 证明存在两个Identical or More General Safe RL (IoMG-SafeRL)问题，其他常见问题可被转换或保守近似到这两个问题

## 方法论
- 基于有限时域折扣CMDP框架 M ∪ C，引入safety constraint function (SCF)统一各类约束表示
- 为每种约束形式化梳理代表性算法（CPO、Lagrangian、RCPO、SafeLayer等）
- 理论分析：证明transformability（精确等价转换）和conservative approximation（保守近似）关系
