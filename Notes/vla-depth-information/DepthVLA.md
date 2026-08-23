# DepthVLA: Enhancing Vision-Language-Action Models with Depth-Aware Spatial Reasoning

## 主题
Depth-aware spatial reasoning VLA

## 背景
Vision-Language-Action (VLA) 模型继承自 VLM，具备强大的语义理解与跨任务泛化能力，已成为机器人操作的主流范式。但 VLM 在 3D 空间推理上很弱（对物体形状、精细几何不敏感），导致 VLA 在抓小物体、精确操作、避碰等需要精细空间理解的任务上表现下降。本文在 π0 的 mixture-of-transformers (MoT) 框架基础上，显式引入一个预训练的 depth expert 来补充几何感知。

## 现有局限与研究问题
- **Limitation:** 现有 VLA 主要靠大规模 action-data 预训练把 VLM "grounding" 到 3D 空间，既低效、可扩展性差，又仍不足以获得精确空间理解；引入外部深度估计器的方法（如 SpatialVLA 用现成 depth estimator 生成伪点云）本质是 workaround，深度模块不与 VLA 端到端联合优化，存在性能上界；基于 generative world model 或 Chain-of-Thought 的方法要么缺显式 3D 知识，要么需自回归生成数百个 spatial token，推理延迟超过 2 秒。
- **Problem:** 如何在不牺牲推理速度的前提下，将 3D 感知（monocular depth/3D foundation models）的最新进展引入 VLA，使其获得显式、端到端的精细空间推理能力？

## 贡献
- **DepthVLA 架构**：提出把预训练 depth prediction expert 集成进 mixture-of-transformers 框架的新型 VLA，在保留 VLM 语义 grounding 的同时实现显式空间推理。
- **Per-expert 预训练策略**：MoT 设计允许每个 expert（VLM 与 depth）在各自的多样化数据集上独立预训练，突破 embodied action 数据的限制，提升训练效率与可扩展性。
- **大规模真机 + 仿真验证**：在真机、LIBERO、Simpler 上都显著超越 SOTA，量化增益为真机 78.5% vs 65.0%、LIBERO 94.9% vs 93.6%、Simpler 74.8% vs 58.8%，且只在抓取精度、避碰等需空间推理的任务上拉开差距。

## 方法论
- **三专家 MoT 结构**：在 π0 的两专家（VLM + action expert）基础上加入独立的 depth expert，共三个 transformer 专家——
  - **VLM expert**：Paligemma-3B，编码图像与语言指令 `l`，提供语义与开放词表感知；视觉用 SigLIP。
  - **Depth expert**：encoder-decoder 结构。encoder 用 DINOv2-L，从 **Depth Anything V2** 的预训练 checkpoint 初始化以继承 3D foundation model 的强空间先验；decoder 镜像 VLM 的 transformer 结构，末端接 linear head 输出深度。采用与 VLM 相同的 backbone 但**独立权重与维度**。
  - **Action expert**：flow-matching 动作专家，从头训练，接收 proprio 与 noise，输出 k 步连续动作 chunk。
- **depth/3D 信息如何进入模型（核心）**：不是只把最终深度图喂进去，而是让 action expert 在**每一层都 attend 到 depth expert 的中间层特征**，利用丰富的几何表示（而非低维深度输出）来生成动作。三个专家**共享同一套 attention 层**，但通过 **block-wise mask** 控制信息流：VLM token 与 depth token 各自只 attend 自己（保护预训练能力），action token 可以 attend 所有 stream（VLM + depth + proprio + noise）。这样动作生成同时融合语义、视觉与空间几何线索。
- **depth 在哪个阶段起作用 / 训练分几阶段**：两阶段——
  1. **Per-expert 预训练**：depth expert 先在多样化 3D 数据集（WildRGB-D、Scannet、Scannet++、HyperSim）上做 monocular depth prediction 预训练，损失为 **scale-invariant log loss**（`L_si = sqrt( (1/n)Σy² − λ((1/n)Σy)² )`，`y=log d̂ − log d`，λ=0.5），获得鲁棒空间推理能力；VLM 直接继承 Paligemma 预训练。此阶段 depth 与动作解耦，可用海量非 embodied 的 3D 数据。
  2. **端到端 VLA 训练**：在 embodied action 数据上用 imitation learning（最大化 `log π_θ`）+ **flow-matching loss** `L_flow` 训练动作生成；同时**保留 depth prediction loss**，最终损失 `L = L_si + L_flow`，让空间推理与动作生成端到端联合优化。各 benchmark 上再 fine-tune 4k–30k 步。
- **效率**：相比 π0 baseline 仅多 600M 参数（DINOv2 encoder 300M + depth decoder 300M），VRAM 8.0GB vs 6.7GB，推理 210ms vs 190ms/step；因动作以 1 秒 chunk 预测（15Hz 平台 16 步），额外延迟可忽略——这是相比 CoT 类方法（>2s）的关键优势。
- **消融结论**：(i) depth expert 预训练、(ii) VLA 训练期保留 depth loss、(iv) block-wise mask 均必要；(iii) 冻结 depth expert 影响很小（说明学到的空间表示鲁棒通用，便于无 GT 深度时部署）；(v) **预测深度优于直接输入 GT 深度**（94.9% vs 93.3%），作者归因于 modality competence——让模型自己预测深度可避免对外部信号过度依赖、把几何推理更好地融进共享表示空间。
- **局限**：monocular depth 本身是 ill-posed 问题，在细小边缘、透明/无纹理物体上仍会出错；未来可探索 multi-view depth 或 pointmap 预测。
