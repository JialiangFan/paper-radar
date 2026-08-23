# UnderwaterVLA - Dual-brain VLA for Autonomous Underwater Navigation

## 主题
First VLA framework for AUVs

## 背景
自主水下航行器 (AUV) 在海底测绘、生态监测与海洋基础设施巡检等任务中不可或缺，但其自主性长期受限于强非线性 hydrodynamics、湍流与漩涡扰动、水体浊度与光照衰减、以及水下声学通信带宽受限等问题。传统 PID、自适应控制以及 reinforcement learning 等方法在非结构化海洋环境中泛化能力有限，而新兴的 Vision–Language–Action (VLA) 范式虽然在地面机械臂、自动驾驶、四足机器人和无人机领域取得突破，但在水下机器人方向几乎没有被探索。

## 现有局限与研究问题
- **Limitation:** 现有 end-to-end VLA 模型缺乏适合水下场景的 hierarchy，无法在带宽受限和算力受限条件下解耦高层任务推理与低层实时控制；同时它们是 data-hungry 的，需要大量昂贵的水下示教数据，且缺少对非线性流体动力学的实时补偿能力 (no real-time hydro-compensation)。
- **Problem:** 如何构建一个面向 AUV 的 VLA 框架，使其能够 (1) 在水声通信和算力受限的条件下保持鲁棒决策，(2) 摆脱对水下示教数据的依赖 (zero-data training)，(3) 在执行层显式补偿 hydrodynamic effects，从而在浊水和低光等真实海洋退化条件下仍能完成 language-conditioned 导航与避障任务。

## 贡献
- 提出 UnderwaterVLA，作者声称这是首个专为 AUV 设计的 VLA 框架，系统性地应对水下通信受限、感知退化与数据采集成本高昂等挑战。
- 设计 dual-brain architecture：cloud brain (QVQ-MAX-72B) 在浮出水面时进行长时程任务分解，cerebellum (Qwen 2.5-VL-7B) 在本地执行 step-wise 闭环 perception–action 控制，实现高层 deliberative reasoning 与低层 reactive control 的解耦。
- 提出 zero-data training methodology：基于预训练 multimodal foundation models 加上 underwater-specific transfer learning，避免传统 VLA 所需的大规模水下示教数据 (baseline 需要 262K 样本，本文为 0)。
- 提出 hydrodynamics-informed MPC 方案，将 added mass、二次 drag 等流体效应嵌入到离散动作执行的代价函数中，并通过 IMU 在线估计 drag 系数 (real-time fluid adaptation)。
- 在真实水池实验中相对 QUAR-VLA baseline 在 perception、basic navigation、tunnel traversal 与 obstacle avoidance 等任务上取得 +19% 至 +27% 的提升，并在低光高浊度条件下相比 single-brain end-to-end model (SBM) 表现出更强的 graceful degradation 能力。

## 方法论
- **Dual-brain 架构形式化：** 用 $\Phi_{\text{cloud}}^{\text{QVQmax}} \to \{S_1,\dots,S_N\}$ 表示 cloud brain 输出的 high-level sub-goal 序列，$\Phi_{\text{local}}^{\text{Qwen-VL}} \to \mathcal{J}_t$ 表示 cerebellum 在每个时刻输出的 JSON 控制决策；cloud brain 仅在 surfacing event 时间歇调用，cerebellum 持续运行。
- **Prompt engineering 与 CoT：** cloud brain 与 cerebellum 都被强制输出 Chain-of-Thought 推理；cerebellum 输出固定 schema 的 JSON 字段 (`reasoning`, `decision`, `velocity`, `sub_task_done`, `mission_done`)，便于日志、可解释性与失败诊断。
- **Discrete motion 离散动作集：** 离散方向 $\mathcal{D}\in\{$forward, backward, left, right$\}$ 与三档速度 $\mathcal{V}\in\{$low, medium, high$\}$，平动速度 0.2/0.5/0.8 m/s，转动 0.5/1.0/1.5 rad/s。
- **时间约束的运动剖面：** 每个动作严格在 1 秒内完成，分为 0–0.2 s 加速、0.2–0.5 s 匀速、0.5–1.0 s 减速三阶段，平动与转动分别使用对应的 $v(t)$ 与 $r(t)$ 参考曲线。
- **Hydrodynamics-informed MPC：** 优化推力 $\tau$ 以最小化 $\beta\|v-v_{\text{ref}}\|^2 + \gamma\|\tau\|^2 + \delta\|F_{\text{drag}}\|^2$ (转动模式同理用 $\theta$ 与 $\tau_{\text{drag},r}$)，其中 quadratic drag 建模为 $F_{\text{drag},v}=D_v v|v|$、$\tau_{\text{drag},r}=D_r r|r|$。
- **在线 drag 系数估计：** $\hat D_v=(\tau_v - M\dot v)/(v|v|)$、$\hat D_r=(\tau_r - I_z \dot r)/(r|r|)$，使用 IMU 测量的加速度与角加速度，无需任务特定训练数据。
- **MPC 执行循环：** 控制周期 $\delta t = 0.02$ s，依据动作类型选择 translation 或 turning 模式，求解后通过 $\mathbf u_t = \mathbf B^{\dagger}\tau_t^{*}$ 分配到 thrusters，最后用 active braking 直至 $\|v\|<0.01$ m/s 或 $|r|<0.01$ rad/s。
- **Fluid–structure interaction 阶段化处理：** 加速段补偿 added mass $M_A=\rho\nabla C_A$，匀速段补偿 quadratic drag，减速段利用自然流体阻尼实现平滑制动。
- **实验设置：** 在含三个圆柱障碍的实验水池进行 vision-guided navigation 演示；通过逐步降低照明并加入 5–200 µm diatomaceous earth，将浊度从 0.5 NTU 提升至 18 NTU (1.5 m 处对比度下降 65%)，对 dual-brain model (DBM) 与 single-brain model (SBM) 进行对比；定量指标对照 QUAR-VLA 在仿真中的报告结果。
- **局限性 (skim 时观察到的):** 实验仅在受控水池而非真实海洋中进行，定量比较的 baseline 是仿真结果而非同等真实环境下的方法，样本量较小 (例如 4/5、3/5)；此外 cloud brain 依赖云端调用，水下实际通信链路如何接入未做完整论证。
