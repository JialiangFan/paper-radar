# Neuro-Symbolic RL with First-Order Logic

## 主题
First-Order Logic RL

## 背景
Deep reinforcement learning 在文本游戏、机器人控制等领域取得了成功，但通常需要大量训练回合才能收敛，且训练得到的 policy 存储在黑盒神经网络中，缺乏可解释性。Logical Neural Network (LNN) 是一种新兴的 neuro-symbolic 框架，能够在可微分网络中同时实现神经网络的学习能力与符号逻辑的推理能力。本文将 LNN 引入 text-based game 的 RL 场景，通过 first-order logic 表示从文本观察中提取的事实，实现可解释且快速收敛的策略学习。

## 现有局限与研究问题
- **Limitation:** 传统 deep RL 方法（如 LSTM-DQN++）的 policy 以黑盒形式存储在神经网络中，人类无法理解、验证或修改学到的规则；同时收敛速度慢，泛化能力有限。
- **Problem:** 如何在 text-based interaction game 中，利用 first-order logic 和 neuro-symbolic 方法实现既可解释又快速收敛的 RL policy 学习？

## 贡献
- 设计并实现了一种新的 neuro-symbolic RL 方法（FOL-LNN），将 Logical Neural Network 应用于 text-based game 的策略训练
- 提出了从自然语言文本观察中提取 first-order logic facts 的算法，利用 semantic parser、agent history 和 ConceptNet 外部知识将文本转化为 FOL predicates
- 在 TextWorld CoinCollector benchmark 上的实验表明，FOL-LNN 在收敛速度上显著优于 LSTM-DQN++、NLM-DQN 等 state-of-the-art 方法，并且是唯一能提取人类可读逻辑规则的方法

## 方法论
- **问题建模：** 将 text-based game 形式化为 POMDP，agent 从文本观察中获取部分信息，action 由 verb + noun 组成（如 "go east", "take coin"）
- **FOL Converter：** 将自然语言观察文本通过 semantic parser 转为 propositional logic，再借助 ConceptNet 获取词语类别（如 "east" 属于 direction 类），将 propositional logic 提升为 first-order logic predicates（如 Find(x), Visited(x)）
- **LNN Training：** 构建 AND-OR 结构的 Logical Neural Network，第一层为所有 FOL facts，第二层为多个 AND gates，最终连接一个 OR gate；通过 DQN 式训练机制（replay buffer + reward-based loss）更新网络权重
- **规则提取：** 训练后通过设置阈值 alpha 将连续权重离散化为 True/False，从高权重连接中提取可解释的逻辑规则（如"发现未访问方向则前往该方向"）
- **评估：** 在 TextWorld CoinCollector 的 easy/medium/hard 三个难度上测试，FOL-LNN 在所有难度下均实现最快收敛和最高 reward，且成功提取了人类可理解的 action rules
