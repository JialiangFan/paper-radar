# Multi-Agent Path Finding via Offline RL and LLM Collaboration

- **Title:** Multi-Agent Path Finding via Offline RL and LLM Collaboration
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** arXiv preprint
- **Year:** 2025
- **Affiliations:** University of Southern California


## 主题
基于Decision Transformer的离线RL框架结合LLM，实现高效去中心化多智能体路径规划

## 背景
多智能体路径规划（MAPF）是机器人和物流领域的关键问题，组合复杂度高且现实环境中存在部分可观测性。去中心化RL方法是主流解决方案，但面临训练时间长和智能体自利行为导致碰撞的双重挑战。

## 现有局限与研究问题
- **Limitation:** 去中心化RL方法存在两大问题：(1) 智能体的自利行为导致频繁碰撞；(2) 依赖复杂通信模块使训练时间长达数周。在线RL的长期信用分配和稀疏奖励问题在MAPF中尤为突出。
- **Problem:** 如何在大幅缩短训练时间的同时，提高去中心化多智能体系统在静态和动态环境中的路径规划性能？

## 贡献
- 提出基于Decision Transformer（DT）的去中心化规划框架，利用离线RL将训练时间从数周缩短到数小时
- 引入GPT-4o作为动态环境中的策略引导，提升智能体在环境变化时的适应能力
- 在静态和动态环境条件下均展示了改进的性能
- 将序列建模范式引入MAPF问题

## 方法论
- **Decision Transformer架构：** 将路径规划建模为序列决策问题，DT基于历史轨迹和期望回报生成动作，避免了传统RL的时序差分学习
- **离线强化学习：** 使用预先收集的数据集训练，无需在线交互，大幅缩短训练周期。离线数据来自专家策略或启发式求解器
- **LLM集成：** 利用GPT-4o的推理能力动态引导智能体策略，特别是在环境意外变化时提供高层决策建议，弥补离线策略的泛化局限
- **评估：** 在多种MAPF基准场景中验证，包括不同规模的智能体数量和静态/动态环境设置
