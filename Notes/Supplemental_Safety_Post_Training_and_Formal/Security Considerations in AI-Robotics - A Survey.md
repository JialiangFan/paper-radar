---
imported_title: "Security Considerations in AI-Robotics"
imported_from: "/Users/jfan/ND/看论文/robotic-safety/papers/Security Considerations in AI-Robotics - A Survey.md"
imported_reason: "Useful for adversarial and security risks in embodied AI."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Security Considerations in AI-Robotics: A Survey of Current Methods, Challenges, and Opportunities

## 主题
AI-Robotics Security Survey

## 背景
AI-Robotics系统已深入交通、制造、医疗、农业等行业，但AI的集成也带来严重安全问题。对抗攻击、数据泄露、系统操纵可能导致事故、财产损失甚至危及人命。2020年研究者通过细微改变路边限速标志即操纵Tesla加速50英里/小时。

## 现有局限与研究问题
- **Limitation:** 现有综述仅聚焦AI-Robotics安全的特定方面（如操作系统攻击、物理层攻击、IoT通信安全），缺乏整合attack surfaces、ethical/legal concerns和HRI security的全面视角
- **Problem:** 如何在通用混合AI-Robotics架构（Perception-Navigation-Control）中系统性地识别和缓解安全威胁？

## 贡献
- 提出三维度分类法：攻击面与缓解策略、伦理法律关切、HRI安全
- 首次在通用混合AI-Robotics架构中系统剖析各层（perception、navigation/planning、control）的攻击面
- 涵盖对抗攻击（adversarial patches、物理对抗样本）、数据投毒、模型窃取等具体威胁
- 讨论伦理问题（依赖性、心理影响、自主性丧失）和法律框架（GDPR、CCPA、问责制）
- 分析HRI中的隐私、完整性、安全、可信赖性和可解释性

## 方法论
- 基于sense-plan-act架构的分层分析
- 感知层：对抗样本攻击（CNN、RNN、Visual Transformer）
- 规划层：路径规划和代价地图的攻击
- 控制层：执行器命令注入
- 跨层安全防御策略综述
