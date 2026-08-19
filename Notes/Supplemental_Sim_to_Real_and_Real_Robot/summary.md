---
imported_title: "Sim-to-Real Transfer for Robotics Summary"
imported_from: "/Users/jfan/ND/看论文/sim-to-real-transfer/summary.md"
imported_reason: "Summary note connecting sim-to-real, real-to-sim, and VLA post-training."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Sim-to-Real Transfer for Robotics — 文献调研

> 调研时间：2026-04-10
> 范围：2024-2026 年 sim-to-real 迁移相关重要工作

## 研究主题概述

Sim-to-Real Transfer 是机器人学习的核心挑战之一：在仿真中训练的策略如何有效迁移到真实机器人上。主要涉及视觉差距（渲染 vs 真实图像）、物理差距（仿真动力学 vs 真实接触/摩擦/形变）、以及状态差距（精确状态 vs 传感器噪声）。

## 论文分类

### 1. 综述 (Survey)
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| The Reality Gap in Robotics | 2025 | 2510.20808 | 全面综述，覆盖DR/real-to-sim/co-training |

### 2. 仿真平台 (Simulation Platforms)
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| Isaac Lab (NVIDIA) | 2025 | 2511.04831 | GPU加速，PhysX，Isaac Gym继任者 |
| MuJoCo Playground | 2025 | 2502.08844 | 开源，MJX，单GPU零样本迁移 |
| ManiSkill3 (SAPIEN) | 2024 | 2410.00425 | 最快GPU并行仿真，30000+ FPS |

### 3. Real-to-Sim-to-Real & 数字孪生 (Digital Twins)
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| RialTo | 2024 | 2403.03949 | 扫描真实环境构建数字孪生，inverse distillation |
| Real-is-Sim | 2025 | 2504.03597 | Gaussian Splatting动态数字孪生，60Hz同步 |

### 4. Domain Randomization 进阶
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| GoFlow | 2025 | 2502.01800 | Normalizing flow学习最优DR分布，ICML 2025 |
| Continual Domain Randomization | 2024 | 2403.12193 | 渐进式DR + 持续学习，IROS 2024 |

### 5. Sim-to-Real 灵巧操作 & 人形机器人
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| Sim-to-Real RL for Humanoid Dexterous | 2025 | 2502.20396 | 人形灵巧操作，real-to-sim调参，90%成功率 |
| Sim-and-Real Co-Training | 2025 | 2503.24361 | 仿真+真实数据混合训练，平均+38%提升 |

### 6. 系统辨识 (System Identification)
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| PACE | 2025 | 2509.06342 | 数据驱动系统辨识，腿足机器人，进化优化 |

### 7. 生成式仿真 (Generative Simulation)
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| GenSim2 | 2024 | 2410.03645 | LLM自动生成仿真任务，CoRL 2024 |

### 8. 基准测试 (Benchmarks)
| 论文 | 年份 | ArXiv | 关键词 |
|------|------|-------|--------|
| REALM | 2025 | 2512.19562 | Real-to-sim验证基准，3500+物体，评估VLA泛化 |

## 核心技术路线图

```
                        Sim-to-Real Transfer
                              |
         ┌────────────────────┼────────────────────┐
         |                    |                    |
    缩小仿真差距           直接对齐              跳过仿真
         |                    |                    |
  ┌──────┴──────┐      ┌─────┴─────┐         真机RL
  |             |      |           |         (Pi0.6 RECAP)
Domain      System   Real-to-Sim  Co-Training
Randomization  ID    Digital Twin  仿真+真实混合
(GoFlow,CDR) (PACE) (RialTo,      (Sim-and-Real)
                     Real-is-Sim)
```

## 与 VLA Post-Training 的关联

- **Sim-and-Real Co-Training** 直接回答了"VLA能否同时利用仿真和真实数据"的问题
- **仿真平台**（Isaac Lab, ManiSkill3）是 VLA-RL、RIPT-VLA 等在线RL工作的基础设施
- **Real-to-Sim** 方向（RialTo, Real-is-Sim）可能为 VLA 提供更高保真的训练环境
- **GenSim2** 的自动任务生成可用于扩展 VLA 预训练数据的多样性
- Pi0.6 RECAP 代表了"完全跳过仿真"的极端路线，与 sim-to-real 形成互补视角

## 推荐阅读优先级

1. **The Reality Gap in Robotics** — 先读综述，建立全局认知
2. **Sim-and-Real Co-Training** — 与 VLA 研究最直接相关
3. **RialTo / Real-is-Sim** — Real-to-Sim 是当前最热的新方向
4. **Isaac Lab / ManiSkill3** — 了解主流仿真基础设施
5. **GoFlow** — Domain Randomization 的最新进展
6. **GenSim2** — 生成式仿真，数据扩展新思路
