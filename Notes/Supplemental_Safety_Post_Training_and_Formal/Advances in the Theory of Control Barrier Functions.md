---
imported_title: "Advances in the Theory of Control Barrier Functions"
imported_from: "/Users/jfan/ND/看论文/robotic-safety/papers/Advances in the Theory of Control Barrier Functions.md"
imported_reason: "CBF theory supplement beyond the core Ames papers."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Advances in the Theory of Control Barrier Functions

## 主题
Control Barrier Functions Theory

## 背景
Control Barrier Functions (CBFs) 已成为非线性约束控制系统验证和轨迹综合的核心工具。CBF通过约束barrier function沿系统轨迹的变化率（使用class K函数），确保constrained set的前向不变性，从而在给定动力学和控制输入约束下保证安全。

## 现有局限与研究问题
- **Limitation:** 为任意系统找到有效CBF非trivial；高相对度安全约束加上输入约束使问题更加复杂；建模/参数不确定性需要鲁棒CBF
- **Problem:** 标准CBF导出的控制输入仅是pointwise最优（myopic），在时间约束、输入约束、干扰、对抗输入、采样数据效应等实际场景下如何保证安全和可行性？

## 贡献
- 提出Fixed-Time Barriers等新型timed CBFs，同时处理时间、安全和输入约束
- 构建InputConstrained CBFs，作为High-Order CBFs的泛化，处理高相对度约束下的干扰和输入约束
- 提出在线自适应方法调整CBF参数，防止controllability丧失并减少保守性
- 引入考虑未来轨迹的CBF形式化，解决pointwise最优的局限性
- 讨论输出反馈控制和零阶保持控制下的安全保持实现挑战

## 方法论
- 基于控制仿射系统 ẋ = f(x) + g(x)u，通过CBF-QP框架综合安全控制器
- Timed CBFs: FxT-CLF-CBF-QPs用于时空控制和递归可行性
- InputConstrained CBFs: 泛化HOCBF处理输入约束和干扰
- 非光滑CBFs: 处理多约束下的不连续输入场景
