# QDepth-VLA: Quantized Depth Prediction as Auxiliary Supervision for Vision-Language-Action Models

## Topic
Quantized depth auxiliary supervision for VLA

## Background
Vision-Language-Action (VLA) models need strong spatial perception and 3D geometric reasoning for fine-grained manipulation, yet RGB-only VLAs frequently misjudge object positions and gripper-object relations on long-horizon, fine-grained tasks due to a persistent gap between semantic understanding and geometric reasoning. Three paradigms exist for injecting 3D into VLAs: direct 3D feature injection (e.g., point clouds, which need an extra encoder and disrupt pretrained 2D priors), 2D-projected 3D feature integration (e.g., BridgeVLA, which loses information in projection), and auxiliary 3D prediction. This work takes the auxiliary route and focuses it on depth, since depth maps exhibit a far smaller modality gap to RGB than point clouds do.

## Limitations & Research Problem
- **Limitation:** Prior works using depth-map prediction as an auxiliary task (e.g., DreamVLA) have not delivered consistent gains and can even hurt policy learning, for three reasons: (1) depth estimation quality is limited and spatial-temporal consistency across frames is poor, injecting noise that weakens geometric grounding; (2) pixel-wise depth regression produces highly redundant learning signals, forcing per-pixel reconstruction instead of focusing on salient structural cues needed for manipulation; (3) using the vision-language backbone to predict dense depth maps interferes with its pretrained semantic alignment, degrading multimodal reasoning.
- **Problem:** How can depth/3D geometric information be injected as auxiliary supervision in a compact, optimization-friendly way that does not disrupt pretrained semantic alignment, so as to genuinely improve spatial reasoning and manipulation success?

## Contributions
- **QDepth-VLA:** a large VLA (built on Open π0 / PaliGemma-3B) augmented with quantized depth prediction as auxiliary supervision, internalizing geometric understanding for more accurate reasoning about object spatial relationships.
- A dedicated **Depth Expert** that predicts quantized depth tokens (codebook indices) rather than raw pixel-wise depth, mitigating depth noise and providing a more compact, optimization-friendly geometry-aware supervision signal.
- A redesigned **hybrid attention mask** regulating cross-modal attention among text/image/depth/proprio/action tokens, preventing noisy depth from interfering with action generation under causal attention.
- Surpasses Open π0 by 6.1% (Simpler) and 7.7% (LIBERO) average success rate, and by 10.0% on a real-world Piper arm, validating effectiveness and generalizability.

## Methodology
- **Overall three-stage pipeline** (depth enters the model as *quantized latent codes*, not as RGB-D concatenation or point clouds):
  - **Step 1 — Depth Annotation:** Since VLA datasets (OXE/LIBERO) lack 3D annotations, Video-Depth-Anything (ViDA, ViT-Large) generates temporally-aligned monocular relative depth from main-view RGB frames, providing geometric supervision for depth tokenization.
  - **Step 2 — VQ-VAE Reconstruction:** A VQ-VAE is pretrained independently on depth maps (codebook K=256, dim d=160, latent grid 16×16; loss = reconstruction + codebook update + commitment, β=0.25). It compresses each depth frame into discrete code indices that serve as the depth expert's supervisory targets. The VQ-VAE encoder and codebook are frozen in Step 3.
  - **Step 3 — Co-Training:** A MoE structure jointly trains the VLM (PaliGemma-3B with SigLIP encoder + Gemma decoder, kept trainable), the Action Expert, and the new Depth Expert.
- **How depth enters the model / VQ + codebook + auxiliary-loss design (core):**
  - The Depth Expert is a transformer that takes SigLIP visual embeddings *before* language fusion (to avoid semantic interference), passes them through a lightweight MLP → transformer backbone → shallow CNN decoder, predicting 256 latent depth tokens.
  - Each predicted token is aligned against the frozen VQ-VAE codebook: logits over the codebook are ℓ_{i,k} = -(1/τ)‖x_i − c_k‖² (i indexes spatial positions, k indexes the K=256 codes, τ is temperature).
  - The **auxiliary depth loss is a cross-entropy** against the ground-truth code indices z*_i from the VQ-VAE: L_depth = -(1/(B·N)) Σ log( exp(ℓ_{i,z*_i}) / Σ_k exp(ℓ_{i,k}) ). This drives the SigLIP visual encoder to learn geometry-aware embeddings aligned with the quantized depth representation.
  - Discrete classification (not pixel regression): quantized latent tokens encourage abstraction of geometric cues and reduce redundancy, avoiding entangling the model in manipulation-irrelevant local detail (ablation: w/o Latent Prediction drops 3.9% on average, 14.6% on Eggplant).
- **Action branch:** Inherits Open π0's Conditional Flow Matching (CFM) action loss; the action chunk A_t is conditioned on observation O_t=[I_t, ℓ_t, s_t] (RGB image, language instruction, end-effector state).
- **Hybrid Attention Mask:** text/image tokens attend only within their own modality to preserve pretrained semantics; depth tokens attend to image+text to contextualize geometric features; action tokens attend to all modalities to fuse perceptual and geometric cues. More effective than the pure causal attention of DreamVLA/CoT-VLA at isolating depth noise (removing it drops 5.5% on average).
- **Co-Training objective and schedule:** L_total = L_action + λ_t · L_depth, with λ_t = λ0·γ^t decaying exponentially over training steps (λ0=0.01) — first establishing stable geometric alignment, then gradually focusing on action refinement. AdamW, VLM learning rate 5×10⁻⁵, cosine scheduler.
- **When it acts:** depth supervision is used only during the **training (co-training) stage**; at inference no depth input, point cloud, or extra encoder is required — RGB (single- or multi-view) suffices, so inference overhead stays comparable to Open π0 (params +12.2%, mostly from the depth expert; wall-clock latency essentially unchanged).
- **Quantified gain over RGB-only VLA:** LIBERO average 85.4 vs Open π0's 77.7 (+7.7%), with single-view reaching Goal 94.0; Simpler Google Robot average 75.1 vs Open π0 71.4 (+3.7%), leading by 29.7% on the open-top-drawer-put-apple task; Simpler WidowX average 68.5 vs Open π0 60.0; real-world Piper average 42.5 vs Open π0 32.5 (+10.0%).
