# AquaBot: Self-Improving Autonomous Underwater Manipulation

**arXiv:** [2410.18969](http://arxiv.org/abs/2410.18969)
**Date:** 2024-10-24
**Authors:** Ruoshi Liu, Huy Ha, Mengxue Hou, Shuran Song, Carl Vondrick
**Keywords:** underwater manipulation, behavior cloning, self-improving policy, autonomous grasping, open-source robotics

---

## 相关主题
- [[literature_review]] — 水下机器人自主系统
- 与 [[DREAM - Domain-aware Reasoning for Efficient Autonomous Underwater Monitoring]] 的关系：两者均致力于提升水下机器人自主能力，但 AquaBot 专注于操作（manipulation）层面的自主学习与优化，DREAM 则侧重于感知与规划层面的自主探索

## 核心创新点
提出 AquaBot 系统，将行为克隆（从人类遥操作演示中学习）与自学习优化相结合，构建了一个能够超越人类遥操作性能的全自主水下操作系统，并开源了全部软硬件实现。

## 主要方法
- **行为克隆基础策略**: 从人类遥操作演示中通过行为克隆（Behavior Cloning）学习基础操作策略，将人类专家的操作经验转化为机器人的初始控制策略
- **自学习优化（Self-Learning Optimization）**: 在行为克隆策略基础上，通过自我探索和优化机制进一步提升策略性能，使机器人能够发现并学习超越人类演示的更优操作方式
- **全自主操作系统**: 将感知、规划和控制整合为完全自主的端到端系统，消除了对人类遥操作的依赖
- **开源软硬件**: 公开发布了完整的硬件设计和软件实现，降低了水下机器人研究的门槛

## 关键发现
> AquaBot 的自优化策略在操作速度上超越人类操作员 41%，证明了通过行为克隆结合自学习优化，机器人不仅能模仿人类技能，还能突破人类遥操作的性能上限。这一发现对水下操作领域具有重要意义，表明自主系统有潜力在复杂水下环境中取代低效的人类遥操作。

## 结论/性能
- 自优化策略在速度上超越人类操作员 **41%**
- 在多种真实水下操作任务中验证了系统的通用性：物体抓取（grasping）、垃圾分类（trash sorting）、救援打捞（rescue retrieval）
- 系统实现了从人类演示学习到自主超越的完整闭环：行为克隆 -> 自优化 -> 超人性能
- 全部软硬件开源，促进了水下机器人操作研究的可复现性和社区发展
- 研究证明了在复杂流体动力学和非结构化水下环境中实现全自主操作的可行性
