# Evo-0: Vision-Language-Action Model with Implicit Spatial Understanding

## 主题
Implicit 3D-aware VLA model

## 背景
Vision-Language-Action (VLA) 模型通常在预训练 VLM 上微调，但 VLM 基于 2D image-text pair 训练、缺乏 3D 监督，因此精确的 spatial understanding 不足。为弥补这点，近期方法（如 SpatialVLA、PointVLA、3D-VLA）显式注入 depth map 或 point cloud，但需依赖额外 depth 传感器或预训练 depth estimation 网络。

## 现有局限与研究问题
- **Limitation:** 现有 3D-aware VLA 依赖显式 3D 输入（depth/point cloud），需要专用传感器或辅助估计模型；depth 估计带来额外噪声、对相机视角变化敏感，限制了 scalability 与部署灵活性。
- **Problem:** 能否在仅输入 RGB 图像、不依赖 depth 传感器和显式 depth estimation 的前提下，为 VLA 模型隐式注入 3D 几何先验以增强空间理解？

## 贡献
- 提出一个 plug-and-play 模块，借助 Visual Geometry Foundation Model（VGGT）隐式注入 3D 几何先验，无需 depth 传感器或显式 depth 估计即可增强 VLA 的空间理解。
- 在 5 个 RLBench 仿真任务 + 5 个真实世界操作任务上评测，相比强基线（OpenVLA-OFT、π₀）持续提升，平均成功率有明显增益。
- 设计了含 5 类扰动（未见干扰物、背景色变化、目标位置/高度变化、相机视角变化）的鲁棒性评测，验证真实扰动下的有效性。

## 方法论
- **隐式 3D 注入（非显式 depth）**：以 VGGT 作为 spatial encoder。VGGT 是一类 Visual Geometry Foundation Model，输入任意数量 RGB 视图、前馈式预测 camera pose / depth map / point map / 3D point track。Evo-0 不取这些显式几何输出，而是抽取 VGGT 最后一层的 **3D tokens t_3D**（原本为 3D 任务训练，蕴含 depth-aware context、跨视图物体轨迹与空间对应关系），从而隐式引入几何信息。模型输入仍只是 RGB 图像，不喂 depth/point cloud。
- **Fusion Layer（单层 cross-attention）**：2D 路径用 ViT image encoder 得到 visual token t_2D；几何路径用 VGGT 得到 t_3D。融合时令 **t_2D 作 Query，t_3D 作 Key/Value**（Q=t_2D·W_Q, K=t_3D·W_K, V=t_3D·W_V），每个视图独立做 cross-attention，更新后的 token 拼接成 fused output。即用 3D token 去"丰富"2D 视觉 token，得到 spatially enriched 表征。
- **下游 pipeline**：融合后的 token 送入 PaliGemma VLM，与 language token 联合注意；再经 flow-matching action expert 输出连续动作。整体构建在开源 SOTA 模型 π₀ 之上。
- **训练阶段起作用方式**：冻结核心 VLM backbone，仅微调 **fuser 模块 + LoRA 层 + flow-matching action expert**；VGGT spatial encoder 提供现成几何先验。因此 3D 注入发生在 fine-tuning / imitation learning 阶段，开销小。训练用 AdamW、单张 A800、batch 32。
- **量化增益（相比纯 RGB VLA）**：
  - 仿真（RLBench 5 任务）平均成功率 **Evo-0 56% vs π₀ 41%（+15pp）vs OpenVLA-OFT 25%（+31pp）**；在 PlaceHangerOnRack、TakeUmbrellaOut 等任务增益最大（+20~25pp）。
  - 真实世界（5 任务）平均 **57.41% vs π₀ 28.53%**，约 +28.88pp。
  - 鲁棒性：5 类扰动下普遍优于 π₀（如未见干扰物全流程成功率 70% vs 20%）。
  - 代价：因 VGGT 编码增加计算量，控制频率从 π₀ 的 11.3 Hz 降到 6.94 Hz，仍满足实时控制；训练效率更高（15k 步即超过 π₀ 的 20k 步）。
