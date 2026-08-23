# Tutorial: Safe, Secure, and Trustworthy AI via Formal Verification of Neural Networks and Autonomous CPS with NNV

## 主题
Neural Network Formal Verification

## 背景
随着 AI 和 machine learning 组件在安全关键系统中的广泛部署，确保这些组件的安全性、可靠性和可信赖性变得至关重要。深度神经网络（DNN）存在鲁棒性不足和易受 adversarial perturbation 攻击等问题，微小的输入变化可能导致截然不同的输出。Neural network verification 通过 formal methods 证明神经网络满足特定 specification，是实现 trustworthy AI 的关键途径之一。

## 现有局限与研究问题
- **Limitation:** DNN 缺乏鲁棒性，容易受到 adversarial attack 的影响；同时现有 AI 系统往往无法按预期运行，缺少形式化的安全保证。
- **Problem:** 如何对神经网络及基于神经网络控制器的 autonomous CPS（即 Neural Network Control Systems, NNCS）进行形式化验证，以证明其满足 safety 和 security specification？

## 贡献
- 提供了一个基于 NNV 工具的交互式 tutorial，系统介绍神经网络和 autonomous CPS 的 formal verification 方法
- 涵盖三个部分：(1) safe/trustworthy AI 和 neural network verification 概述讲座，(2) 基于 NNV 的神经网络验证实操，(3) 基于 NNV 的 autonomous CPS 验证实操
- 展示了来自 security（malware classification）、medicine（medical imaging）和 CPS（autonomous vehicles）领域的验证实例
- 介绍了 ONNX 模型格式和 VNN-LIB specification language 等新兴标准

## 方法论
- 基于 reachability analysis 的 formal verification：将神经网络表示为函数 f: R^n -> R^m，对输入空间子集 X 计算输出集合 Y = f(X)（精确或过近似），然后检查不期望行为集合 B 与 f(X) 是否有交集
- 使用 NNV 工具实现自动化验证，支持多种网络类型（FFNN、CNN、语义分割网络等）
- 对于 autonomous CPS，将神经网络作为闭环系统中的 feedback controller，结合 plant model（ODE 或 hybrid automata）进行 reachability analysis
- 通过评估 targeted 和 random adversarial attack 下的鲁棒性来验证神经网络的安全属性
- 提供了设计指导建议，如最小化 ReLU 层数和 ReLU 神经元总数以降低分析复杂度
