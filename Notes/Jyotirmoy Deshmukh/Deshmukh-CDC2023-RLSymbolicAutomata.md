# Model-Free Reinforcement Learning for Symbolic Automata Objectives

- **Title:** Model-free Reinforcement Learning for Spatiotemporal Tasks using Symbolic Automata
- **Authors:** Anand Balakrishnan, Stefan Jaksic, Edgar A. Aguilar, Dejan Nickovic, Jyotirmoy V. Deshmukh
- **Venue:** CDC 2023 (62nd IEEE Conference on Decision and Control)
- **Year:** 2023
- **Affiliations:** University of Southern California; AIT Austrian Institute of Technology GmbH


## 主题
将时序逻辑目标编译为符号自动机，实现 model-free RL 在符号目标上的策略学习

## 背景
强化学习（RL）在复杂控制任务中取得了显著成功，但标准 RL 依赖手工设计的奖励函数，难以精确表达复杂的时序行为目标。形式化方法社区使用时序逻辑（如 LTL、STL）精确描述期望行为，但传统的 model-based 验证方法需要系统模型，限制了其在未知环境中的应用。

## 现有局限与研究问题
- **Limitation:** 直接将 STL 鲁棒度作为稀疏奖励导致 RL 探索困难；现有 LTL + RL 方法多基于 Büchi 自动机或 DFA，不支持定量语义；将时序目标与 RL 结合的方法通常需要环境模型或预定义的原子命题评估。
- **Problem:** 如何在 model-free RL 框架中高效利用符号自动机结构的时序逻辑目标，提供密集的奖励信号引导策略学习？

## 贡献
- 提出将时序逻辑规约编译为符号自动机（symbolic automata），自动机状态转移作为 RL 的 reward shaping 机制
- 设计基于自动机进展（automaton progression）的密集奖励函数，解决稀疏奖励问题
- 方法完全 model-free，不需要环境的转移模型
- 证明所提 reward shaping 保持最优策略不变性（potential-based reward shaping）

## 方法论
- **符号自动机构造：** 将 STL/LTL 规约通过标准算法编译为有限状态符号自动机。自动机的状态表示规约的满足进展，转移条件为符号谓词（关于系统状态的布尔表达式）
- **Reward Shaping：** 定义基于自动机状态的势函数（potential function）：Φ(q) 反映当前自动机状态 q 距离接受状态的"距离"。shaped reward = r(s,a,s') + γΦ(q') - Φ(q)，根据 potential-based shaping 理论，保证最优策略不变
- **进展奖励：** 每当系统状态触发自动机状态转移（向接受状态推进），给予正奖励；后退或停留则给予负/零奖励。这提供了密集的引导信号
- **Model-Free 集成：** 将自动机状态附加到 RL 的观测空间，使用标准 model-free 算法（PPO, SAC 等）训练策略
- **评估：** 在 grid-world 和连续控制环境中，方法显著加速收敛并提高最终策略的规约满足率
