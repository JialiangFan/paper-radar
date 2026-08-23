# Robust Testing for Cyber-Physical Systems using Reinforcement Learning

- **Title:** Robust Testing for Cyber-Physical Systems using Reinforcement Learning
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** MEMOCODE 2023 (ACM-IEEE International Conference on Formal Methods and Models for System Design)
- **Year:** 2023
- **Affiliations:** University of Southern California


## 主题
利用深度强化学习生成鲁棒的CPS测试用例，即使被测系统发生微小变化仍能提供有意义的测试

## 背景
信息物理系统（CPS）运行在不确定环境中，测试需要精心定义环境以涵盖所有可能的现实场景，同时识别系统违反规约的操作场景。传统的测试方法（如随机测试、覆盖引导测试）在高维连续环境中效率低下。

## 现有局限与研究问题
- **Limitation:** 基于优化的对抗测试方法在被测系统（SUT）发生微小变化时可能失效，需要重新生成测试；传统RL测试方法倾向于过拟合特定SUT版本；手工设计测试场景无法充分覆盖边界情况。
- **Problem:** 如何设计鲁棒的测试生成框架，使生成的测试在SUT发生小幅变化时仍能提供有意义且具有挑战性的测试？

## 贡献
- 提出基于深度RL的鲁棒测试框架，测试生成对SUT的小幅变化具有鲁棒性
- RL代理学习生成对抗性但现实的测试场景，最大化SUT违反STL规约的可能性
- 在自动驾驶仿真器中三个系统上验证有效性
- 将鲁棒性概念引入基于RL的CPS测试领域

## 方法论
- **测试建模：** 将测试生成建模为MDP，RL代理控制环境参数（如其他车辆行为、天气条件），目标是使SUT违反其STL安全规约
- **鲁棒性训练：** 在训练过程中对SUT施加微扰（参数变化），使RL代理学到的测试策略不依赖于SUT的特定参数值，而是发现系统性的薄弱环节
- **STL奖励：** 使用STL鲁棒度语义作为RL的奖励信号，负鲁棒度表示规约违反，鲁棒度的绝对值表示违反/满足的程度
- **评估：** 在photo-realistic自动驾驶仿真器中的三个场景上实验，包括车道保持、跟车和避障任务，验证鲁棒测试相比非鲁棒方法的优势
