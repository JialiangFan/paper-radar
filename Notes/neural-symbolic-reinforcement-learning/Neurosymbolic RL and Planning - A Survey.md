# Neurosymbolic RL and Planning: A Survey

## 主题
Neurosymbolic RL Survey

## 背景
Neurosymbolic AI 将 neural network（connectionist AI）与 symbolic reasoning 相结合，被视为 AI 的第三次浪潮。Reinforcement Learning (RL) 作为通过奖惩机制训练 agent 在环境中最大化累积回报的范式，在 Deep RL (DRL) 的推动下取得了显著进展（如 AlphaGo、AlphaStar）。Neurosymbolic RL 将两者融合，旨在保留 DRL 强大学习能力的同时，利用 symbolic reasoning 提升策略的可解释性、可验证性与泛化能力。

## 现有局限与研究问题
- **Limitation 1:** DRL 数据效率极低（如 Rainbow DQN 需约 83 小时游戏时间才能达到人类数分钟即可达到的水平），且除少数场景外，domain-specific 算法往往优于通用 DRL。
- **Limitation 2:** DRL 模型是 black box，缺乏 interpretability 和 explainability，难以进行 formal verification，在 safety-critical 应用中存在严重隐患。
- **Limitation 3:** Symbolic AI 虽具备推理与可解释性，但无法处理大规模非结构化数据，也难以从不完整数据中泛化。
- **Problem:** 目前缺乏专门针对 Neurosymbolic AI 与 RL 交叉领域的系统性综述；现有 survey 要么聚焦 Neurosymbolic AI，要么聚焦 RL，未覆盖二者的结合。

## 贡献
- 首次对 Neurosymbolic RL 领域进行全面系统的文献综述，填补了该交叉领域的 survey 空白。
- 提出基于 neural 与 symbolic 组件在 RL 中所扮演角色的三类分类法（taxonomy）：**Learning for Reasoning**、**Reasoning for Learning** 和 **Learning-Reasoning**。
- 对每项研究的 RL 组件（state space、action space、policy module、RL algorithm）进行了系统分析与比较。
- 识别了 Neurosymbolic RL 在 robotics、gaming、question answering、safe RL 等领域的研究机遇，并梳理了 symbolic knowledge 自动生成、verification、算法设计、neural-symbolic 平衡等关键挑战。

## 方法论
- **分类框架：** 根据 D. Yu et al. 提出的三类 Neurosymbolic 系统分类，将相关工作归入三种 RL 模型：
  - **Learning for Reasoning RL model：** Neural component 作为辅助，将非结构化数据抽象为 symbolic representation，symbolic component 负责推理与动作生成。连接方式为 serial/unidirectional（neural → symbolic）。应用包括：将非结构化数据转为 symbolic representation（DSRL、SRL+CS、NSRL、Deep Symbolic Policy）、Knowledge Graph reasoning（DeepPath、MINERVA）、Verification（VIPER、REVEL）、Gaming（AlphaGo Zero）。
  - **Reasoning for Learning RL model：** Symbolic system 作为辅助，向 neural network 提供结构化知识以改善学习。连接方式为 parallel/unidirectional（symbolic → neural）。应用包括：Reward Shaping（MCTS-A、MATS-A、Buchi automaton）、Programmatic Policy Design（PROPEL、IP-PRL、PIRL）、Task Segmentation（DeepSynth）、Knowledge Initialized Model（PROLONETS）。
  - **Learning-Reasoning RL model：** Neural 与 symbolic 组件双向交互，互为输入输出，兼具学习与推理优势。连接方式为 bi-directional。应用包括：Task Segmentation（SDRL）。
- **分析维度：** 对每项工作从 neural component 类型（CNN、DNN、RNN、Transformer 等）、symbolic component 类型（First Order Logic、Decision Tree、Knowledge Graph、Programmatic Policy 等）、RL algorithm、state/action space、policy module 五个维度进行系统对比（Table III-V）。
- **机遇与挑战识别：** 总结了 Robotics and Control、Gaming RL、Intelligent Question Answering、Safe RL、Optimizing RL Parameters 五大应用机遇；梳理了 symbolic knowledge 自动生成、model verification and validation、Neurosymbolic RL algorithm 设计、neural-symbolic balancing 四大核心挑战。
