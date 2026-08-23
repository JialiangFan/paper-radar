# Quantitative Verification of Learning-Enabled Systems Using ProbStar Reachability

## 主题
Probabilistic Neural Network Verification

## 背景
深度神经网络（DNN）的形式化验证对于保障 learning-enabled safety-critical autonomous systems 的安全性至关重要。现有 DNN 验证方法主要关注 qualitative verification，即判断网络是否违反安全或鲁棒性属性，返回 SAT/UNSAT 结果。然而，在实际应用中，传感器输入往往包含不可避免的噪声，可建模为 multivariate Gaussian distribution，因此需要 quantitative verification 来计算属性被违反的概率。

## 现有局限与研究问题
- **Limitation:** 现有 quantitative verification 方法大多针对 binary neural networks 或 quantized finite discrete input space，仅有一种方法针对连续输入空间的 ReLU 网络，且仅考虑椭球输入集（ellipsoidal input）。此外，系统级验证（system-level verification）仅提供 Safe/Unsafe/Unknown 等定性结果，缺乏概率量化能力。
- **Problem:** 如何在连续输入空间上对使用多种 piecewise linear activation functions（ReLU, LeakyReLU, SatLin, SatLins）的 FFNN 及闭环 Learning-Enabled Cyber-Physical Systems (Le-CPS) 进行 quantitative verification，同时计算安全属性被违反的精确概率？

## 贡献
- 提出 Probabilistic Star (ProbStar) 集合表示，将 star set 扩展为支持 truncated multivariate Gaussian distribution 的概率集合，适用于多种 piecewise linear activation functions 的量化推理
- 开发精确验证（exact verification）和过近似验证（over-approximate verification）两种算法：前者精确计算违反概率，后者通过过滤低概率路径减少计算开销
- 提出首个统一的闭环 Le-CPS 系统级方法，同时支持 qualitative 和 quantitative verification
- 基于 SVD 分解和 Gaussian approximation of Dirac Delta distribution，解决了 rank-deficient constraint matrix 下 ProbStar 概率计算问题
- 在 StarV 工具中实现并开源，在 HorizontalCAS、ACASXu、rocket landing、AEBS、adaptive cruise control 等 benchmarks 上验证有效性

## 方法论
- **ProbStar 定义：** 将 star set 与 truncated Gaussian distribution 结合，定义为元组 ⟨c, V, N, P, l, u⟩，其中谓词变量服从 Gaussian 分布 N(μ, Σ)，并受线性约束 P(α) ≜ Cα ≤ d 和上下界 l ≤ α ≤ u 约束
- **概率计算：** 对 rank-deficient constraint matrix C 使用 SVD 分解将高维空间映射到低维空间，对奇异 Gaussian 分布用 Dirac Delta 的 Gaussian 近似处理，最终调用 Genz/Botev 方法计算截断正态分布的概率
- **逐层可达性分析：** 对 FFNN 的每一层执行 affine mapping 后逐神经元处理激活函数（stepReLU/stepSatLin/stepLeakyReLU/stepSatLins），将输入 ProbStar 分裂为多个子 ProbStar 并计算各自概率
- **优化策略：** 使用 Proposition 6 的 estimated bounds 快速判断是否需要求解 LP 来获取 tight bounds，并在添加新约束后使用 domain contraction 更新谓词变量的上下界
- **Le-CPS 系统级验证：** 将 FFNN 控制器 F 与线性物理模型 x(k+1) = Ax(k) + Bu(k) 耦合，在有限时间步 k_max 内迭代传播 ProbStar reachable sets，验证安全属性 S 并计算每步满足概率 P_i
