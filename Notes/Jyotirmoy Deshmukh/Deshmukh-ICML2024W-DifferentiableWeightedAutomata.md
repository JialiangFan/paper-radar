# Differentiable Weighted Automata

- **Title:** Differentiable Weighted Automata
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** ICML 2024 Workshop
- **Year:** 2024
- **Affiliations:** University of Southern California


## 主题
设计可微分的加权自动机框架，使离散符号结构能融入基于梯度的机器学习流水线

## 背景
加权自动机（weighted automata）广泛用于研究系统的定量属性、概率系统建模、文本/语音/图像处理等领域。近年来，加权自动机以reward machine的形式在强化学习任务规约中越来越流行，能对输入序列赋予定量评分。

## 现有局限与研究问题
- **Limitation:** 加权自动机的本质是离散结构（离散状态、离散转移），无法直接计算梯度，因此难以与基于梯度的优化方法（如神经网络训练）结合。现有方法要么完全放弃自动机结构，要么使用粗糙的近似。
- **Problem:** 如何系统性地设计可微分的加权自动机，使其能利用自动微分工具计算自动机输出关于输入序列的梯度？

## 贡献
- 提出系统性的可微加权自动机（differentiable weighted automata）框架
- 使加权自动机的权值计算过程可微分，支持自动微分工具的梯度计算
- 连接了形式化自动机理论与现代深度学习的可微编程范式
- 为reward machine在RL中的端到端训练奠定理论基础

## 方法论
- **松弛策略：** 将自动机的离散转移函数替换为连续/可微的软转移，使状态分布可以平滑变化而非硬切换
- **权值可微化：** 确保自动机计算的权值（输出）对输入序列可微，可通过反向传播计算梯度
- **自动微分集成：** 框架设计兼容PyTorch等自动微分工具，可直接嵌入神经网络训练流水线
- **应用场景：** 可用于RL中的可微reward shaping、时序规约的可微评估、以及自动机参数的梯度优化
