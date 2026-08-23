# Neurosymbolic Verification of Signal Temporal Logic

- **Title:** A Neurosymbolic Approach to the Verification of Temporal Logic Properties of Learning-enabled Control Systems
- **Authors:** Navid Hashemi, Bardh Hoxha, Tomoya Yamaguchi, Danil Prokhorov, Georgios Fainekos, Jyotirmoy Deshmukh
- **Venue:** ICCPS 2023 (ACM/IEEE 14th International Conference on Cyber-Physical Systems)
- **Year:** 2023
- **Affiliations:** University of Southern California; Toyota Research Institute of North America


## 主题
将 STL 属性编码为 ReLU 神经网络，利用 NN 验证器实现时序逻辑验证

## 背景
Signal Temporal Logic (STL) 是描述信号时序行为的形式化规约语言，广泛用于 cyber-physical systems (CPS) 的安全性描述。随着神经网络控制器在 CPS 中的应用增多，需要验证闭环系统是否满足 STL 属性。然而，STL 验证工具与神经网络验证工具分属不同社区，缺乏统一的验证框架。

## 现有局限与研究问题
- **Limitation:** 传统 STL 监控器基于仿真轨迹评估，无法提供形式化保证；现有 NN 验证器（如 α,β-CROWN）仅支持输入-输出属性验证，不直接支持时序逻辑属性；两个验证社区的工具互不兼容。
- **Problem:** 如何将 STL 属性验证问题转化为标准的神经网络验证问题，从而利用高效的 NN 验证器进行时序逻辑验证？

## 贡献
- 提出将 STL 公式系统性地编码为 ReLU 神经网络的方法，STL 的 min/max 鲁棒语义自然映射为 ReLU 操作
- 构建 neurosymbolic 验证框架：将 STL 验证问题转化为等价的 NN 验证问题
- 支持利用任意 off-the-shelf NN 验证器（如 α,β-CROWN, Marabou）进行 STL 属性验证
- 在多个 CPS 基准上验证了方法的可行性和效率

## 方法论
- **STL → ReLU 编码：** STL 的鲁棒语义（robustness semantics）基于 min 和 max 操作定义。利用恒等式 max(a,b) = ReLU(a-b) + b 和 min(a,b) = -ReLU(b-a) + b，将 STL 公式的递归语义编码为 ReLU 神经网络的前向传播
- **网络构造：** 对于给定的有界时间 STL 公式和离散化轨迹，构造一个 ReLU 网络，其输入为系统轨迹（展平为向量），输出为 STL 鲁棒度值。网络深度与 STL 公式的嵌套深度成正比
- **验证流程：** (1) 用户提供 STL 规约和系统模型 (2) 将 STL 编码为 ReLU 网络 (3) 将系统模型（如神经网络控制器 + 动力学模型）与 STL 网络串联 (4) 使用 NN 验证器验证组合网络的输出是否始终为正（即 STL 满足）
- **评估：** 在 adaptive cruise control 和 mountain car 等基准上测试，证明方法可有效验证神经控制器满足 STL 规约
