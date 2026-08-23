# TACO - TActile World Model as a Self-COrrector for Scalable VLA Post-Training

> 作者: Shengbang Liu et al. (2026, arXiv 2607.02840)

## 主题
Tactile world model for VLA post-training

## 背景
VLA 模型在 contact-rich manipulation 中依然脆弱：细微的接触扰动（打滑、力度不足、异常力矩）就会导致不可恢复的失败，而这类失败在 RGB 观测上几乎不可见——视觉几乎没变，触觉信号却已经剧烈偏移。这类失败是 localized（局部接触阶段）而非 semantic（任务级语义错误），因此针对 failure-adjacent 状态做 corrective post-training 是高效路径。但靠人工介入采集 corrective demonstration 难以 scale，用 world model 合成 imagined rollout 又受限于 vision-only world model 会生成「视觉上合理、接触动力学上不一致」的轨迹。

## 现有局限与研究问题
- **Limitation:** (1) 人工 intervention/DAgger 式纠错数据采集成本高、无法规模化；(2) 现有 world-model-driven post-training 多为 vision-only，生成的 imagined rollout 在接触阶段物理不一致，无法提供可用的 corrective supervision；(3) 朴素地把 tactile 输入塞进 VLA 全量微调，会侵蚀预训练的 visual-language priors，反而损害 pre-contact perception 与 spatial grounding（论文用 TACO w/o KI 消融证实）。
- **Problem:** 如何在不依赖重复人工干预的前提下，自动把真实 rollout 中的接触失败转化为**物理一致**的纠错监督信号，并把这种 tactile-heavy 的监督注入 VLA post-training 而不破坏预训练先验？

## 贡献
- 提出 **TACO**：tactile-aware world-model-driven 的 VLA post-training 框架，走 *Recognize–Imagine–Label* 闭环，把真实失败自动转化为 imagined visuo-tactile corrections，形成 real-to-imagine-to-real 的自主迭代。
- 构建 **visuo-tactile generation model**：在 Wan2.2-TI2V-5B 上做 video 与 6D force-torque 序列的 **joint denoising**，通过 temporal RoPE alignment 把 force token 对齐到 video latent 时间轴，并用 first-frame force anchoring 稳定生成。
- 构建 **unified progress-action model**：从 RGB + 12 维力矩信号同时预测 dense task progress 与 7-DoF corrective action，一个模型同时承担「识别失败」与「标注纠错动作」两个角色。
- 提出 **knowledge-insulated tactile adaptation**：对 VLM backbone 施加 stop-gradient，把 tactile-action 学习限制在 action expert 与适配层，防止 tactile 梯度侵蚀预训练视觉语言先验。
- 引入 **advantage-conditioned training**（binary advantage $y_t\in\{0,1\}$ 区分 corrective segment 与 failed segment）作为 offline RL 目标，使策略能从失败中学习而非只过滤成功轨迹。
- 真机六任务验证：两轮 post-training 后平均成功率相对 base policy **+44%**（0.38 → 0.82），相对无 KI 版本 +32%、相对 Filtered BC +39%；且在 unseen background / object / position 三类 OOD 下仅一轮适配即大幅回升。

## 方法论
- **Recognize（识别失败邻近状态）**：用当前策略 $\pi_\theta^{(k)}$ 采集真实 rollout，unified progress-action model 输出逐帧 dense progress $p_t$；选取 progress 停滞或下降的时刻作为 correction anchor（$p_{t+\Delta}-p_t<\epsilon$），每条失败轨迹最多取 10 个 anchor；以第一个 anchor 作为 failure onset，之前的时间步赋 advantage $y=1$，之后赋 $y=0$；专家演示全程 $y=1$。
- **Imagine（想象纠错片段）**：从每个 anchor 状态出发，visuo-tactile generation model 以当前视觉观测、力信号、语言指令为条件，联合 flow-matching 去噪出 $T=49$ 步的未来视频与 12 维 force 序列，损失为 $\mathcal{L}_{\text{joint}}=\|u^v_\psi-(\xi^v_1-\xi^v_0)\|^2+\lambda_f\|u^f_\psi-(\xi^f_1-\xi^f_0)\|^2$；video token 与 force token 拼接后在同一 DiT self-attention 内双向交互，而非把力当作外部条件。
- **Label（标注可执行动作）**：同一个 unified progress-action model（DINOv2 视觉通路 + MLP 触觉通路，双 head 输出 action 与 progress）对 imagined 片段回标 corrective action 与 progress，imagined corrections 一律赋 $y=1$，作为正向 recovery supervision。
- **Knowledge-insulated post-training**：基于 $\pi_{0.5}$（PaliGemma 2B backbone + 300M action expert）。VLM prefix 表征前置 stop-gradient，force history 与 advantage 经 adaRMSNorm 只注入 action expert；只更新 tactile encoder、adaptation layers、action expert，vision/language backbone 冻结。训练目标为 advantage-conditioned flow matching，$c_{\text{adaRMS}}=c_t+\lambda_f c_f+\lambda_a c_a$，配 classifier-free guidance（条件 dropout 0.1），推理时以正 advantage 条件诱导高 progress 的 recovery 行为。
- **实验设置**：Franka Research 3 + 双指 Xense 触觉传感器（6D force/torque）+ 前视 RealSense D455；六个 contact-rich 任务（Insert Flower / Wipe Whiteboard / Twist Bottle Cap / Play Xylophone / Toast Bread / Move Hanoi Rings），每任务 50 条 SpaceMouse 遥操演示，2 轮迭代，每方法每任务 40 次独立评测。
- **关键消融**：去掉 tactile generation 成功率跌至 28%，去掉 labeling 阶段的触觉输入跌至 65%（完整 82%）；去掉 advantage-conditioning 在 Insert Flower 从 93%→83%、Wipe Whiteboard 65%→56%；把 anchor 换成均匀随机采样跌至 78%/25%——说明「在哪里想象」和「是否用失败信号」都是必需的。real-to-imagined 数据比例从 1:2 提到 1:8/1:10 仍持续涨点。

## 与 STL×VLA 主线的关联
TACO 的 Recognize 步骤本质上是在 rollout 上做一次**时序谓词监控**：用学到的 dense progress $p_t$ 检测「进度在窗口 $\Delta$ 内未增长」（$p_{t+\Delta}-p_t<\epsilon$）来定位 failure-adjacent 状态——这在语义上非常接近 STL 里对 progress monotonicity 的 always/eventually 规约，但它是**学出来的标量**（progress target 来自人工标注的 task-stage 标签），既没有形式化语法、也没有 robustness degree，$\epsilon$ 与 $\Delta$ 纯属超参；而 anchor 选择消融（均匀采样导致成功率从 93% 跌到 78%）恰好说明「监控信号定位得准不准」直接决定纠错数据的价值，正是 STL robustness 可以替换 binary advantage $y_t\in\{0,1\}$ 提供连续、可组合、可解释信号的切入口。

与 runtime monitoring 的核心差异在于**闭环发生在训练时而非部署时**：论文在 Limitations 中明确承认 imagined corrections 是 offline 生成的、而非部署中在线生成，因此 TACO 是一个 world-model-as-post-training-harness，而不是 runtime shield——failure 仍然真实发生过一次，只是不再需要人来纠。这与「STL 监控器在线判违约并触发修正」是互补而非重叠的：TACO 提供了把违约片段转成可执行纠错监督的完整机械装置，缺的是一个 principled 的违约判据。

触觉模态之外留下的空间也很明确：TACO 的 world model 已经能联合生成 video 与 12 维 force-torque 轨迹，这意味着**力信号本身已成为可预测、可写谓词的一等信号**（例如 $\square(|F|<F_{\max})$ 或 $\lozenge_{[0,T]}(F_z>F_{\text{contact}})$），但论文全程没有任何安全约束或力上界规约，成功判据是每任务人工写的 stage 描述；同样，progress 标签靠人工标注 task stage，这正是 STL 公式可以自动生成 stage/progress 监督、免去人工标注的位置。另外，knowledge-insulated adaptation（stop-gradient 隔离 VLM backbone + adaRMSNorm 注入条件）与触觉本身无关，是任何 constraint-conditioned 或 robustness-conditioned VLA post-training 都可直接复用的训练配方。
