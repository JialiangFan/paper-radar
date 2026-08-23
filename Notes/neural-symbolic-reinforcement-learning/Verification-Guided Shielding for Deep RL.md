# Verification-Guided Shielding for Deep RL

## 主题
Efficient Safety Shielding

## 背景
Deep Reinforcement Learning (DRL) 在解决复杂决策任务方面取得了显著成功，但其策略无法保证在所有输入下的绝对安全性，限制了在 safety-critical 场景中的部署。现有的安全保障方法主要分为两类：formal verification（离线验证策略是否安全，但无法提供替代动作）和 shielding（在线覆盖不安全动作，但需要在每个 time step 都调用 shield，带来巨大的 runtime overhead）。本文由 Corsi, Amir 等人提出 verification-guided shielding，旨在融合两者优势，在保持 formal safety guarantees 的同时显著降低 shielding 的计算开销。

## 现有局限与研究问题
- **Limitation:** 传统 shielding 方法需要在每一个 time step 都激活 shield 来检查和纠正动作，即使绝大多数情况下 agent 的决策本身是安全的（实验中 shield 实际干预不足 9%），依然导致 31x-40x 的 runtime overhead，在实时系统中不可行。同时，formal verification 虽然可以离线判定策略是否存在不安全行为，但无法在发现不安全后提供补救措施。
- **Problem:** 如何在保留 formal safety guarantees 的前提下，仅在必要时（即 agent 处于不安全输入区域时）才激活 shield，从而大幅减少运行时开销？

## 贡献
- 提出 verification-guided shielding 框架，首次将 formal verification 与 shielding 有机结合：利用 verification 划分输入空间为 safe/unsafe regions，仅在 unsafe regions 临时激活 shield
- 设计五步流水线：domain splitting（epsilon-ProVe）、formal verification（Marabou）、clustering（agglomerative clustering 压缩 unsafe regions）、symbolic representation（命题逻辑/SMT 编码）、shield synthesis and execution
- 在 Particle World 和 Mapless Navigation 两个 benchmark 上验证，runtime overhead 降低 20%-71%（相对 full shielding），同时保持与传统 shielding 相同的 formal safety guarantees
- 提供 scalability 和 completeness 的深入分析，讨论了 probabilistic guarantees（epsilon-ProVe 近似阶段）与 sound guarantees（Marabou 精确验证阶段）的互补关系

## 方法论
- **(1) Domain Splitting:** 使用 epsilon-ProVe 算法对输入域进行分割，通过构建搜索树将连续输入空间划分为近似安全和近似不安全的子区域；该算法基于采样估计安全概率，迭代细分直至满足置信度阈值
- **(2) Formal Verification of Safe Regions:** 对 epsilon-ProVe 近似为安全的区域，使用 sound and complete 的 DNN verifier Marabou 进行精确验证；若发现 counterexample（SAT），则将该区域重新标记为 unsafe，确保 safe region 的划分具有绝对正确性
- **(3) Clustering:** 针对 unsafe regions 数量庞大的问题（Particle World 中约 60,000 个），采用 agglomerative clustering 合并相邻 unsafe regions，以 overapproximation 换取更紧凑的表示；这不影响 soundness（最多导致 shield 被多激活几次）
- **(4) Symbolic Representation:** 利用 propositional logic / first-order logic modulo theories（SMT）对 unsafe regions 进行符号编码，并通过 Z3 solver 的 simplify 操作进一步化简公式，降低在线查询判断当前状态是否属于 unsafe region 的开销
- **(5) Shield Synthesis and Execution:** 基于 LTL specification 合成 shield（支持 LTL modulo theories 以处理连续域）；运行时每个 time step 仅需检查当前输入是否属于 unsafe region 的符号公式——若是则激活 shield 纠正动作，否则直接执行原始策略的输出
- **评估:** 离线阶段在 160 CPU 集群上运行，formal verification 为最耗时步骤（约 2 小时/策略）；在线阶段实验显示 shield active time 从 100% 降至 1.3%-61.7%，overhead 从 31x-40x 降至 1.5x-21.5x，gain 达 20.5%-71.1%
