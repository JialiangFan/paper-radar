# Assessing VLMs for Underwater Perception

> Authors: Muhammad Yousaf, Aitor Arrieta, Shaukat Ali, Paolo Arcaini, Shuai Wang
> Affiliations: Simula Research Laboratory / Oslo Metropolitan University / Mondragon University / NII Tokyo / DNV
> Year: 2026 (arXiv:2602.10655 v3)
> Industrial context: EU InnoGuard project, industrial partner DNV AS

## Topic
VLM perception evaluation for AUR software

## Background
Autonomous Underwater Robots (AURs) operate in low-visibility, noisy environments where conventional deep-learning perception modules are limited by scarce and noisy labeled data, undermining the trustworthiness of AUR software. Vision-Language Models (VLMs) promise better generalization to unseen objects and robustness to noise via contextual reasoning, but their performance, uncertainty, and calibration in underwater contexts remain understudied from a software engineering perspective. Motivated by the assurance and risk-management needs of the industrial partner DNV AS within the EU InnoGuard project, the authors empirically evaluate VLMs as components of AUR perception modules for underwater trash detection.

## Limitations & Research Problem
- **Limitation:** Deep-learning perception in AUR software depends on scarce, noisy labels; meanwhile VLMs lack systematic evidence on performance, uncertainty quantification, and calibration in underwater conditions, leaving software engineers and maritime industry partners without grounds to safely integrate them into ACPS / AUR software.
- **Problem:**
  - RQ1 (Performance): How well do VLMs classify underwater images?
  - RQ2 (Uncertainty Quantification): How uncertain are VLMs when classifying underwater images?
  - RQ3 (Performance-Uncertainty Relationship): What is the relationship between performance, confidence, uncertainty, and calibration, and how should it guide engineers selecting VLMs for AUR software?

## Contributions
- An empirical, software-engineering-oriented evaluation of four open-source ~7B VLMs (InstructBLIP, LLaVA-1.6, DeepSeek-VL2, QWen2.5-VL) on two underwater datasets (TrashCan1.0, SeaClear) for trash and object classification.
- A joint study of performance, confidence, uncertainty, and calibration that shows high confidence / low uncertainty does not imply high performance, highlighting calibration as a primary selection criterion.
- Industry-actionable findings: BLIP and DeepSeek are strongest overall, with BLIP best calibrated; LLaVA is overconfident and unreliable for safety-critical AUR perception, providing concrete guidance for ACPS / maritime adoption.
- A reproducible methodology and replication package for assessing VLMs as software components inside AUR perception modules.

## Methodology
- **AUR software architecture:** A VLM-based perception block feeds a planner and a controller; the VLM consumes the image plus a text instruction (e.g., "identify all visible objects in this underwater image") and emits multi-label predictions together with token-level logits used for uncertainty quantification (Fig. 1).
- **Datasets:** TrashCan1.0 (7,212 images) and SeaClear (8,610 images), with original fine-grained labels collapsed into a four-class multi-label task (Animal / Vegetation / Object / Trash) to test generalization to unseen underwater objects.
- **Subject VLMs:** InstructBLIP (ViT), LLaVA-1.6 (CLIP ViT-L/14), DeepSeek-VL2 (SigLIP + SAMB), QWen2.5-VL (redesigned ViT); all ~7B parameters, evaluated zero-shot at temperature 0 on a single NVIDIA RTX-5090.
- **Prompt design:** A single domain-dependent, instruction-style zero-shot prompt asks the VLM to list detected items per Animals / Vegetation / Objects / Trash with counts, enforcing structured output and semantic consistency across models.
- **Evaluation metrics:**
  - Performance (RQ1): F1 (Macro/Micro), Jaccard (Macro/Micro), Precision, Recall, plus per-class scores for the safety-critical Trash class.
  - Uncertainty (RQ2): probability-based metrics computed from token-level probabilities (confidence scores, entropy-style measures) plus calibration analysis.
  - Performance-uncertainty relationship (RQ3): reuses the RQ1/RQ2 metrics to test whether high-performing VLMs are also well calibrated.
- **Key findings:** BLIP and DeepSeek lead overall, especially on Trash and Object classes; LLaVA is highly confident but poorly calibrated (overconfident); BLIP offers the best performance-calibration trade-off and is the most reliable choice for industrial AUR software, demonstrating that VLM selection for AUR perception should jointly optimize performance and calibration rather than confidence alone.
