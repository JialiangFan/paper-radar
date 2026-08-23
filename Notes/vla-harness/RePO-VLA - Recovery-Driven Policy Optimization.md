# RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Model

> arXiv: 2605.09410 | 年份: 2026

## 主题
Recovery-driven VLA policy optimization

## 背景
Vision-Language-Action (VLA) 模型在长时序、contact-rich 的双臂操作中依然脆弱：抓取位姿、接触状态或双臂时序上的微小偏差会迅速演变为 execution drift。这类扰动通常并不使任务变得不可完成，而是把系统推入可恢复的 adverse state，需要有针对性的 correction 才能回到 success manifold。然而当前主流训练范式仍以成功演示上的 supervised fine-tuning (SFT) 为主，失败 rollout 被整体丢弃，导致模型对「漂移—纠正」这一时间结构几乎没有监督信号。

## 现有局限与研究问题
- **Limitation:** 成功导向的模仿学习存在 failure-utilization blind spot——失败轨迹早期往往包含有效的 approach、contact preparation 与 partial-manipulation prior，却被连同末段的 terminal breakdown 一起丢弃；反之，recovery 演示若被整段照搬模仿，会把「造成漂移的分布」和「修复漂移的分布」混为一谈，产生 causal confusion 与 mode averaging（策略把前序错误当成触发 recovery 的必要条件）。稀疏二值奖励也无法区分有效 approach、暂时停滞、主动 recovery 与终局失败。
- **Limitation:** 现有 recovery 方案多依赖外部模块——VLM/LLM replanning、interactive correction、在线 failure detector 或手写 retry 规则——与底层策略解耦，且大多针对 high-level 错误，对 low-level contact dynamics 无能为力；FailSafe 等合成 recovery 数据的方法仍用 SFT，未把 erroneous state 与 corrective action 分离。评测层面也缺少能把 nominal 能力与 recovery 能力解耦的基准。
- **Problem:** 如何在统一的策略中，把 success / recovery / failure 三类混合质量轨迹按语义角色差异化利用，使单一 VLA 策略无需在线失败检测器或启发式重试即可从 adverse state 自主恢复？

## 贡献
- 提出 **RePO-VLA**：two-phase (RAI + VCR) recovery-driven policy optimization 框架，为成功、恢复、失败轨迹分配不同角色——progress alignment 保留失败前缀的有用部分，low-value 标签暴露 drift-to-correction 边界，data engine 把 adverse state 转化为 corrective rollout 用于 value-conditioned refinement。
- 提出 **PAS-VF**（Progress-Aware Semantic Value Function）：冻结双塔编码器 + 轻量 adapter，在语义隐空间中以 self-referential 方式给混合质量数据打 dense progress 标签，无需人工进度标注。
- 提出 **FRBench**：面向 recovery 的基准，含标准化 error injection（E1–E4）、phase-based 评测协议（Nominal / Error / Recovery），覆盖 RoboTwin 仿真与真实双臂任务，且 recovery 评分以「已验证的 adverse state」为条件，避免把 reaching/grasping 改善误判为真正的纠正能力。
- 给出实证验证：相对 SFT 基线的显著 recovery 增益，以及随 recovery-data 密度增加的 scaling 趋势。

## 方法论
- **Phase I — Recovery-Aware Initialization (RAI):** 用 **TSHR**（Trajectory Slicing with History Reset）把原始 recovery 轨迹在 `t_rec` 处切开，丢弃 failure prefix，仅保留 `τ' = {(o_t, a_t)}_{t=t_rec}^{T}` 作为独立 correction episode，并在首个 recovery 帧清空 observation-history buffer 让其自然重填，得到 `D_rec^reset`。使策略把 recovery 学成 **state-conditioned skill** 而非对特定失败 rollout 的回放。损失为 expert 数据与 reset recovery 数据的加权 SFT（式 1，权重 λ）。TSHR 仅用于 RAI；VCR 与部署均使用标准 rolling buffer。
- **PAS-VF（进度感知语义价值）:** 冻结 V-JEPA 时空视觉编码器 `E_v` 与文本编码器 `E_t`，仅训练 vision/text adapter，把轨迹与语言指令投影到共享流形 `Z`。训练阶段在成功轨迹上做 **monotonic progress alignment**：让前缀 `τ_{0:t}` 的 `CosSim(z_t^v, z^l)` 回归归一化时间进度 `t/T_τ`（式 2）。推理阶段做 **self-referential progress estimation**：对无标签失败轨迹取其与成功嵌入参考簇 `C_ref` 的最大余弦相似度 `V(τ_fail) = max_{z∈C_ref} CosSim(z^v_{τ_fail}, z)`（式 3），从而免除人工标注且保持 task-relative。
- **Progress-Aware Hindsight Labeling:** 对混合数据逐帧赋 `v_t ∈ [0,1]`——成功轨迹与有效 recovery 后缀 `v_t = 1.0`；recovery 中的 error prefix（deviating segment）`v_t = 0.0`（显式告诉策略即便共享同一 raw history，导致 adverse state 的动作不应与随后的 corrective 动作被平均）；纯失败轨迹用 **reliability decay** `v_t = V(τ_fail)·(1 - t/T)^α`（式 4，α = 3.0），保留早期 kinematic prior 同时快速压低接近不可逆失败的状态。
- **Phase II — Value-Conditioned Refinement (VCR):** 以 flow-matching **π₀.₅** 为 backbone，增加 value token `e_val = MLP_val(v_t)`，transformer 与视觉、语言、history token 联合注意；在 `D_total = D_succ ∪ D_rec^raw ∪ D_fail` 上做 value-conditioned 微调（式 5）。此阶段使用未重置的原始 rolling history `H_t^raw`，让 value 标签而非历史截断来消解「low-value drift vs. high-value correction」的歧义。
- **部署（Goal-Conditioned Autonomous Recovery）:** 不在线估计 `V(τ)`、不清空 history、不使用 failure detector，仅固定 value token `v = 1.0`，把学到的 success manifold 当作 attractor，使 high-value token 在 buffer 中仍残留 low-value 观测时自动选中 corrective 分支。
- **Failure-Recovery Data Engine:** 双源互补。(a) **Interception-based synthetic injection**：挂钩 expert planner 执行节点，在 grasp/lift 等关键段注入 E1–E4 扰动，再由 hierarchical recovery planner 合成纠正动作，五步拦截流程（oracle 参考轨迹 → 监控并拦截关键节点 → 扰动覆盖 nominal 动作 → 投射进 adverse state → 规划器合成 corrective action）。(b) **Policy-induced rollouts**：从训练好的 base policy 的闭环失败中采集，由 expert planner 介入，得到 in-distribution、模型特异的 recovery 数据，覆盖合成误差无法刻画的复合 execution drift。
- **FRBench 扰动分类法（作用于 `a_t = [p_t, R_t, g_t]`）:** E1 `premature_close`（approach 中提前闭合夹爪，`g'_t = g_closed`，持续 `N_hold`）；E2 `grasp_slip`（lift 期确定性窗口内开爪，`t ∈ [t_lift, t_lift + 30]`）；E3 `grasp_position_offset`（厘米级平移偏置 `δp_trans ~ U(-d, d)`）；E4 `grasp_orientation_mismatch`（大幅旋转失配 + 侧向位移）。仿真中失败事件由执行时长超过 nominal 成功最大时长触发：`F_t = I(t > T_max)`，`T_max = max_i(T_succ^i)`；真实场景由人类遥操作刻意制造 adverse state 并演示纠正。

## 实验与关键数字
- **FRBench-Sim 规模（Table 2）:** 共 23,453 条生成的双臂操作 episode，覆盖 46 个任务、2 种环境模式（Clean / Random）；其中 nominal success 17,061 条、verified failure-recovery 6,392 条。误差类型计数：E1 Premature Close 8,022、E2 Grasp Slip 3,516、E3 Position Offset 4,686、E4 Orientation Mismatch 688（各类计数之和超过 6,392，因为在最终序列过滤前跨环境做了组合测试）。
- **仿真协议:** 10 个 RoboTwin 任务、每任务 50 次 rollout；recovery trial 在 grasp 起始处保持夹爪张开 30 帧（约 1 s）注入 Dynamic Grasp Failure。基线含 RDT、GO-1、π₀、π₀.₅ 及 Phase I 消融。
- **仿真 nominal 鲁棒性（Table 3）:** Phase I（w/o Fail）平均成功率 Clean 44.6 → Random 44.0（相对 π₀.₅ 分别 +17.2 / +10.4），几乎不随随机化下降；对照 π₀ 从 33.9 跌到 12.9，说明 recovery-aware 初始化不牺牲基础任务能力。π₀.₅ 自身为 Clean 27.4 / Random 33.6；RDT 为 22.5 / 8.8，GO-1 为 28.1 / 26.0。
- **仿真注入失败（Table 3）:** π₀.₅ 平均 Clean 15.0 / Random 15.4；完整 RePO-VLA 提升到 **Clean 37.0（+22.0）/ Random 43.0（+27.6）**。单任务上增益最大的是需要真正重新抓取或重新对齐的任务（如 Blocks RGB 由 20/22 提升到 70/80，Blocks Size 由 2/6 提升到 60/40，Place Bread 由 0 提升到 90/60）。
- **真机设置:** 两台 Dobot X-Trainer 手臂，四个任务 Pour Water / Cook Vegetable / Tidy Desk / Fold Towel，每任务 200 条 expert 演示 + 50 条遥操作 recovery episode，每任务 10 次试验；adversarial 设定由人在关键阶段注入动态位移、运动学干扰或强制滑脱。
- **真机主结果（Table 4）:** Standard 平均——π₀ 27.5、π₀.₅ 25.0、Phase I **42.5**、Full (1x) 40.0（较 π₀.₅ +15.0）；Adversarial 平均——π₀ 12.5、π₀.₅ 20.0、Phase I **37.5**、Full (1x) 30.0（+10.0）。Full (1x) 未超过 Phase I，作者据此指出 value-conditioned refinement 存在 data-density bottleneck：稀疏 recovery 数据会让 value landscape 变噪。
- **Recovery 数据 scaling（Table 5 / Fig. 6）:** 在 Pour Water 与 Fold Towel 上把真机 recovery 数据从 1x 增到 2x、4x。Standard 平均：π₀ 40、π₀.₅ 35、Phase I 50、Full (1x) 40、Full* (2x) 70、**Full** (4x) 80**（较 π₀.₅ +45，较 Phase I +30）。Adversarial 平均：π₀ 20、π₀.₅ 20、Phase I 40、Full (1x) 30、Full* (2x) 65、**Full** (4x) 75**（较 π₀.₅ +55，较 Phase I +35）。单任务上 Pour Water adversarial 达到 80（+60 相对 π₀.₅），Fold Towel adversarial 达到 70（+50）。摘要据此概括为「adversarial success 平均由 20% 提升至 75%，scaled real-world trial 中最高 80%」。
- **消融（Fig. 7）:** (a) 直接用未做 history reset 的原始 failure-recovery 数据会引发 causal confusion，TSHR 可恢复性能；在相同 recovery 数据下，heuristic retry 基线仍弱于 value guidance，说明关键收益来自把动作分布条件化到 high-progress 区域，而非单纯重试。(b) 30 次试验验证中开启 `v = 1` 一致提升成功率：Pour Water 达 76.7%、Fold Towel 达 73.3%（`v = 0` 分别约 50% 与 46.7%），表明 value conditioning 是稳定的部署期控制信号。(c) decay 率扫描确认 **α = 3** 为最佳折中：α = 1 对接近终局的失败惩罚不足，α = 10 则丢弃了有用的早期 approach 行为。
- **定性可视化（Sec. 6）:** 在 RoboTwin + ALOHA-Agilex 上，对 E1–E4 四类错误各给 6 个任务示例，覆盖 Clean 与 domain-randomized 环境；每段由单个 episode 采样 9 个关键帧组成——帧 1–3 为 Error Attempt（物理驱动扰动而非简单高斯噪声）、帧 4–8 为 Recovery（含重感知与纠正动作的规划轨迹）、帧 9 为从纠正后状态恢复的 Normal 执行。
