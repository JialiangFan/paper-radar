# Multi-agent Path Finding for Timed Tasks using Evolutionary Games

- **Title:** Multi-agent Path Finding for Timed Tasks using Evolutionary Games
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** QEST 2024 (International Conference on Quantitative Evaluation of Systems)
- **Year:** 2024
- **Affiliations:** University of Southern California


## 主题
结合加权自动机任务规约和演化博弈论，训练多智能体系统完成具有时间约束的路径规划任务

## 背景
自主多智能体系统（如医院机器人、快递无人机）在高度不确定的环境中运行，需要完成复杂的时序任务目标同时确保安全。RL是训练此类系统的主流方法，但将RL应用于轨迹级（trajectory-level）任务目标仍是挑战。

## 现有局限与研究问题
- **Limitation:** 标准RL使用基于状态的奖励函数，难以表达轨迹级时序目标（如"在截止期限前按顺序完成多个子任务"）；深度RL方法训练成本高，扩展性差；多智能体间的协调增加了问题复杂度。
- **Problem:** 如何高效训练同构多智能体团队完成具有时间约束的复杂轨迹级任务目标？

## 贡献
- 使用加权自动机（weighted automata）规约轨迹级目标，自动机最大路径对应期望行为，超越简单的截止期限属性，支持"迅捷性"等性能属性
- 利用演化博弈论（EGT）原理训练同构多智能体团队
- 路径长度比SOTA RL方法减少约30%
- 计算速度比深度RL方法快至少一个数量级

## 方法论
- **加权自动机规约：** 将时序任务目标编码为加权自动机，自动机的权值反映轨迹对任务目标的满足程度。与布尔自动机不同，加权自动机可以区分"刚好满足"和"优秀满足"，提供定量的优化目标
- **演化博弈论训练：** 利用同构智能体的对称性，通过EGT的复制者动力学（replicator dynamics）更新策略。智能体共享经验，EGT策略更新比独立RL训练更高效
- **混合策略：** EGT自然产生混合策略（概率性行为选择），增加多智能体系统的多样性和鲁棒性
- **评估：** 在多种规模的环境中实验，验证随智能体数量增加的可扩展性优势，以及相比深度RL的效率提升
