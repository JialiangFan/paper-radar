# What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies

> arXiv: 2605.28527 | 年份: 2026

## 主题
Probing value-like structure in VLAs

## 背景
Vision–language–action (VLA) 策略以模仿学习为训练目标，其损失函数从不要求模型估计 reward、progress 或未来成功概率。然而部署时收集的成功/失败 rollout 天然携带 outcome 标签，这类信息是否已经以线性可解码的形式存在于 frozen representation 中，此前缺乏系统检验。本文用轻量 linear probe 在完全冻结的 VLA 特征上回答两个问题：该信号能否被读出，以及读出后能否在不更新策略参数的前提下改变动作选择。

## 现有局限与研究问题
- **Limitation:** 现有机器人 foundation policy（RT-1/RT-2、OpenVLA、Octo、SmolVLA、π₀、π₀.₅）一律只训练模仿动作，无一训练估计 reward、progress 或未来成功；这种训练目标不对称带来的表征后果几乎无人研究。同时，test-time 候选动作选择（Visual Foresight、Diffusion Policy 等）通常依赖外部单独训练的 reward/cost/world model，而非策略自身表征。
- **Limitation:** 单纯发现 offline probe 拟合得好并不足以说明问题——操作数据充满表层捷径：不同任务 baseline 成功率不同（task identity 捷径）、timestep 与 progress 强相关（elapsed-time 捷径）、成功与失败 rollout 的粗视觉统计本就不同。以往 probing 工作很少显式排除这些混淆。
- **Problem:** frozen VLA 表征中是否真的存在一个 value-like 信号，它能否在 same-task、same-timestep 的严格 matched control 下存活，并且能否在 test time 真正改变策略执行哪个动作？

## 贡献
- **多骨干可解码性**：outcome-derived value-like target 可从多个 frozen 表征族（autoregressive VLA、VLA-distilled VLM、self-supervised vision、contrastive vision-language）中线性解码，强度相当，说明这不是单一模型或单一层的 artifact；而 progress、time-to-go、task identity、proprioception 等 scalar nuisance baseline 远达不到该水平。
- **排除任务/时间捷径**：提出 same-step matched-pair control，按 (task, timestep) 分组构造 high/low 配对，配合 label-shuffle 负对照，证明信号不是 task ID 或 elapsed time 的代理。
- **行为可用性**：将同一个 offline 训练好的 probe 直接插入 π₀.₅ 的 test-time candidate 选择回路（best-of-K，无任何 policy update、无单独 reward model），在 hard non-ceiling 任务上显著提升成功率，把「表征里有什么」转化为「行为上能改变什么」。
- **分阶段可证伪协议**：三阶段（decodability → matched control → online selection）刻意不合并为单一指标，并明确记录信号失效的边界情形（drawer 无增益、cross-benchmark task split 崩溃、compute 代价），而非平滑掉负结果。

## 方法论
- **Value-like target 定义**：语言条件操作 episode，成功轨迹（长度 T）在时刻 t 赋 discounted Monte-Carlo 目标 v_t = γ^(T−1−t)，γ = 0.99；失败轨迹全程 v_t = 0。γ=0.99 对应约 100 步有效 horizon，匹配 LIBERO-Goal（episode 上限 300 步、多数成功轨迹 150 步内完成）。用 Monte-Carlo return 而非 bootstrapped TD，避免在 frozen 特征上自举带来的不稳定，代价是目标更 noisy，但保证 probe 成败反映真实表征内容而非二阶学习 artifact。作者明确声明这是 value-like 而非 Bellman-consistent value function。
- **Offline probing**：对每个 feature family 拟合标准化 linear ridge probe v̂_t = wᵀφ̄_m(o_t, g) + b，ridge 强度在固定网格上交叉验证；报告 R²、Spearman、RMSE/MAE 及 per-task R²。两种 split：demo split（按 suite/task/source demonstration 分组，组在任务内采样，测同任务未见轨迹）与更严格的 task split（按 suite/task 分组，测未见任务）。task identity、progress、time-to-go 不作为 VLA probe 的协变量，只作为独立 baseline 行。
- **Deconfounding（matched control）**：按 (task name, timestep) 分组，组内构造 value-like 标签差 ≥ 0.20 的 high/low 对；probe 若给高标签行更高分记正确，平局记半分。同时做 label-shuffle 负对照（随机交换配对中哪一行算正例）。
- **Test-time candidate selection**：frozen π₀.₅ 策略，每个 replan step 采 K = 16 个 action chunk（种子由 episode seed、replan index、candidate index 确定性导出），只执行长度 h = 5 的短 prefix。simulator-backed teacher selector 对每个候选：恢复 simulator 到当前快照 → rollout prefix → 记录是否成功、累积 reward r_k、以及由结果观测提取 frozen 特征后 probe 打分 s_k。决策规则：若存在 rollout 成功的候选集合 S ≠ ∅，取 argmax_{k∈S} s_k；否则取 argmax_k [z(r_k) + z(s_k)]（组内归一化）。选定后 simulator 恢复原快照，只提交所选 prefix。Baseline：random（同一候选集均匀随机）与 greedy（直接执行解码 chunk）。
- **Goal-conditioning 诊断**：goal-swap control——固定视觉观测、替换语言指令，看 probe 分数是否移动；并配 vision-only run 作为「必须为零」的负对照。

## 实验与关键数字
- **数据规模**：LIBERO-Goal 为主基准，offline probing 用 311,719 条 frame-level 行，来自 1,400 条混合成功/失败轨迹；CALVIN-D（82,436 行）与 RobotWin 作 cross-benchmark 检验。
- **Table 1（offline R²，demo / task split）**：π₀.₅ vision encoder 0.7377 / **0.5510**（task split 最优）；OpenVLA-OFT LLM layer 07 **0.7561**（demo 最优）/ 0.5505；OpenVLA vision backbone 0.7553 / 0.5493；OpenVLA-v0.1 0.7354 / 0.5429；SmolVLA 0.7028 / 0.5257；DINOv2 0.6899 / 0.5104；CLIP 0.6747 / 0.5095。Nuisance baseline：random projection 0.5568 / 0.3916；proprioception 0.2010 / 0.1107；progress 与 time-to-go 均 0.0325 / 0.0302；task one-hot −0.0009 / −0.0018。
- **π₀ 的反例**：π₀（建在 VLM 之上的 flow-matching action head）task split R² 仅 0.0702，接近 scalar baseline，而同一血统的 π₀.₅ 达 0.5510；作者据此推测 value-like 信号存在于仍编码 goal-conditioned scene state 的部分，在为 action token 预测高度特化的表征中被挤出。
- **Table 2（same-step matched control）**：primary probe 4,605 对，pairwise accuracy **94.22%**，label-shuffle 50.05%，gap +44.17 pp；seed/layer 稳健性（10 × 4,605 对）92.16% vs 49.67%，+42.49 pp；分任务：open middle drawer 1,053 对 92.31% / 51.19%（+41.12），push plate 1,892 对 94.56% / 50.79%（+43.77），wine rack 1,660 对 95.06% / 48.49%（+46.57）。十次 same-step run（跨 `vlm_final_output` 与 `vlm_layer_08` 两种特征、每种 5 个 probe seed）pairwise accuracy 区间 89.58%–94.22%，shuffle 区间 49.01%–50.05%，无任何 probe 配置低于 89.58%、无任何 shuffle 配置高于 51.19%。
- **Table 3（在线正面证据，成功数/episode 数）**：hard-3 aggregate — greedy 140/450 (31.1%)、random 166/450 (36.9%)、value-guided **191/450 (42.4%)**，ΔV−R +5.56、ΔV−G +11.33，McNemar p = 0.0614（作者判为 borderline），wall-clock 2.06×；push plate — 80/300 (26.7%) / 101/300 (33.7%) / **133/300 (44.3%)**，+10.67 / +17.67，p = 0.00294，2.10×；wine rack — 107/300 (35.7%) / 108/300 (36.0%) / **132/300 (44.0%)**，+8.00 / +8.33，p = 0.0264，2.01×。
- **边界（负结果）**：open middle drawer 相对 random 仅 +2.00、相对 greedy 仅 +0.67，落在采样噪声内，作者明确记为 no-gain case。
- **任务 regime 划分（Table 4）**：定义 hard non-ceiling 为 greedy 成功率 ≤ 40%。open middle drawer 38.67%（150 episodes）、wine rack 35.67%（300）、push plate 26.67%（300）合格；open top drawer 82.00%（50）；bowl on stove 98.00%、bowl on cabinet 100.00%（各 50）属 ceiling case，按设计排除。
- **计算代价**：value-guided selection 每 episode 约为 random 的 2×、超过 greedy 的 20×。折算成「每多一次成功的额外 wall-clock」：push plate ≈ 39 分钟，wine rack ≈ 47 分钟，drawer（几乎无额外成功）≈ 185 分钟。probe 本身在单卡上 5 分钟内训完，主要开销来自 simulator-backed 候选评估。
- **Goal-swap 诊断**：vision-only 负对照在 14,080 对上给出精确为零的特征变化与精确为零的分数变化。π₀.₅ VLM 特征在语言 swap 下确实移动：平均 L2 位移 1.96，cosine similarity 0.9985；seed-7 `vlm_final_output` probe 分数平均变化 +0.12，原始 goal 在 53.7% 的配对上得分更高；但第二个 seed 与更深 VLM 层给出 −0.08 与 −0.02，符号不一致（drawer 类任务倾向给原 goal 更低分，rack/container 类更高）。作者据此认为 probe 继承了 goal-conditioned 表征，但不是校准良好的 reward model。
- **Cross-benchmark（Table 5）**：CALVIN-D demo split OpenVLA L20 R² = 0.3007（ρ = 0.6034），task split OpenVLA L07 仅 0.0393（ρ = 0.3434）；RobotWin demo split 拟合很强（π₀.₅ vision 0.8715，seed 区间 0.8452–0.8916；VLM final 0.8407；layer 08 0.8276），但 task split R² 为负（−0.8528 / −0.9314 / −0.7790，对应 Spearman ρ 仅 0.1088 / 0.1848 / 0.1330）。作者仅将其作为 LIBERO 之外「benchmark 内可解码性」的证据，不主张 cross-task transfer。
- **Supporting runs（Table 6，未与正式 balanced run 合并）**：π₀.₅ full 上 open middle drawer 32%→48%（+16 pp）、push plate 32%→46%（+14）、wine rack 40%→48%（+8）（各 n=50）；OpenVLA 50ep open middle drawer 38%→70%（+32）、open top drawer 40%→52%（+12）。K sweep：push plate K=8 +10 pp、wine rack K=8 +4 pp、push plate K=32 +14 pp、wine rack K=32 −2 pp（mixed）。Temperature sweep（n=20）：open middle t=0.7 25%→90%（+65 pp）、open middle t=0.3 65%→55%（−10，mixed）、open top t=0.3 15%→30%（+15）、open top t=0.7 55%→55%（0，mixed）。
- **K 的选定依据**：早期两任务 sweep 显示整体成功率从 K=4 与 K=8 的 60% 升到 K=16 的 80%，故正式实验固定 K=16；作者声明此为 design calibration 而非正式验证。
- **实验控制**：episode 上限 300 环境步；每个 ridge probe 跨 5 个随机种子训练；online rollout 分布在 3 台独立服务器上并预先固定 seed 分配（hard-3 用 1111–3333，push-plate follow-up 用 4444–6666，wine-rack follow-up 用 7777–9999）；绝对成功率报 Wilson 95% CI，策略对比用 paired bootstrap 95% CI 与 exact McNemar，Fisher exact 作为 unpaired 敏感性检查。

## 局限
- 不主张 VLA 内部存在 Bellman-consistent value function，probe target 是 outcome-derived 的。
- 在线增益与任务强相关：仅在 policy 本身「足够弱但非病态」（greedy ≤ 40%）且采样候选集中确实存在下游结果不同的备选时才出现。
- selector 依赖 simulator 恢复状态并 rollout 候选，成本约为 random 的 2×、greedy 的一个数量级以上，属 diagnostic intervention 而非可部署 controller；要实用需更廉价的候选评估或可替代 simulator 的 learned scorer。
