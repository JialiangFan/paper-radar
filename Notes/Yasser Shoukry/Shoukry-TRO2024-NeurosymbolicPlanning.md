# Neurosymbolic Motion and Task Planning for Linear Temporal Logic

## 主题
Neural-symbolic 框架统一运动规划与 LTL 任务规划

## 背景
机器人需要完成复杂的长时序任务（如按顺序访问目标、条件响应），同时满足运动学和碰撞避免约束。LTL 可精确描述高层任务需求，但将 LTL 规划与连续运动规划统一仍是开放问题。传统分层方法（先任务规划再运动规划）无法保证全局最优，且层间不一致可能导致失败。

## 现有局限与研究问题
- **Limitation:** 分层规划方法中任务层和运动层独立求解，可能产生运动学不可行的任务计划；端到端学习方法缺乏对 LTL 规约的形式化保证；现有 neural-symbolic 方法在规划效率和规约满足率之间难以平衡。
- **Problem:** 如何设计一个 neural-symbolic 框架，同时优化 LTL 任务规划和连续运动规划，并提供形式化的规约满足保证？

## 贡献
- 提出 neurosymbolic 运动与任务规划框架，将 LTL 规约的符号结构与神经网络的运动规划能力统一
- 设计可微的 LTL 满足度指标，支持端到端梯度优化
- 利用自动机引导的搜索策略减少规划空间
- 在复杂机器人任务中展示方法的有效性和可扩展性

## 方法论
- **LTL → 自动机分解：** 将 LTL 规约转换为确定性 Rabin 自动机（DRA）或有限轨迹上的 DFA，获取接受条件的结构化表示。自动机状态代表任务进展
- **神经运动规划器：** 训练神经网络作为局部运动规划器，输入当前状态和目标状态，输出满足运动学约束的轨迹段。网络通过模仿学习或强化学习训练
- **符号-神经协同：** 自动机提供高层任务分解（当前应追求哪个子目标），神经规划器负责子目标间的运动规划。两者通过可微接口连接，支持联合优化
- **自动机引导搜索：** 使用自动机的接受条件引导搜索有效的任务计划（状态序列），避免枚举所有可能。结合 A* 搜索和神经网络启发式评估
- **形式化保证：** 通过 post-hoc 验证检查生成的轨迹是否满足 LTL 规约。如果不满足，利用反例信息精化搜索
- **评估：** 在移动机器人导航、多目标任务和操纵任务中测试，方法在规约满足率和规划效率上均优于纯符号方法和纯学习方法

> **Title:** Neurosymbolic Motion and Task Planning for Linear Temporal Logic Tasks
> **Authors:** Xiaowu Sun, Yasser Shoukry
> **Venue:** IEEE Transactions on Robotics (TRO 2024)
> **Year:** 2024
> **Affiliations:** University of California, Irvine