# Task-Level ILC - Dynamic Rope Manipulation

- **Title:** Learning Dynamic Rope Manipulation Using Task-Level Iterative Learning Control
- **Authors:** Krishna Suresh, Chris Atkeson
- **Venue:** arXiv preprint (arXiv:2602.21302)
- **Year:** 2026
- **Affiliations:** Carnegie Mellon University

## 主题
Task-level ILC for rope manipulation

## 背景
可变形物体（绳、布）的动态操作对机器人和人类都极具挑战，因为其自由度极高且难以精确建模。本文以"飞结"（flying knot，单手甩绳打 overhand knot）这一非平面动态绳索任务为案例，展示如何在**极少真机试验**下学会该任务，而不依赖大规模示范数据或海量仿真。

## 现有局限与研究问题
- **Limitation:** 典型 ILC（Iterative Learning Control）针对机器人**轨迹跟踪**设计，沿整条轨迹**均匀加权**误差；用于可变形物体操作时会失败。
- **Limitation:** 基于仿真的策略学习依赖大量仿真数据，且受 sim-to-real gap 影响；domain randomization 是 worst-case 鲁棒设计，会牺牲名义性能。
- **Problem:** 如何用**单次人类示范 + 一个简化绳索模型**，直接在真机上用 <10 次试验学会动态绳索操作，并能在不同绳子间迁移？

## 贡献
- 将 ILC 从"机器人状态轨迹"扩展到**被操作物体（非驱动自由度）的状态轨迹**的精化。
- 提出 **Task-Level ILC** 用于动态绳索操作，单次示范 + <10 次真机试验即可打成飞结，且能在多种绳子间迁移。
- 提出 **critical point objective**：把学习注意力聚焦到误差历史中的**关键点**（绳-绳碰撞时刻），而非沿轨迹均匀加权；实验证明这是任务成功的关键。
- 在 7 种绳子（链条、乳胶手术管、编织/加捻绳，粗 7–25mm、密度 0.013–0.5 kg/m）上做到 100% 成功率，并可在多数绳型间 2–5 次试验完成迁移。

## 方法论
- **整体框架：** Task-Level ILC 迭代循环——初始命令 u(t) 在真机执行 → 测得任务状态 x(t) → 在 critical point 处计算任务误差 → 经逆模型 M⁻¹ 映射为命令修正 Δu(t) → 更新命令。
- **Critical point objective：** 选定关键时刻 t_c（本案例为绳-绳碰撞），只最小化该点的加权误差 ‖x(t_c) − x^demo(t_c)‖²_Q，而非整条轨迹积分误差；避免碰撞前后自由绳段误差干扰学习。
- **命令参数化：** 前馈命令用 10 条 Bézier 曲线（7 关节 + 3 基座平移维）、每条 8 个 knot points 表示，大幅降维（O(N) 参数）；base-translation 约束保证任务目标的平移不变性。
- **逆模型（optimization-based inverse model）：** 构造 QP，最小化二次任务目标同时满足线性化动力学约束 Δx=MΔκ 及关节位置/速度/加速度/力矩上下限；用 Drake + Clarabel 求解，返回命令修正 Δκ*。
- **模型：** 机器人建为运动学链（100:1 减速比，绳对机器人动力学影响可忽略）；绳建为 3D 点质量串联链（11 段，末端加配重），用 maximal-coordinate 变分积分器仿真。
- **实验设置：** xArm 7 机械臂，250Hz；Vicon Vantage 16 动捕跟踪绳上 11 个反光标记；与两个基线对比——直接跟踪人手运动、均匀加权 ILC 学绳运动；40 次试验测成功率；评估跨绳型迁移与对模型参数（刚度、末端质量）的鲁棒性。
