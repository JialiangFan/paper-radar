# HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents

- **Title:** HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents
- **Authors:** Tencent Robotics X & HY Vision Team
- **Venue:** arXiv preprint (arXiv:2604.07430)
- **Year:** 2026
- **Affiliations:** Tencent


## Topic - Embodied Foundation Models with Post-Training for Real-World Agents

## Background
Vision-Language Models (VLMs) have made significant progress in general visual understanding, but two core gaps remain for real-world embodied agents: (1) **Fine-grained visual perception** — mainstream VLMs trained on static web data fail to capture the granular spatial details required for physical grounding; (2) **Embodied prediction, interaction, and planning** — lack of modeling for dynamic prediction, interactive feedback, and long-horizon planning in the physical world. HY-Embodied-0.5 systematically bridges the divide between general VLMs and embodied intelligence across architecture, data, and training.

## Limitations & Research Problem
- General VLMs underperform on spatial reasoning, 3D understanding, and embodied interaction tasks, making them unsuitable for direct robot control
- Edge deployment imposes strict constraints on model size and inference latency that existing large models cannot meet
- Heavy visual training during VLM pretraining degrades language capabilities (modality conflict)
- Existing post-training methods lack a unified reward design for the heterogeneous output formats of embodied tasks (geometric grounding, trajectory prediction, discrete decisions, open-ended reasoning)
- Large model reasoning abilities are difficult to distill efficiently into compact models; standard offline distillation suffers from train-inference distribution mismatch

## Contributions
- Proposes the HY-Embodied-0.5 model family: an efficient MoT-2B variant (2B activated / 4B total parameters) for edge deployment and a powerful MoE-A32B variant (32B activated / 407B total parameters) for complex reasoning
- Architectural innovation — **Mixture-of-Transformers (MoT)**: introduces independent QKV and FFN parameters for vision and language branches, decoupling modality processing to prevent language degradation from heavy visual training; introduces **Visual Latent Tokens** to bridge visual and language modalities
- Efficient visual encoder **HY-ViT 2.0** (400M parameters): natively supports arbitrary-resolution inputs with accurate representations distilled from a larger internal ViT
- Iterative self-evolving post-training pipeline: alternates between RL (GRPO) and Rejection Sampling Fine-tuning (RFT) to progressively deepen embodied reasoning
- **Task-aware reward design**: categorizes embodied outputs into four types (Grounding-Based, Trajectory-Based, Regression-Based, Textual-Based) with specialized reward functions for each
- **Large-to-Small On-Policy Distillation (OPD)**: the student generates rollouts first, and the teacher applies teacher forcing on the student-generated prefixes; KL divergence minimization enables on-policy distillation that resolves the distribution mismatch of offline distillation
- MoT-2B achieves best performance on 16 of 22 embodied benchmarks among similar-sized models; MoE-A32B achieves 67.0% average score, surpassing Gemini 3.0 Pro (63.6%)
- Real-robot experiments on three tasks (Packing 85%, Stacking 80%, Hanging 75%) significantly outperform Pi0 and Pi0.5 baselines

## Methodology
- **Model architecture**: Built on the VLM paradigm (Vision Encoder + LLM) with MoT architecture that duplicates independent FFN and QKV parameters for vision and text branches (initialized from pretrained LLM weights); vision branch uses Local Full Attention while language branch uses Global Causal Attention; visual latent tokens are appended at the end of visual sequences with independent supervision loss and mixed optimization loss connecting vision and language
- **Pretraining data**: Over 100M samples spanning four categories — basic visual perception, embodied-centric (robot manipulation/navigation/autonomous driving), spatial-centric (3D/depth/multi-view), and general understanding
- **Three-stage training strategy**: Stage 1 jointly optimizes LLM Loss + Vision Loss + Global Loss for large-scale pretraining; Stage 2 mid-training optimizes LLM Loss only; Stage 3 post-training consists of SFT Cold Start → RL (GRPO) → RFT iterative cycles
- **RL training details**: Uses GRPO objective with group size G=16, asymmetric clip ratio [0.8, 1.35], batch size 128, learning rate 8e-7; each RL stage trains for 5 epochs on 50K freshly constructed samples; dynamic data construction discards all-correct (too easy) and all-wrong (too hard) samples, retaining only frontier samples with partial success
- **Evolving Deep Thinking**: After RL, performs multi-sample rollout on a curated data pool; a stronger teacher model scores chain-of-thought quality, filtering ~300K high-quality traces for the subsequent RFT stage; alternating RL-RFT cycles gradually consolidate occasional successes into stable reasoning patterns
- **On-Policy Distillation**: The student first rolls out a response y, then the teacher computes next-token distributions under teacher forcing on the student-generated prefixes; optimization minimizes per-token KL divergence, providing precise teacher guidance exactly where the student makes errors
- **VLA extension**: Extends MoT-2B with an Action Expert module (following Pi0/Pi0.5 structural design), first fine-tuned on 5K hours of UMI data, then SFT on 300-700 task-specific real demonstrations before deployment
