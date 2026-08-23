# SAFECAST: Robust Failure Detection for VLA Policies with Contrast-Set Training and Calibration

> arXiv: 2608.04246 | 年份: 2026

## 主题

Contrast-set calibrated VLA failure detection

## 背景

Vision-language-action (VLA) 策略（OpenVLA、π₀ 等）在干净的训练分布下表现良好，但在部署期遇到 clutter、distractor objects、光照变化、novel objects、机器人初始状态改变或指令改写时会显著退化，这在 assistive robotics、human-robot interaction 等安全攸关场景中构成风险。当前主流的 runtime failure detection 路线以 SAFE (Gu et al., NeurIPS 2025) 为代表：冻结 VLA 策略，用一个轻量 MLP probe 读取其 pre-final-layer hidden state $h_t$ 输出逐时刻 failure score $r_t = f_\phi(h_t)$，再用 functional conformal prediction (FCP) 把 $r_t$ 校准成随时间变化的干预阈值 $\delta_t$，在任务真正失败前提前报警。本文由 USC（Rajaprakash, Prajapati, Xue, Anwar, Thomason）完成，受 DARPA ARC SAFRON 资助。

## 现有局限与研究问题

- **Limitation:** SAFE 式方法的可靠性依赖一个关键假设——calibration trajectories 与 deployment trajectories 同分布（conformal prediction 的 exchangeability 前提）。而 probe training 与 conformal calibration 的数据都只采自 source distribution $\mathcal{D}_\mathrm{src}$；一旦部署时出现 visual shift、language shift 或二者叠加的 multimodal shift，hidden-state risk trajectory 的分布会大幅漂移，使得只在源分布上标定的阈值 $\delta_t$ 失准，导致 late warning 或 missed warning。
- **Problem:** 对冻结 VLA 策略，在 $\mathcal{D}_\mathrm{eval} \neq \mathcal{D}_\mathrm{src}$ 的部署分布偏移下，如何做可靠的 rollout-level failure detection？具体地：能否用低成本的 contrast-set perturbation 同时改造 probe 的训练分布与 conformal 的校准分布，使 risk trajectory 更接近部署条件？

## 贡献

- 提出 SAFECAST（**Sc**alable **F**ailure **E**stimation with **C**ontrast-**S**et **A**ugmentation for **S**afety **T**racking）：把 visual / language / joint visual-language 的 contrast-set rollouts 同时注入 **probe training** 与 **functional conformal calibration** 两个环节，是对 SAFE 的数据分布层面（而非模型架构层面）的干预。
- 在 real-world DROID（Franka，π₀ 与 π₀-FAST）与 LIBERO 仿真（OpenVLA 与 π₀）上，相对 SAFE 基线在 ROC-AUC 上取得统计显著提升（多个设置 $p$ 值见原文 Appendix C）。
- 通过 TrainAug / CalAug / 全量三种消融，分离出「增强训练」与「增强校准」各自的作用，并发现其相对收益依策略而异。
- 证明 joint visual-language contrast sets 优于单模态扰动。
- 提出并验证 sim-to-real 校准路径：probe 完全在仿真中训练，仅用少量真实世界 contrast-set 轨迹做 conformal 校准，效果优于在昂贵的真实数据上端到端训练 probe。
- 修正了 SAFE 的评测协议：SAFE 把 LIBERO-Spatial 切成同分布的 seen/unseen 任务，本文则显式分离 source / calibration / deployment 三个分布，以受控地度量 deployment shift。

## 方法论

- **基座设定**：策略 $\pi$ 全程冻结（probe 训练、conformal 校准、评测阶段均不更新）。probe 为轻量 MLP，$r_t = f_\phi(h_t)$，对长度 $T$ 的 rollout 产生时间对齐的 risk 序列 $r_{1:T}$。
- **Calibration（重点，确为 conformal）**：采用 **functional conformal prediction**（Diquigiovanni et al., *Statistica Sinica* 2024 的 functional prediction band 思路），而非普通 split conformal。在 calibration rollouts $\tau_j^\mathrm{cal}$ 上取 probe 的 risk 轨迹 $r^{(j)}_{1:T}$，在**成功的**校准轨迹上计算 nonconformity score $S_\mathrm{cal}$，构造 one-sided time-varying threshold $\delta_t = \mu_t + q_\alpha$；部署时 $r_t > \delta_t$ 即判定该 rollout 将失败。$\alpha \in (0,1)$ 是操作风险容忍度：$\alpha$ 越小阈值越高、FPR 越低（更保守的干预），$\alpha$ 越大阈值越低、FPR 越高。**SAFECAST 的改动就是把校准池从 $\mathcal{D}^\mathrm{cal}_{\phi,\mathrm{src}}$ 换成含 contrast-set 轨迹的 $\mathcal{D}^\mathrm{cal}_{\phi,\mathrm{aug}} = \mathcal{D}_\mathrm{src} \cup \mathcal{D}_\mathrm{CS}$**，训练池同理换成 $\mathcal{D}^\mathrm{train}_{\phi,\mathrm{aug}}$。校准子集按成功/失败数量做受控采样，避免阈值估计被单一 outcome class 主导。
- **Contrast set 的构造（关键细节）**：对 source rollout 的视觉与/或语言输入施加受控 perturbation operator 后**重新执行冻结策略**，得到 $\tau^\mathrm{CS} = \{(\tilde o_t, \tilde l, \tilde a_t)\}_{t=1}^T$。因为是重新 rollout 而非重标注，$\tau^\mathrm{CS}$ **不是** $\tau^\mathrm{src}$ 的 counterfactual/relabeled 副本，其动作序列与 hidden-state 轨迹都会改变；作者因此**明确不假设** $\mathcal{D}_\mathrm{src}$ 与 $\mathcal{D}_\mathrm{CS}$ 之间的 trajectory-level exchangeability，而是把 contrast set 当作构造「更接近部署分布」的训练/校准分布的手段。
  - **Visual**：保持指令不变。LIBERO-Spatial 加入 distractor objects——要求不改变目标任务、不被指令引用、不遮挡原始 rollout 路径；DROID 包含 distractor objects、cluttered backgrounds、novel objects、altered object configurations。
  - **Language**：保持视觉场景不变。LIBERO-Spatial 用 ChatGPT 5.1 Instant 为每个任务生成 3 条 paraphrase（保持目标物体、动作、目标位置不变），为控制采集成本每条 paraphrase 只在每个任务的 3 个 episode 上评测（而非全部 50 个 source episodes）；DROID 包含 paraphrased instructions 与（适用时）negated / distractor phrasing。
  - **Joint visual-language**：同时扰动观测流与指令，构造 multimodal shift，主要用于 real 设定；这类样本正是最可能违反源分布 conformal exchangeability 假设的情形。
- **候选轨迹过滤**：用基于 Dynamic Time Warping (DTW) 的 active rejection 流程，对与已选轨迹过于相似（DTW 距离低于固定阈值）的候选做拒绝，降低 $\mathcal{D}^\mathrm{train}_{\phi,\mathrm{CS}}$ 中的近重复。
- **四种配置对照**：SAFE（源分布训练 + 源分布校准）、SAFECAST_TrainAug（仅增强训练）、SAFECAST_CalAug（仅增强校准）、SAFECAST（两者都增强）。
- **评测协议**：在 $\alpha$ 上做 sweep，报告 $\alpha$-marginalized F1（对 $\alpha$ 取平均，度量跨风险容忍度的鲁棒性，而非单一工作点），并在每个 $\alpha$ 计算 TPR/FPR、以所得 TPR–FPR 曲线下面积作为 ROC-AUC。

## 实验与关键数字

- **设置**：真实端为 Franka/DROID，策略 π₀ 与 π₀-FAST。π₀ 用开源 DROID checkpoint 在 20 条 teleoperated spatial pick-and-place 演示上做 LoRA 微调（因为 zero-shot checkpoint 在预实验中成功率为 0）；π₀-FAST 不额外微调即有非零成功率。评测 rollouts $\tau^\mathrm{eval}$ 含 novel objects、new tasks、clutter、lighting variation、altered robot initial states 等更强偏移。仿真端为 LIBERO-Spatial 与 LIBERO-Plus，策略 OpenVLA 与 π₀。所有数字对 $\alpha \in \{0.1, 0.2, \dots, 0.9\}$ 与 **30 seeds** 平均。
- **Table 1（SAFE → SAFECAST）**

  | Method | F1 Sim-π₀ | F1 Sim-OpenVLA | F1 Real-π₀ | F1 Real-π₀-FAST | AUC Sim-π₀ | AUC Sim-OpenVLA | AUC Real-π₀ | AUC Real-π₀-FAST |
  |---|---|---|---|---|---|---|---|---|
  | Always guess failure | 0.5266 | 0.8314 | **0.7322** | 0.7654 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
  | SAFE | 0.7132 | 0.8589 | 0.4085 | 0.7475 | 0.3267 | 0.5937 | 0.2626 | 0.5501 |
  | SAFECAST_TrainAug | 0.7516 | 0.8687 | 0.5838 | **0.8109** | 0.4278\* | 0.6514 | 0.2649 | 0.6621\* |
  | SAFECAST_CalAug | 0.7373 | 0.8628 | 0.4480 | 0.7534 | 0.4382\* | 0.6782\* | 0.3415\* | 0.6578\* |
  | **SAFECAST** | **0.7528** | **0.8728** | 0.5412 | 0.8053 | **0.4469\*** | **0.8014** | **0.3807\*** | **0.6664\*** |

  （\* 表示统计显著，检验对象为 ROC-AUC 在每个 $\alpha$ 阈值上的配对性能。）ROC-AUC 相对 SAFE 的绝对提升：Sim-π₀ +0.1202、Sim-OpenVLA +0.2077、Real-π₀ +0.1181、Real-π₀-FAST +0.1163。
- **策略间差异**：真实 DROID 上，π₀ 从 augmented **probe training** 获益最大（F1 0.4085→0.5838），说明表征学习阶段接触扰动轨迹显著改善下游可分性；π₀-FAST 则更依赖 SAFECAST **calibration**，作者推测对更强的预训练策略而言，源分布与部署条件之间的 calibration mismatch 才是主要瓶颈。仿真侧 OpenVLA 同样最受益于 augmented probe training，π₀ 则在完整 SAFECAST 下最鲁棒。
- **模态消融（Figure 4，仿真）**：Mean F1 by modality —— visual only: OpenVLA 0.871 / π₀ 0.649；language only: 0.872 / 0.664；**visual + language: 0.873 / 0.753**（两者均最优，π₀ 上联合扰动的增益尤为明显）。正文另给出 OpenVLA 上 multimodal contrast sets 把 F1 从 visual-only 的 **0.922 提升到 0.959**。结论：部署期校准更受益于覆盖执行中实际存在的**联合**扰动空间，而非独立建模视觉或语言偏移。
- **Sim-to-real（Figure 5）**：probe 完全在 LIBERO-Spatial 上训练，仅用较小的真实 DROID contrast-set 轨迹做 functional conformal 校准，在整个 $\alpha$ 区间上的 F1 都优于「只在小规模真实数据上同时训练与校准」的 DROID π₀ SAFECAST，说明 SAFECAST 使 sim-to-real 迁移在 deployment mismatch 下依然可行，且比昂贵的真实世界 probe 训练更划算。
- **需要注意的负面/边界结果**：在 Real-π₀ 上，平凡基线 "Always guess failure" 的 F1（0.7322）仍高于所有学习型检测器（SAFECAST 0.5412、TrainAug 0.5838），即在该设定下失败率本身很高、F1 对多数类有利；ROC-AUC 才是区分能力的可靠指标（该指标上 SAFECAST 0.3807 vs. 平凡基线 0.0000）。此外真实 π₀ 与 π₀-FAST 的 ROC-AUC 绝对值仍偏低（0.38 / 0.67），距离可用的强保证仍有距离。
- **局限（作者自述）**：SAFECAST 依赖 contrast-set 轨迹能代表真实的部署偏移；若遇到 contrast-set 分布之外的扰动，性能仍会退化。contrast-set 采集带来额外 rollout 成本，且当前扰动族只覆盖可能的 visual / language / task-level 变化的一个子集。最关键的是，该方法**只是经验性地改善了校准对齐，并未在任意部署偏移下恢复形式化的 conformal exchangeability 保证**。
- **与 SAFE 的关系小结**：SAFECAST 不改 SAFE 的 probe 架构与 FCP 机制，只改「用什么数据训练 probe、用什么数据做 conformal 校准」；同时把评测协议从 SAFE 的同分布 seen/unseen 划分，改成显式分离 source / calibration / deployment 的受控偏移设定。
