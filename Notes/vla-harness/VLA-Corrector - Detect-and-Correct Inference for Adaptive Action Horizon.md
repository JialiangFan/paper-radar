# VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon

> arXiv: 2607.01804 | 年份: 2026

## 主题
Adaptive action horizon via detect-and-correct

## 背景
主流生成式 VLA 策略采用 action chunk 机制：一次前向推理预测未来动作序列，并在固定 action horizon *H* 内以开环（open-loop）方式连续执行，以此摊薄策略调用成本并保持时序平滑。但这种"predict-then-blindly-execute"范式牺牲了闭环反应性：在 horizon 内新观测持续到达却被忽略，形成 open-loop blind spot。在 contact-rich 操作中，微小的局部扰动会在这一盲区内被迅速放大为 compounding error，最终导致任务失败。作者在 π0.5、SmolVLA、X-VLA 三个 backbone 上系统量化了这一 performance–efficiency 权衡：以 π0.5 为例，增大 horizon 可将策略调用次数降低约 4×，但成功率从约 64% 跌至 49% 以下。

## 现有局限与研究问题
- **Limitation:** 固定 action horizon 在两个极端间强制取舍——*H*=1 完全闭环但每步都要跑一次完整 VLA 推理，抵消了 chunking 的效率收益；大 *H* 摊薄计算却扩大盲区，让误差静默累积。由于最优 horizon 依赖任务难度、环境动态与 sim-to-real 差异，不存在跨场景通用的静态取值。
- **Problem:** (1) 如何**及时检测执行偏差**并在误差累积到不可恢复之前**终止 stale actions**；(2) 截断之后如何**纠正轨迹**——朴素 replanning 往往不够，VLA 可能在已偏离状态下重新生成同样失败的动作，使机器人再次被困。

## 贡献
- 系统量化了 action-chunked VLA 中固定 horizon 引发的 performance–efficiency 权衡，验证 open-loop blind spot 对鲁棒性的影响在不同 backbone 上普遍存在。
- 提出 VLA-Corrector：一个**不改动 backbone 权重**的轻量推理期框架，由 latent-space monitoring、event-triggered truncation 与面向恢复的 guided re-inference 三部分组成，天然诱导出 event-triggered 的**自适应 action horizon**。
- 在仿真与真机任务上验证其鲁棒性、success-per-call 效率与自适应纠正行为，并证明其可跨架构迁移。

## 方法论
- **外部 latent dynamics corrector 训练：** 先在 benchmark 训练集上微调 VLA，随后冻结 backbone，用其视觉编码器 *E* 抽取 latent。给定 transition (o_t, a_t, o_{t+k})，目标残差为 ΔZ*_{t+k} = Z^real_{t+k} − Z^real_t；训练轻量模块 M_φ 预测 ΔẐ_{t+k} = M_φ(Z^real_t, a_t)。预测**残差**而非绝对未来状态，可抑制静态场景内容、聚焦任务相关动态。损失兼顾幅值与方向：L_corr = ‖ΔẐ − ΔZ*‖² + β[1 − CosSim(ΔẐ, ΔZ*)]。实践中一个 40M 的 MLP 即足够。
- **Latent-space Vision Monitor (LVM) 在线检测：** 执行期虽不再查询策略，但新观测仍可用。计算实际残差 ΔZ^real_{t+k} 与期望残差 ΔZ^exp_{t+k}，取不一致分数 E_t = 1 − CosSim(ΔZ^exp_{t+k}, ΔZ^real_{t+k})，作为连续的视觉动态失配信号。
- **Event-triggered truncation：** 直接对 E_t 设阈值不稳定（瞬时离群会误触发）。改用滑动窗口的中位数 M_e 与 MAD 构造双自适应阈值 T_on = M_e + λ_on·MAD、T_off = M_e + λ_off·MAD（λ_on > λ_off，提供 hysteresis）；仅当 E_t > T_on 连续成立 *p* 步才触发 interrupt，孤立尖峰被忽略。触发后丢弃队列中剩余动作，实际 horizon 变为 H_adaptive = h < H。
- **Online Gradient Guidance (OGG) 纠正推理：** 仅作用于 interrupt 之后的那一次策略调用。在 flow matching 去噪步 τ，由速度场 v_τ 估计干净 chunk Â_0 = A^τ − τ·v_τ 并取首动作 â_t，预测其潜在效应 ΔẐ_act = M_φ(Z^real_t, â_t)。纠正方向定义为 ΔZ_corr = ΔZ_exp − ΔZ_dev，其中 ΔZ_dev = Z^real_t − Z^real_{t−k} 为累积偏差、ΔZ_exp 为 t−k 时刻预测的期望残差。以 L_OGG = 1 − CosSim(ΔẐ_act, ΔZ_corr) 的梯度修正速度场：v^guide_τ = v_τ − η∇_{v_τ}L_OGG。因修改的是速度场而非直接扰动动作坐标，与原 flow-matching 过程兼容，纠正更平滑。

## 实验与关键数字
- **评测设置：** MetaWorld、LIBERO 与真机 AgileX PiPER 6-DoF；主 backbone 为 π0.5，另用 SmolVLA / X-VLA 做跨架构评测。
- **MetaWorld 跨架构（Table 1，平均成功率 %）：** π0.5 48.70 → 64.35（+15.65）；SmolVLA 61.90 → 66.65（+4.75）；X-VLA 55.55 → 59.60（+4.05）。最大增益出现在 π0.5 的 Very Hard 分档：41.0 → 65.0（+24.0）。
- **LIBERO 样本效率（Table 2）：** 全量微调 π0.5 平均 96.95；few-shot 微调 94.00；few-shot + VLA-Corrector 达 **97.80**（+3.80），**超过全量微调基线**。Long 分档 86.6 → 93.4（+6.8）。
- **Success-per-call 效率（Table 4）：** 最大相对效率增益为 π0.5 +29.9%、SmolVLA +45.3%、X-VLA +39.1%。π0.5 @ horizon 50：成功率 48.72 → 58.70，平均策略调用 5.15 → 4.98（+24.6%）。SmolVLA @ horizon 10：61.90 → 73.00，调用 19.27 → 15.64（+45.3%）。效率增益在长 horizon 处更大。
- **Corrector 数据效率（Table 3，horizon 50）：** 基线 48.72；r=0.2 → 48.32（−0.40）、r=0.4 → 49.15（+0.43）、r=0.6 → 52.20（+3.48）、r=0.8 → 52.26（+3.54）、r=1.0 → 54.32（+5.60）；在 r≈0.6–0.8 已趋饱和，呈现明显递减收益。
- **机制分析：** 83.7% 的截断发生在 critical phase（精细抓取、对准），仅 16.3% 在 non-critical phase，即关键阶段的截断频率是非关键阶段的 5.1×；失败 episode 的 E_t 分布具有更重的高分尾部并触发更多 interrupt。OGG 使 post-interrupt 恢复率在各难度均提升（Easy +0.28、Medium +0.13、Hard +0.22、Very Hard +0.30，Overall +0.23；恢复判定为 interrupt 后 10 步内 E_t < T_off）。
- **真机（Table 5，AgileX PiPER，3 组任务 × 3 任务 × 20 trials，95% 二项置信区间）：** Pick-place 70.0±11.6 → 78.3±10.4（+8.3）；Alignment 56.7±12.5 → 73.3±11.2（+16.6）；Disturbance recovery 40.0±12.4 → 68.3±11.8（+28.3）；平均 55.6±7.3 → 73.3±6.5（+17.7）。增益在在线扰动场景最大。
- **消融（Table 6/7）：** 仅 truncation 即把平均成功率从 48.70 提到 60.35（+11.65），再加 OGG 到 64.35（+15.65）；检测器设计上，解耦的外部 LVM + OGG（64.35）显著优于在 backbone 上加辅助头的耦合方案（49.55，+14.80），说明内部辅助目标会干扰 VLM-to-action 的表征。灵敏度分析表明适中的 guidance strength 与 40M 的 LVM 已足够，进一步增大监控器收益有限。
