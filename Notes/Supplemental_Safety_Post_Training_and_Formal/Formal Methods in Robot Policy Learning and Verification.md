---
imported_title: "Formal Methods in Robot Policy Learning and Verification"
imported_from: "/Users/jfan/ND/看论文/robotic-safety/papers/Formal Methods in Robot Policy Learning and Verification.md"
imported_reason: "Supports formal verification and runtime assurance framing."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Formal Methods in Robot Policy Learning and Verification: A Survey on Current Techniques and Future Directions

## 主题
Formal Methods Robot Policy

## 背景
深度学习驱动的机器人策略（参数化为深度神经网络）在操作、导航等任务中取得了显著进展，但这些策略缺乏可解释性、对OOD场景泛化差、易受对抗输入攻击。在安全关键场景下，这些弱点可能导致灾难性后果。

## 现有局限与研究问题
- **Limitation:** 传统的reward functions或行为示范缺乏形式化安全规约的表达力，无法简洁地定义复杂、组合性、时间扩展的行为要求
- **Problem:** 形式化方法如何被开发和适配，以指导DL-based机器人策略的学习过程并验证已学策略的正确性？

## 贡献
- 首篇专注于FM与DL-based机器人策略学习交叉领域的综述（TMLR 2025）
- 围绕两大支柱组织：FM-informed policy learning (phi -> pi) 和 policy verification (pi |= phi)
- 涵盖RL with Formal Specifications、Imitation Learning with FS、Offline RL with FS
- 验证方面涵盖Environment-Abstractions、Reachability Analysis、Certificate Functions、Runtime Monitoring & Falsification
- 识别关键gap和未来方向

## 方法论
- 基于三阶段流程图：Formal Methods (Temporal Logic/Automata, Program Synthesis, Program Verification) -> Policy Learning -> Policy Verification
- Policy Learning with FM：使用LTL/STL作为reward shaping信号或约束规约
- Policy Verification：通过环境抽象、可达性分析、证书函数（Lyapunov/CBF）、运行时监控验证策略合规性
- 讨论FM在基础模型时代（VLA/VLM）的适用性和挑战
