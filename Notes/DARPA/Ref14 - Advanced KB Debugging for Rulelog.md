# Advanced Knowledge Base Debugging for Rulelog

## Research Problem
How to provide systematic debugging tools for large-scale Rulelog knowledge bases, including automatic non-termination diagnosis and justification-based explanation.

## 主题
Rulelog Knowledge Base Debugging Tools

## 背景
Rulelog 是一种表达能力极强的 knowledge representation and reasoning (KRR) 逻辑语言，基于 well-founded semantics 下的 declarative logic programs (LP)，支持 higher-order logic (HiLog)、defeasibility（基于 argumentation theories）、rule cancellation/priorities、default 与 explicit negation 等特性。Rulelog 已在 Silk（基于 Flora-2/XSB 的 Java 层）和 Cyc 中实现，并与 RDF(S)、SPARQL、OWL-RL、RIF 等主流 semantic web 标准兼容。该调试方法作为 Silk 集成开发环境（Silklipse，基于 Eclipse）的一部分，旨在帮助 knowledge engineers 理解和修复复杂知识库中的推理错误与性能问题。

## 现有局限与研究问题
- **Limitation 1:** Rulelog 的高阶语法、递归语义和 defeasibility 机制使传统 Prolog 风格的交互式调试器（interactive debugger）不可行，因为 Rulelog 到 normal LP 的转换过程复杂且依赖 tabled resolution（SLG resolution）。
- **Limitation 2:** Knowledge engineers 通常精通逻辑但不一定是程序员，他们以声明式方式构建知识库时缺乏对 procedural 行为的关注，容易导致 non-termination 和性能瓶颈。
- **Problem 1 (Justification Problem):** 如何解释缺失或意外的查询结果？在 defeasibility 存在时，答案可能因规则被 defeat 而与预期不同，需要解释 why-not 和 provenance。
- **Problem 2 (Performance/Termination Problem):** 如何诊断推导过程中的 runaway computation（包括 non-termination），识别其根因（如 function symbols 导致的无限项、递归组件过大等）？

## 贡献
- 提出了一套完整的 Rulelog 知识库调试工具集，集成于 Silk/Silklipse IDE 中，覆盖 correctness、performance 和 termination 三个维度。
- **Justification 工具：** 基于 on-demand meta-rules 的 justification 机制，支持 defeasible reasoning 的解释（包括 why-not、prioritization、defeated arguments），并可自动生成英文文本摘要；通过可导航的 GUI 树形结构呈现 justification graph。
- **Table Dump 工具：** 利用 tabled LP inferencing tables 报告最频繁调用的 subgoals 和拥有最多 answers 的 subgoals，帮助定位性能瓶颈。
- **Forest Logging 工具：** 基于 XSB 的 forest log 机制记录 SLG resolution 中的 tabling events，支持对数亿条 facts 的日志进行加载与分析，包括递归组件分析（recursive component analysis）和抽象化（mode abstraction、predicate abstraction）。
- **Terminyzer：** 一种自动化 non-termination 分析工具，通过 call-sequence analysis 和 answer-flow analysis 识别导致 non-termination 的 subgoal/rule 序列，并启发式建议运行时 subgoal reordering（结合 delay quantifier `wish(ground(?X))`）来避免 runaway。
- **Restraint 机制：** 利用 Rulelog 的 bounded rationality 特性（radial restraint、skipping restraint、unsafety/unreturn restraint、anytime restraint），从语义层面限制推理深度/广度，从根本上防止 non-termination，同时保持语义健全性（soundness）。
- 提出了一套从宏观到微观的整体调试流程：先用 table dump/forest log 识别宏观瓶颈，再逐步深入到 justification 和 restraint 层面进行微观修复。

## 方法论
- **Justification（Section 2）：** 不同于先前方法（如直接转换原始规则），采用一组小型 meta-rules 在用户请求时 on-demand 调用，避免膨胀知识库；支持 argumentation theories 下的 defeasible reasoning 解释，用彩色图标标注 goal/argument/fact/priority 状态（true/false/defeated/undefeated）。
- **Trace-based Analysis（Section 3）：** (1) Table dump 通过检查 tabled inferencing tables 统计 subgoal 调用频次与 answer 数量；(2) Forest logging 利用 XSB 字节码级日志（性能开销 <20-30%）记录 SLG 操作序列，支持分析递归组件结构及 calling/called subgoal 对；(3) Terminyzer 基于 forest log 执行 call-sequence 和 answer-flow 分析，自动检测 non-termination 模式并建议 delay quantifier 重写。
- **Restraint（Section 4）：** 通过对 subgoal 的 term size 或 depth 设置上界（radius），在语义层面限制推理，超出限制的 derivations 赋予 undefined truth value；还支持 skipping（条件性跳过规则实例）、unsafety/unreturn（处理 NAF-unsafe 或外部查询失败）等变体，以及 anytime restraint（逐步增大 radius 直到时间限制）。
- **Incremental Truth Maintenance：** 利用 XSB 和 Flora-2 的增量 tabling 技术实现快速 edit-test-inspect 循环，支持知识库的交互式修订。
- **整体调试流程（Section 5）：** 查询无性能问题时直接使用 justification 工具检查答案正确性；查询出现 runaway 时，先查看 table dump 判断是否 non-termination（深度嵌套 function symbols），再用 Terminyzer 定位具体规则序列，或用 forest log 分析大型递归组件，最后结合 restraint 确保终止。
