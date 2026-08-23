# GeoVLA: Empowering 3D Representations in Vision-Language-Action Models

## 主题
3D-aware VLA via point clouds

## 背景
Vision-Language-Action (VLA) 模型让机器人能跟随语言指令并预测动作，近期工作（OpenVLA、π0、CogACT 等）多基于预训练 VLM，并用 action expert（diffusion / flow matching）输出连续动作 chunk。但这些模型几乎只用 2D RGB 输入，忽略了 3D 物理世界中的几何先验，导致空间感知与对视角/高度/尺度变化的适应性受限。

## 现有局限与研究问题
- **Limitation:** 现有引入 3D 的两条路线各有缺陷：(1) 把 3D positional encoding 直接注入 VLM（如 LLaVA-3D、SpatialVLA、3D-VLA、3D-CAVLA），会破坏 vision encoder 与 LLM 之间已对齐的表征，需要大规模 3D embodied instruction-tuning 数据来重新对齐；(2) 把点云特征注入冻结的 action expert（如 PointVLA 用 zero-initialized ControlNet 模块），虽保住底层能力，但冻结 expert 阻碍了对新引入点云模态的适配。
- **Problem:** 如何以端到端方式将 3D 信息融入 VLA，既保留 VLM 的预训练知识，又能充分利用几何模态，同时不依赖大规模 3D 指令数据。

## 贡献
- 提出 **GeoVLA**：双分支（dual-branch）VLA 框架，并行处理视觉与点云模态，显式利用 3D 几何，提升高度适应性（height adaptability）、尺度感知（scale awareness）、视角不变性（viewpoint invariance）。
- 提出 **Point Embedding Network (PEN)**：以末端执行器（end-effector）为锚点的几何点编码器，提取判别性、抗噪的细粒度 3D 结构特征。
- 提出 **3D-enhanced Action Expert (3DAE)**：基于 Diffusion Transformer 的动作头，用 Mixture-of-Experts（MoE）按模态做专门化处理，融合视觉-语言与几何特征。
- 在 **LIBERO**（平均 97.7%，超 OpenVLA-OFT 2.4%）和 **ManiSkill2**（平均 77%，超 π0 ... 实际超 Dita 11%、CogACT 8%）取得 SoTA；真机平均成功率 86.3%（8 任务），在需要高度/尺度/视角鲁棒性的任务上优势显著。

## 方法论
- **整体（两路并行 / dual-path）**：输入为 RGB 图像 V、深度图 D 与语言指令 L。
  - **视觉-语言路**：预训练 2D VLM（Prismatic-7B，用 OpenVLA 在 Open X-Embodiment 上的预训练权重初始化）处理 V 与 L，输出融合的 vision-language 特征 F_VL。该路**保留 VLM 的预训练知识与通用理解能力**。
  - **几何路**：把深度图 D 用相机参数**重投影成点云 P**（end-effector 坐标系，当前末端位置为原点），由 PEN 编码成几何特征 F_P。两路特征 concat 后送入 3DAE。
- **depth/3D 如何进入模型**：以**点云作为独立输入模态**进入一个**专门的几何编码器（PEN）**，再在 action expert 层（3DAE）与 RGB 特征融合——而非把 3D positional encoding 注入 VLM 主干。深度来自 RGB-D 相机（RealSense），非单目深度估计；点云在末端坐标系下表达，天然带来视角/高度不变性。
- **PEN（Point Embedding Network，双路结构）**：
  - *Geometric feature path*：轻量 CNN + 多层大核卷积（large-kernel conv）+ local pooling，把点云编码成 patch 级 token F_pc ∈ R^{N×C}，再过 transformer blocks 聚合全局信息。
  - *Positional encoding path*：对原始点云下采样到与 F_pc 同尺寸，用 **RoPE（rotary positional encoding）** 注入位置信息（消融显示 RoPE 比 1D 可学习 PE 把成功率从 95.4% 提到 97.7%）。
  - *Spatial anchor 设计*：选**坐标原点对应的 token（即 end-effector token）作为 anchor token**，喂入 transformer 让各 token 在 RoPE 引导下交互；最后只取最后一层更新后的 anchor token 作为 F_P 输出给 3DAE。带来聚焦式表征学习与显式空间关系建模（末端与周围物体的接触关系）。消融显示 end-effector anchor（97.7%）优于 max pooling（96.3%）和 mean pooling（95.9%）。
- **3DAE（3D-enhanced Action Expert）**：
  - 架构为 **Diffusion Transformer (DiT)**，处理 concat 后的多模态 token（F_VL + F_P）并生成 action chunk（T=16），动作参数化为 (Δx,Δy,Δz,Δα,Δβ,Δγ,g)。训练时对真实动作序列加噪声预测噪声，推理时用 DDIM 采样后在多模态条件下逐步去噪。
  - **MoE on FFN**：在 DiT 的 FFN 引入 MoE，给每个模态做专门化处理。因 VLM 分支是预训练的而点云分支从零初始化，**动态路由会偏向 VLM 分支**，故改用 **static routing（静态路由）**：训练时随机丢弃一个模态，形成三种输入配置（仅 VL / 仅语言+几何（去掉 RGB image token）/ 完整多模态），各 expert 的激活由模态的存在确定性决定。消融：MoE 静态路由（97.7%）> 动态路由（97.3%）> 无 MoE（96.0%）。
- **训练阶段**：**端到端单阶段联合训练**（区别于 PointVLA 的两阶段+冻结 expert）。VLM 用预训练权重初始化，PEN 与 3DAE 从零初始化，三者一起训练。8×A100，FSDP，batch 256，lr 2e-5；LIBERO 约 6 epochs / ManiSkill2 约 2 epochs，真机约 8 小时。
- **相比纯 RGB VLA 的量化增益**：
  - LIBERO 平均 97.7%（OpenVLA-OFT 95.3%，CogACT 93.2%）；LIBERO-Long 96.6%（+5.9%）、LIBERO-90 97.7%（+5.6%）。
  - ManiSkill2 平均 77%（Dita 66%、CogACT 69%）；最难的 PickClutterYCB 达 45%（Dita 36%）。
  - 真机 8 任务平均 86.3%（π0 57.5%、CogACT 76.3%）；3D-aware 任务平均 77.5%。
  - 鲁棒性变体：篮筐最高层 H1 仍 60%（CogACT 20%）；相机偏到 45° 仍 70%（CogACT 0%）；说明 3D 表征显著提升对高度/视角变化的泛化。
