# Ergo: A Quest for Declarativity in Logic Programming

## Research Problem
How to maximize declarativity in logic programming by eliminating Prolog's procedural pitfalls (negation ambiguity, cut dependency) through Well-Founded Semantics and explicit quantification.

## 主题
Declarative Logic Programming System

## 背景
Declarativity（声明性）一直是 Logic Programming（LP）领域的核心追求，即让程序的 declarative semantics（声明语义）与 operational semantics（操作语义）尽可能一致透明。Ergo 是由 Coherent Knowledge Systems 开发的高阶逻辑编程系统，作为 Flora-2 的继任者，编译到 XSB Prolog 上运行，属于开源 ErgoAI 工具套件的一部分。Ergo 从设计之初就以提升 declarativity 和 usability 为核心目标，融合了 HiLog、F-logic、Well-Founded Semantics (WFS)、Transaction Logic 等多项研究成果，已被应用于 financial compliance、legal reasoning、healthcare 及 battlefield assessment 等领域。

## 现有局限与研究问题
- **Limitation 1:** 传统 Prolog 的核心执行策略 SLDNF 缺乏充分的 declarativity——程序的语义高度依赖子目标顺序和 negation 的写法，导致 termination 和 correctness 难以保证。
- **Limitation 2:** Prolog 中 negation 的语法表达力不足，缺乏 explicit quantifiers，使得 well-founded negation 的精确含义对用户不透明；`tnot` 和 `not_exists` 等操作符的语义依赖于上下文位置，具有 non-declarative 特性。
- **Limitation 3:** 处理规则冲突时，传统方法依赖层层叠加 negation 来编码 exceptions，随着规则数量增长，复杂度急剧上升，难以维护。
- **Problem:** 如何在保持 LP resolution-based 计算范式的前提下，构建一个真正 declarative 的系统，使程序员能在较高的概念层次上编程，同时确保 termination、explainability 和 knowledge consistency？

## 贡献
- 提出并实现了基于 Well-Founded Semantics (WFS) 的逻辑编程系统 Ergo，将 WFS 作为默认核心语义，显著扩大了可保证 termination 的程序类别（涵盖所有 Datalog 程序并远超 SLDNF 的 termination class）。
- 引入 subgoal abstraction 和 answer abstraction 机制（统称 restraint），为具有无限模型的程序提供 sound approximation，实现 bounded rationality 的声明式终止控制。
- 支持 Transaction Logic，提供完全语义化的 update operations（transactional insert/delete），以及 reactive 和 passive 两种数据变更响应模式，基于 XSB 的 incremental tabling 保证正确性。
- 引入 explicit quantifiers（`\exist`、`\forall`）和 delay quantifiers（`wish/1`、`must/1`），消除 Prolog 中 negation 语义的歧义性，并支持 unbound variables 的自动延迟求值。
- 实现了基于 Logic Programming with Defaults and Argumentation Theories (LPDA) 的 defeasible reasoning，支持多种 argumentation theories，通过 rule tagging、overriding relation 和 `\opposes` 声明优雅地处理规则冲突。
- 提供自动 explainability 功能：为每个查询结果生成基于 natural deduction 风格的完整证明，支持有向图和可展开树形式的可视化，并可通过 NLP 模板自动生成自然语言解释。
- 支持与 Python、SQL、RDF/OWL、RESTful Web services 等的双向接口互操作，以及 JSON、XML、HTML 等数据格式连接器。

## 方法论
- **核心语义：** 采用 Well-Founded Semantics (WFS) 作为默认执行语义（区别于 Prolog 的 SLDNF），通过 tabling 技术确保 termination 和逻辑正确性，将该类系统称为 WFS-based Logic Programming (WFSLP)。
- **语法基础：** 核心语法融合 HiLog（高阶谓词语法，支持 syntactically higher-order terms）和 F-logic frames（面向对象的 frame 表示，支持 classes、inheritance、complex objects），提升抽象层次和 declarativity。
- **终止控制：** 通过 subgoal abstraction（限制 subgoal 最大深度）和 answer abstraction（限制 answer 的 term depth）实现 bounded rationality；同时支持 tripwires 机制用于调试和资源控制。
- **Defeasible reasoning：** 基于 LPDA 框架，通过为规则分配 tags、定义 overriding/priority 关系和 `\opposes` 约束，实现 argumentation-based 的规则冲突消解，支持 defeat、rebuttal、refutation 等多种形式。
- **Transactionality 与 Reactivity：** 基于 Transaction Logic 实现语义完备的 transactional updates（`t_insert`/`t_delete`），支持 integrity constraints；reactive 模式下数据变更自动触发依赖表的增量更新。
- **Explainability：** 自动生成 natural deduction 风格的证明图（directed graph / collapsible tree），结合 NLP 模板将逻辑推导映射为自然语言解释。
- **应用验证：** 在 U.S. Internal Revenue Code Section 162（税法费用抵扣）和 Regulation W（银行合规监管）两个实际案例中验证了系统的 defeasible reasoning、object-oriented modeling 和 explainability 能力。
