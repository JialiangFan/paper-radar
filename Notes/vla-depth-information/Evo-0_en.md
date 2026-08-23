# Evo-0: Vision-Language-Action Model with Implicit Spatial Understanding

## Topic
Implicit 3D-aware VLA model

## Background
Vision-Language-Action (VLA) models are typically fine-tuned on pretrained VLMs, but VLMs are trained on 2D image-text pairs without 3D supervision and thus lack precise spatial understanding. To address this, recent methods (e.g., SpatialVLA, PointVLA, 3D-VLA) explicitly inject depth maps or point clouds, which requires extra depth sensors or pretrained depth-estimation networks.

## Limitations & Research Problem
- **Limitation:** Existing 3D-aware VLAs rely on explicit 3D inputs (depth/point cloud) that need specialized sensors or auxiliary estimation models; depth estimation introduces extra noise and is sensitive to camera-viewpoint changes, limiting scalability and deployment flexibility.
- **Problem:** Can 3D geometric priors be injected implicitly into a VLA model — using RGB images only, without depth sensors or explicit depth estimation — to enhance spatial understanding?

## Contributions
- Propose a plug-and-play module that implicitly injects 3D geometric priors via a Visual Geometry Foundation Model (VGGT), enhancing the spatial understanding of VLA models without depth sensors or explicit depth estimation.
- Evaluate on 5 RLBench simulation tasks plus 5 real-world manipulation tasks, showing consistent improvements over strong baselines (OpenVLA-OFT, π₀) with clear average success-rate gains.
- Design a robustness benchmark with 5 disturbance categories (unseen distractor, background-color change, target position/height variation, camera-viewpoint shift) to validate effectiveness under real-world perturbations.

## Methodology
- **Implicit 3D injection (not explicit depth):** VGGT serves as a spatial encoder. VGGT is a class of Visual Geometry Foundation Model that takes an arbitrary number of RGB views and feed-forward predicts camera poses / depth maps / point maps / 3D point tracks. Evo-0 does NOT consume these explicit geometric outputs; instead it extracts the **3D tokens t_3D** from VGGT's final layer (originally trained for 3D tasks, encoding depth-aware context, cross-view object trajectories, and spatial correspondences), thereby injecting geometry implicitly. The model input remains RGB images only — no depth/point cloud is fed in.
- **Fusion layer (single cross-attention):** The 2D path uses a ViT image encoder to produce visual tokens t_2D; the geometry path uses VGGT to produce t_3D. In fusion, **t_2D acts as Query and t_3D as Key/Value** (Q=t_2D·W_Q, K=t_3D·W_K, V=t_3D·W_V); each view is processed independently with cross-attention, and the updated tokens are concatenated into the fused output. Thus 3D tokens "enrich" the 2D visual tokens into a spatially enriched representation.
- **Downstream pipeline:** The fused tokens go into a PaliGemma VLM, jointly attended with language tokens, then a flow-matching action expert outputs continuous actions. The whole model is built upon the open-source SOTA model π₀.
- **Where it acts during training:** The core VLM backbone is frozen; only the **fuser module + LoRA layers + flow-matching action expert** are fine-tuned, while the VGGT spatial encoder provides off-the-shelf geometric priors. Hence 3D injection happens at the fine-tuning / imitation-learning stage with minimal overhead. Trained with AdamW on a single A800, batch size 32.
- **Quantitative gains (vs RGB-only VLA):**
  - Simulation (5 RLBench tasks) average success rate: **Evo-0 56% vs π₀ 41% (+15pp) vs OpenVLA-OFT 25% (+31pp)**; largest gains on PlaceHangerOnRack and TakeUmbrellaOut (+20–25pp).
  - Real-world (5 tasks) average: **57.41% vs π₀ 28.53%**, about +28.88pp.
  - Robustness: consistently better than π₀ across all 5 disturbance conditions (e.g., unseen-distractor full-pipeline success 70% vs 20%).
  - Cost: due to the added VGGT encoding, control frequency drops from π₀'s 11.3 Hz to 6.94 Hz (still real-time capable); training is more efficient (15k steps already surpass π₀ at 20k steps).
