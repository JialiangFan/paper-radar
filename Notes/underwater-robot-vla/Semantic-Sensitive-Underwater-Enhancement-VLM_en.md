# Semantic-Sensitive Underwater Image Enhancement with VLM

## Topic
VLM-guided semantic underwater enhancement

## Background
Underwater images suffer from severe degradation due to light absorption and scattering, making underwater image enhancement (UIE) a critical pre-processing step for ocean exploration, biological monitoring, and underwater robotics. While modern deep-learning UIE methods achieve visually pleasing outputs for human observers, a clear disconnect exists between perceptual image quality and the requirements of downstream machine cognition tasks such as detection and segmentation.

## Existing Limitations and Research Problem
- **Limitation:** Current UIE methods are "task-agnostic" or "semantic-blind": their pursuit of globally uniform enhancement introduces imperceptible artifacts and causes distribution shifts that misalign with downstream models. Earlier semantic-guided variants relied on scarce, pixel-level segmentation annotations that are particularly hard to obtain underwater, while recent VLM-based approaches employ only global, style-driven text prompts (e.g., "a clear underwater photo") that ignore specific object content and cannot perform fine-grained, object-centric processing.
- **Problem:** How can we leverage the open-world understanding of VLMs to make a UIE network aware of *what* to focus on, allocating restoration capacity to semantically critical regions so that the enhanced image is robust for both human perception and downstream machine vision?

## Contributions
- Proposes a VLM-driven, semantic-sensitive (-SS) learning strategy that addresses the semantic blindness of traditional UIE, producing results robust for both human and machine perception.
- Designs a dual-guidance mechanism that uses the semantic map to (i) structurally steer the network's information flow via a cross-attention injection module and (ii) explicitly regularize intermediate decoder features via a new semantic alignment loss.
- Demonstrates the strategy as a plug-and-play module on five SOTA encoder-decoder UIE baselines (PUIE, SMDR, UIR, PFormer, FDCE), consistently improving PSNR/SSIM/LPIPS/UIQM/UCIQE on UIEB, U45, and Challenge60, and boosting mAP and mIoU on Trash-ICRA19 detection and SUIM segmentation.

## Methodology
- **Semantic guidance map generation:** A VLM (LLaVA) generates a textual description T of key objects in the degraded image Id; BLIP's visual encoder Φv extracts patch features Fv and its text encoder Φt extracts a global text feature ft.
- **Cross-modal alignment and sharpening:** Cosine similarity si between each normalized patch feature and the text feature yields raw relevance scores. A sharpening function Ψsharp(si; γ, δ) = (max(0, N(si) − δ))^γ combines min-max normalization, thresholding to suppress noisy background activations, and a power-law to amplify high-relevance regions. Scores are reshaped and upsampled to the original resolution, producing a single-channel spatial semantic guidance map Msem.
- **Cross-attention injection:** At each decoder stage l, Msem is downsampled to the spatial size of the encoder skip feature el, yielding M̃(l). The map element-wise modulates el, which is then linearly projected to generate keys Kl and values Vl. The decoder feature dl serves as the query Ql, and softmax(QlKl^T/√dk)Vl lets the decoder preferentially extract information from semantically "illuminated" encoder features.
- **Explicit semantic alignment loss:** L(l)_align(F(l), M̃(l)) = ‖F(l) ⊙ (1 − M̃(l))‖²_F − η⟨F(l), M̃(l)⟩. The first term suppresses unwanted activations in non-key (background) regions, while the second rewards strong responses in key object regions consistent with the semantic guidance.
- **Overall objective:** Ltotal = Lrecon + λalign · Σ_{l∈L} L(l)_align, where Lrecon combines an L1 pixel loss with a VGG-19 perceptual loss, and λalign is empirically set to 0.1.
- **Ablation insights:** BLIP's fusion-based alignment yields cleaner, more spatially accurate guidance maps than ViT class-attention or CLIP. Injecting the semantic guidance only into the decoder outperforms encoder-only or all-stage injection, because it directly steers the image reconstruction process rather than the feature extraction stage.
