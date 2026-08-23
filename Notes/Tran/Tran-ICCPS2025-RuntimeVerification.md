# Perception-based Quantitative Runtime Verification for Learning-enabled Cyber-Physical Systems

## 主题
Perception-based Runtime Verification

## 背景
深度神经网络 (DNN) 在安全关键的自动驾驶等应用中日益普及，但 DNN 在与物理世界交互时可能因未知不确定性而失效，从而威胁人身安全。现有的 Learning-enabled Cyber-Physical Systems (Le-CPS) 验证方法主要在设计阶段 (design time) 运行，依赖预定义的动态模型和全局视角，仅提供定性结果 (Yes/No/Unknown)，无法在运行时动态适应真实环境中的不确定性。本文首次提出基于感知 (perception) 的定量 runtime verification 方法，利用 ProbStar reachability 在运行时实时计算碰撞概率。

## 现有局限与研究问题
- **Limitation:** 现有 Le-CPS 验证方法仅在 design time 运行，依赖预定义的物理模型和有限的预选场景，只能给出定性 (qualitative) 的验证结果 (safe/unsafe/unknown)，无法量化安全违规的概率；同时这些方法假设结构化环境，难以应对动态变化的非结构化现实环境。
- **Problem:** 如何在运行时仅基于感知数据，对 Le-CPS 在动态非结构化环境中的安全性进行定量验证，实时计算碰撞概率，并同时考虑感知 (perception)、传感 (sensing) 和执行 (actuation) 的不确定性？

## 贡献
- 首次提出基于感知的定量 runtime verification 方法，利用 perception-based modeling 和 ProbStar reachability 实现 Le-CPS 的实时安全验证
- 在真实 F1Tenth 自动驾驶测试平台上成功部署和验证，涵盖多种驾驶场景（追尾碰撞、侧面碰撞、车道跟随、对向行驶等）
- 对准确性和计时性能进行全面评估：在 NVIDIA Jetson NX 上可在 0.25 秒内计算未来 100 个控制时间步的碰撞概率，在笔记本电脑上可缩短至 0.05 秒

## 方法论
- **Perception-based Runtime Modeling:** 使用概率性感知网络（YOLO 目标检测 + Monte Carlo Dropout 姿态估计）估计移动障碍物的位姿，建模为多元正态分布 N(μ_p, σ_p²)，同时捕获 aleatoric 和 epistemic uncertainty
- **Linearized Motion Model:** 基于估计的姿态，使用改进的 kinematic bicycle model 建立线性化离散状态空间模型 X_{k+1} = A_k X_k，通过引入方向分量 φ_x, φ_y 解决角度非线性问题
- **Probabilistic Initial Conditions:** 将感知、传感和执行的不确定性转化为初始状态的概率分布，使用 Taylor 展开进行误差传播，得到标准化的 ProbStar 初始集 Θ_0
- **ProbStar Reachability Analysis:** 基于初始 ProbStar Θ_0 递归计算可达集 Θ_k，通过半空间交集 (half-space intersection) 定义碰撞约束（基于车辆 bounding polytope 的 Minkowski 差），并行计算每个 ProbStar 满足碰撞约束的概率
- **Quantitative Verification Algorithm:** 区分 modeling timestep dt_m 和 reachability timestep dt_r（dt_m 可比 dt_r 小 10-1000 倍），在每个 dt_r 步计算碰撞概率，同时支持 verification-guided collision avoidance（评估不同转向角和制动力下的碰撞概率变化）
