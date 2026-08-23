# cplint: A Suite for Probabilistic Logic Programming

## Research Problem
How to provide a comprehensive, unified probabilistic logic programming toolkit supporting exact/approximate inference, parameter/structure learning, and causal reasoning on SWI-Prolog.

> Riguzzi, F., & Azzolini, D. (2025). *cplint (4.5) - software for probabilistic logic programming*. Software documentation, Sep 12, 2025.

## 主题
Probabilistic Logic Programming Software

## 背景
Probabilistic logic programming (PLP) 将概率推理与逻辑编程相结合，为不确定性条件下的知识表示与推理提供统一框架。核心形式化语言包括 LPADs (Logic Programs with Annotated Disjunctions) 和 CP-logic，它们通过在逻辑子句的头部附加概率标注来定义 possible worlds 上的概率分布。cplint 是建立在 SWI-Prolog 之上的综合性工具套件，提供从概率推理 (inference) 到参数与结构学习 (learning) 的完整 pipeline，同时兼容 ProbLog、PRISM 和 Distributional Clauses 等多种语法。

## 现有局限与研究问题
- **Limitation:** 传统 logic programming 系统无法原生处理概率不确定性；而早期 PLP 系统（如 PRISM、ProbLog）往往仅支持离散分布或仅提供推理功能，缺乏统一的推理与学习框架，且对 continuous random variables 的支持有限。
- **Problem:** 如何在单一软件框架中同时支持离散与连续概率分布、多种推理策略（exact 与 approximate）、因果推理 (causal inference via do-calculus)、决策理论、以及参数和结构学习，并兼容多种 PLP 语法标准？

## 贡献
- 提供统一的 PLP 软件套件，集成 exact inference（基于 BDD 的 PITA 程序变换）和多种 approximate inference 方法（Monte Carlo sampling、rejection sampling、Metropolis-Hastings MCMC、Gibbs sampling、likelihood weighting、particle filtering）
- 同时支持 discrete probability distributions 和 continuous probability densities（包括 Gaussian、Beta、Gamma、Dirichlet、Poisson、Binomial 等十余种分布）
- 兼容四种 PLP 语法：LPAD/CP-logic 原生语法、ProbLog 语法、PRISM 语法和 Distributional Clauses (DC) 语法
- 提供 MPE (Most Probable Explanation)、MAP (Maximum A Posteriori) 和 Viterbi inference 能力
- 支持基于 do-calculus 的 causal inference
- 支持 decision theory（遵循 DTProbLog 语法）
- 集成三种学习算法：EMBLEM（基于 BDD 的 EM 参数学习）、SLIPCOVER（结构学习，搜索 clause space 和 theory space）、LEMUR（基于 Monte Carlo tree search 的结构学习）
- 提供 web 应用 cplint on SWISH，支持在线交互式使用与结果可视化

## 方法论
- **Exact Inference (PITA):** 将 LPAD 程序通过 program transformation 编译为包含 BDD (Binary Decision Diagram) 操作的 Prolog 程序，利用 bddem 库在 BDD 上高效计算概率；变体 PITA(IND,IND) 和 PITA(IND,EXC) 通过独立性假设加速计算
- **Approximate Inference (mcintyre):** 基于 sampling 的 program transformation 技术，通过 meta-interpreter 随机采样 possible worlds 并统计查询成功率来估计概率；支持 unconditional 和 conditional queries
- **Conditional Inference 策略:** 对离散变量支持 rejection sampling、Metropolis-Hastings MCMC 和 Gibbs sampling；对连续变量额外支持 likelihood weighting 和 particle filtering
- **Semantics:** 基于 LPAD 的 possible worlds semantics -- 通过 grounding 程序并为每个 ground clause 选择一个 head atom 来定义 world，查询概率为所有使查询为真的 worlds 的概率之和；连续变量的语义扩展基于 Borel sigma-algebra 上的 Lebesgue measure
- **Parameter Learning (EMBLEM):** 在 BDD 上直接运行 Expectation Maximization 算法，利用 BDD 的紧凑表示高效计算 expectations
- **Structure Learning (SLIPCOVER/LEMUR):** SLIPCOVER 分别搜索 clause space 和 theory space 来学习程序结构；LEMUR 使用 Monte Carlo tree search 搜索 clause space；两者均采用 Progol 风格的 language bias（mode declarations）来约束搜索空间
