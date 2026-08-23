# RoboUniView: Visual-Language Model with Unified View Representation for Robotic Manipulation

## 主题
Unified view representation VLA

## 背景
用 VLM 做机器人操作是新范式，目标是提升对新物体/新指令的泛化能力。但不同机器人平台的相机规格和安装位置差异巨大，导致现有 imitation/RL 方法跨平台性能波动很大——模型难以从不同视角的图像里准确理解真实物理空间，从而影响动作预测。作者验证 SOTA 方法 RoboFlamingo 仅改变推理时相机参数，成功率就从 86.3% 掉到 80.8%。

## 现有局限与研究问题
- **Limitation:** 现有方法的视觉特征与相机参数强耦合，换相机即失效；RT-X 靠堆更多数据缓解，3D Diffusion Actor 靠额外注入 depth/点云，二者都显著增加数据采集或硬件成本。已有的 view transform 工作（RVT/VIHE/BEVFormer 等）依赖真实 depth 且仍停留在 perspective view，视觉特征与动作空间不对齐。
- **Problem:** 能否把"视觉特征提取"与"动作学习"解耦，先从多视角图像学到一个不受相机参数约束、与动作空间对齐的统一 3D 视图表示，从而在不同相机配置间泛化、并支持跨数据集联合训练？

## 贡献
- 提出 RoboUniView：带 unified view representation 的视觉-语言模型，把视觉特征提取与动作学习解耦，提升性能与对相机参数的泛化。
- 提出一种有效的预训练方法（3D occupancy 任务）来获得能更好理解真实物理世界的统一视图表示；预训练只需简单 RGB-D 图像，不需要人工标注（语义分割/物体/动作等）。
- 在 CALVIN benchmark 上大量实验取得 SOTA：D→D 成功率 93.0%→96.2%，ABC→D 92.2%→94.2%；并展示对未见相机参数、多相机参数数据集、跨任务联合学习的强适应性。

## 方法论
- **总体架构**：Vision Encoder（ViT + UVFormer）→ Feature Fusion Decoder（融合语言 token）→ Policy Head 输出 7-DoF 末端位姿 + gripper 状态。两阶段训练。
- **depth/3D 信息怎么进模型（核心）**：depth 不作为模型输入模态，而是作为**预训练阶段的辅助监督**注入。具体地，受 BEVFormer 启发设计即插即用插件 **UVFormer**：用网格状的 UniView Queries（空间形状 L×B×P，L=B=20，每个 pillar cell 对应真实世界 0.05² 米、垂直方向 0.5 米内均匀采 P 个 3D 点）+ 相机参数 Cam，通过 Spatial Cross-Attention（Deformable Attention，每个 query 只与其 P 个 3D 点投影到的像素特征交互，Proj 透视变换）+ Self-Attention，把多视角 ViT 特征转成统一 3D 视图表示 UF_t（L×B×P 的 3D 网格）。相机参数即通过此投影显式编码进表示。
- **预训练阶段（监督在这里起作用）**：在 CALVIN 仿真里采集多视角 RGB-D 图像，连同相机参数生成 RGB-enriched 点云并体素化，得到 Calvin_rgbd 数据集。UVFormer 输出经一个纯卷积的极简 **Occupancy Decoder**，预测每个网格 cell 的 occupancy 与 RGB 值。损失 l_pre-train = λ_rgb · L1(RGB) + 交叉熵(occupancy)。即用 3D occupancy + RGB 重建作为辅助任务，迫使统一视图表示编码真实 3D 几何，而非真把 depth/点云喂给主干。
- **微调阶段**：冻结 Vision Encoder（UVFormer 权重 copy 并 frozen），只微调 Feature Fusion Decoder（Cross-Attention 用语言 token 作 query，UF_t 与 wrist 特征作 key/value）和 Policy Head（MaxPooling + LSTM + MLP）。用 imitation learning：相对位姿用 MSE，gripper 用 BCE。wrist 视角缺失时可从其它视角重建虚拟 wrist 特征。
- **训练阶段数 = 2**（pre-train on 3D occupancy → fine-tune on action data）。
- **相比纯 RGB VLA 的量化增益**：CALVIN D→D 成功率 93.0%→96.2%、平均序列长 3.300→3.855；ABC→D 92.2%→94.2%、3.270→3.647。消融（Table 3）显示统一视图表示价值：U1 baseline 0.860 → U2 from-scratch 0.893 → U3 预训练+微调 0.912 → U4 预训练+冻结 0.954（task1 成功率）。未见相机参数下（D→D_uc）从 baseline 0.808 提升到 0.956，且波动极小（<0.004 vs baseline 最高 0.177）。
