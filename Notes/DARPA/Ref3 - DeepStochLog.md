# DeepStochLog: 神经随机逻辑编程

## Research Problem
How to build a scalable neural-symbolic framework using stochastic definite clause grammars instead of possible-world semantics, achieving orders-of-magnitude faster inference than PLP-based approaches.

> Winters, T., Marra, G., Manhaeve, R., & De Raedt, L. (2022). DeepStochLog: Neural Stochastic Logic Programming. *The Thirty-Sixth AAAI Conference on Artificial Intelligence (AAAI-22)*.

## 主题
Neural Stochastic Logic Programming

## 背景
神经符号学习方法（如 DeepProbLog）将概率逻辑程序与神经谓词结合，允许端到端训练。然而，这些基于概率逻辑编程（PLP）的方法采用可能世界语义（distribution semantics），需要在所有可能世界上求和来计算查询概率，推理计算代价高昂，限制了可扩展性。与此同时，随机逻辑编程（SLP）基于随机文法语义，将推理视为随机游走（random walk）过程而非对可能世界的枚举，计算效率更高。DeepStochLog 提出基于随机定子句文法（Stochastic DCG）的神经符号框架，作为 PLP 方法的高效替代。

## 现有局限与研究问题
- **Limitation 1:** 基于可能世界语义的神经 PLP 方法（如 DeepProbLog、NeurASP）推理需要枚举可能世界并进行加权模型计数，随着程序规模增大计算代价急剧增加，在大规模问题（如多位数加法、长表达式）上容易超时。
- **Limitation 2:** 现有 SLP 方法（如 Tensorlog）虽然计算效率高，但仅限于 Datalog 和二元谓词，表达能力不足，且未应用于子符号数据（如图像）。
- **Limitation 3:** 神经文法方法（如 Neural Grammars）限于上下文无关文法（CFG），不支持基于合一的上下文敏感文法，且不处理子符号输入。
- **Problem:** 如何设计一个基于随机文法语义（而非可能世界语义）的神经符号框架，在保持表达能力（支持上下文敏感文法和通用逻辑程序）的同时，实现比 PLP 方法显著更好的推理和学习可扩展性？

## 贡献
- 提出 DeepStochLog，基于**随机定子句文法（Stochastic DCG）**引入**神经文法规则（neural definite clause grammar rules）**，将神经网络封装为文法规则中的概率产生器。
- 推理基于 **SLG 解析（tabling）**构建 AND-OR 电路，再通过 (+, ×) 半环自底向上计算概率。SLG 解析（相当于 CFG 的 CYK 算法的推广）通过缓存避免重复推导，使 AND-OR 电路成为 AND-OR 森林，大幅提升效率。
- 学习通过**梯度下降**直接在 AND-OR 电路上反向传播，等价于 EM 算法的 inside-outside 过程，但无需为每种文法形式化单独设计 outside 算法。
- 在 6 项任务上达到或超越 SOTA：MNIST 加法（T1）、手写公式（T2）、良构括号（T3）、上下文敏感文法（T4）、引文网络半监督分类（T5）、自然语言数学应用题（T6）。
- 比 DeepProbLog 和 NeurASP 快数个数量级：在 MNIST 加法 4 位数时，DeepStochLog 推理仅需 5.7ms，而 DeepProbLog 和 NeurASP 均超时。

## 方法论
- **语言设计：** DeepStochLog 程序是扩展的随机 DCG（SDCG），额外支持神经定子句文法规则。神经规则形如 `nn(m, I, O, D) :: nt → g₁, ..., gₙ`，其中 `m` 标识神经网络，I 为输入变量，O 为输出变量，D 为输出域。神经网络定义了输出变量在给定输入条件下的概率分布，类似条件 PCFG。空产生式（ε-production）允许在不消耗序列元素的情况下做概率决策，使 DCG 能表达超越纯文法的通用逻辑程序。
- **逻辑推理：** 给定目标 G 和终端序列 T，使用 SLD 解析（或 SLG 解析实现 tabling）找到所有推导，构建 AND-OR 电路。SLG 解析通过制表缓存子目标的答案，避免重复证明相同子目标，将 SLD 推导树转化为 AND-OR 森林。
- **概率推理：** AND-OR 电路编译为算术电路（将 AND 节点替换为乘法、OR 节点替换为加法），使用 (+, ×) 半环自底向上求值计算 P(derives(G,T))。最可能推导通过 (max, ×) 半环求得。
- **学习：** 目标为最小化可微损失函数 L(P(derives(G_iθ_i, T_i)), t_i)。算术电路的计算图天然可微，梯度通过反向传播自动计算。当损失为负对数似然时，梯度下降等价于 EM 的 inside-outside 算法。使用 Adam 优化器。
- **实验任务：**
  - **T1（MNIST 加法）：** 训练 1-4 位数加法。DSL 在 4 位数时仍达 92.7%（DPL/NA 超时）。推理时间：4 位数 DSL 5.7ms vs DPL/NA 超时。
  - **T2（手写公式 HWF）：** 识别手写数字和运算符组成的数学表达式。表达式长度 1-7，DSL 在长度 7 时达 94.8%（DPL 超时，NGS 20.4%）。
  - **T3（良构括号）：** 识别 MNIST 图像序列是否为良构括号。DSL 与 DPL 均达 ~100%，但 DSL 在更长序列上更准确。
  - **T4（上下文敏感文法 aⁿbⁿcⁿ）：** DCG 支持上下文敏感文法。DSL 在长度 3-18 时达 98.8%（DPL 超时）。
  - **T5（引文网络半监督分类）：** Cora/Citeseer 数据集。DSL 达 69.4%/65.0%，DPL 超时，与专用方法可比。
  - **T6（自然语言数学应用题 WAP）：** 300 训练样本，DSL 与 DPL 均达 ~94-95%。
  - Tabling 对效率至关重要：HWF 长度 11 时，无 tabling 需 1996 秒，有 tabling 仅需 132 秒。
