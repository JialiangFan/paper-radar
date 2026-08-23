# Tutorial: Neural Network and Autonomous Cyber-Physical Systems Formal Verification for Trustworthy AI and Safe Autonomy

## 主题
Neural Network CPS Verification

## 背景
深度学习模型在安全关键应用中的使用日益增多，需要对系统行为进行 formal analysis，包括对单个组件（如 controller robustness）以及组件间交互和整体系统效果的推理。NNV（Neural Network Verification）是一款支持多种深度学习模型验证的软件工具，其核心是 reachability algorithm 和多种集合表示方法（如 star sets、polytopes、zonotopes、ImageStars）。近年来，neural network verification 领域不断成熟，已形成 VNN-COMP 和 ARCH-COMP AINNCS 等竞赛以及 ONNX、VNN-LIB 等标准格式。

## 现有局限与研究问题
- **Limitation:** 安全关键 CPS 中越来越多地使用 ML 组件，但缺乏对这些组件和整体系统行为的形式化安全保证；现有验证方法在可扩展性和支持的网络类型方面仍有局限。
- **Problem:** 如何对多种类型的神经网络（CNN、RNN、SSNN、BNN、Neural ODE 等）及基于神经网络的闭环控制系统（NNCS）进行形式化验证，以确保 trustworthy AI 和 safe autonomy？

## 贡献
- 提供半天交互式 tutorial，系统展示 NNV 工具在神经网络和 autonomous CPS 验证中的能力
- 涵盖广泛的网络类型验证：FFNN、CNN、RNN、Semantic Segmentation NN、Binary NN、Neural ODE 以及 NNCS
- 展示了 aerospace、automotive 和 maritime 等多个领域的安全关键应用验证实例
- NNV 工具已被 AFRL、Collins Aerospace、Northrop Grumman、General Motors、Toyota 等工业界机构采用
- 支持通过 CodeOcean 等平台进行浏览器内执行，便于交互式演示

## 方法论
- 基于 reachability analysis 的验证方法，使用 star sets、polytopes、zonotopes 和 ImageStars 等集合表示计算精确和过近似 reachable sets
- 对 open-loop 神经网络进行 safety 和 robustness 验证，评估模型在 targeted 和 random adversarial attack 下的表现
- 对 closed-loop NNCS 进行验证：逐步展示如何加载/创建 NNCS 模型、定义 specification、计算 reachable sets，并给出验证证明或反例
- 结合 Matlab/Simulink 的 model-based design flow，适配嵌入式系统和 CPS 的典型开发流程
- 通过 DARPA Assured Autonomy、ANSR 及 NSF Safe Learning-Enabled Systems 等项目中的实际用例展示方法的有效性
