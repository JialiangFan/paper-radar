# Quantitative Verification for Temporal Properties of Massive Linear Systems

## 主题
Massive linear systems quantitative verification

## 背景
线性时不变（LTI）系统的验证是确保航空航天、汽车控制和信号处理等领域工程系统安全可靠的关键任务。传统的 reachability analysis 方法主要面向 qualitative verification，提供 YES/NO 的二值结果，但无法量化系统满足时序性质的概率。对于大规模离散时间 LTI 系统，计算矩阵指数 $e^{At}$ 在高维情况下面临计算和内存爆炸问题，现有方法难以扩展到数千维以上。

## 现有局限与研究问题
- **Limitation:** 现有工具（如 Hylaa）仅支持 qualitative verification（不变性质检查），无法进行 quantitative verification 以计算满足概率；直接计算矩阵指数（Taylor series / Pade approximation）在大规模系统中因内存和计算开销而不可行；缺乏能表达复杂时序性质（嵌套时序算子）并计算其满足概率的形式化框架。
- **Problem:** 如何对大规模（可达 10,000 维）离散时间 LTI 系统进行高效的 quantitative verification，使其既能验证复杂 temporal properties，又能计算精确或有界的满足概率？

## 贡献
- 提出基于 simulation 的 probabilistic reachability 方法，利用 Krylov subspace（Arnoldi 和 Lanczos 迭代）高效构建高维离散时间 LTI 系统的可达集，结合 initial/output space projection 减少模拟次数
- 利用 ProbStar 表示和 ProbStarTL 对 ProbStar signal 上的复杂时序性质进行量化分析和验证
- 在九个大规模线性系统 benchmark 上（维度从 Motor 到 MNA5 的 10,922 维）验证了方法的可扩展性和有效性，与 Hylaa 工具进行了对比

## 方法论
- **问题建模：** 聚焦于离散时间 LTI 系统 $\dot{x}(t) = Ax(t) + Bu(t)$，初始状态用 ProbStar 表示（融合 Gaussian 分布的概率 star set），定义 probabilistic reachability 和 quantitative verification 两个核心问题
- **ProbStar Temporal Logic (ProbStarTL)：** 基于离散时间 Signal Temporal Logic (DT-STL) 语法，在 ProbStar signal（可达 ProbStar 集序列）上解释时序公式，递归构造约束集合 $C(\mathcal{R}, t, \varphi)$，支持 always ($\Box$)、eventually ($\Diamond$) 和 next ($\bigcirc$) 算子
- **DNF 变换：** 将 ProbStarTL 规约转换为 Abstract DNF (ADNF) 再实例化为 Computable DNF (CDNF)，通过 inclusion-exclusion 原理计算精确满足概率（CDNF 长度 $\leq 11$ 时），否则计算近似上下界
- **Krylov Subspace 加速：** 采用 Arnoldi（通用矩阵）和 Lanczos（对称矩阵）迭代将 $n$ 维系统投影到 $k$ 维子空间（$k \ll n$），利用 $e^{At}v \approx \|v\| V_k e^{H_k t} e_1$ 近似矩阵指数，配合 a posteriori error bounds 控制精度
- **Initial/Output Space Projection：** 定义 output space $O$ 和 initial space $I$ 投影矩阵，将模拟次数从 $n$ 维降至 $\min(o, i)$ 维，当 output 维度低于 initial 维度时使用转置动力学 $A^T$ 进一步减少计算
- **评估：** 在九个 benchmark 上验证三类 ProbStarTL 规约（$\varphi_1$: eventually, $\varphi_2$: always, $\varphi_3$: 嵌套时序），系统维度从 Motor（小规模）到 MNA5（10,922 维）和 Heat3D（8,000 维），所有模型均成功完成 qualitative 和 quantitative verification，Hylaa 仅能对部分模型的 $\varphi_1$ 进行 qualitative 验证
