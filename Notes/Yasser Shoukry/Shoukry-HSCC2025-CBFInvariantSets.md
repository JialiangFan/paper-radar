# Extracting Forward Invariant Sets from Control Barrier Functions

## 主题
从控制屏障函数中系统性提取前向不变集

## 背景
控制屏障函数（Control Barrier Functions, CBF）是保证系统安全性的主要工具之一。CBF 定义了一个安全集，通过确保系统状态始终留在该集合内来保证安全。然而，CBF 的有效性依赖于安全集确实是前向不变的（forward invariant），即系统不会离开该集合。验证和提取前向不变集是 CBF 设计中的关键步骤。

## 现有局限与研究问题
- **Limitation:** 传统 CBF 设计假设安全集是前向不变的，但缺乏系统性验证方法；Lyapunov 方法可证明不变性但通常需要保守的线性化；Sum-of-Squares (SOS) 方法适用于多项式系统但不直接支持 NN 控制器。
- **Problem:** 如何从给定的 CBF 中系统性地提取最大前向不变集，特别是在使用神经网络控制器的系统中？

## 贡献
- 提出从 CBF 中系统性提取前向不变集的算法
- 结合 NN 验证技术处理含神经网络控制器的系统
- 提供不变集的可靠内逼近（inner approximation）保证
- 适用于非线性系统和学习型控制器

## 方法论
- **CBF 安全集定义：** 给定 CBF h(x)，安全集 C = {x : h(x) ≥ 0}。前向不变性要求：对所有 x ∈ ∂C（边界），存在控制输入 u 使得 ḣ(x,u) ≥ 0
- **不变集提取：** 从 CBF 零水平集开始，通过迭代收缩找到最大前向不变子集。每次迭代移除不满足不变性条件的状态
- **NN 控制器处理：** 当控制器为神经网络时，使用 BERN-NN 验证器计算 ḣ(x, π_NN(x)) 的范围。如果对某状态 x 验证 ḣ ≥ 0 成功，则 x 属于不变集
- **内逼近算法：** 使用区间分析将状态空间网格化，对每个网格单元验证不变性条件。保留所有验证通过的单元构成不变集的内逼近
- **迭代精化：** 对边界附近的网格单元进行自适应细化，提高不变集估计的精度
- **评估：** 在二维和三维非线性系统上测试，方法成功提取比传统保守方法大 30-50% 的前向不变集

> **Title:** Extracting Forward Invariant Sets from Neural Network-Based Control Barrier Functions
> **Authors:** Goli Vaisi, James Ferlez, Yasser Shoukry
> **Venue:** ACM International Conference on Hybrid Systems: Computation and Control (HSCC 2025)
> **Year:** 2025
> **Affiliations:** University of California, Irvine