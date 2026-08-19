---
imported_title: "Revisiting Formal Methods for Autonomous Robots"
imported_from: "/Users/jfan/ND/看论文/robotic-safety/papers/Revisiting Formal Methods for Autonomous Robots - A Survey.md"
imported_reason: "Broad formal-methods context for robotics safety."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Revisiting Formal Methods for Autonomous Robots: A Structured Survey

## 主题
Formal Methods Autonomous Robots

## 背景
随着Robotic Autonomous Systems (RAS)在核能、航空航天、农业、交通等安全关键领域的应用增加，仅靠测试不足以保证无bug——形式化方法提供数学证明级的正确性保证。形式化方法包括theorem proving、Model Checking (MC)和Runtime Verification (RV)。

## 现有局限与研究问题
- **Limitation:** 2019年的前序综述覆盖2007-2018年的文献，但此后DL-based系统在机器人中的比重大幅增加，形式化方法需要适应这一变化
- **Problem:** 形式化方法在RAS中的应用如何随时间演变？Sub-Symbolic AI（机器学习）的兴起是否影响了FM的使用方式？哪些新趋势正在出现？

## 贡献
- 扩展前序综述，覆盖2007-2024年的文献（初始搜索返回20,764篇，最终筛选181篇）
- 发现一些持续趋势（如Model Checking仍是最常用方法，Temporal Logic仍是最常用形式化框架）
- 识别新兴趋势：Formal Synthesis方法和Probabilistic Verification Techniques的采用显著增加
- 讨论Sub-Symbolic AI (SSAI)对形式化验证的影响和挑战

## 方法论
- 结构化文献综述方法：定义3个研究问题（RQ1:使用哪些FM方法? RQ2:SSAI如何影响FM? RQ3:研究如何演变?）
- 使用Rayyan工具进行系统筛选：20,764 -> TAK过滤 -> 428 -> 全文筛选 -> 181篇
- 数据库：Google Scholar、ACM Digital Library、IEEE Xplore
- 分类维度：FM方法类型、形式化框架、目标属性（safety/liveness等）
