# Ergo: A Quest for Declarativity in Logic Programming

## Research Problem
How to maximize declarativity in logic programming by eliminating Prolog's procedural pitfalls (negation ambiguity, cut dependency) through Well-Founded Semantics and explicit quantification.

## Topic
Declarative Logic Programming System

## Background
Declarativity -- the alignment between a program's declarative semantics (what a program means) and its operational semantics (how it derives results) -- has been a central quest in Logic Programming (LP) since its inception. Ergo is a higher-level logic programming system developed by Coherent Knowledge Systems as a successor to Flora-2, compiled into XSB Prolog, and distributed as part of the open-source ErgoAI suite. From its design inception, Ergo has been built with the explicit goal of maximizing declarativity and usability, integrating research advances including HiLog, F-logic, Well-Founded Semantics (WFS), and Transaction Logic. It has been deployed in commercial and research applications spanning financial compliance, legal reasoning, healthcare, and battlefield assessment.

## Limitations & Research Problem
- **Limitation 1:** Prolog's core execution strategy, SLDNF, provides insufficient declarativity -- program semantics are highly sensitive to subgoal ordering and the syntactic placement of negation, making termination and correctness difficult to guarantee.
- **Limitation 2:** The syntax for negation in Prolog-based systems lacks explicit quantifiers, rendering the precise meaning of well-founded negation opaque to users. Operators such as `tnot` and `not_exists` exhibit context-dependent, non-declarative semantics.
- **Limitation 3:** Managing rule conflicts through layered negation (encoding exceptions to exceptions) scales poorly, becoming intractable as the number of interacting rules grows in real-world domains such as tax codes and financial regulations.
- **Problem:** How can one build a truly declarative LP system within the resolution-based computational paradigm that enables programming at a high conceptual level while ensuring termination, explainability, and knowledge consistency?

## Contributions
- Designed and implemented Ergo with Well-Founded Semantics (WFS) as the default core semantics, substantially expanding the class of terminating programs beyond SLDNF (subsuming all of Datalog and beyond).
- Introduced subgoal abstraction and answer abstraction mechanisms (collectively termed "restraint") that provide informationally sound approximations for programs with infinite models, enabling a declarative form of bounded rationality for termination control.
- Supported Transaction Logic for fully semantic update operations (transactional insert/delete with integrity constraints), along with both reactive and passive modes for responding to data changes, leveraging XSB's incremental tabling for correctness.
- Introduced explicit quantifiers (`\exist`, `\forall`) and delay quantifiers (`wish/1`, `must/1`) that eliminate the ambiguity of Prolog's negation semantics and support automatic delayed evaluation of unbound variables.
- Implemented defeasible reasoning based on Logic Programming with Defaults and Argumentation Theories (LPDA), supporting multiple argumentation theories with rule tagging, overriding relations, and `\opposes` declarations for principled conflict resolution.
- Provided automatic explainability: every query answer is accompanied by a complete justification in natural deduction style, rendered as a directed graph or collapsible tree, with NLP template-based generation of natural language explanations.
- Enabled bidirectional interoperability with Python, SQL, RDF/OWL, RESTful Web services, and data connectors for JSON, XML, HTML, and other common formats.

## Methodology
- **Core Semantics:** Adopted Well-Founded Semantics (WFS) as the default execution semantics (in contrast to Prolog's SLDNF), using tabling to ensure termination and logical soundness. Systems of this kind are termed WFS-based Logic Programming (WFSLP).
- **Syntactic Foundation:** The core syntax combines HiLog (syntactically higher-order predicate terms enabling meta-programming) and F-logic frames (object-oriented frame representation supporting classes, inheritance, and complex objects), raising the level of abstraction and declarativity.
- **Termination Control:** Subgoal abstraction (bounding subgoal depth) and answer abstraction (bounding answer term depth) provide bounded rationality guarantees. A complementary tripwires mechanism supports debugging and resource-limit enforcement.
- **Defeasible Reasoning:** Built on the LPDA framework, rules are assigned tags and organized via overriding/priority relations and `\opposes` constraints, enabling argumentation-based conflict resolution with support for defeat, rebuttal, and refutation.
- **Transactionality and Reactivity:** Transaction Logic provides semantically complete transactional updates (`t_insert`/`t_delete`) with integrity constraints. In reactive mode, changes to underlying data automatically trigger incremental updates to dependent tables via XSB's incremental tabling.
- **Explainability:** Automatic generation of natural deduction-style proof graphs (directed graphs / collapsible trees), combined with NLP templates that map logical derivations to natural language explanations.
- **Empirical Validation:** The system was validated on two real-world applications: U.S. Internal Revenue Code Section 162 (tax deductibility of business expenses) and Regulation W (Federal Reserve banking compliance), demonstrating defeasible reasoning, object-oriented modeling, and explainability in practice.
