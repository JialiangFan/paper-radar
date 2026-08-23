# SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model

## Topic
Spatial representations for VLA

## Background
The dominant recipe for generalist robot policies is to fine-tune a VLM (e.g., PaliGemma2) on cross-embodiment data to obtain a VLA model. Yet existing VLAs largely consume only 2D RGB observations and lack a structured perception of the 3D physical world, whereas humans instinctively rely on rich spatial mental representations when manipulating objects. This paper argues that spatial understanding is the keypoint in robot manipulation and proposes SpatialVLA (built on PaliGemma2) to inject 3D spatial representations into VLAs.

## Limitations & Research Problem
- **Limitation:** Existing VLAs are confined to 2D observation inputs and lack precise 3D perception. Cameras across robot embodiments are mounted differently (wrist / third-person), so observations are non-3D-aligned. Robots also differ in DoF, controllers, and workspaces, yielding heterogeneous action spaces that make generalizable, transferable spatial actions hard to learn.
- **Problem:** How to effectively equip VLA models with a profound spatial understanding of the 3D physical world, while keeping observation and action representations spatially aligned and transferable across embodiments.

## Contributions
- SpatialVLA: a generalist robot policy that explores spatial representations on top of a vision-language model.
- **Ego3D Position Encoding** to inject 3D spatial context into observations, with no need for robot-camera extrinsic calibration, making it universally applicable across embodiments.
- **Adaptive Action Grids** that discretize continuous actions into spatial action tokens according to the dataset's statistical action distribution, aligning cross-robot actions with 3D spatial structure; grids can be re-discretized at post-training for fast adaptation to new setups.
- Pre-trained on 1.1M real robot episodes; extensively evaluated (zero-shot and fine-tuning) across 7 robot scenarios, 24 real-robot tasks, and 3 simulation environments, achieving SOTA with faster inference (~20Hz, fewer tokens per action).

## Methodology
- **Pipeline**: SigLIP extracts 2D semantic features → Ego3D Position Encoding injects 3D structure → PaliGemma2 backbone autoregressively predicts spatial action tokens (only 3 per action: ΔT, ΔR, G) → de-tokenized into continuous actions A_t for control. Pre-trained with a next-token cross-entropy objective.
- **Ego3D Position Encoding (how depth/3D enters the model)**:
  - Depth comes from **monocular depth estimation**: a depth map D is estimated with ZoeDepth.
  - A **back-projection π⁻¹** with camera intrinsics recovers each pixel's 3D position p = {x, y, z} in an **egocentric 3D coordinate frame**, which **eliminates the need for robot-camera extrinsic calibration** and is agnostic to specific robot setups.
  - The SigLIP encoder yields 2D features X ∈ R^{d×h×w} and the corresponding 3D positions P ∈ R^{3×h×w}.
  - **Position-encoding computation**: P is passed through a sinusoidal function γ(·) followed by a learnable MLP to form the 3D position embedding P'; this is **added directly to the visual tokens**: **O_3d = X + P' = X + MLP(γ(P))**. The 2D semantic tokens thus carry 3D spatial structure.
- **Adaptive Action Grids (action representation)**:
  - A single-arm 7-DoF action a = {x, y, z, roll, pitch, yaw, grip} is split into a = {a_trans, a_rot, a_grip}.
  - Translation (x,y,z) is converted to **polar coordinates (φ, θ, r)** to disentangle movement direction (φ,θ) from distance r.
  - ΔT and ΔR are aggregated over the whole dataset mixture and **fit with a Gaussian N(μ, Σ²)**; each action variable is split into M intervals with equal probability 1/M (adaptive discretization, with finer grids on directions φ/θ for fine-grained movement). This gives translation grids M_trans = M_φ·M_θ·M_r and rotation grids M_rot, with learnable token embeddings E_a = {E_trans, E_rot, E_grip} and total token count V = M_trans + M_rot + 2.
  - Each action needs only **3 spatial action tokens** (vs. 7 in RT-1/RT-2/OpenVLA), enabling fast inference (21Hz; ~20Hz and 8.5GB GPU memory on an RTX 4090).
- **Pre-training**: from PaliGemma2, on **1.1M real robot demonstrations** (a subset of OXE plus the RH20T dataset, with mixture ratios tuned per OpenVLA, finally dropping DROID); trained on 64×A100 for 10 days, batch size 2048. Only a single third-person camera is used to build the egocentric 3D representation.
- **Post-training (adapting to new setups)**: Spatial Embedding Adaption — fit a new Gaussian N(μ_new, Σ_new) to the new dataset's action distribution, re-discretize into new action grids G_new, and initialize new action-token embeddings via **trilinear interpolation** with pre-trained grids (weighted by normalized distances to neighboring grid centroids); the text embedding is frozen to preserve instruction-following.
- **Quantitative gains (vs. pure-RGB VLA)**:
  - SimplerEnv Google Robot (zero-shot): Visual Matching 71.9% vs. RoboVLM 56.3% (+15.6); Variant Aggregation 68.8% vs. RT-2-X 64.3% (with 3.5B vs. 55B params).
  - SimplerEnv WidowX: zero-shot overall 34.4% vs. RoboVLM 13.5%; fine-tuning 42.7%, with 100% on "Put Eggplant in Yellow Basket".
  - LIBERO fine-tuning average 78.1% (rank 1), LIBERO-Spatial 88.2%.
  - Franka spatial-prompt task 73% accuracy (+12% over OpenVLA).
  - Ablation: removing ego3d encoding drops Variant Aggregation from 81.6% to 68.9% and Visual Matching 70.7%→66.7%, showing 3D injection is key to robustness under scene changes.
