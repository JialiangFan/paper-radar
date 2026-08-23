# AugVLA-3D: Depth-Driven Feature Augmentation for Vision-Language-Action Models

## 主题
Sensor-free depth augmentation for VLA

## 背景
当前 Vision-Language-Action (VLA) 模型（如 OpenVLA、π0、GR00T）大多继承自用 2D 图像训练的 VLM，依赖纯 2D 视觉特征。这类特征语义对齐能力强，但缺乏显式的 3D 结构感知，难以推理深度、几何与空间关系。已有的 3D-enhanced 方案要么需要昂贵的大规模 3D embodied 数据（3D-VLA、SpatialVLA），要么依赖 LiDAR 等专用传感器（PointVLA），无法复用驱动 VLA 成功的海量 2D 语料。

## 现有局限与研究问题
- **Limitation:** 主流 VLA 受限于 2D 表征，缺乏显式 3D 几何推理，在碰撞规避、物体堆叠、可达性分析等需要精细空间推理的任务上表现不佳；而引入 3D 的现有方法依赖专用 3D 传感器（如 LiDAR）或大规模 3D 数据集，限制了适用域、可扩展性，且无法复用 2D 语料。
- **Problem:** 如何在不需要任何专用 3D 传感器（sensor-free）、且保持与大规模 2D 训练管线兼容的前提下，把可靠的 3D 结构特征注入 VLA，从而提升其空间推理与鲁棒性？

## 贡献
- 提出一种 **sensor-free 3D 特征提取方法**：用深度估计模型 **VGGT** 把 2D RGB 图像转成 point cloud，再用 **PointNet** 抽出 compact 几何特征来增强原始 VLA，从而无需 3D 硬件即可在规模化的 2D 数据上训练。
- 设计 **Action Assistant** 模块（镜像 Action Expert 但参数更少）：作为 task-guided 正则器，用 action priors 约束所学的 3D 表征，保证其与下游控制任务一致、避免直接注入原始几何信号导致的优化不稳与性能退化。
- 在真实灵巧手（ROH-A001，5 个任务）与 RoboCasa/robocasa-gr1-tabletop-tasks 仿真（24 任务）上验证：在受限算力（单张 RTX 4090、仅用 10% 数据、1 epoch）下仍稳定超越 GR00T 与 Diffusion Policy，仿真平均成功率从 GR00T 的 50%（100 demos）提升到 54%。

## 方法论
整体 backbone 沿用 GR00t（Eagle-2 VLM + Action Expert，diffusion 风格 action head），核心是「3D Feature Injection 框架」，分两条线：

- **Depth → 3D 特征（sensor-free，公式 1）：** 输入 N 张 RGB 观测 $\{I_i\}_{i=1}^N$（单视角时 N=1），用冻结的 **VGGT-1B**（state-of-the-art 单目深度估计）预测 dense depth，按已知相机内参反投影成 camera-centered point cloud $P$；经离群点过滤、归一化、采样算子 $\mathcal{S}$ 降到 $M'$ 个点得 $\bar P$，再用 **PointNet** 编码成 compact 几何描述子 $f_{3D}=\text{PointNet}(\bar P)\in\mathbb{R}^{M'\times C}$。整条链路只用 RGB，不需要 LiDAR/深度相机，因此能在已有海量 2D 语料上复用、规模化训练。
- **3D 特征注入主 Action Expert：** 把 PointNet 特征与 Action Assistant 的中间激活，注入到主 Action Expert 对应层（图 2 中通过 Adapter 接到各 Attention Block），与 2D 视觉 token 融合，实现 2D 语义与 3D 几何的紧耦合多模态融合。
- **Action Assistant（task-guided 正则，公式 2）：** 一个结构与主 Action Expert 一致但参数显著更少的 auxiliary expert，采用 compact transformer-diffusion（降隐藏维、denoising 步间共享权重、缩短 diffusion horizon）。它把 PointNet 抽的 3D 特征转成 action-relevant embedding，并对主 backbone 做 layer-wise 注入：$\tilde h^{(l)} = h_{\text{orig}}^{(l)} + \alpha^{(l)}\cdot\mathcal{T}(h_{\text{aux}}^{(l)}, f_{3D})$，其中 $\alpha^{(l)}$ 为可学习标量门控，$\mathcal{T}(\cdot)$ 用轻量投影或 cross-attention 实现平滑对齐。关键设计：Assistant 生成的 auxiliary action **只用于计算 auxiliary loss 来约束 3D 特征学习，绝不直接更新机器人电机指令**，因此主策略保留完整控制权，仅借其正则提升稳定性。
- **生效阶段：** 3D 增强与 action-guided 正则都作用于 **training 阶段**（VLM、VGGT 冻结，主要训练注入模块/Adapter/Action Assistant）；推理时主 Action Expert 独立输出动作。
- **Intropy 分析：** 在 Intropy 框架下，depth-derived 特征注入 dense、task-relevant 信息提升 intelligence gain $\delta S$，几何对齐的 action-assisted 正则用物理上有意义的结构约束优化、提升有效 resistance $R$，从而提高 Intropy（$dL=\delta S/R$），得到更鲁棒、可泛化的 3D 操作。
