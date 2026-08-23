# ROVER: Regulator-Driven Robust Temporal Verification of Black-Box Robot Policies

**arXiv:** [2511.17781](http://arxiv.org/abs/2511.17781)
**Date:** 2025-11-21
**Authors:** Kristy Sakano, Jianyu An, Dinesh Manocha, Huan Xu
**Keywords:** Signal Temporal Logic, robustness metrics, black-box verification, robot safety, regulator-in-the-loop

---

## 相关主题
- [[literature_review]] — 形式化方法与机器人安全

## 核心创新点
提出了一种基于"监管者在环"(regulator-in-the-loop)的迭代框架 ROVER，利用信号时序逻辑(STL)规范对黑盒机器人策略的执行轨迹进行事后安全评估，并引入三种互补的鲁棒性度量指标（TRV、LRV、AVRV）来量化策略对安全规范的遵守程度，从而为策略重训练提供可操作的定量反馈。

## 主要方法
- **STL 规范定义与轨迹评估**: 领域专家将人类可读的时序安全规则形式化为 STL 规范，对黑盒策略生成的 N 条执行轨迹计算鲁棒性值，完全不依赖于策略内部结构的访问权限
- **三重鲁棒性度量体系**:
  - **Total Robustness Value (TRV)**: 聚合所有轨迹的鲁棒性值，反映平均性能与整体安全裕度
  - **Largest Robustness Value (LRV)**: 捕获最坏情况行为（所有轨迹中最小鲁棒性值），识别最关键的违规
  - **Average Violation Robustness Value (AVRV)**: 仅针对违规轨迹计算平均违规严重程度
- **监管者决策规则**: 基于 TRV、LRV、AVRV 的阈值组合，监管者将策略分类为"无需改进"、"需要策略改进"或"需要边缘案例分析"（当 LRV 远小于 AVRV 时，表明存在罕见但灾难性的失败）
- **加权安全评分**: 监管者计算加权安全评分 S(π) = Σwᵢ × M_φᵢ，结合领域知识的重要性权重与每个规范的鲁棒性度量三元组
- **STL 引导的奖励重塑与重训练**: 根据监管者反馈调整奖励函数结构（如增大道路惩罚权重、添加速度限制奖励项），迭代重训练策略直至满足安全要求

## 实验验证
- **虚拟赛车域（Mario Kart SNES）**: 定义三条 STL 规范（全局速度限制、保持在赛道上、转弯后延迟加速），100 条轨迹评估。重训练后满足率从 30%→83%（速度限制）、8%→99%（保持赛道）、87%→95%（延迟加速）
- **移动机器人导航（TurtleBot3 仿真）**: 定义三条 STL 规范（无急转弯、定时完成、不停留在障碍物附近），重训练后满足率从 9%→36%（无急转弯）、18%→54%（定时完成）、45%→67%（不停留）
- **真实世界验证（TurtleBot3 实物）**: 后验证模型在平滑导航满足率上提升 27%，路径更平滑，但观察到仿真到真实的差距（真实环境中转弯更频繁）

## 关键发现
> 跨六条 STL 规范和两个域，监管者引导的重训练平均将满足率提升 43.8%，同时在半数规范中改善了平均性能（TRV）并降低了违规严重程度（LRV），证明了黑盒策略的事后 STL 验证作为安全认证流程的可行性。

## 结论/性能
- 六条 STL 规范平均满足率提升 43.8%
- 最显著改进：虚拟赛车中"保持在赛道上"规范从 8% 提升至 99%（+91%）
- 真实世界 TurtleBot3 平滑导航满足率提升 27%
- 该框架不需要访问策略内部，适用于任何黑盒策略的安全评估与迭代改进
- 存在 sim-to-real gap，真实环境中策略表现略有退化

## 与 SafeVLA 项目的关联
本文的核心思路（用 STL 鲁棒性度量评估策略安全性并引导重训练）与 SafeVLA 项目高度相关。区别在于：ROVER 在策略重训练时通过修改奖励函数间接利用 STL 反馈，而 SafeVLA 计划将 STL 鲁棒性直接作为 GRPO/RLVR 的连续步级安全奖励信号进行端到端优化。ROVER 的 TRV/LRV/AVRV 度量体系可作为 SafeVLA 评估阶段的参考指标。
