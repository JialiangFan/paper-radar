# Signal Temporal Logic-Guided Apprenticeship Learning

- **Title:** Signal Temporal Logic-Guided Apprenticeship Learning
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** IROS 2024 (IEEE/RSJ International Conference on Intelligent Robots and Systems)
- **Year:** 2024
- **Affiliations:** University of Southern California


## 主题
利用时序逻辑规约编码任务结构，改进从人类示范中学习奖励函数和控制策略的效率

## 背景
学徒学习（apprenticeship learning）从用户示范中学习奖励函数和控制策略，是机器人从人类学习的重要范式。当任务包含多个具有时序依赖的子目标时，准确推断奖励尤为困难。示范质量的好坏直接影响推断的奖励和策略质量。

## 现有局限与研究问题
- **Limitation:** 传统学徒学习方法（如逆强化学习IRL）假设奖励是状态特征的线性组合，无法表达时序依赖关系；示范数量不足时，推断的奖励质量急剧下降；现有方法忽略了任务的时序结构信息。
- **Problem:** 如何利用任务的高层时序结构来改进学徒学习中的奖励推断和策略学习，减少对示范数量的依赖？

## 贡献
- 将STL规约编码为图结构，定义基于时序的行为度量（temporal-based metric）
- 度量同时评估示范者和学习者的行为，提高推断奖励的质量
- 大幅减少学习控制策略所需的示范数量
- 在多种机器人操作仿真中验证有效性

## 方法论
- **STL图编码：** 将描述高层任务目标的STL规约编码为有向图，图中节点表示子目标，边表示时序关系。图结构捕获任务的层次和时序依赖
- **时序行为度量：** 基于STL图定义度量函数，量化轨迹与期望时序行为的匹配程度。该度量同时用于评估示范轨迹和学习者轨迹，提供比标准特征匹配更丰富的反馈信号
- **奖励推断改进：** 将时序度量集成到逆强化学习框架中，使推断的奖励函数自然反映任务的时序结构，而非仅匹配状态特征统计量
- **评估：** 在机器人操作臂仿真的多种任务中实验，包括顺序操作和条件分支任务，所需示范数量显著减少
