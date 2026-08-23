# VLA-FAIL: Efficient Task Failure Detection for Finetuned Vision-Language-Action Models

> arXiv: 2606.21386 | 年份: 2026

## 主题
Runtime failure detection for VLAs

## 背景
Vision-language-action models (VLAs) 在机器人操作任务上已达到 SOTA，但在 out-of-distribution 场景中仍会出现不可预测的行为，即使已在下游任务上 finetune。因此，runtime failure detection 是 VLA 安全落地的前提——需要尽早发现失败以触发人工干预或 safe fallback。作者来自 KIT Autonomous Learning Robots Lab，在 π0.5 与 X-VLA 两个 VLA 上验证方法。

## 现有局限与研究问题
- **Limitation:** 现有 VLA 失败检测器存在三类硬约束：(1) 需要昂贵的 action sampling（如 ACE、Diff 使用 32 个 action samples），实时性不足；(2) 依赖特定架构假设或外部模型（VLM 推理、object-centric perception、video model），限制适用范围；(3) 监督式方法（如 SAFE）需要 failure rollouts，而采集失败数据代价高且潜在不安全。此外，单纯的 novelty-based 检测不充分：OOD 状态不必然导致任务失败，而部分失败源于内部动作生成不一致、并无明显视觉异常。
- **Problem:** 能否设计一个既不需要 failure data、不依赖外部模型、计算开销可忽略，又能在 episode 早期准确检出失败的通用 VLA runtime detector？同时，如何用一个 threshold-independent 指标同时衡量检测准确性与检测延迟？

## 贡献
- 提出 **VLA-FAIL**：轻量级 runtime failure detection 框架，融合两个互补检测器，无需 failure data 与辅助模型，计算开销极小。
- **LLMD**（last-layer token-wise Mahalanobis distance）：将 Mahalanobis OOD 检测从分类模型扩展到 flow matching VLA，通过固定 prior noise 消除随机采样引入的特征扰动。
- **ACC**（action chunk consistency）：利用 receding-horizon control 天然产生的 chunk 重叠，计算 velocity-normalized 的动作不一致度，复用已生成的动作、零额外前向。
- 提出 **AUCPDT**（area under penalized detection time curve）：threshold-independent 指标，联合评估 precision、recall 与检测时刻。
- 在 6 个真实世界任务与 Libero-Plus 仿真基准上系统验证，证明 LLMD 与 ACC 捕捉互补的失败模式。

## 方法论
- **问题设定：** 时刻 t 观测 o，VLA 预测长度 H 的 action chunk $a_{1:H}$，receding horizon 只执行前 R < H 个动作后重新推理；目标是在 episode horizon T 之前预测失败。
- **Fixed prior noise：** flow matching 专家的 last-layer feature 同时依赖观测 o、flow timestep t 与噪声动作 $a_t$。为隔离观测的影响，固定采样一个 $a_0^* \sim \mathcal{N}(0, I)$ 并在 t=0 处评估 $f^*(o) := f(o, t=0, a_0^*)$，只需一次可与 action sampling 并行的前向。
- **LLMD：** finetune 后对训练集 $\mathcal{D}$ 做一次 gradient-free 预处理，逐 token 位置 s 计算均值 $\mu_s$ 与协方差 $\Sigma_s$（数值稳定性用 $\Sigma_s + \lambda I$，$\lambda \ll 1$）。rollout 时取所有 token 位置上平方 Mahalanobis 距离的**最大值**作为分数，最大值聚合保证单个异常 feature 即可触发；无需时间平滑。
- **ACC：** 比较上一 chunk 未执行的后缀 $a^{t-1}_{R+1:H}$ 与新 chunk 前缀 $a^t_{1:H-R}$ 的逐维平均绝对误差，并用该维度的平均速度 $v_d^t$ 归一化（下限 $v_{\min}$ 防止近静止时分数虚高）。实践中只用 D=3 的预测末端执行器位置。由于成功执行中偶发 replanning 属正常，只有持续不一致才意味着失败，故施加 EMA 平滑，$\alpha = 0.9$（强平滑是取得良好检测率的必要条件）。
- **融合：** $F_{\text{FAIL}}(t) := (s^t_{\text{ACC}} \ge \tau_{\text{ACC}}) \lor (s^t_{\text{LLMD}} \ge \tau_{\text{LLMD}})$，阈值由基于 calibration data 的 time-constant conformal prediction 确定；不采用 time-dependent 阈值，因为其不适用于长度差异极大的 episode（如真实 Drawer 任务）。评估时对两路分数各做 rank transformation 后取最小值，得到 task-agnostic 的单一分类器分数。
- **AUCPDT：** 对失败 episode，PDT 定义为首次超过阈值的归一化时刻 t；未检出记为 1（等价于在 episode horizon 自动检出的 baseline）。在 precision–PDT 平面取 Pareto-optimal 阈值，用右端 Riemann 和在 precision 区间上积分，数值越低越好。

## 实验与关键数字
- **模型与基线：** π0.5（3.6B，PaliGemma VLM，逐层 cross-attention 融合）与 X-VLA（0.9B，Florence-2-Large encoder-decoder VLM，仅末层 encoder feature 条件化）。基线 ACE、STAC、Diff 均使用 32 个 action samples，因不具备实时能力，只能在 rollout 回放上评估（RTX 5090，17 ms 的 VLM 开销已扣除）。
- **评估规模：** 6 个真实任务（Blocks、Stack T、Cups、Kitchen、Drawer、Mixer，覆盖高精度、多模态演示、多阶段、语言条件化），每个 policy 约 80 次 rollout，每次 rollout 用 3 个 seed；仿真用 Libero-Plus（Object / Spatial / Goal / 10 套件），单 seed。
- **总体表现：** FAIL 是唯一在几乎所有真实与仿真任务上都进入 top-3 的方法。例如 X-VLA 在 Kitchen 上 ACC / LLMD / FAIL 的 PR 均为 1.00，FAIL 的 PDT 为 0.21；X-VLA 在 Stack T 上 FAIL 达 PR 0.98 / PDT 0.08，优于 ACE（0.96 / 0.09）与 Diff（0.97 / 0.08）。
- **互补性：** ACC 检测更可靠、LLMD 检测更早，组合后 FAIL 在 Cups、Stack T、Mixer（尤其 π0.5）以及 X-VLA 的 Libero-Plus 套件上取得最低 AUCPDT。ACC 擅长机器人出现快速、抖动运动的 OOD 情形；LLMD 擅长策略陷入无限重试循环或退化到与环境状态无关的「default」动作。
- **Token-wise 消融（Table 3）：** 用全局单一均值/协方差替代 per-token 统计显著变差，X-VLA 在 Drawer 上 AUCPDT 从 0.19 恶化到 0.24；Kitchen 上 PR 从 1.00 掉到 0.67、PDT 从 0.20 升到 0.42。
- **速度归一化消融（Table 5）：** 在 Libero-Plus 上效果显著，X-VLA 在 Spatial 上 AUCPDT 从 0.38 降到 0.28、PR 从 0.86 升到 0.95；真实任务上增益较小但方向一致（Table 4）。
- **Chunk overlap 消融（Figure 5）：** ACC 性能随重叠动作数减少而下降，但即使只有 1 个重叠动作仍保留部分检测能力；π0.5 比 X-VLA 对短重叠更鲁棒。
- **ACC vs STAC：** ACC 可视为 STAC 的 velocity-normalized 单样本估计，在几乎所有真实任务上优于 STAC；在 Libero-Plus 上 STAC 的 AUCPR 更高（多处达 1.00），但 ACC 检测明显更早。作者推测 ACC 只对已执行的 chunk 评估规划一致性、不对反事实轨迹评估，因而在策略进行 mode selection 时误报更少。
- **局限：** LLMD 需要访问 finetuning 数据做一次预处理，大数据集或数据不可得时受限；ACC 需要足够重叠的 receding-horizon control，不适用于完全开环 chunk 执行；VLA-FAIL 会漏掉在特征与动作上都自洽的失败（如自信地停止或忽略语言指令），此时可与 VLM 语义级检测互补。
