# DREAM: Domain-aware Reasoning for Efficient Autonomous Underwater Monitoring

**arXiv:** [2509.13666](http://arxiv.org/abs/2509.13666)
**Date:** 2025-09-17
**Authors:** Zhenqi Wu, Abhinav Modi, Angelos Mavrogiannis, Kaustubh Joshi, Nikhil Chopra, Yiannis Aloimonos, Nare Karapetyan, Ioannis Rekleitis, Xiaomin Lin
**Keywords:** VLM-guided autonomy, underwater monitoring, domain-aware reasoning, habitat monitoring, autonomous exploration

---

## 相关主题
- [[literature_review]] — 水下机器人自主系统
- 与 [[AquaBot - Self-Improving Autonomous Underwater Manipulation]] 的关系：两者均针对水下机器人自主性问题，但 DREAM 聚焦于感知与规划层面的自主探索，而 AquaBot 侧重于操作层面的自主抓取

## 核心创新点
提出 DREAM 框架，利用视觉语言模型（VLM）赋予水下机器人实时环境感知与自主决策能力，通过三层架构（感知层、认知规划层、控制层）和领域感知推理增强提示（reasoning-augmented prompts），实现无需先验位置信息的高效水下探索与栖息地监测。

## 主要方法
- **三层架构设计**: 将系统分为感知层（Perception）、认知感知规划层（Cognitive-aware Planning）和控制层（Control），实现从视觉输入到运动指令的端到端自主决策
- **VLM 引导的自主性**: 利用视觉语言模型作为机器人的"智能大脑"，根据实时视觉观测做出环境感知决策，无需人工干预
- **领域感知推理增强提示**: 设计针对水下场景的推理增强提示策略（reasoning-augmented prompts），将水下领域知识融入 VLM 的推理过程，提升决策的专业性和准确性
- **无先验信息探索**: 系统无需预先获取目标对象的位置信息，即可高效地发现和探索目标（如牡蛎群落、沉船）

## 关键发现
> DREAM 框架在牡蛎监测任务中比基线方法节省 31.5% 的时间，同时覆盖相同数量的牡蛎；相比原始 VLM，使用少 23% 的步数却多覆盖 8.88% 的牡蛎。在沉船探索场景中，框架实现了 100% 的覆盖率（原始 VLM 仅 60.23%），且所需步数减少 27.5%，全程无碰撞。

## 结论/性能
- 牡蛎监测任务：比基线方法节省 **31.5%** 的时间，覆盖相同数量牡蛎
- 与原始 VLM 对比：步数减少 **23%**，牡蛎覆盖率提高 **8.88%**
- 沉船探索任务：实现 **100%** 覆盖率（原始 VLM 为 60.23%），步数减少 **27.5%**
- 沉船探索全程零碰撞，展现了框架在安全性方面的优势
- 研究动机源于海洋升温和酸化对温敏贝类（如牡蛎）的威胁，凸显了低成本、持续性底栖生物监测的重要需求
