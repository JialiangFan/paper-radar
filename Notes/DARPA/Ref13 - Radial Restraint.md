# Radial Restraint: Bounded Rationality for Logic Programs

## Research Problem
How to guarantee termination and decidability of logic program evaluation under non-monotonic negation while soundly approximating the well-founded model with minimal overhead.

## 主题
Bounded rationality in logic programs

## 背景
基于 well-founded semantics (WFS) 的 declarative logic programs (LP) 广泛应用于知识表示 (KR)，包括数据库、business rules 和 semantic web 等领域。Logical functions 在 KR 中具有重要的表达能力，尤其在 SILK 项目的 Rulelog 扩展中，functions 支撑了 HiLog、defeasibility via argumentation theories 以及 omniform rules 中的 existentials 等特性。然而，当 LP 中包含 functions 时，Herbrand universe 变为无穷大，导致 LP 推理 (inferencing) 不可判定 (undecidable)，模型可能无穷，单个查询可能产生无穷多答案。

## 现有局限与研究问题
- **Limitation:** 现有实践中应对 functions 导致的不可判定性的主要方法是设置引擎参数（如 timeout 或 term-depth bound），将未在限定内推导出的 atom 视为 false。但当 atom A 的信息不完整时，若另一 atom A' 对 A 存在 negative dependency，则会导致 unsoundness。此外，推理结果依赖于具体实现代码或会话状态，缺乏声明式语义保障。
- **Problem:** 如何在 LP 中允许 functions 的使用，同时保证模型有限性 (finiteness of models)、推理可判定性 (decidability of inferencing) 以及在 non-monotonicity 存在时的 soundness？

## 贡献
- 提出 **radial restraint**：一种基于 norm 和 abstraction function 的 bounded rationality 新方法。当 term 的 norm 值超过给定 bound 时，该 term 被赋予 WFS 的第三真值 *undefined*（而非 false），从而在保持 soundness 的前提下限制推理。
- 定义了 **radially restrained well-founded model** 的 fixed-point semantics，证明其对标准 well-founded model 构成 sound approximation（Theorem 2, Corollary 1）。更弱的 abstraction function 产生更紧的近似，形成逐步逼近的模型链。
- 证明当 abstraction function 是 finitary 时，radially restrained model 的 true atoms 集合有限 (Proposition 1)，模型在有限序数处达到不动点 (Theorem 1)，从而保证推理可判定性和终止性。
- 提出 **SLG_ABS**：扩展 tabled SLG resolution 的推理方法，同时在 subgoal creation 和 answer derivation 阶段使用 abstraction。SLG_ABS 相对于 radially restrained model 是正确的 (Theorem 4)，并在 finitary abstraction 下保证终止 (Theorem 3)。
- 复杂度分析表明 SLG_ABS 的代价为 O(|subgoals(F_fin)| x size(P_Q(E)))，与已知 well-founded semantics 计算的最优复杂度一致 (Theorem 5)。
- 在 XSB Prolog (v3.3.7) 中实现了基于 depth-k abstraction 的 SLG_ABS，answer abstraction 的开销仅 0-4%，系统可扩展至 10^8 以上规模的知识库。

## 方法论
- **Norm 与 Abstraction Function 框架：** 定义 norm N(.) 为从 term 到非负整数的函数，满足空 term 映射为 0 且 subsumption 单调性。Abstraction function abs(.) 将超出 norm bound 的 subterms 替换为 position variables，使 abs(t) subsume t。典型实例为 depth-k abstraction（将深度超过 k 的 subterms 替换为变量）。
- **Radially Restrained Well-Founded Model：** 修改 dynamic stratification 的 iterated fixed-point 构造（Definition 4），在 True_I^P 和 False_I^P 算子中加入约束条件 abs(B*theta) = B*theta，仅对满足 abstraction 不变性的 ground instances 判定 true/false，其余归为 undefined。
- **SLG_ABS 推理机制：** 在 SLG 的 NEW SUBGOAL 操作中对 subgoal 施加 subgoal abstraction (Definition 7)；在 POSITIVE RETURN 操作中对 answer 施加 answer abstraction (Definition 8)，非平凡抽象的 answer 被附加 undefined_abs 标记到 Delays 中，使其永久保持 undefined 真值。NEGATIVE RETURN 扩展为支持 non-ground failed subgoals。
- **实现策略：** 在 XSB 的 SLG-WAM 引擎的 answer check/insert 步骤中维护 depth counter，当 answer 深度超过 k 时替换 subterm 为 free variable 并标记 undefined_abs。Depth-k abstraction 可按 predicate 粒度配置。
