# UniLACT: Depth-Aware RGB Latent Action Learning for Vision-Language-Action Models

## 主题
Depth-aware RGB latent action

## 背景
从无标注视频中学习 latent action representation 已成为预训练 VLA 模型、绕开昂贵机器人动作标注的主流范式（如 LAPA、Moto）。但现有 latent action 几乎都只从 RGB 观测学习，捕获的是 appearance-driven dynamics，缺乏对 3D 几何结构的显式建模——而后者对精确抓取、放置、避碰等 contact-rich 操作至关重要。

## 现有局限与研究问题
- **Limitation:** 现有把 depth 引入 VLA 的工作（DepthVLA、QDepth-VLA、SpatialVLA、3D-VLA 等）都在 pixel/feature 层面处理 depth，且依赖大量带标注的机器人轨迹；纯 RGB 的 latent action（Moto/LAPA）对 3D 几何完全 blind。与本文最接近的 UniSkill 虽用 RGB-D，但只学 embodiment-agnostic 的通用 skill、共享一个联合 latent 空间。
- **Problem:** 能否在无监督预训练阶段，把几何结构直接嵌入到 RGB latent action representation 内部，使下游策略在不需要额外标注数据、推理时只用 RGB 的前提下，继承更强的 spatial prior？

## 贡献
- 提出 **UniLARN**（Unified Latent Action leaRNing）：基于 IDM–FDM 的统一 latent action 学习框架，用 inverse/forward dynamics 联合学习 modality-specific（RGB/depth）与 unified 离散 latent action，在共享 latent 空间中同时捕获视觉语义与 3D 几何。
- 提出 **UniLACT**：跨模态训练的 VLA，利用 UniLARN 产出的 unified + modality-specific latent 作为 action-free 伪标签做预训练，提升 policy 的 3D 空间理解。
- 大量仿真（CALVIN）与真机实验证明：unified latent 相比纯 RGB latent 显著增强几何感知；OXE 预训练下 avg sequence length 比 Moto 提升 **+29.2%**，且模型大小/推理延迟与纯 RGB baseline 完全相同（推理不需要 depth）。

## 方法论
**三阶段训练**（depth 只在训练用，推理只需 RGB + 指令）：

1. **Stage 1 — UniLARN 统一 latent action 学习**：对 RGB 和 depth 两个模态各用一个 IDM $I_m$，把成对帧 $(o_t^m, o_{t+H}^m)$ 映射为连续 latent $\tilde z_t^m$，再用**两模态共享的 VQ codebook $\mathcal C^{(s)}$** 离散化得 modality-specific token $z_t^m$。取出两模态 codebook embedding 后**拼接并线性投影**到统一连续空间 $\bar e_t^c=[e_t^r;e_t^d]\to h_t=W_f\bar e_t^c+b_f$，再用**第二个 VQ codebook $\mathcal C^{(u)}$** 离散化得 unified latent $z_t^u$。该 unified latent 连同各模态当前观测去 condition 各自的 FDM $F_m$ 重建未来帧 $\hat o_{t+H}^m=F_m(o_t^m,z_t^u)$。这一"解耦重建"目标迫使 unified 表征同时承载两模态的互补动力学——这正是 depth 几何被注入 RGB latent 的核心环节：depth 通过 IDM/FDM 与共享 codebook 反向约束统一 token，使其携带 3D 几何先验。IDM 用 MAE 初始化的 frozen ViT-L 编码器 + spatio-temporal transformer，FDM 用 ViT-B decoder（MSE loss），离散化用 VQ-VAE。

2. **Stage 2 — Unified Latent Pretraining**：用 UniLARN 编码器从 RGB-D 视频抽取 modality-specific $z_t^r,z_t^d$ 与 unified $z_t^u$，作为 action-free 监督信号。基于 GPT-2 因果 transformer，输入视觉观测 $o_t$（ViT-L 编码）、T5 编码的任务指令 $l$ 和 unified latent $z_t^u$，自回归预测目标 token 序列 $z_{1:N}^m$（$m\in\{r,d,u\}$，每个 batch 在 RGB/depth/unified 间交替）。这种 cross-modal next-token prediction 让模型内化互补语义与几何线索，并对齐 modality-specific 与 unified 空间。

3. **Stage 3 — Action Fine-Tuning**：在带动作标注的少量机器人轨迹上微调。追加 action query token，用轻量 action decoder（2 层 MLP + 分离线性头）把 transformer 输出映射为 7-DoF 末端执行器动作（位置 delta $\Delta p\in\mathbb R^3$、旋转 delta $\Delta r\in\mathbb R^3$、二值夹爪 $g$）。损失 $\mathcal L_{ft}=\mathcal L_{latent}^u+\mathcal L_{action}$，其中 $\mathcal L_{latent}^u$ 是 unified-latent 的 next-token 预测损失（只保留 unified、丢弃 RGB/depth latent 预测），$\mathcal L_{action}=\mathcal L_{reg}(\Delta p)+\mathcal L_{reg}(\Delta r)+\mathcal L_{bce}(g)$（L1 + BCE），以在学策略时保留预训练的 latent 结构。

**关于 depth 的形式**：depth 不是作为额外输入通道喂给 policy，而是在预训练阶段经 UniLARN 被"蒸馏"进 unified discrete latent action；真机实验中 OXE 数据缺 depth 时用 Depth-Anything-V2 从 RGB 生成 depth map。**量化增益**：CALVIN ABC→D 上 OXE 预训练 avg seq len 2.40(Moto)→3.10(+29.2%)，in-domain ABC 预训练 2.60→2.86；消融中 Unified+Modality-specific 2.859 > RGB-only 2.601 > Depth-only 2.402 > 无 latent 0.744；真机平均成功率 +10%，几何相关任务（move slider、turn on light bulb）增益最大。
