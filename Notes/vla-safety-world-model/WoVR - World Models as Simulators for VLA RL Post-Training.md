# WoVR - World Models as Reliable Simulators for Post-Training VLA Policies with RL

> 作者: Zhennan Jiang et al. (2026, arXiv 2602.13977)

## 主题

Hallucination-aware world-model RL for VLA

## 背景

VLA 模型主流靠 imitation learning 训练，性能上限被示教数据的质量与覆盖度锁死；用 RL 做 post-training 能突破这个上限，但 on-policy RL 需要海量并行环境交互，真机上不现实，而仿真器与真实动力学又难以对齐。因此一条自然路线是用 learned world model 充当 simulator，把 policy optimization 从真实环境解耦出来。问题在于：learned world model 并不是 faithful simulator，闭环 imagined rollout 会产生 hallucination——视觉上合理但物理上错误的轨迹，甚至伪造 success 信号。

## 现有局限与研究问题

- **Limitation:** 已有工作（WMPO、World-Env、Prophet 等）基本把 world model 当作 drop-in simulator 直接替换真实环境，没有正面处理 hallucinated dynamics。闭环 autoregressive rollout 中误差有两个复合来源：(1) autoregressive feedback，模型以自己生成的帧为条件，早期小误差被逐步放大；(2) distribution shift，policy 在优化中不断漂离训练 world model 所用的数据分布，触发 OOD 预测失败。一旦用 hallucinated trajectory 做优化，RL 会被激励去 exploit 模型系统性误差而非真实任务进展（论文实测 WMPO 在 LIBERO-Long 上增益为 0）。
- **Problem:** 如果 world model 必然会 hallucinate，RL 如何在不完美的 imagined dynamics 下保持可靠？作者主张这本质上不是 modeling problem 而是 **reliability problem**，必须在三个互相耦合的层级上控制 hallucination：controllable simulator design、reliable interaction protocol、policy–model alignment。

## 贡献

- 把 closed-loop imagined interaction 中的 hallucination 明确识别为 world-model-based VLA RL 的核心可靠性瓶颈，并归因于 autoregressive 误差累积与 policy-induced distribution shift 两条机制。
- 提出 WoVR 框架，用三个 hallucination-aware 机制联合调控「模拟器可控性 / 交互协议 / 策略–模型对齐」，实现完全在 imagination 中的稳定 on-policy 优化。
- 构建了 SOTA 级的 action-conditioned video world model：在 LPIPS/FID/FVD/FloLPIPS 全面超过 EVAC、Cosmos-Predict2、OpenSora（WMPO 的 backbone），且推理吞吐达 23 FPS（OpenSora 为 7 FPS），rollout 越长优势越明显。
- LIBERO 上大幅提升：one-trajectory SFT 设定下平均 SR 由 40.5% → 69.5%（WMPO 仅 50.9%，online GRPO 仅 44.6%）；full-trajectory SFT 下 88.1% → 96.0%。
- 真机验证跨两个平台：Franka Panda 平均 SR +28.9 分（51.1% → 80.0%），噪声更大的 AgileX Piper +13.4 分；换 π0.5 backbone（配 Flow-SDE）仍有 +22.3 分增益，说明方法不绑定特定 VLA 架构。
- 代码与模型开源于 RLinf 生态（github.com/RLinf/RLinf、HuggingFace RLinf/rlinf-wovr）。

## 方法论

- **Stabilized Action-Conditioned World Model（simulator-level control）**：基于 Wan2.2-TI2V-5B video diffusion backbone 改造为 action-conditioned generator。采用 **dual-channel action injection**——action 一方面通过 timestep-conditioned normalization 调制 denoising 特征，另一方面替换 cross-attention 中的 text embedding 提供全局 action context，在保留原 DiT 结构的前提下实现 frame-level 可控。训练用 Rectified Flow 目标，推理只需 5 个 diffusion step + 3D VAE，因此比更小的 OpenSora 还快。
- **First-frame-anchored context + noisy context augmentation**：每个 autoregressive step 以 `[o_0, o_{t-c:t}]` 为条件（1 个固定 reference frame + 4 个 memory frame），固定首帧锁住全局布局与外观，memory frame 保留局部动力学；训练时对非 reference 的 context latent 注入轻微噪声（reference 保持 clean），缩小 train–inference gap，抑制对自生成帧的脆性 copying。消融显示去掉 ref 或 noisy context 都会在长 horizon 上显著退化（drift、物体消失）。
- **Keyframe-Initialized Rollouts, KIR（interaction-level reshaping）**：不总是从 episode 起点 `o_0` 起 rollout，而是把一部分 rollout 初始化在 task-critical 中间状态（尤其是当前 policy 的 failure state）附近，context 取 `[o_0, o_{T_KIR-3:T_KIR}]`。这样缩短 effective prediction depth，避免模型先幻想一长段前缀再到关键接触点。实现上按 task 设一个固定 task-level keyframe index，不逐条轨迹挑帧，保持低成本可复现。
- **GRPO with valid-step normalization**：用 GRPO 在 imagined rollout 上更新 policy，trajectory 长度归一化只算到首次 success 为止的 valid step，使梯度由「短的、task-critical 的片段」主导，而非长的、易漂移的续段——与 KIR 天然互补。
- **PACE: Policy-Aligned Co-Evolution（alignment-level regulation）**：先用 base policy 采的 1,500 条轨迹训 WM_Base，在其中优化 policy 后，用 evolved policy 再采 1,000 条轨迹低频 refine 得到 WM_Evo。关键是 **low-frequency** refinement，区别于经典 MBRL 的高频 dynamics 更新：既不需要训练期间持续的人工监督与环境 reset，又能纠正 simulator–policy 分布错配。训练曲线显示 PACE 切换前 imagined SR 持续上升而真实评测滞后（over-optimism），切换后两条曲线重新对齐。
- **Reward model**：支持两种——ResNet 轻量二分类给 sparse binary reward（HiL-SERL 式），以及 Qwen3-VL + LoRA 把 dense reward 建模为 ordinal visual progress 估计（0–10 级，按到首次 success 的时间邻近度线性打标）。Dense reward 早期样本效率更高但最终收敛相当，且慢约 3×，主实验统一用 sparse。
- **系统层**：沿用 RLinf-VLA 的 collocated GPU 分配，Generation / Simulator / Training 共享同一组 GPU，但 offload/onload 只在 rollout phase 首尾各做一次，避免闭环交互中每步搬运参数。

## 与 STL×VLA 主线的关联

这篇是「learned world model 作为 VLA 训练 harness」这条线上目前最完整的可靠性工程方案，它的核心命题——world model 用作 RL simulator 时，真正的瓶颈不是生成质量而是 **reliability**（imagined outcome 与 real outcome 的系统性错配）——正好是 STL 想解决的那类问题的非形式化版本。但 WoVR 全程没有任何 safety constraint、约束满足或形式化规约：它的「可靠」完全由架构手段（first-frame anchor、noisy context）、采样手段（KIR）和数据手段（PACE）经验性地保证，success 判定退化成一个 ResNet 二分类器或 VLM 的 0–10 进度打分，既不能表达时序结构，也无法区分「hallucinated success」与「真 success」。

留下的空间相当直接。论文 Limitations 自陈两点缺口：没有对 hallucination 如何传播进 policy optimization 做形式化刻画，也没有 imagined policy 相对真实环境最优策略的 regret bound——这正是形式化时序规约可以切入的位置，例如把 STL robustness 作为对 imagined rollout 的物理/时序一致性 monitor，用 robustness margin 而非分类器概率来否决 spurious success 信号。其次，KIR 的 keyframe 目前靠人工按 task 设一个固定 index，而「task-critical state」用 STL robustness 接近零的时刻来定义会更有原则性且可自动化；同理，那个手工设计的 ordinal progress dense reward 天然可以由 STL robustness 直接给出。最后，附录 E 罗列的真机失败模式（过早松夹、到位后不松夹、接触序列不完整、放置位姿错误）几乎逐条都是可以用时序逻辑写死的规约，说明这类 pipeline 缺的正是一层 spec-level 的监控与评估，而不是更大的视频模型。
