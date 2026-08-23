# Learning Control Barrier Functions and their Application in Reinforcement Learning: A Survey

## 主题
Learning CBF for Safe RL

## 背景
在现代机器人学中，设计能在复杂动态环境中安全运行的自主系统是核心挑战。CBF因其计算效率和在安全集前向不变性方面的保证而受到广泛关注，但手工设计CBF需要大量领域知识且难以泛化。

## 现有局限与研究问题
- **Limitation:** 基本CBF方法是model-based的，需要先验系统模型知识；手工crafting编码安全的CBF对复杂应用来说困难且缺乏可扩展性
- **Problem:** 如何从数据中自动学习CBF，使其更适合与RL集成应用于实际机器人场景？

## 贡献
- 全面综述CBF在安全强化学习中的应用，涵盖soft constraints、hard constraints和probabilistic constraints三类
- 系统梳理从数据中学习CBF的方法，包括从专家示范学习和CBF增强方法
- 分析model-based、data-driven和mixed approaches在保守性-灵活性谱系上的trade-off
- 讨论各方法的局限性，包括sim-to-real gap对CBF安全保证的影响

## 方法论
- 基于Zeroing CBF (ZCBF)定义：L_f h(x) + L_g h(x)u >= -alpha(h(x))
- CBF-QP框架：min ||u - k(x)||^2 s.t. CBF constraint，实现最小干预安全控制
- 安全滤波器：通过"shield"过滤RL策略的不安全动作
- 从示范中学习CBF：使用GP、SVM、神经网络等方法从数据中拟合barrier function
