# StarV: A Qualitative and Quantitative Verification Tool for Learning-Enabled Systems

## 主题
Learning-enabled systems verification tool

## 背景
深度学习模型在自动驾驶、机器人等安全关键领域广泛应用，但容易受到 adversarial attacks 的影响，因此对 learning-enabled systems (LES) 的 formal verification 至关重要。现有的 star-based verification 工具（如 NNV、NNENUM）主要提供 qualitative verification（SAT/UNSAT），缺乏对系统在概率不确定性下安全性的 quantitative verification 能力。StarV 是一个用 Python 开发的新一代验证工具，是 NNV（MATLAB）的继承者，首次同时支持 qualitative 和 quantitative verification。

## 现有局限与研究问题
- **Limitation:** 现有工具（NNV、NNENUM 等）仅支持 qualitative verification，无法量化系统在概率不确定性下的安全违规概率；验证深度 CNN（如 VGG16）时面临严重的内存和可扩展性问题；缺乏对 LES temporal properties 的量化验证方法。
- **Problem:** 如何构建一个统一的验证框架，同时支持 qualitative 和 quantitative verification，并能高效处理大规模神经网络和大规模线性系统的验证？

## 贡献
- 提出 SparseImageStar 和 SparseStar 数据结构，通过稀疏矩阵格式（COO/CSR）显著提升内存效率，可在本地计算机上验证 VGG16 网络在最多 3000 像素攻击下的鲁棒性，内存效率比 ImageStar 和 NNV 提升最高 18 倍
- 引入 ProbStar reachability 用于 quantitative verification，支持 ReLU、LeakyReLU、Satlin 等 piecewise linear activation functions 的精确概率安全违规计算
- 提出 ProbStar Temporal Logic (ProbStarTL) 形式化框架，首次实现对 LES temporal properties 的量化验证，支持 always 和 eventually 时序算子
- 新增 LSTM 和 GRU 网络架构支持，使用 SparseStar reachability 实现验证
- 基于 Krylov subspace 方法实现大规模线性系统（可达 10,000 维）的高效 quantitative reachability 分析

## 方法论
- **架构设计：** StarV 包含五个模块：User Interface、Parser（支持 PyTorch 和 ONNX）、Specification（Safety、Robustness、ProbStarTL）、Modeling（ODE、Hybrid Automaton）和 Engine（核心验证算法）
- **SparseImageStar：** 将 3D RGB 图像展平为稀疏矩阵列向量（COO/CSR 格式），通过 indices-shifting 技术在 feature map 层面操作，实现 SpGEMM 卷积和平均池化直接运算，避免从输入提取特征的开销
- **ProbStar Reachability：** ProbStar 是传统 star set 的扩展，通过 affine mapping of truncated multivariate Gaussian distribution 建模概率输入，逐层传播通过网络构建可达输出集（ProbStar 的并集），支持 exact 和 over-approximate 两种验证模式
- **ProbStarTL Verification：** 基于 ProbStar signal（有界时间 ProbStar 可达集序列），将用户定义的时序规约转换为 Abstract Disjunctive Normal Form (ADNF)，再实例化为 Computable DNF (CDNF)，通过 inclusion-exclusion 原理计算满足概率
- **大规模线性系统：** 利用 Krylov subspace 方法（Arnoldi/Lanczos 迭代）高效近似矩阵指数 $e^{At}$，结合 initial/output space projection 减少计算维度
- **评估：** 在 MNIST LSTM/GRU、VGG16 CNN、ACASXu 网络和 Le-ACC 控制系统上进行验证实验，SparseImageStar 在 MNIST CNN 上比 NNV 快最高 8.45 倍，ProbStarTL 在 Le-ACC 上比 NeuroSymbolic 方法显著更快
