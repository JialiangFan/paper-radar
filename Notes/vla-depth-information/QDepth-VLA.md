# QDepth-VLA: Quantized Depth Prediction as Auxiliary Supervision for Vision-Language-Action Models

## 主题
Quantized depth auxiliary supervision for VLA

## 背景
Vision-Language-Action (VLA) 模型要完成精细 manipulation 需要 spatial perception 与 3D 几何推理能力，但现有基于纯 2D RGB 的 VLA 在 long-horizon、fine-grained 任务上常因 semantic understanding 与 geometric reasoning 之间的 gap 而误判 object 位置和 gripper-object 关系。将 3D 信息引入 VLA 已有三条路线：direct 3D feature injection（如 point cloud，需额外 encoder、破坏预训练 2D prior）、2D-projected 3D feature integration（如 BridgeVLA，投影会丢信息）、以及 auxiliary 3D prediction。本文走第三条路线，并将其聚焦到 depth 上——因为 depth map 与 RGB 的 modality gap 远小于 point cloud。

## 现有局限与研究问题
- **Limitation:** 已有把 depth-map 预测作为辅助任务的工作（如 DreamVLA）未稳定带来增益，甚至有害。原因有三：(1) depth 估计质量受限、跨帧 spatial-temporal 一致性差，引入 noise 削弱 geometric grounding；(2) pixel-wise depth regression 产生高度冗余的学习信号，迫使模型逐像素重建而非聚焦 manipulation 所需的 salient structural cue；(3) 用 vision-language backbone 直接预测 dense depth map 会干扰其预训练 semantic alignment，损害多模态推理。
- **Problem:** 如何以 compact、optimization-friendly 且不破坏预训练语义对齐的方式，将 depth/3D 几何信息作为辅助监督注入 VLA，从而真正提升 spatial reasoning 与 manipulation 成功率？

## 贡献
- 提出 **QDepth-VLA**：在大型 VLA（基于 Open π0 / PaliGemma-3B）上引入 quantized depth prediction 作为 auxiliary supervision，内化 geometric understanding，提升 object spatial relationship 的推理精度。
- 设计专门的 **Depth Expert**：预测 quantized depth tokens（codebook indices）而非 raw pixel-wise depth，缓解 depth noise，提供更紧凑、利于优化的 geometry-aware 监督信号。
- 重设计 **hybrid attention mask** 调控 text/image/depth/proprio/action 跨模态注意力，避免 noisy depth 在 causal attention 下干扰 action 生成。
- Simpler 与 LIBERO 上平均成功率分别超过 Open π0 6.1% 与 7.7%；real-world Piper 机械臂上提升 10.0%，验证有效性与泛化性。

## 方法论
- **整体三阶段流程**（depth 以「量化潜码」形式进入模型，而非 RGB-D 直接拼接或 point cloud）：
  - **Step 1 — Depth Annotation：** OXE/LIBERO 等 VLA 数据集缺 3D 标注，用 Video-Depth-Anything (ViDA, ViT-Large) 对 main-view RGB 帧生成 temporally-aligned 的 monocular relative depth，作为后续 depth tokenization 的几何监督来源。
  - **Step 2 — VQ-VAE Reconstruction：** 在 depth map 上独立预训练一个 VQ-VAE（codebook K=256，维度 d=160，latent grid 16×16；loss = reconstruction + codebook update + commitment，β=0.25）。VQ-VAE 把每帧 depth 压成离散 code indices，这些 indices 就是 depth expert 的监督目标。（VQ-VAE encoder 与 codebook 在第三阶段冻结。）
  - **Step 3 — Co-Training：** MoE 结构同时训练 VLM（PaliGemma-3B，含 SigLIP encoder + Gemma decoder，保持可训）、Action Expert、与新增 Depth Expert。
- **Depth 如何进入模型 / VQ + codebook + 辅助 loss 设计（核心）：**
  - Depth Expert 是 transformer 模块，输入为 SigLIP 的 visual embeddings（在 language fusion 之前取，避免语义干扰），经轻量 MLP 投影 → transformer backbone → shallow CNN decoder，预测 256 个 latent depth token。
  - 每个预测 token 与冻结 VQ-VAE codebook 对齐：对 image features 在 codebook 上算 logits ℓ_{i,k} = -(1/τ)‖x_i − c_k‖²（i 为空间位置，k 为 K=256 个 code，τ 为温度）。
  - **辅助 depth loss 为 cross-entropy**，监督目标是 VQ-VAE 给出的 ground-truth code indices z*_i：L_depth = -(1/(B·N)) Σ log( exp(ℓ_{i,z*_i}) / Σ_k exp(ℓ_{i,k}) )。这迫使 SigLIP visual encoder 学到与 quantized depth 对齐的 geometry-aware embedding。
  - 用「离散分类」而非「pixel 回归」：量化潜码鼓励对几何线索做抽象、降低冗余，避免 pixel 预测把模型缠在 manipulation 不需要的 local detail 上（ablation 中 w/o Latent Prediction 平均掉 3.9%，Eggplant 任务掉 14.6%）。
- **Action 分支：** 沿用 Open π0 的 Conditional Flow Matching (CFM) 动作 loss，action chunk A_t 以 observation O_t=[I_t, ℓ_t, s_t]（RGB、language、end-effector state）为条件。
- **Hybrid Attention Mask：** text/image token 仅在各自模态内注意以保预训练语义；depth token 注意 image+text 以语境化几何特征；action token 注意所有模态以融合感知+几何线索。比 DreamVLA/CoT-VLA 的纯 causal attention 更能隔离 depth noise（ablation 去掉后平均掉 5.5%）。
- **Co-Training 目标与调度：** L_total = L_action + λ_t · L_depth，其中 λ_t = λ0·γ^t 随训练步数指数衰减（λ0=0.01）——先建立稳定 geometric alignment，再逐步聚焦 action refinement。AdamW，VLM 学习率 5×10⁻⁵，cosine scheduler。
- **作用阶段：** depth 监督只在 **training（co-training）阶段** 起作用；inference 时不需要 depth 输入、point cloud 或额外 encoder，仅靠单张/多视 RGB 即可，因此推理开销几乎与 Open π0 持平（参数量 +12.2%，主要来自 depth expert，wall-clock 延迟基本不变）。
- **相比纯 RGB VLA 的量化增益：** LIBERO 平均 85.4 超 Open π0 的 77.7（+7.7%），其中 single-view 即达 Goal 94.0；Simpler Google Robot 平均 75.1 超 Open π0 71.4（+3.7%），open-top-drawer-put-apple 任务大幅领先 29.7%；Simpler WidowX 平均 68.5 超 Open π0 60.0；real-world Piper 平均 42.5 超 Open π0 32.5（+10.0%）。
