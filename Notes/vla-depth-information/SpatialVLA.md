# SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model

## 主题
Spatial representations for VLA

## 背景
Generalist robot policy 的主流范式是在 cross-embodiment 数据上微调 VLM（如 PaliGemma2）得到 VLA model。但现有 VLA 大多只吃 2D RGB 观测，缺乏对 3D physical world 的结构化感知，而人类操作时天然依赖丰富的空间心理表征。本文主张 spatial understanding 是 robot manipulation 的关键，并基于 PaliGemma2 提出 SpatialVLA，把 3D 空间表征注入 VLA。

## 现有局限与研究问题
- **Limitation:** 现有 VLA 受限于 2D 观测输入，缺乏对 3D 世界的精确感知；不同 robot 的相机安装位置各异（wrist / third-person），观测在 3D 上不对齐（non-3D-aligned）；不同机器人自由度/控制器/工作空间不同，动作空间异构，难以学到可迁移的 generalizable spatial action。
- **Problem:** 如何用 3D 物理世界的深层空间理解来武装 VLA model，并让 observation 与 action 表征在跨本体（cross-embodiment）下空间对齐、可迁移。

## 贡献
- 提出 SpatialVLA：探索 spatial representations 的 generalist robot policy，建立在 vision-language model 之上。
- **Ego3D Position Encoding**：把 3D 空间上下文注入观测，无需 robot-camera 外参标定，普适于不同本体。
- **Adaptive Action Grids**：按数据集动作统计分布自适应离散化连续动作为 spatial action tokens，对齐跨机器人动作与 3D 空间结构；post-training 时可对 grid 重离散化以快速适配新本体。
- 在 1.1M real robot episodes 上预训练，跨 7 类机器人场景、24 真机任务 + 3 仿真环境做了广泛 zero-shot 与微调评测，SOTA 性能且推理更快（~20Hz，每个动作 token 更少）。

## 方法论
- **整体**：SigLIP 提取 2D semantic features → Ego3D Position Encoding 注入 3D → PaliGemma2 backbone 自回归预测 spatial action tokens（每动作仅 3 个 token：ΔT、ΔR、G）→ 反 tokenize 成连续动作 A_t 控制机器人。预训练用 next-token 交叉熵目标。
- **Ego3D Position Encoding（depth/3D 怎么进模型）**：
  - depth 来自**单目深度估计**：用 ZoeDepth 估计深度图 D。
  - 用相机内参做**反投影 π⁻¹**，把每个像素恢复成 egocentric 3D 坐标系下的 3D 位置 p = {x, y, z}（egocentric 自我中心相机坐标系，**消除对 robot-camera 外参标定的依赖**，普适于任意本体）。
  - SigLIP 视觉编码器提取 2D 特征 X ∈ R^{d×h×w}，并算出对应的 3D 位置 P ∈ R^{3×h×w}。
  - **位置编码计算**：3D 位置 P 先过正弦函数 γ(·)，再过可学习 MLP，得到 3D position embedding P'；最终把位置编码**直接加到视觉 token 上**：**O_3d = X + P' = X + MLP(γ(P))**。这样 2D 语义 token 就携带了 3D 空间结构。
- **Adaptive Action Grids（动作表示）**：
  - 单臂 7D 动作 a = {x, y, z, roll, pitch, yaw, grip}，分三部分 a = {a_trans, a_rot, a_grip}。
  - 平移 (x,y,z) 转**极坐标 (φ, θ, r)**，解耦运动方向 (φ,θ) 与距离 r。
  - 对整个数据集混合统计 ΔT、ΔR，**拟合高斯分布 N(μ, Σ²)**，按等概率 1/M 把每个动作变量切成 M 个区间（自适应离散化，对方向 φ/θ 分更细的格以捕捉细粒度方向）；得到平移网格 M_trans = M_φ·M_θ·M_r、旋转网格 M_rot，配可学习 token embedding E_a = {E_trans, E_rot, E_grip}，总 token 数 V = M_trans + M_rot + 2。
  - 每个动作只需 **3 个 spatial action token**（对比 RT-1/RT-2/OpenVLA 的 7 个），推理更快（21Hz，RTX 4090 上 ~20Hz、8.5GB 显存）。
- **预训练**：从 PaliGemma2 起，在 **1.1M real robot demonstrations**（OXE 子集 + RH20T 数据集，按 OpenVLA 经验调混合比例，最终剔除 DROIDE）上跨本体预训练；64×A100 训练 10 天，batch 2048。仅用单个 third-person 相机构建 egocentric 3D 表征。
- **Post-training（适配新本体）**：Spatial Embedding Adaption——对新数据集动作分布拟合新高斯 N(μ_new, Σ_new) 并重新离散化构建新 action grids G_new；新 action token embedding 用与预训练 grid 的**三线性插值（trilinear interpolation）**初始化（按到相邻网格质心的归一化距离加权），冻结 text embedding 以保留指令跟随能力。
- **量化增益（vs 纯 RGB VLA）**：
  - SimplerEnv Google Robot（zero-shot）：Visual Matching 71.9% vs RoboVLM 56.3%（+15.6），Variant Aggregation 68.8% vs RT-2-X 64.3%（且参数 3.5B vs 55B）。
  - SimplerEnv WidowX：zero-shot 总体 34.4% vs RoboVLM 13.5%；微调 42.7%，"Put Eggplant in Yellow Basket" 达 100%。
  - LIBERO 微调平均 78.1%（排名第一），LIBERO-Spatial 88.2%。
  - Franka spatial prompt 任务 73% 准确率（OpenVLA +12%）。
  - 消融：去掉 ego3d encoding，Variant Aggregation 从 81.6% 掉到 68.9%、Visual Matching 70.7%→66.7%，证明 3D 注入对场景变化鲁棒性关键。
