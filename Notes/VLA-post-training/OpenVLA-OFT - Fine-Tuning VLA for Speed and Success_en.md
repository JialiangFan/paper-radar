# Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success

- **Title:** Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success
- **Authors:** Moo Jin Kim, Chelsea Finn, Percy Liang
- **Venue:** arXiv preprint (arXiv:2502.19645)
- **Year:** 2025
- **Affiliations:** Stanford University


## Topic - VLA Fine-Tuning Recipe Optimization

## Background
Vision-language-action models (VLAs) built by fine-tuning pretrained vision-language models on large-scale robot datasets have demonstrated strong task execution, semantic generalization, and language following abilities. However, adapting VLAs to novel robot setups requires fine-tuning, and the most effective strategies remain unclear given the large design space encompassing action decoding schemes, action representations, and learning objectives. In particular, autoregressive VLAs suffer from slow inference (3-5 Hz), making them impractical for high-frequency bimanual control (25-50+ Hz), while alternative approaches such as diffusion-based VLAs introduce architectural complexity and multi-step denoising latency.

## Limitations & Research Problem
- Original OpenVLA's autoregressive decoding takes 0.33 seconds to generate a single 7-dimensional action on an A100 GPU, far too slow for high-frequency control
- Autoregressive generation makes action chunking impractical, as a chunk size of K increases latency by K-fold due to sequential token generation
- Discretizing continuous actions into 256 bins sacrifices fine-grained precision, degrading performance on dexterous manipulation tasks
- Diffusion-based VLAs achieve higher throughput but introduce substantial architectural differences, slower training convergence, and multiple denoising steps at inference
- Vanilla LoRA fine-tuning with the original training recipe yields unsatisfactory performance on bimanual manipulation tasks
- In multi-viewpoint settings, policies latch onto spurious visual correlations instead of attending to language instructions, resulting in poor language following

## Contributions
- Systematic empirical study of three key VLA fine-tuning design decisions: action generation strategy (autoregressive vs. parallel decoding), action representation (discrete vs. continuous), and learning objective (next-token prediction vs. L1 regression vs. diffusion)
- Proposed the Optimized Fine-Tuning (OFT) recipe combining parallel decoding with action chunking, continuous action representations, and an L1 regression objective, improving inference efficiency, task performance, and model input-output flexibility while maintaining algorithmic simplicity
- Achieved state-of-the-art 97.1% average success rate on the LIBERO benchmark while increasing action generation throughput by 26x with 8-step action chunks
- Introduced FiLM (Feature-wise Linear Modulation) for enhanced language grounding in the OFT+ variant, outperforming fine-tuned VLAs (RDT-1B, pi_0) and from-scratch baselines (ACT, Diffusion Policy) by up to 15% absolute on real-world ALOHA bimanual robot tasks
- Demonstrated that simple L1 regression with a high-capacity VLA matches diffusion-based methods in performance while offering faster training convergence and inference speed

## Methodology
- **Parallel Decoding**: Replaces causal attention with bidirectional attention and feeds empty action embeddings as input, enabling the decoder to generate all action dimensions in a single forward pass; naturally extends to action chunking where a single pass produces K x D action values for chunk size K
- **Continuous Action Representation**: Replaces discrete tokenization and softmax output with a 4-layer MLP (ReLU activation) action head that maps decoder hidden states directly to normalized continuous action values, avoiding precision loss from 256-bin discretization
- **L1 Regression Objective**: Minimizes mean L1 difference between predicted and ground-truth normalized actions; requires only a single forward pass at inference (unlike diffusion's multi-step denoising) and converges faster during training
- **FiLM Language Conditioning (OFT+)**: Averages task description language embeddings and projects them to obtain scaling (gamma) and shifting (beta) vectors; applies spatially-agnostic affine modulation (F_hat = (1+gamma) * F + beta) to visual features in each SigLIP and DINOv2 vision transformer block, strengthening the model's attention to language instructions
- **Flexible Input Processing**: Supports multiple camera viewpoints (256 patch embeddings per view via shared SigLIP-DINOv2 backbone) and low-dimensional robot state (projected via separate network), all concatenated along the sequence dimension before the Llama-2 decoder
- **Experimental Evaluation**: Systematic evaluation on LIBERO simulation (4 task suites, 10 tasks x 500 trials each) and real-world ALOHA bimanual platform (4 dexterous manipulation tasks, 20-300 demonstrations), fine-tuning OpenVLA 7B via LoRA (rank 32)
