# How VLAs Fail Differently - Black-Box Action Monitoring Reveals Architecture-Specific Failure Signatures

> 作者: Krishnam Gupta (2026, arXiv 2605.28726)

## 主题
Black-box VLA action monitoring

## 背景
VLA 模型端到端从视觉与语言预测机器人动作，但从模型输出层到电机之间发生了什么几乎无人系统研究：OpenVLA 的部署脚本把原始输出直接送给电机且零边界检查，pi0 通过 WebSocket 流式发送动作而不做校验，LeRobot 的 `EEBoundsAndSafety` 处理器则是命令式、不可组合且容易被省略。业界的隐含假设是「好模型自然产生安全动作」。作者在 PushT 与 ALOHA 14-DOF 双臂操作两个任务、VQ-BeT / Diffusion Policy / ACT 三种架构、共 450 个 episode 上做黑盒动作监控，发现 VLA 在电机指令层的失败方式是架构特异且可预测的。

## 现有局限与研究问题
- **Limitation:** 现有安全工作要么是 training-time（SafeVLA、RobustVLA 需重训）、要么是 inference-time 但依赖动力学模型或架构内部访问（AEGIS 的 CBF-QP、SafeDiffuser/CoDiG 的扩散内嵌 barrier、SafeDec 的解码约束），要么是 failure detection 但需要训练辅助模型和模型内部特征（SAFE、FIPER、Sentinel）。真正 training-free、无需模型访问的动作空间监控几乎空白。
- **Limitation:** discrete/continuous 的 VLA 架构划分早已众所周知，但没有任何前人工作在**同一任务、同一评测协议**下实证比较过监控器在不同架构族之间的有效性，也没有回答「哪种监控信号能预测哪种架构的失败」。
- **Problem:** 部署代码中最常见的安全机制——速度违规检查——到底有没有失败预测能力？是否存在通用监控器，还是必须按架构族匹配监控器？

## 贡献
- 提出 **SafeContract**：training-free、黑盒（无需模型访问、无需重训）的动作监控与强制执行工具包，带 conformal calibration 与 CUSUM 漂移检测，单次推理开销 <13 µs（占 VLA 推理时间 <0.001%），已开源。
- **通用失败预测器**：direction reversal rate（动作换向比例）是唯一在三种架构上都有效的监控器，AUROC = 0.93 (VQ-BeT) / 0.79 (Diffusion) / 0.91 (ACT)，均 p<0.001；高换向率表示策略在振荡而非推进，是架构无关的「犹豫」signature。
- **discrete→continuous 梯度**：jerk 监控只对离散 token 架构有效，AUROC 从 0.88 (VQ-BeT) → 0.69 (ACT，chunk 边界效应) → 0.41 (Diffusion)，该梯度反映动作生成机制而非任务差异。
- **对最常用安全机制的强负面结果**：velocity violation 在所有架构上都不具预测性（AUROC 0.41–0.69）；对连续族尤其失效（ACT 0.52 = 随机、Diffusion 0.41 = 低于随机）。ACT 有 38%（19/50）失败率，但失败是**行为性**的——动作物理上完全合法却指向错误目标，速度检查完全看不见。
- **two-family 模式**：discrete family（autoregressive、VQ-VAE）因量化产生高 jerk / 高换向 / 速度尖峰，jerk + reversal 强预测（AUROC>0.85）；continuous family（diffusion、flow matching、action chunking）轨迹平滑、主要失败是行为错误，reversal 仍有效但 jerk 掉到随机水平。同任务同数据下 VQ-BeT 的速度违规是 Diffusion 的 2.4 倍（1847 vs 772），平均 jerk RMS 高 2.7 倍（21.6 vs 8.0），而 stall step 几乎为零（1 vs 117）。
- 给出可操作的**架构匹配监控建议表**：Diffusion 用 reversal + momentum coherence（避开 jerk/velocity/spectral）；VQ-BeT 用 reversal + jerk（避开 stall）；ACT 用 reversal + momentum/spectral（避开 velocity/stall）。

## 方法论
- **Safety contract**：契约 C = (l, u, v_max) 指定 per-joint 上下界与速度上限。执行时先裁剪到边界、再钳制速度、然后重新裁剪（因为速度钳制可能把动作推出边界）。所有违规带 timestep、维度、幅值记录日志。
- **Conformal calibration**：手调阈值不可靠（v_max=0.05 会裁掉相当比例的 expert 动作）。改用 split-conformal：示范 episode 按 80/20 分割，在校准集上算 nonconformity score，取 (1−α)(1+1/n) 分位数得到有限样本覆盖保证。α=0.05 时实现 97.9% holdout coverage，且比 4σ 启发式收紧 25%。速度上限取 per-joint 连续动作差分的 99 分位。
- **五个 per-episode health metric**：(1) direction reversal rate = 动作换符号的 (timestep, joint) 对占比；(2) jerk RMS = 动作轨迹三阶导的均方根；(3) momentum coherence = 相邻动作差分的余弦相似度（衡量轨迹平滑性）；(4) spectral energy ratio = 低频能量占比；(5) stall detection = 连续位移低于阈值 τ 的步数。每个指标按 episode 计算并与任务成功率做 AUROC 关联。
- **CUSUM shift detection**：conformal p-value 输入 CUSUM 检测器 S_t = max(0, S_{t−1} + 1[p_t<α] − α)，S_t > h 时报警，具备形式化的误报率界（ad-hoc EWMA 无法提供）。
- **实验设计**：同数据集跨架构对照（PushT，seed 0–199，contract 边界 [0,512]，v_max=30 px/step，成功判据 coverage ≥0.95，n=200/条件）隔离架构效应；再泛化到 ACT/ALOHA 14-DOF cube transfer（n=50）。平台 NVIDIA A40 + LeRobot 预训练 checkpoint。
- **无退化验证**：450 个 episode 上 SafeContract 的监控与强制执行未造成统计显著的任务退化（Fisher p = 0.92 / 0.76 / 0.68），说明 conformal 边界足够紧以提供信息、又足够松不裁剪正确动作。

## 与 STL×VLA 主线的关联
这篇文章的 safety contract 本质上是一组**动作空间的时不变安全不变量**——G(l ≤ a_t ≤ u) 与 G(|Δa_t| ≤ v_max)——但作者完全没有用时序逻辑的形式化语言表述，也没有 robustness semantics、没有嵌套时序算子（until / eventually within window），因此它是「conformal 校准的阈值监控 + CUSUM 统计报警」，而非 STL runtime monitoring。它确实**既检测又干预**（裁剪边界、钳制速度），干预层次在最内层，作者明确说 SafeContract 只是 monitoring infrastructure、可与 CBF 类约束组合，不构成 safety guarantee。

与 STL 主线最直接的接口在于它的负面结果：纯 pointwise magnitude 约束（速度）不预测失败，真正有预测力的是**轨迹形状类**指标——direction reversal rate（振荡模式）、momentum coherence（方向一致性）、stall detection（缺乏进展）。这些恰恰是自然的时序性质：振荡对应「有界窗口内反复穿越」、stall 对应 F_[0,T](progress)、coherence 对应窗口内的方向持续性，但论文只把它们做成 per-episode 的标量统计量再算 AUROC，丢掉了时序结构与何时违反的定位信息。用 STL 把这几个 signature 写成带时间窗的公式并取 robustness 作为连续失败分数，是一条明确且论文自己没走的路。

另一个 gap 是论文承认的盲区：动作空间监控对**语义正确性**完全无效——ACT 的失败是「物理合法但指向错误目标」，semantic correctness 是 (action, observation, instruction) 三元组的性质而非动作本身的性质。这正好是 STL over 观测/任务级信号（而非纯动作信号）能补上的位置，也是 STL×VLA 相对纯动作监控的差异化理由。
