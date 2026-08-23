# ProbStar Temporal Logic for Verifying Complex Behaviors of Learning-enabled Systems

## 主题
Probabilistic Temporal Logic Verification

## 背景
Learning-enabled Systems (LES) 在安全关键领域中日益广泛应用，需要验证其在环境不确定性和对抗攻击下的正确行为。现有的形式化验证方法主要关注 open-loop 和 closed-loop LES 的安全性和鲁棒性验证，但在验证时空 (spatio-temporal) 行为和时序属性方面存在关键空白。本文提出 ProbStar Temporal Logic (ProbStarTL)，一种基于 ProbStar reachable sets 的新型时序逻辑，支持 LES 时序属性的定量验证——计算满足概率 (satisfaction probability)。

## 现有局限与研究问题
- **Limitation:** 现有 LES 验证方法主要关注安全性和鲁棒性的定性验证，无法定量地验证复杂的时序属性（如 "always" 和 "eventually" 等 temporal behaviors）；neurosymbolic 方法虽使用 STL 语法，但计算的是 robustness value 而非 satisfaction probability，不适用于涉及概率性不确定性的应用场景。
- **Problem:** 如何设计一种时序逻辑形式化方法，能够基于 ProbStar reachable sets 对 closed-loop LES 的复杂时序行为进行定量验证，精确计算时序规范的满足概率，并同时保证可靠性 (soundness) 和完备性 (completeness)？

## 贡献
- 提出 ProbStarTL 时序逻辑，具有清晰的语法和双重语义（定性 + 定量），支持 always (□) 和 eventually (◇) 等时序算子，以及满足概率的计算
- 设计 Depth-first Search (DFS) ProbStar reachability 算法，用于构建 closed-loop LES 的精确和近似 ProbStar traces (reachable set traces)
- 提出新的定量验证算法，将 ProbStarTL 规范转化为 Computable Disjunctive Normal Form (CDNF)，计算精确和近似的满足概率上下界，并引入 conservativeness 和 constitution 两个评估指标
- 基于 StarV 工具实现验证框架，在 Le-ACC (学习增强自适应巡航控制) 和 AEBS (高级紧急制动系统) 两个案例上验证有效性

## 方法论
- **ProbStarTL 定义:** 基于 DT-STL (Discrete-Time Signal Temporal Logic) 语法，将 ProbStarTL 定义在有界时间的 ProbStar signal (ProbStar trace) 序列上；递归定义约束函数 C(R, t, φ)，捕获满足时序规范的轨迹集合的符号表示
- **DNF 转换:** 将 ProbStarTL 约束公式转换为 Disjunctive Normal Form (DNF)，每个 conjunctive term 中的 literal 是 ProbStar 与半空间的交集；利用 inclusion-exclusion 原理或 max 下界近似计算 DNF 的概率
- **DFS Reachability Algorithm:** 由于 ReLU 网络控制器在每个时间步可能将一个 ProbStar 分裂为多个，采用 DFS 策略生成所有 ProbStar traces；支持 filtering probability p_f 过滤低概率 traces 以提高可扩展性
- **Quantitative Verification Algorithm:** 对每条 ProbStar trace 实例化时序规范的 CDNF，计算满足概率的上界 (ρ_max) 和下界 (ρ_min)；引入 conservativeness（衡量估计范围的紧致度）和 constitution（衡量被忽略 traces 和 CDNFs 对估计的贡献比例）两个指标
- **实验验证:** 在 Le-ACC 系统上验证了 4 组复杂时序属性（涵盖安全距离、速度跟随等），在 AEBS 系统上验证了紧急制动的时序安全属性；与 neurosymbolic 方法相比，验证速度显著更快且结果一致
