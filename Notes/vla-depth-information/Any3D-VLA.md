# Any3D-VLA: Enhancing VLA Robustness via Diverse Point Clouds

## 主题
3D-aware VLA via point-cloud fusion

## 背景
现有 Vision-Language-Action (VLA) 模型通常只吃 2D 图像，空间理解能力受限于 2D backbone，在小物体、视角变化、遮挡等复杂场景下脆弱。作者做了一项 pilot study，横向比较不同 observation space 与视觉表征，发现把视觉输入显式 lift 成 point cloud 得到的 3D 表征，能比隐式/重建式空间先验（如 VGGT、depth-pretrained encoder）更好地补充对应的 2D 表征。论文目标是给已有 VLA backbone 提供一个可插拔的 3D 注入管线（plug-in pipeline），并解决 3D 数据稀缺与跨环境 domain gap 问题。

## 现有局限与研究问题
- **Limitation:** 隐式/重建式空间先验（VGGT、depth-pretrained encoder）依赖重建目标，缺乏精确 metric 对齐，处理 fine-grained 空间关系时不准、易产生空间幻觉；而直接把 depth 当成额外 image channel 输入（image-plane RGBD）会破坏 3D 数据固有的拓扑结构，2D backbone 难以从压扁的 depth map 推断遮挡关系与绝对尺度。
- **Limitation:** 3D VLA 面临三重瓶颈——(1) 相比海量 2D 图像，3D 数据极度稀缺；(2) 不同来源（simulator/sensor/model-estimated）的 3D 数据在噪声特性、尺度分布、几何 bias 上差异巨大（domain gap）；(3) 常需要高质量 depth（昂贵的 depth 硬件）。
- **Problem:** 如何把 3D 信息注入 VLA 以增强空间理解，同时对多样且带噪声/尺度偏差的 point cloud 保持鲁棒，并在部署时摆脱对昂贵 depth 传感器的依赖？

## 贡献
- 提出 **Any3D-VLA**：通过把视觉输入 lift 成 point cloud、做 3D compression、再融合 2D–3D 表征，给 VLA 提供一个通用、模块化、可插拔到已有 backbone 的 3D 注入框架。
- 针对 3D VLA 训练的 scaling 瓶颈与跨环境 domain gap，提出 **hybrid point-cloud training** 策略，并构建大规模 VLA RGBD 数据集（基于 Objaverse LVIS 子集，290 类、10,680 个 instance，仿真合成 + 多种 depth 模型估计）。
- 大量 sim 与真机实验验证。真机 zero-shot 平均成功率最高 62.5%，比最强 baseline SpatialVLA(33.3%) 高 **29.2 个百分点**；post-training 后最高达 **93.3%**。即使 depth 带噪或有尺度偏差仍鲁棒，并额外在 LIBERO/CALVIN 上验证泛化。

## 方法论
- **整体架构：** VLM (InternLM2 1.8B) + 条件 flow-matching action expert，经 Progressive Action Generation (PAG) 连接；沿用 GraspVLA 的 imitation learning + PAG 训练范式，输出连续 end-effector 动作 chunk。
- **Depth/3D 如何进入模型（核心 lifting 链路）：**
  1. **Lifting + 3D compression：** 用相机内参 (fx, fy, cx, cy) 把每个有效 depth 像素 (u,v,d) 反投影到相机坐标系 3D 点：x=(u−cx)d/fx，y=(v−cy)d/fy，z=d。为避免把全部点直接喂进 encoder，在 (x,y,z) 空间做 Sonata 式 grid/voxel 采样（voxel size 1cm），每个非空 voxel 只保留一个代表点并继承 color/normal——把约 30k–60k 点压到约 3k–8k 点，得到紧凑且空间均匀的 3D 表示（即 "3D compression"）。
  2. **双编码器：** 压缩后的点云送入预训练 point cloud encoder **Concerto**（2D–3D 联合自监督预训练），输入点坐标 + 逐点属性（color、normal），输出逐点特征 f_i^3D（冻结大部分参数，只微调最后几层 sparse conv）；并行用 2D image encoder（DINOv2 + SigLIP，维度 1024+1152=2176）得到 patch-level token。
  3. **Patch-Wise Alignment：** 把每个 3D 点投影回图像平面 (u_i,v_i)=π(x_i)，按 ViT patch 网格离散化得到 patch index a_i；对落入同一 patch j 的点做 scatter-mean 聚合，得到 patch 级 3D 特征 g_j^3D；patch 内无点时用可学习 empty token e^3D。关键是在相机坐标系里做 native 3D 理解后再投回 2D patch，而不是在 image plane 上直接编码 depth。
- **2D–3D 融合机制：** 先经线性层把 g_j^3D 投到 token 维度 h_j^3D=W_3D·g_j^3D；与对应 2D token h_j^2D concat 后过小 MLP 得残差 δ_j=MLP([h_j^2D; h_j^3D])；再用 **gated residual fusion**：h_j^fused = h_j^2D + σ(g)·LayerNorm(δ_j)，其中 g 是可学习标量门控，初始化为 −2.1972 使训练初期 σ(g) 很小。设计上把 3D 表征当作对 2D 表征的"修正"而非替换，保护预训练 2D 表征不被破坏。融合 token + 语言 token + proprioceptive token 一起送入 VLA backbone。
- **训练：** 联合 GRIT grounding 数据集与合成 RGBD 数据集；VLM 自回归预测离散 bbox/grasp pose token，flow-matching action expert 生成连续动作。**不**对 depth/point cloud 加显式重建损失，性能增益只通过融合特征 h_fused 体现，确保增益来自更好的空间观测与表征。
- **Hybrid point-cloud training：** Setting 1 仅 simulator GT 点云；Setting 2 从头训于混合源（每条轨迹按固定概率选 simulator/sensor 点云或单帧 RGB 估计的 metric 点云，混合比 Simulator/Sensor 30% / UniDepthV2 30% / Depth Anything 3 20% / MapAnything 20%）；Setting 3 仅 sensor 点云。Setting 2 让模型见过各类点云，学到对 depth 来源不变的几何模式，从而容忍尺度偏差与 model-estimated 点云的不完美。
- **相比纯 RGB VLA 的量化增益：** Pilot study（Table 2，仿真）point cloud–2D patch fusion 最佳，Single-Trial SR 61.1 vs 2D-only 45.3（+15.8）、vs 次优 image-plane RGBD 56.8（+4.3）；Ablation（Table 6）2D-only 45.3 / 3D-only 44.2 → full 2D–3D fusion 61.1，说明 2D 语义与 3D 几何的恰当融合才是关键。真机 post-training（Table 3）Setting 2 + DA3：Task1 93.3% / Task2 86.7%，远超 π0.5、GraspVLA、SpatialVLA。LIBERO 比 GraspVLA 高 13.9%；把 3D 分支插入 π0.5 后 LIBERO 平均 82.9→87.1(DA3)/87.3(Sim)、CALVIN 平均长度 3.22→3.41/3.43。推理 3D compression 后 RealSense 2.0 FPS / DA3 1.7 FPS（2D baseline 3.0 FPS），开销可接受。
