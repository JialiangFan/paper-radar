# ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models

> arXiv: 2606.09740 | 年份: 2026

## 主题
Training-free VLA failure recovery

## 背景
Vision-Language-Action (VLA) 模型主要通过在大规模专家演示上做 behavioral cloning 训练，在训练分布内的语言条件操作任务上表现强劲，但在 out-of-distribution (OOD) 扰动下极为脆弱：光照变化、相机视角改变、纹理替换或初始状态的微小偏移都可能让成功率骤降。作者将这种脆弱性归因于 behavioral cloning 目标导致的过拟合——策略不再基于当前视觉上下文做主动空间推理，而是回放记忆中的运动学轨迹，即所谓 "memory trap"。作者的 probing 实验进一步表明，失败瓶颈并不在感知：VLA 的视觉主干在扰动场景下仍维持准确的目标空间表征，崩溃发生在 action head 从特征到运动指令的投影环节。

## 现有局限与研究问题
- **Limitation:** 现有的 inference-time 纠错方法（online corrections、外部 VLM 推理模块、visual symbols、显式 3D 重投影）引入了显著的结构性开销，依赖外部感知硬件或外部推理模型，并往往完全接管 VLA 的原生动作流；传统失败恢复路线（TAMP、behavior tree 反应式重规划、recovery RL）则要求严格的环境建模、已知失败概率或昂贵的失败案例训练数据。
- **Problem:** 在不修改预训练 VLA 权重、不引入额外演示、不依赖外部 3D 传感器或外部推理模块的前提下，能否仅利用 VLA 自身的内部隐状态作为几何参考，在运行时检测并恢复抓取与放置失败？

## 贡献
- 提出 PROBEACT：一个轻量、闭环、training-free 的 inference-time 干预框架，直接从冻结 VLA 的隐状态中提取稳健的 3D 几何参考，彻底消除外部视觉传感器的结构性开销。
- 设计 object-agnostic kinematic state machine 与 hierarchical Control Barrier Function (CBF) filter 的耦合：将相对空间同步性转化为闭式动作投影，自主把策略从灾难性失败循环中救出，同时保留 baseline 能力。
- 在 LIBERO-plus 上的系统评估显示，跨多种视觉与空间扰动类别取得一致的成功率提升，全部在推理时完成，无需 VLA 权重修改、外部推理模块或额外演示；同时验证该方法对 base 与 fine-tuned VLA 策略均适用。
- 定量刻画了 VLA 的 OOD 失败机理：隐状态仍保留正确空间信息，而动作端点已漂移，为 "读取隐状态 + 最小修正" 的设计提供了实证基础。

## 方法论
- **整体架构**：在冻结的 VLA 旁并行运行三个模块——(1) 感知：内部 probe 从中间 LLM 激活提取稳定 3D 物体轨迹；(2) 逻辑：kinematic state machine 通过相对 object-robot 同步性检测物理执行失败；(3) 控制：hierarchical CBF filter 对 nominal action $a_t$ 做最小闭式投影，得到安全动作 $a_t^{cbf}$。
- **Multi-Target Hidden-State Probe**：多头 MLP $\phi: \mathbb{R}^{d_{pca}} \to \mathbb{R}^{K\times 3}\times\mathbb{R}^{K}$。特征取自 VLA 第 8 层，把 16×16 空间 token 平均池化为 4×4 的 4096 维向量网格，再经 PCA 降到 $d_{pca}=1024$。probe 为 4 层 MLP，隐层维度 [2048, 1024, 512, 256]，每层接 LayerNorm + ReLU + dropout ($p=0.1$)；每个预测位置附带 sigmoid 置信度 $c_k$，$c_k<0.5$ 的预测被丢弃。
- **Hungarian matching 训练与在线身份跟踪**：每帧物体数可变（1 到 $K$），用二部图匹配损失（定位 L2 + 置信度 BCE，权重 $\beta$）训练，因此 probe 输出是 permutation-invariant 的、槽位无时序一致性。推理时沿时间轴做 online Hungarian matching，按成对欧氏位移最小化把新预测分配到已有轨迹；用基于最大合理帧间物体速度的空间门限抑制错误 ID 切换，未匹配的预测自动生成新轨迹。
- **Object-Agnostic Kinematic State Machine**：围绕六个机械阶段（APPROACH、MONITOR、GRASPING、POST GRASP 等）与一个 PLACED 事件设计，仅使用 object-agnostic 信号：夹爪宽度 $q$、末端位姿 $\mathbf{e}=(x_e,y_e,z_e)$ 与 probe 跟踪的物体位置；阈值只依赖 embodiment 级硬件容差（如 nominal lift clearance），不做任务特定调参。
  - **抓取校验**：在滚动观察窗内计算相对竖直位移 $\Delta z_e$ 与 $\Delta z_{obj}$，只有夹爪稳定在机械最小值之上（$q>\epsilon_{limit}$）且两者同步正向位移超过硬件噪声底（$\Delta z_e>\tau_{lift}$ 且 $\Delta z_{obj}>\tau_{track}$）才确认抓取成功，从而避免把空抓判为成功。
  - **两类抓取失败**：hard empty grasp（$q\le\epsilon_{limit}$，完全闭合无物）与 soft empty grasp（$\Delta z_e>\tau_{lift}$ 但 $\Delta z_{obj}\le\tau_{noise}$，运动学解耦证明未抓到物体）。
  - **中途掉落**：POST GRASP 阶段末端运动中夹爪宽度突然塌陷到机械极限，掉落位置随后被编码为 CBF zone 并触发返回原抓取目标的恢复动作。
  - **放置校验**：需同时满足三条件——夹爪宽度相对保持值增大（$q>q_{hold}+\epsilon_{release}$）、末端建立发散式回撤轨迹（$\|\mathbf{e}_t-p_{obj}\|>\|\mathbf{e}_{t-1}-p_{obj}\|$）、被持物体坐标稳定在目标位置容差内。
- **Hierarchical CBF Filter（两级策略）**：首次失败只执行无状态的 push-back，让 VLA 自行纠错；若在同一空间区域再次失败，才判定为 memory trap 并在失败坐标 $c$ 处实例化持久 CBF zone，barrier 函数 $h(x;c,r_{safe})=\|x-c\|^2-r_{safe}^2$，安全集 $\mathcal{H}=\{x:h(x)\ge0\}$。PRE_GRASP 阶段对 VLA 名义平移动作 $u_{vla}\in\mathbb{R}^3$ 施加一阶 CBF 条件 $\nabla h(x)^\top u \ge -\gamma h(x)$，通过 minimal-intervention QP 得到闭式修正 $u_{filtered}=u_{vla}+\max\left(0,\frac{-\gamma h(x)-\nabla h(x)^\top u_{vla}}{\|\nabla h(x)\|_2^2}\right)\nabla h(x)$，其中 $\nabla h(x)=2(x-c)$。若 VLA 动作本已满足安全边界，投影为零、filter 退化为恒等映射，从而保留 baseline 能力。安全区在末端进入真实目标终端邻域 $\rho_{close}$ 或触发 PLACED 时动态清空；GRASPING 与 TRANSPORTING 阶段主动旁路 filter 以允许物理接触。
- **多步任务支持**：对 "put both moka pots on the stove" 一类任务，解析语言关键词（both/two/and）分解为 $N$ 个 (pick, place) 子任务；PLACED 后把刚放置物体加入黑名单、重置 probe tracker、清空所有 CBF zone，再重入 PRE_GRASP，从而在复用同一检测基础设施的同时隔离子任务间的失败模式。

## 实验与关键数字
- **设置**：backbone 为 OpenVLA-OFT；benchmark 为 LIBERO-plus，覆盖七类扰动（Camera Viewpoints、Robot Initial States、Language Instructions、Lighting condition、Background Textures、Sensor Noise、Objects Layout），以 LIBERO 内建 goal predicate 判定成功。probe 训练数据为回放 baseline VLA 采集的 50,000 组 (hidden-state, object-positions) 对，物体位置取自仿真器 `obj_of_interest`；训练 200 epochs（AdamW，batch 512，cosine LR）。全部实验使用 2 张 NVIDIA RTX PRO 6000 (Blackwell) GPU。
- **主结果（Table 1，成功率 %）**：PROBEACT 总分 **74.1**，为所有对比 VLA 中最高，相对 OpenVLA-OFT 基线 69.6 提升 4.5 点。分项 PROBEACT vs OpenVLA-OFT：Camera 63.8 vs 56.4、Robot 40.3 vs 31.9、Language 82.0 vs 79.5、Light 93.6 vs 88.7、Background 93.5 vs 93.3、Noise 76.8 vs 75.8、Layout 80.9 vs 74.2。其他对比方法总分：OpenVLA 15.6、NORA 39.0、WorldVLA 25.0、UniVLA 43.9、$\pi_0$ 53.6、$\pi_0$-Fast 61.6、RIPT-VLA 68.4。
- **提升集中于几何分布偏移**：最大增益出现在 Robot Initial States (+8.4) 与 Camera Viewpoints (+7.4)，与 "memory trap / Phantom Grasp" 假设一致——策略识别到正确目标但运动执行塌陷到记忆中的训练均值。
- **对 fine-tuned VLA 的泛化（Table 2，Robot Initial States 类别成功率 %）**：在已用 LIBERO-plus 扰动数据混训的 OpenVLA-OFT-mixdata 上，PROBEACT 在四个 LIBERO suite 上一致提升——Spatial 30.6→32.6 (+2.0)、Object 23.9→30.7 (+6.8)、Goal 20.8→25.7 (+4.9)、10: 36.6→39.7 (+3.1)，平均 28.0→32.2。说明 mixdata 式训练"缓解但未消除"记忆导致的执行失败，PROBEACT 与数据侧方案正交而非替代。
- **动作输出漂移分析（Table 3，300 个 Objects Layout 扰动 episode，同一次 VLA 前向）**：hidden-state probe 误差 vs action endpoint 误差——All 6.9 cm vs 23.6 cm；Success 3.4 cm vs 7.8 cm；Failure 10.4 cm vs 34.9 cm。失败 episode 上端点漂移到距 GT 34.9 cm，而 probe 仍保持在 10 cm 量级，说明空间信息仍存在于中间表征中，失效的是特征到运动指令的投影。（正文对应处写作 "probe holds at 12.4 cm"，与表中 10.4 cm 不一致，属原文笔误。）
- **Probe 训练数据选择（Table 4，3D 位置回归 $R^2$）**：比较 img-spatial / img-mean / last token / lang-mean 四种池化在 layer 8/12/16/20/24/28 上的表现。img-spatial 在每一层都占优，且空间信息在浅-中层达峰、深层衰减。全局最优为 **layer 8 + image-spatial pooling，$R^2=0.968$**（同层其他池化 0.926 / 0.815 / 0.869；layer 28 的 img-spatial 降至 0.934），该配置被采用为全文默认。
- **步数效率（Table 5，libero-plus goal，共 2,591 个任务）**：两法都成功的 1,643 个任务上，baseline 114 步、PROBEACT 120 步，仅多 6 步（约 5% 开销）；PROBEACT 从 baseline 失败中救回的 151 个任务，从 600 步 timeout 降到平均 197 步（−403 步）；两法都失败的 724 个任务均为 600 步。全 benchmark 平均 PROBEACT 反而更少（255 vs 275 步，−20 步）。图 1 标注 probe 运行时开销 <3 ms per call。
- **局限**：验证目前局限于理想刚体动力学的仿真 benchmark；kinematic state machine 的 sim-to-real 可迁移性尚未验证，真实硬件的可变接触摩擦、软体形变与高频编码器噪声是否会破坏运动学同步信号，是物理部署前的必要前提。
