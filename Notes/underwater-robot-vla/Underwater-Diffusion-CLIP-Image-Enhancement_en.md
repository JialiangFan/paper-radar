# Underwater Diffusion Attention Network with CLIP Joint Learning

## Topic
CLIP-Guided Diffusion Underwater Enhancement

## Background
Underwater images suffer from light absorption, scattering, color casts and haze, which directly degrades the visual perception of AUVs and downstream tasks such as detection, segmentation and scene understanding. Existing diffusion-based underwater image enhancement (UIE) methods rely on synthetic paired datasets and naive fine-tuning, which both introduce domain shift and corrupt the natural in-air priors learned by the backbone. The paper (Shaahid and Behzad, King Fahd University of Petroleum and Minerals; arXiv 2505.19895, May 2025) proposes UDAN-CLIP to address these issues.

## Limitations and Research Question
- **Limitation:** Diffusion-based UIE methods depend on synthetic paired data (causing distribution bias and limited generalisation), and fine-tuning a pretrained diffusion model tends to wipe out its valuable in-air natural-image prior, producing unrealistic enhancements. CLIP guidance for UIE is also unstable: prompts describing abstract degradations (haze, low contrast) are hard to design, and small rephrasings produce very different CLIP scores.
- **Problem:** How can we build a diffusion-based UIE framework that (i) preserves the in-air natural-image prior during fine-tuning, (ii) attends to localized degradations such as haze and turbidity, and (iii) enforces stable visual–textual semantic alignment without hand-crafted prompts or large real paired datasets?

## Contributions
- Proposes UDAN-CLIP, an underwater diffusion attention network with contrastive vision–language joint learning, extending the CLIP-UIE baseline.
- Introduces a VLM-based classifier with learnable prompts (CoOp / CLIP-LIT style, 77 tokens for in-air and underwater) used as classifier guidance to preserve in-air priors and prevent catastrophic forgetting during fine-tuning.
- Adds a spatial attention module on top of a ResNet-101 backbone that produces a 1-channel attention mask to amplify locally degraded regions (haze, low contrast, turbidity) before alignment with the text embedding.
- Defines a new joint CLIP-Diffusion loss L_UDAN-CLIP that combines pixel-level noise prediction with a perceptual/semantic alignment term in the encoder embedding space (weights λ1=0.6, λ2=0.4).
- Demonstrates state-of-the-art performance on T200, Color-Checker7 and C60 with PSNR 27.949, SSIM 0.952 and UCIQE 0.654 on T200, outperforming CLIP-UIE, DM_underwater, UDAformer, TCTL-Net, UIEC²-Net, UDCP and ULAP.

## Methodology
- **Data synthesis (UIE-air):** Reinhard-style CIELAB colour transfer maps in-air iNaturalist 2021 images into synthetically degraded underwater versions using a pool of underwater templates, producing paired (synthetic-underwater, in-air ground-truth) samples for pre-training.
- **Diffusion pre-training:** Trains a conditional image-to-image diffusion model ε_θ(x_t, y, t) on UIE-air with the standard L2 noise-prediction objective to learn the underwater-to-in-air transition prior. Uses 2000 timesteps with a linear noise schedule from 1e-6 to 1e-2 (300 hours pre-training on RTX 3090).
- **Multi-condition classifier guidance:** During fine-tuning on real datasets, two conditions are used: y1 (source underwater image) and y2 (in-air natural domain). The score function is decomposed via Bayes as ∇log p(x_t|y1,y2) = ∇log p(x_t) + λ∇log p(y1|x_t) + (1−λ)∇log p(y2|x_t), and the noise predictor ε_θ(x_t,y1,y2,t) is rewritten to incorporate both classifier gradients, steering the reverse diffusion toward the in-air domain.
- **Prompt-learning classifier:** Keeps the CLIP-UIE backbone frozen and trains two learnable prompt tensors (T_n for in-air, T_u for underwater) of length N=77, optimised with binary cross-entropy on (in-air, underwater) image pairs, replacing brittle hand-written prompts.
- **Spatial attention:** A learnable conv+sigmoid head generates a spatial mask A on the ResNet-101 feature map F (B×1024×H×W); F' = A ⊙ F is then pooled into a global descriptor φ(I) and aligned with the text embedding via cosine similarity, focusing the model on turbid / hazy regions.
- **Joint visual–textual alignment & CLIP-Diffusion loss:** A classifier loss L_classifier built from the optimised prompts is added to the noise predictor; the overall fine-tuning objective is L_UDAN-CLIP = λ1·L1(ε, ε_θ(x)) + λ2·D_CLIP(f_θ(x), f_θ(x_target)), balancing pixel reconstruction with perceptual semantic alignment.
- **Training and evaluation:** Fine-tuned on the SUIM-E train split (1525 pairs) plus 800 random UIEB pairs; tested on T200 (SUIM-E test + remaining UIEB), with extra robustness tests on Color-Checker7 and C60. Reference (PSNR, SSIM) and non-reference (UIQM, UISM, UCIQE, CPBD, NIQE) metrics are reported and compared against UDCP, ULAP, Ucolor, TCTL-Net, UIEC²-Net, UDAformer, DM_underwater, and CLIP-UIE.
