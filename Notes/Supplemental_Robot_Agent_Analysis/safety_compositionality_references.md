---
imported_title: "Safety Compositionality Failure References"
imported_from: "/Users/jfan/ND/看论文/robot_agent/safety_compositionality_references.md"
imported_reason: "Local reference list for agentic safety-compositionality examples."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Safety Compositionality Failure — 参考文献

> **术语说明**：
> "Safety compositionality failure" 是一个描述性表述，不是固定文献术语。它对应的核心假设是：
> **机器人系统中，各层局部安全约束的满足，并不足以保证全局安全约束的满足。**
>
> 这个概念在以下几条文献线索中均有讨论：
> - 形式化方法中的 compositional verification / assume-guarantee 失效
> - 控制理论中的 layered safety-critical control
> - LLM / VLA 机器人中的 cross-layer safety
> - 系统工程中的 emergent safety (STAMP)

---

## 1. 形式化方法 & Assume-Guarantee 组合失效

最接近"局部安全 ≠ 全局安全"的理论根源。

- **Programming Safe Robotics Systems: Challenges and Advances** (Desai et al.)
  P 语言的 modular assume-guarantee testing，直接讨论机器人 software stack 的组合验证。
  <https://ankushdesai.github.io/assets/papers/isolapaper.pdf>

- **A Compositional Approach to Verifying Modular Robotic Systems**
  ROS 节点之间的 FOL (first-order logic) assume-guarantee contracts。
  <https://www.researchgate.net/publication/362643591_A_Compositional_Approach_to_Verifying_Modular_Robotic_Systems>

- **Learning Assumptions for Compositional Verification**
  CAV 的经典工作，讨论 AG reasoning 中 assumption 学习的基础问题。
  <https://i-cav.org/cavlinks/wp-content/uploads/2019/07/assume-guarantee.pdf>

- **A Component-Based Approach to Hybrid Systems Safety Verification**
  针对混合系统（连续 + 离散动力学，机器人控制的典型设定）的组合验证。
  <https://link.springer.com/chapter/10.1007/978-3-319-33693-0_28>

- **A hierarchical verification approach based on STAMP**
  基于 Leveson STAMP 框架，直接论证 layered safety 不等于 component safety。**与 hypothesis 最直接对应**。
  <https://www.sciencedirect.com/science/article/pii/S0167642318304325>

---

## 2. Layered Safety-Critical Control（CBF + 分层架构）

工程落地角度，展示"低层满足但全局未必"的具体案例。

- **Learning for Layered Safety-Critical Control with Predictive CBFs** (arXiv 2412.04658)
  RoM (Reduced-order Model) / FoM (Full-order Model) 两层间 CBF gap 的典型工程化案例。
  <https://arxiv.org/abs/2412.04658>

- **Resolving Conflicting Constraints in MARL with Layered Safety** (arXiv 2505.02293)
  多 agent 强化学习下的多层安全约束冲突。
  <https://arxiv.org/html/2505.02293>

- **Guided by Guardrails: CBFs as Safety Instructors for Robotic Learning** (arXiv 2505.18858)
  CBF 作为 learning-based 机器人控制的 safety filter。
  <https://arxiv.org/html/2505.18858>

- **Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning** (Brunke et al.)
  该领域最常被引用的 survey，明确讨论分层架构下的安全组合问题。**强烈推荐作为 survey 引用。**
  <https://www.researchgate.net/publication/358158657_Safe_Learning_in_Robotics_From_Learning-Based_Control_to_Safe_Reinforcement_Learning>

---

## 3. LLM / VLA Agent 的 Cross-Layer 安全

最贴近 agentic robot 的现代设定。

- **Safe LLM-Controlled Robots with Formal Guarantees via Reachability Analysis** (arXiv 2503.03911)
  明确指出 LLM 概率输出与下层控制形式保证之间的 gap。**与 hypothesis 高度对应的近期工作。**
  <https://arxiv.org/abs/2503.03911>

- **Towards Embodied Agentic AI: Review and Classification of LLM- and VLM-Driven Robot Autonomy** (arXiv 2508.05294)
  2025 年的 survey，讨论 System 1 / System 2 双层架构（如 NVIDIA Groot N1）的安全挑战。
  <https://arxiv.org/html/2508.05294v4>

- **Vision-Language-Action Models: Concepts, Progress, Applications and Challenges** (arXiv 2505.04769)
  VLA 模型的总览 survey。
  <https://arxiv.org/html/2505.04769v1>

---

## 4. 经典系统工程理论基础

- **Leveson, N. G. — *Engineering a Safer World: Systems Thinking Applied to Safety* (MIT Press, 2011)**
  STAMP 模型的奠基著作。核心论断：
  > "Safety is an emergent system property that cannot be determined by examining components in isolation."

  **这句话基本就是 hypothesis 的原始表述**——强烈建议作为 paper 的理论基石引用。

---

## 引用策略建议

Paper 中可把该 insight 定位为三条线索的合流：

1. **Leveson 的 emergent safety 论点**（系统工程基础）
2. **Assume-Guarantee reasoning 的失效**（形式化方法基础）
3. **LLM 层概率输出 + 形式保证 gap**（机器人 agentic AI 的新场景）

前两者提供 credibility 与理论基础，第三点承载 novelty。
