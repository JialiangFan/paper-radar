# Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning

## 主题
Safe Robot Learning Survey

## 背景
过去五年，机器人安全学习方法的研究贡献急剧增加，来自控制论和强化学习两个社区。机器人在复杂场景中自主操作时，动力学模型通常是不确定或部分已知的，需要在不确定性下做出安全决策。

## 现有局限与研究问题
- **Limitation:** 控制论方法在特定场景下有强保证但难以泛化到新场景；纯数据驱动的RL方法虽泛化性强但难以提供形式化安全保证
- **Problem:** 两个社区使用不同的语言和框架，缺乏统一视角来理解安全学习控制问题

## 贡献
- 统一控制论和RL框架，将安全学习控制问题形式化为包含系统模型、代价函数和安全约束的优化问题
- 提出三级安全保证层次：硬约束满足（Safety Level III）、概率约束满足（Level II）、约束鼓励（Level I）
- 提供开源基准测试平台 safe-control-gym，促进跨社区公平比较
- 综述三大类方法：学习不确定动力学以安全提升性能、鼓励RL中的安全或鲁棒性、形式化认证学习控制策略的安全性

## 方法论
- 将安全学习控制问题建模为离散时间系统 x_{k+1} = f_k(x_k, u_k, w_k)，包含状态约束、输入约束和稳定性保证
- 按model-driven（控制论）、data-driven（RL）、combined approaches三个维度组织文献
- 涵盖Gaussian Process动力学学习、robust MPC、Lyapunov稳定性、CBF安全滤波、constrained policy optimization等具体技术
