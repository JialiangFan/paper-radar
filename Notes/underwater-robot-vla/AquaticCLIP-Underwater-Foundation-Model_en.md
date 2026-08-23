# AquaticCLIP - Vision-Language Foundation Model for Underwater Scenes

## Topic
Underwater vision-language foundation model

## Background
Aquatic ecosystems are under severe threat from overfishing, coastal development and climate change, making automated marine scene understanding critical for biodiversity monitoring. Vision-Language Models (VLMs) such as CLIP have achieved strong zero-shot performance in general domains, but transferring them to underwater imagery is hindered by low visibility, motion blur, color distortion and the lack of large-scale paired image-text data covering marine semantics.

## Limitations & Research Problem
- **Limitation:** Existing aquatic VLM efforts (e.g., MarineGPT, MarineInst) are scarce, rely on image-only datasets or target a single task (segmentation/QA), and lack a large-scale, domain-specific image-text paired corpus; off-the-shelf CLIP performs poorly on aquatic data because its pre-training distribution barely contains marine concepts.
- **Problem:** How to (i) construct a large-scale underwater image-text dataset without manual annotation, and (ii) design a contrastive pre-training framework in which visual and textual contexts mutually guide each other, so that the resulting VLM generalises across zero-shot and fine-tuned aquatic downstream tasks (classification, detection, segmentation, counting).

## Contributions
- Releases a **2 million underwater image-text paired dataset** assembled from heterogeneous sources (YouTube, Netflix, National Geographic, Marine Twitter, Fishes of Australia, Corals of the World, plus 1,200 marine biology textbooks); descriptions are enriched at both image and instance level using MarineGPT and refined by a textual description cleaning module.
- Proposes **AquaticCLIP**, a dual-encoder contrastive pre-training framework introducing two lightweight modules: a **Prompt-Guided Vision Encoder (PGVE)** that progressively aggregates patch features via learnable prompts, and a **Vision-Guided Text Encoder (VGTE)** that injects visual context into textual embeddings for cross-modal alignment.
- Demonstrates extensive zero-shot and fine-tuned evaluations across marine species classification (MAI, SAI), fine-grained fish/coral classification (FishNet, FNOI, LSF, CSC, CC), object detection (FishNet, DeepFish, Brackish, URPC), instance/semantic segmentation and object counting, consistently outperforming SOTA VLMs (CoOp, MaPLe, GPT-4V, BLIP2, MarineGPT, MarineInst) and vision-only baselines (ConvNeXt, ViT-L, AquaticVision DINOv2).

## Methodology
- **Dataset Construction:** Two-step pipeline of gathering and cleaning. Frames are extracted every ~50 from videos to avoid blur; PDF-Figures 2.0 mines figures and captions from textbooks; Twitter posts are filtered by hashtags (#MarineBiology, #Oceans, #Fisheries) and follower counts. Non-aquatic content is discarded.
- **Unsupervised Caption Generation:** A frozen MarineGPT (ViT image encoder + Q-former) generates image-level descriptions; for instance-level captions, MRegionCLIP and MarineDet detect objects, then MarineGPT captions each crop with the prompt "The image is <image>. Describe the object in this image:".
- **Textual Description Cleaning Module (TDCM):** Each generated caption is split into k keywords; cosine similarity between every keyword embedding and the image embedding is computed via a CLIP-style encoder pair, retaining only the top-p% most relevant keywords, which are then concatenated with manually verified ground-truth descriptions to form enriched captions C_i.
- **Prompt-Guided Vision Encoder (PGVE):** A frozen ViT-B/16 (Φ_v) produces patch embeddings P_i over n_p non-overlapping patches. A set of learnable prompt vectors Q_i (n_r=20) acts as queries in cross-attention with P_i (keys/values), followed by layer norm, MLP and softmax-based attention weights a_i(j) that aggregate patches into a single image-level feature f_i.
- **Vision-Guided Text Encoder (VGTE):** Cleaned captions are embedded by the CLIP text encoder Φ_t to obtain T_i. Patch features P_i and learned prompts E_i are concatenated as keys/values, while T_i serves as the query of a vision-guided attention layer; the residual update yields a context-aware text feature that better aligns with the visual modality.
- **Cross-Modal Contrastive Loss:** Symmetric InfoNCE loss L_cont = L_i2t + L_t2i with a learnable temperature τ, pulling matched (f_i, T_i) pairs together and pushing mismatched ones apart over a batch of W=512 pairs.
- **Training:** Four components (image encoder, text encoder, PGVE, VGTE) are jointly fine-tuned with Adam (lr 1e-4, weight decay 1e-5) for 80 epochs on 4 A100 GPUs.
- **Zero-shot Inference:** Class names are injected into prompt templates ("An image of {class}."), encoded by the text branch, and matched to image embeddings via cosine similarity; the same backbone is lightly fine-tuned to instantiate AquaticDet (detection) and AquaticOC (counting).
- **Ablations:** Systematic ablations confirm the value of PGVE, VGTE, the TDCM, and the combination of image-level and instance-level captions, with the full AquaticCLIP achieving e.g. 96.80% accuracy and 96.40% F1 on coral species classification (CSC) and substantial gains on fine-grained datasets (FishNet 84.20%, FNOI 80.10%, LSF 93.40% F1).
