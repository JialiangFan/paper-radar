---
imported_title: "Safe Learning for Contact-Rich Robot Tasks"
imported_from: "/Users/jfan/ND/看论文/robotic-safety/papers/Safe Learning for Contact-Rich Robot Tasks - A Survey.md"
imported_reason: "Relevant to real-robot contact and manipulation safety."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Safe Learning for Contact-Rich Robot Tasks: A Survey from Classical Learning-Based Methods to Safe Foundation Models

## 主题
Safe Learning Contact-Rich Robotics

## 背景
机器人日益需要在非结构化动态环境中操作，装配、插入、切割等接触密集型任务因复杂的不连续动力学和精确力控需求而极具挑战性。学习方法虽带来灵活性，但在接触任务中应用引发严重安全顾虑。

## 现有局限与研究问题
- **Limitation:** 现有安全学习综述忽略物理接触交互引入的复杂性；操作和接触相关综述不直接集成安全学习框架；VLM/VLA等基础模型缺乏物理交互数据，安全问题更加突出
- **Problem:** 如何在接触密集型任务中同时保证探索阶段和执行阶段的安全，特别是在基础模型时代？

## 贡献
- 首篇以安全为核心的接触密集型机器人任务学习综述（覆盖2018-2025年）
- 提出安全中心分类法：按学习阶段（exploration vs execution）、安全集成层次（planning/control/end-to-end）和感知模态（force/torque/vision）分类
- 特别强调VLM/VLA基础模型与安全的交叉：语言级约束规约、多模态安全信号接地
- 识别关键开放挑战：带安全约束的sim-to-real迁移、标准化安全benchmark缺乏、可证明安全泛化

## 方法论
- 系统文献搜索：跨IEEE Xplore、ACM、SpringerLink、Google Scholar，组合"safe/robot/contact-rich/learning"等关键词
- 分类框架：safe exploration（constrained RL、uncertainty-aware control、model-based safety filters）和 safe execution（policy robustness、constraint satisfaction）
- 分析VLM/VLA安全机会与挑战：语言约束、多模态接地、力/接近度安全信号的集成
