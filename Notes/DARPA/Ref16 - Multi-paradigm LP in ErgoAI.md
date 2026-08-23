# Multi-paradigm Logic Programming in the ErgoAI System

## Research Problem
How to unify multiple knowledge representation paradigms (F-logic, defeasible reasoning, reactive updates) in a single system with Python/LLM integration for real-world deployable reasoning.

## 主题
Multi-paradigm Knowledge Representation and Reasoning

## 背景
ErgoAI (简称 Ergo) 是由 Coherent Knowledge 开发的开源 knowledge representation and reasoning (KRR) 系统，面向在动态变化环境中对 hybrid knowledge（结构化知识与 vector embeddings 等外部知识）进行 scalable reasoning。Ergo 是 Flora-2 系统的继承者与替代品，其语言基于 HiLog (higher-order syntax) 和 Frame Logic (F-logic，支持 objects、types、inheritance)，并构建于强大的 dynamic module system 之上。与 ASP solvers 和 description logic provers 不同，Ergo 基于 Well-Founded Semantics (WFS)，具有低阶多项式 data complexity，支持 non-ground negation 的 sound evaluation，且无需 grounding。

## 现有局限与研究问题
- **Limitation:** 传统 logic programming 系统（如 Prolog、Datalog、ASP）各自在 expressiveness、scalability 或 reasoning paradigm 上存在局限——Prolog 缺乏 well-founded negation 的默认支持，ASP 需要 grounding 且 data complexity 较高，Datalog 缺乏对 unrestricted logical terms 作为 data structures 的支持。现有 KRR 系统难以在单一框架中统一 object-oriented modeling、defeasible reasoning、transactional updates 与 higher-order syntax。
- **Problem:** 如何设计一个 multi-paradigm logic programming 系统，在保持 well-founded semantics 的基础上，将 F-logic (non-monotonic inheritance)、HiLog (higher-order syntax)、defeasible reasoning (via argumentation theories)、transactional updates 以及与外部语言（Python、Prolog、C）的紧密集成统一于一体，从而支持动态变化环境中的 scalable KRR？

## 贡献
- 提出并实现了 ErgoAI 系统，将 F-logic、HiLog、defeasible reasoning、transactional updates 等多种 paradigm 统一于 Well-Founded Semantics 框架下，实现了高度 coherent 的 multi-paradigm logic programming
- 设计了强大的 dynamic module system，支持运行时模块创建、规则/数据动态加载、模块间跨调用及 encapsulation，为知识的模块化管理提供支持
- 引入 Generalized Courteous Logic Programming (GCLP) 作为默认 argumentation theory，支持 defeasible inheritance、explicit negation、rule tagging、\opposes/\overrides/\cancel 等机制，并提供多种可插拔的 argumentation theories（包括 RefuteCLP）
- 实现了基于 transaction logic 的 transactional updates 框架，确保动态环境中每次 update 的语义一致性，配合 reactive tabling 与 integrity constraints 实现自动推理更新与 alerting
- 通过 Janus interface 实现与 Python 的紧密集成，使得 Ergo 可直接使用 vector embeddings、Language Models 等外部知识源

## 方法论
- **语言基础：** 以 F-logic 为 base statements（frame formulas、class membership、subclass formulas），支持 plain/inheritable data frames、direct inheritance、overriding 与 monotonic type inheritance；以 HiLog 提供 higher-order syntax（functor/predicate 可为任意 non-ground term），通过 tr_H 变换将 HiLog 翻译为 Prolog 进行 resolution
- **模块系统：** 所有 HiLog/F-logic statements 翻译时绑定到特定 module，module symbol 仅出现于 outermost functor（如 applyMod/n）；模块可动态创建、加载、encapsulate，支持跨模块调用（@OtherMod 语法）
- **Defeasible reasoning：** 基于 GCLP argumentation theory，每条 defeasible rule 附带 tag descriptor；通过 \opposes（声明冲突）、\overrides（优先级）、\cancel（取消规则）三个 predicates 实现 defeat/rebuttal/refutation 机制；规则被 defeat 当且仅当被 refute 或 rebut 或 disqualified；语义通过 Fig. 3 的 pseudo-code 可形式化定义和验证
- **动态 KRR：** 所有 rules/facts 均为 dynamic（可 insert/delete/enable/disable）；基于 transaction logic 保证 updates 的 transactional 语义一致性；reactive tabling 在数据变化时自动更新推理结果；integrity constraints 在 updated inferences 满足指定条件时触发 alerts/actions
- **外部集成：** 通过 Janus interface 与 Python 紧密连接，可调用 Python API（如 TensorFlow Hub）加载 Language Model 并获取 vector embeddings；Prolog、C 作为 special modules 集成；编译至 XSB Prolog，利用 XSB 的 tabled evaluation 实现高效推理
