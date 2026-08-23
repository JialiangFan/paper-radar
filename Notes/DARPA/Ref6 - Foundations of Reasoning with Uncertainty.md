# Foundations of Reasoning with Uncertainty via Real-Valued Logics

## Research Problem
How to provide a sound and finitely strongly complete axiomatization for reasoning over a broad class of real-valued logics, including fuzzy, probabilistic, and weighted variants.

## 主题
Real-valued logic axiomatization completeness

## 背景
Real-valued logics（真值取 [0,1] 区间的逻辑系统）自 Boole 时代即有雏形，近年因 neuro-symbolic AI 的兴起而备受关注。经典 0-1 逻辑不足以表达不确定性，而 neural network 的激活值天然对应连续真值，因此需要在 real-valued logics 上建立严格的 soundness 与 completeness 理论基础。此前已有针对特定逻辑（如 Lukasiewicz logic、Godel logic）的公理化工作，但大多局限于单一逻辑且仅处理公式真值，未涵盖公式真值的组合与交互信息。

## 现有局限与研究问题
- **Limitation:** 已有的 real-valued logic 公理化结果仅针对特定逻辑（如 Lukasiewicz、Godel），每种逻辑需要独立的公理系统；且仅能推断公式是否必然取真值 1，无法推断公式可能取到的真值集合或多个公式真值之间的组合关系。此外，soundness 和 completeness 的形式化对于大量 real-valued logics 而言尚未建立，推理能力仅被定性描述。
- **Problem:** 如何构建一个参数化的、统一的公理系统，使其对包括所有常见 fuzzy logics、weighted logics 以及 probabilistic logics 在内的广泛 real-valued logics 类别同时具备 finite-strongly complete axiomatization，并能精确推断公式真值的所有可能组合？

## 贡献
- 提出 **multidimensional sentences (MD-sentences)** 这一丰富的句子类别：形如 (sigma_1, ..., sigma_k; S)，不仅描述各公式可能的真值，还描述真值之间的交互关系（S 为 [0,1]^k 的任意子集）。
- 建立了一套仅含 **一条公理和七条推理规则** 的统一公理系统，并证明其对 MD-sentences 具备 **soundness and (finite-strongly) completeness**（Theorem 3.4）：即当有限前提集 Gamma 蕴含 gamma 时，存在从 Gamma 到 gamma 的形式证明。
- 证明 MD-sentences 类在 Boolean 组合下封闭：任意有限个 MD-sentences 的 Boolean 组合等价于单个 MD-sentence（Theorem 4.2），展示了该句子类的鲁棒性。
- 针对 Lukasiewicz logic 和 Godel logic，给出基于 **linear programming** 的判定过程 **SoCRAtic**（Sound and Complete Real-valued Axiomatic solver），在固定参数 M 下算法关于 P 和 N 多项式时间运行（Theorem 6.1）。
- 将公理系统扩展至带 **weights** 的情形（Theorem 7.1, 7.2），以及将真值解释为 **probabilities** 的情形（Theorem 8.1, 8.2），均保持 soundness and completeness。
- 实验验证 SoCRAtic 可高效处理 k-SAT 问题、Hajek tautologies 及大规模 stress test（数千 intervals），展示了实用性。

## 方法论
- **两层逻辑架构：** 内层为 real-valued logic（公式取 [0,1] 真值，含 conjunction &、disjunction ∨、implication ->、negation 等连接词）；外层为经典二值逻辑，MD-sentences 在外层取 True/False，使用标准 Boolean connectives。
- **MD-sentences 的形式化：** 句子 (sigma_1, ..., sigma_k; S) 表达"若各 sigma_i 的真值为 s_i，则 (s_1,...,s_k) 属于 S"。信息集 S 可以是 [0,1]^k 的任意子集，允许表达公式间真值的任意约束关系。
- **公理与推理规则体系：** 1 条公理（sigma; [0,1]）+ 7 条规则（包括 permutation、extension、intersection、projection、restriction 以及关键的 Rule 7——依赖具体 real-valued logic 的 good tuple 规则）。Rule 7 通过 good tuple 概念将特定逻辑的语义编码进推理系统。
- **Completeness 证明策略：** 引入 minimized sentence 概念，利用 closure under subformulas，通过 Rule 7 逐步化简，最终归结到基础句子并利用 Axiom 1 完成证明。
- **SoCRAtic 判定过程：** 将 MD-sentences 限制为 interval-based（各 S_i 为有限个 rational intervals 的并），将判定问题分解为多个 linear programming 可行性子问题；利用 MILP 中 Boolean variables 技巧与 CPLEX 求解器实现。
- **扩展至 weights 与 probabilities：** weights 情形下修改 good tuple 定义使连接词函数接受四个参数（含权重）；probabilities 情形下引入 Venn diagram 结构，添加非负性与归一化约束。
