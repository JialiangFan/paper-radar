# MAESTRO: Orchestrating Robotics Modules with Vision-Language Models for Zero-Shot Generalist Robots

> arXiv: 2511.00917 | 年份: 2025

## 主题
VLM-orchestrated modular zero-shot manipulation

## 背景
当前通往通才机器人的主流路线是采集海量「observations-in actions-out」遥操作数据，训练端到端的 vision-language-action (VLA) 模型，复刻 VLM 的规模化配方。本文走另一条路：不训练新策略，而是直接围绕现成 VLM 构建通才策略——把机器人专有能力封装成一组精心策划的 perception、planning、control 模块，由一个 VLM coding agent 动态组合成针对当前任务与场景的 programmatic policy。该思路属于 code-as-policies (CaP) 谱系，但作者主张此前 CaP 系统的瓶颈不在 VLM 本身，而在工具库过窄与人工强加的结构约束。

## 现有局限与研究问题
- **Limitation:** 端到端 VLA 依赖昂贵的大规模真机遥操作数据，训练分布以 pick-and-place 为主，在 open cabinet、rotate cube 等 out-of-distribution 任务上进展接近于零，且缺乏显式 memory 机制；同时牺牲了模块化系统天然具备的 interpretability、debuggability 与 extensibility。
- **Limitation:** 既有 CaP 工作要么是 open-loop 静态程序（无法响应执行中的意外），要么工具集受限于 pick-and-place 与简单对称物体；即便是闭环的 Gemini Robotics 1.5，其 CaP 版本性能仍显著落后于同源的 VLA 模型。此外这些流水线中大模型只自动化了很小一部分，其余仍靠人工设计的刚性 workflow，难以泛化到 in-the-wild 场景。
- **Problem:** 在完全不使用机器人训练数据的前提下，能否通过「扩大工具集广度与质量 + 剥离人工 workflow 约束」，让 VLM agent 在具挑战性的操作技能上零样本匹敌甚至超越 SOTA VLA，并可低成本迁移到新本体？

## 贡献
- 提出 MAESTRO（Managerial Agent for Executing Sensorimotor Tasks in RObotics）：一个 VLM 驱动的 agentic 框架，通过编写并执行代码来编排 perception、geometry、control、learned visuomotor policies、image editing 五类模块，形成 plan-react-replan 的闭环感知—动作—学习循环，覆盖 tabletop 与 mobile 两种本体。
- 在 7 个 tabletop 与 4 个 mobile manipulation 任务上做零样本评测，7 项 tabletop 任务中 6 项显著超过 π0、π0.5 与 Gemini Robotics Agent（CaP baseline）。
- 系统性 ablation 揭示哪些设计选择最关键（advanced perception 与 geometry 模块），并说明 MAESTRO 相对既有 CaP 与 VLA 方法的增益来源。
- 提出基于历史 run 的 evolution 机制，可从少量真实试验中改进代码程序；并展示把 VLA（π0.5）本身作为可调用模块纳入工具库的混合用法。

## 方法论
- **工具库设计原则（Sec. III-A）：** (1) perception 的 "coarse-to-fine" 层级——raw sensory input（最快）→ mask centroid → VLM 选出的 task-relevant keypoints（最精确，ReKep 启发，先 Grounded-SAM 出 mask 再叠均匀点栅格由 GPT-o3 选点），让 agent 自主在速度与精度间权衡；深度用 FoundationStereo 从 RGB 估计。(2) active perception 作为「放大其他模块效果」的使能器（zoom in / look around，改善点云与关键点质量）。(3) geometry & linear algebra 模块（测距、构造向量、向量夹角/相对旋转、按角度旋转向量）为空间推理搭脚手架，弥补当前 VLM 缺乏可靠 spatial chain-of-thought 的短板。(4) 快推理 VLM monitor：本地部署 Qwen2.5-VL-72B-Instruct 以 2 Hz 输出 yes/no 判断任务是否完成，用于精确中断不会自停的 VLA 执行。(5) 用 cuRobo 做点云级 collision-free motion planning。(6) semantic map 缓存已观测物体位置，支撑长时序移动操作规划。
- **闭环 plan-react-replan（Sec. III-B）：** 给定指令与图像先 plan（拆子步并生成首个子步代码）；执行后 react（读入原指令、代码输出、机器人状态与上一子步图像，判断子目标是否达成）；成功则继续 plan 下一子步，失败则 replan（诊断失败原因并为同一子步重写代码）。移动场景下在失败分析前还会被提示主动环视以建立更完整的态势理解。
- **Evolution（Sec. III-C）：** 数据库记录所有历史执行的生成代码、stdout 及 Gemini 对执行视频的成败分析；新 run 前把这些累积记录作为 in-context examples 提供给 Gemini，从过往成败中改进代码生成。
- **模块清单：** control 为 move gripper to / open / close gripper 的简单笛卡尔接口；learned policies 含 GraspGen 抓取模型与 π0.5 VLA；image editing 提供 draw points 与 overlay 6D poses 以增强视觉 grounding；移动端额外含 Faster-LIO 做 6D 状态估计、Nav2 导航、细粒度 nudge 微调工具、look left/right/ground、view carry-on basket、remember object location 与 put in basket。

## 实验与关键数字
- **设置：** VLM 用 Gemini Robotics-ER 1.5；tabletop 平台沿用 DROID（7-DoF Franka Emika Panda + Robotiq 2F 夹爪，腕部相机 + 第三人称相机）；移动平台为 Unitree Go2-W 轮式四足 + 顶部 AgileX PiPER 机械臂 + 标定腕部相机。共 7 个 tabletop、4 个 mobile 任务。评测遵循 STAR-Gen 泛化分类法，沿 visual changes / object poses / action verbs / 全新物体四轴扰动，每个任务 5 次试验（1 次初始设置 + 4 次 STAR-Gen 生成），所有方法共用同一组固定试验；指标为 0–100 的 task progress 分数（按可验证子步分解）。
- **Baselines：** Gemini Robotics Agent（用 Gemini Robotics-ER 1.5 复现 Gemini Robotics 技术报告的 CaP 方案）、π0（π0-FAST-DROID 检查点）、π0.5（π0.5-DROID 检查点）。
- **Tabletop（Table II，Gemini Robotics Agent / π0 / π0.5 / MAESTRO）：** Put item in bowl 73.3±46.2 / 74.0±37.1 / 70.0±41.1 / **98.0±4.5**；Fold four corners of towel 40.0±17.3 / 47.0±25.1 / 70.0±15.4 / **71.3±21.4**；Open cabinet 3.3±5.8 / 8.3±2.9 / 0.0±0.0 / **68.0±31.3**；Rotate cube purple side up 23.6±3.5 / 29.0±1.7 / 10.0±0.0 / **60.0±38.1**；Cut banana with knife 71.0±28.8 / 30.0±23.9 / 14.0±6.5 / **92.0±5.7**；Hang mug on mug holder 46.0±23.2 / 59.0±30.7 / **80.0±14.1** / 69.0±9.6（唯一落后项）；Erase whiteboard then stack cups 26.7±24.7 / 12.0±12.0 / 22.0±22.8 / **63.0±16.8**。
- **Mobile（Table III，仅 MAESTRO）：** Collect all toys on table 85.0±22.4；Throw green ball into garbage can 76.7±14.9；Search item and put on table 96.0±8.9；Press button to open door 93.3±14.9。两个 long-horizon 任务分数偏低源于多阶段物体交互；throwing trash 的 76.7 主要受垃圾桶深度估计不准导致抓取位姿违反 IK 约束、以及无碰撞路径缺失时反应式 replanning 进入振荡循环所限。
- **Ablation（Table IV，Fold Towel / Rotate Cube）：** MAESTRO 71.3±21.4 / 60.0±38.1；w/o advanced perception 40.0±7.1 / 25.0±0.0；w/o geometry modules 67.5±3.5 / 42.5±31.8。说明 advanced perception 对定位毛巾四角至关重要，geometry 模块对基于关键点构造向量、计算旋转不可或缺。
- **Evolution：** 以 open-cabinet 中最差的一次 run（仅 35% progress，识别出把手但用了失败的 top-down grasp）为起点，一次进化更新后改为环视把手并调用 grasp model，成功抓住但仍沿直线而非旋转轴拉动，达到 70.0±5.0；第三次进化用把手与铰链关键点构造向量算出正确旋转并施加，达到 85.0±7.4。
- **已知局限：** 需要对 object affordance 与空间朝向做复杂 chain-of-thought 时仍会失败（如 hang mug 未能对齐把手孔与挂杆）；相比端到端 VLA 有更高延迟与计算开销，VLM API 响应时间在 react/replan 时引入停顿；作者视其为随 VLM 推理优化、模型蒸馏与高效代码生成而缓解的过渡性限制。
