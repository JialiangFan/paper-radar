# UnderwaterVLA: Dual-brain Vision-Language-Action Architecture for Autonomous Underwater Navigation

**arXiv:** [2509.22441](http://arxiv.org/abs/2509.22441)
**Date:** 2025-09-26
**Authors:** Zhangyuan Wang, Yunpeng Zhu, Yuqi Yan, Xiaoyuan Tian, Xinhao Shao, Meixuan Li, Weikun Li, Guangsheng Su, Weicheng Cui, Dixia Fan
**Keywords:** vision-language-action, autonomous underwater vehicle, dual-brain architecture, model predictive control, chain-of-thought reasoning

---

## 相关主题
- [[literature_review]] — 水下机器人 VLA 模型
- 与 [[USIM and U0 - A Vision-Language-Action Dataset and Model for General Underwater Robots]] 的关系：同为水下 VLA 开创性工作，但本文侧重零样本泛化与实机部署，USIM/U0 侧重大规模仿真数据集与端到端训练

## 核心创新点
首次将 Vision-Language-Action 框架应用于自主水下航行器（AUV），提出"双脑"分层架构：云端大脑（QVQmax）负责高层任务规划与链式思维推理，本地大脑（Qwen-VL）负责闭环感知-动作执行，并结合考虑水动力学的 MPC 控制器，实现零训练数据下的水下自主导航。在退化视觉条件下任务完成率比基线高 19-27%。

## 主要方法
- **云端大脑（Cloud Brain / QVQmax）**：在 AUV 上浮通信时运行，通过链式思维提示（Chain-of-Thought）将高层任务分解为有序子任务序列。例如将"导航到珊瑚礁同时避开沉船"分解为"声呐定位 -> 规划无碰撞路径 -> 传输航点"等步骤。
- **本地大脑（Local Brain / Qwen 2.5-VL-7B）**：部署在设备端，以闭环方式执行感知-动作循环。输出结构化 JSON（包含 reasoning、decision、velocity、任务完成标志），在带宽受限条件下独立运行，无需持续云端通信。
- **水动力学感知 MPC 控制器**：采用三阶段速度曲线（加速 0-0.2s、匀速 0.2-0.5s、减速 0.5-1.0s），以 50Hz 频率运行。代价函数最小化跟踪误差 + 控制量 + 阻力补偿。二次阻力模型 F_drag = D_v * v|v| 通过 IMU 在线估计阻力系数，无需预训练。
- **零样本范式**：无需水下示范数据（0 训练样本），直接利用预训练基础模型的泛化能力，对比传统方法需要约 262K 示范图像。
- **链式思维推理**：两个大脑均强制输出显式推理过程，确保决策可解释性，支持实时监控与日志记录。

## 关键发现
> 双脑分层架构在高浊度（18 NTU）退化视觉条件下显著优于单脑端到端模型。单脑模型在高浊度下会持续执行最后一个有效指令而无法重新规划，导致超调和安全边界违反；而双脑架构通过分离规划与执行有效避免了这一问题。

## 实验设置
- **实验室环境**：受控水箱，包含三个垂直圆柱形障碍物
- **退化条件测试**：独立水箱中逐步降低照明（模拟水下衰减）并注入硅藻土将浊度从 0.5 NTU 提升至 18 NTU
- **基线对比**：与 QUAR-VLA（仿真环境）的报告结果进行比较

## 结论/性能
- 字母识别任务（简单）：85% 成功率（51/60），比基线高 **+19%**
- 目标导航任务（中等）：80% 成功率（4/5），比基线高 **+20%**
- 隧道穿越任务（困难）：80% 成功率（4/5），比基线高 **+27%**
- 障碍物规避任务（困难）：60% 成功率（3/5），比基线高 **+19%**
- 零训练数据需求，利用预训练模型实现开箱即用
- 局限性：未验证长时间任务（数小时）、多智能体协作、开放海洋极端深度部署及通信长时间中断后的恢复能力
