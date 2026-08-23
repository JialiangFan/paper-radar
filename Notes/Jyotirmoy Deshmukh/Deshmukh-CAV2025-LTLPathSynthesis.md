# Automatic Synthesis of Smooth Paths Satisfying Linear Temporal Logic

- **Title:** Automatic Synthesis of Smooth Infinite Horizon Paths Satisfying Linear Temporal Logic Specifications
- **Authors:** Samuel Williams, Jyotirmoy Deshmukh
- **Venue:** CAV 2025 (37th International Conference on Computer Aided Verification), LNCS 15934
- **Year:** 2025
- **Affiliations:** University of Southern California


## 主题
自动合成满足 LTL 规约的光滑路径

## 背景
运动规划中，需要合成既满足高层时序逻辑任务规约（如 LTL）又满足低层运动约束（如光滑性、曲率限制）的路径。传统方法将任务规划和运动规划分开处理，导致两层之间的不一致性和次优性。

## 现有局限与研究问题
- **Limitation:** 基于自动机的 LTL 运动规划方法产生的路径通常是分段线性的，不满足光滑性要求；基于优化的运动规划方法难以处理 LTL 这类复杂时序约束；现有联合方法计算开销过大，难以实际应用。
- **Problem:** 如何自动合成同时满足 LTL 时序规约和光滑性约束的运动路径？

## 贡献
- 提出将 LTL 规约编译为可微约束的方法，将离散逻辑约束连续化
- 设计基于优化的路径合成算法，在光滑路径空间中搜索满足 LTL 的解
- 利用 LTL → Büchi 自动机 → 引导搜索的层次化架构
- 在机器人运动规划任务中生成高质量光滑路径

## 方法论
- **LTL → 自动机：** 将 LTL 规约转换为 Büchi 自动机（或有限轨迹上的 DFA），获取接受条件的结构化表示
- **连续化编码：** 将自动机的离散状态转移编码为连续约束。使用光滑逼近函数将布尔条件转化为可微不等式约束，类似 LB4TL 的光滑语义思想
- **路径参数化：** 使用样条（spline）或贝塞尔曲线参数化路径，天然保证光滑性。路径由有限个控制点决定
- **约束优化：** 将问题形式化为：min_{控制点} 路径代价 s.t. LTL 连续约束满足 + 运动约束（碰撞避免、曲率限制等）。使用序列二次规划（SQP）或内点法求解
- **自动机引导：** 利用自动机结构进行分段优化——每个自动机状态对应路径的一个阶段，在该阶段内满足对应的局部约束，跨阶段保证转移条件
- **评估：** 在 2D/3D 导航环境中，方法生成的路径满足复杂 LTL 规约（如顺序访问、条件避障）且光滑度显著优于分段线性方法
