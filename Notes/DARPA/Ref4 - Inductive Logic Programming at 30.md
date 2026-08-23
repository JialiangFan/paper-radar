# Inductive Logic Programming at 30

## Research Problem
How to learn interpretable, general logic programs from small numbers of examples by leveraging background knowledge, meta-level search, and predicate invention.

## 主题
ILP Advances and Future Directions

## 背景
Inductive Logic Programming (ILP) 是一种基于逻辑的机器学习方法，其目标是在给定训练样本和 background knowledge (BK) 的条件下归纳出一个泛化的假设（即 logic program）。与主流 ML 使用向量/张量表示数据并学习函数不同，ILP 使用 logic programs 表示数据并学习 relations。ILP 自 1991 年由 Muggleton 提出以来已有 30 年历史，本文回顾了过去十年间该领域的关键进展，涵盖 meta-level search、recursion learning、predicate invention 以及多种新技术的应用。

## 现有局限与研究问题
- **Limitation 1:** 传统 top-down 和 bottom-up 搜索方法在处理大型假设空间时效率低下；top-down 方法可能生成大量不覆盖样本的假设，bottom-up 方法则倾向于生成过长的 clauses，且难以学习 recursive programs 和支持 predicate invention。
- **Limitation 2:** 大多数 ILP 系统不支持 predicate invention (PI)，而支持 PI 的系统仍高度依赖 metarules 或用户预定义的 symbol space，难以自动发明高层概念。
- **Limitation 3:** ILP 传统上依赖领域专家手工构建的 background knowledge，获取合适的 BK 既困难又昂贵。
- **Limitation 4:** 经典系统（如 FOIL、Progol）难以从少量样本中学习 recursive programs，限制了对任意长度输入的泛化能力。
- **Problem:** 如何通过 meta-level search、recursion、predicate invention 及新技术（ASP、neural networks）突破上述瓶颈，实现更高效、更具表达力和可扩展性的归纳逻辑编程？

## 贡献
- 系统综述了 ILP 过去十年的四大核心进展：(i) meta-level search methods，(ii) recursive program learning，(iii) predicate invention，(iv) 多种新技术的融合使用。
- 对比了 old ILP（top-down/bottom-up、limited recursion、first-order hypotheses、Prolog-based）与 new ILP（meta-level search、full recursion support、ASP/higher-order/probabilistic hypotheses、Prolog+ASP+NNs）的关键差异（Table 1）。
- 明确指出 ILP 相较于主流 ML 的独特优势：data efficiency（从极少样本甚至单个样本中学习）、background knowledge 的利用、expressivity（学习 cellular automata、Petri nets、general algorithms 等复杂关系）、explainability（logic programs 天然可解释）。
- 讨论了当前局限并提出未来研究方向。

## 方法论
- **Meta-level search:** 将 ILP 学习问题编码为 meta-level logic program，将假设搜索委托给 off-the-shelf solver（如 ASP solver）。代表系统包括 ASPAL、ILASP3、Metagol 和 Popper。ILASP3 采用 counter-example-driven select-and-constrain loop；Popper 采用 generate-test-constrain 三阶段循环，从失败假设中学习约束以剪枝搜索空间。
- **Recursion:** 通过 Meta-Interpretive Learning (MIL) 引入 metarules（higher-order clause templates）来约束假设形式，使系统（如 Metagol）能够学习 recursive programs，从而从少量样本泛化到任意长度输入。关键 metarule 包括 *chain*（P(A,B) <- Q(A,C), R(C,B)）和 *tailrec*（P(A,B) <- Q(A,C), P(C,B)）。
- **Predicate invention:** 自动发明新的辅助谓词符号以降低 sample complexity、提升 predictive accuracy 和支持知识复用。方法包括：(a) placeholders（预定义符号，但需用户指定 arity）；(b) metarule-driven PI（MIL 中通过 metarule 自动链式发明谓词）；(c) pre/post-processing PI（如 CUR2LED 通过 clustering BK 发明谓词，ALPs 通过 auto-encoding 学习 latent predicates，Knorf 通过 refactoring 压缩程序）。
- **Lifelong learning:** Metagol_DF 在多任务设置中将已学程序加入 BK 以复用；Forgetgol 引入 forgetting 机制动态管理 BK 大小。
- **Hypothesis representations:** 从传统 Prolog 扩展到 Datalog（保证终止、可编码为 SAT/SMT 问题），以及 ASP、higher-order、probabilistic 表示。
