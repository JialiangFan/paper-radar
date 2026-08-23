# GeoVLA: Empowering 3D Representations in Vision-Language-Action Models

## Topic
3D-aware VLA via point clouds

## Background
Vision-Language-Action (VLA) models let robots follow language instructions and predict actions. Recent systems (OpenVLA, π0, CogACT, etc.) build on pretrained VLMs and use an action expert (diffusion / flow matching) to output continuous action chunks. However, most rely almost exclusively on 2D RGB inputs, neglecting the geometric priors of the 3D physical world. This limits spatial awareness and robustness to changes in viewpoint, height, and object scale.

## Limitations & Research Problem
- **Limitation:** Existing 3D approaches fall into two flawed routes: (1) injecting 3D positional encodings directly into the VLM (LLaVA-3D, SpatialVLA, 3D-VLA, 3D-CAVLA) disrupts the already-aligned representation between the vision encoder and the LLM, requiring large-scale 3D embodied instruction-tuning data to re-align; (2) injecting point-cloud features into a frozen action expert (PointVLA, via a zero-initialized ControlNet-style module) preserves low-level skills but the frozen expert hinders adaptation to the newly introduced point-cloud modality.
- **Problem:** How to integrate 3D information into a VLA in an end-to-end manner that both preserves the VLM's pretrained knowledge and fully exploits the geometric modality, without depending on large-scale 3D instruction data.

## Contributions
- Propose **GeoVLA**, a dual-branch VLA framework that processes visual and point-cloud modalities in parallel, explicitly leveraging 3D geometry to improve height adaptability, scale awareness, and viewpoint invariance.
- Introduce the **Point Embedding Network (PEN)**, an end-effector-anchored geometric point encoder that extracts discriminative, noise-robust fine-grained 3D structural features.
- Introduce the **3D-enhanced Action Expert (3DAE)**, a Diffusion-Transformer action head with a Mixture-of-Experts (MoE) that processes each modality in a specialized way to fuse vision-language and geometric features.
- Achieve SoTA on **LIBERO** (97.7% avg, +2.4% over OpenVLA-OFT) and **ManiSkill2** (77% avg, beating Dita by 11% and CogACT by 8%); real-world 8-task avg success of 86.3%, with clear advantages on tasks requiring height/scale/viewpoint robustness.

## Methodology
- **Overall (dual-path, parallel):** Inputs are an RGB image V, a depth map D, and a language instruction L.
  - **Vision-language path:** a pretrained 2D VLM (Prismatic-7B, initialized from OpenVLA weights pretrained on Open X-Embodiment) processes V and L into fused vision-language features F_VL. This path **preserves the VLM's pretrained knowledge and general understanding**.
  - **Geometric path:** the depth map D is **reprojected into a point cloud P** using camera parameters (in the end-effector coordinate frame, with the current end-effector position at the origin), then encoded by PEN into geometric features F_P. The two feature streams are concatenated and fed to the 3DAE.
- **How depth/3D enters the model:** 3D enters as a **separate point-cloud input modality** processed by a **dedicated geometric encoder (PEN)**, and is fused with RGB features at the action-expert stage (3DAE) — rather than injecting 3D positional encodings into the VLM backbone. Depth comes from an RGB-D camera (RealSense), not monocular depth estimation; expressing the cloud in the end-effector frame inherently yields viewpoint/height invariance.
- **PEN (Point Embedding Network, dual-path):**
  - *Geometric feature path:* a lightweight CNN with multi-layer large-kernel convolutions and local pooling encodes the cloud into patch-level tokens F_pc ∈ R^{N×C}, followed by transformer blocks that aggregate global information.
  - *Positional encoding path:* the raw cloud is downsampled to match F_pc and position information is injected via **RoPE (rotary positional encoding)** (ablation: RoPE lifts success from 95.4% to 97.7% vs. 1D learnable PE).
  - *Spatial anchor design:* the **token at the coordinate origin (the end-effector token) is selected as the anchor token**, fed through transformer blocks so tokens interact under RoPE; only the updated anchor token from the last layer is taken as F_P for the 3DAE. This yields focused representation learning and explicit spatial-relationship modeling (end-effector vs. surrounding objects). Ablation: end-effector anchor (97.7%) > max pooling (96.3%) > mean pooling (95.9%).
- **3DAE (3D-enhanced Action Expert):**
  - A **Diffusion Transformer (DiT)** processes the concatenated multi-modal tokens (F_VL + F_P) and generates an action chunk (T=16), with actions parameterized as (Δx,Δy,Δz,Δα,Δβ,Δγ,g). During training, ground-truth action sequences are perturbed with diffusion noise and the model predicts the noise; at inference, a noise sample (DDIM) is progressively denoised conditioned on the multi-modal tokens.
  - **MoE on the FFN:** an MoE is added in the DiT feed-forward networks to specialize per modality. Because the VLM branch is pretrained while the point-cloud branch is trained from scratch, **dynamic routing biases the model toward the VLM branch**; hence **static routing** is used: during training one modality is randomly dropped, yielding three input configurations (VL-only / language+geometry with RGB tokens removed / full multi-modal), and each expert's activation is determined deterministically by modality presence. Ablation: static-routing MoE (97.7%) > dynamic routing (97.3%) > no MoE (96.0%).
- **Training stages:** **end-to-end single-stage joint training** (unlike PointVLA's two-stage scheme with a frozen expert). The VLM is initialized from pretrained weights; PEN and 3DAE are trained from scratch alongside it. 8×A100, FSDP, batch 256, lr 2e-5; ~6 epochs on LIBERO / ~2 epochs on ManiSkill2, ~8 hours for real-world.
- **Quantitative gains over pure-RGB VLAs:**
  - LIBERO 97.7% avg (OpenVLA-OFT 95.3%, CogACT 93.2%); LIBERO-Long 96.6% (+5.9%), LIBERO-90 97.7% (+5.6%).
  - ManiSkill2 77% avg (Dita 66%, CogACT 69%); hardest PickClutterYCB 45% (Dita 36%).
  - Real-world 8-task avg 86.3% (π0 57.5%, CogACT 76.3%); 3D-aware tasks avg 77.5%.
  - Robustness variants: highest basket level H1 still 60% (CogACT 20%); camera shifted to 45° still 70% (CogACT 0%) — showing 3D representations markedly improve generalization to height/viewpoint changes.
