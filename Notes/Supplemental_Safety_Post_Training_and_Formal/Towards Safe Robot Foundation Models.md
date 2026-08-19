---
imported_title: "Towards Safe Robot Foundation Models"
imported_from: "/Users/jfan/ND/看论文/robotic-safety/papers/Towards Safe Robot Foundation Models.md"
imported_reason: "Directly links robot foundation models with an external safety layer."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Towards Safe Robot Foundation Models

## 主题
Safety Layer Foundation Models

## 背景
Robot Foundation Models (RFMs)如Octo、OpenVLA通过behavior cloning在大规模数据上训练，具有跨任务和环境的泛化能力。然而，当前研究聚焦泛化能力，忽视了安全这一真实部署的关键需求。BC策略可能因distribution shift在安全关键任务中产生灾难性动作。

## 现有局限与研究问题
- **Limitation:** RFMs的训练数据主要来自安全的专家示范，可能隐式地反映安全偏好，但不提供形式化安全保证；BC策略在遇到unseen观测时可能产生灾难性行为
- **Problem:** 如何为任意RFM/VLA策略添加安全保证，而无需针对安全进行额外fine-tuning？

## 贡献
- 提出可作为任何RFM最终层的安全模块，利用domain-specific知识约束动作空间
- 采用ATACOM（Acting on the Tangent space of the Constraint Manifold）算法，将动作映射到约束流形的切空间，确保安全状态转移
- 在robot air hockey任务上验证：ATACOM+Octo全程不违反安全约束，而原始Octo随训练时间增加约束违反加剧
- 安全模块独立于策略训练，不增加额外计算负担

## 方法论
- 要求1：获取系统状态s和控制仿射系统 ṡ = f(s) + G(s)a
- 要求2：安全条件定义为连续可微约束 0 >= g(x) ∈ C^1
- ATACOM构建约束配置的流形，将VLA输出的动作映射到该流形的切空间：a_safe = ψ_{G,f}(a, s, g)
- 实验：Octo策略在MuJoCo仿真和真实系统上的air hockey打击任务
