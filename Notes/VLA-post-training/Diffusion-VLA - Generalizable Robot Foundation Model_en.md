# Diffusion-VLA: Generalizable and Interpretable Robot Foundation Model via Self-Generated Reasoning

- **Title:** Diffusion-VLA: Scaling Robot Foundation Models via Unified Diffusion and Autoregression
- **Authors:** Junjie Wen, Yichen Zhu, Minjie Zhu, Jinming Li, Zhiyuan Xu, Zhengping Che, Chaomin Shen, Yaxin Peng, Dong Li, Feifei Feng, Jian Tang
- **Venue:** ICML 2025 (PMLR 267)
- **Year:** 2025
- **Affiliations:** Midea Group, East China Normal University, Shanghai University


## Topic - Reasoning-Enhanced Vision-Language-Action Model

## Background
Vision-Language-Action (VLA) models have become a dominant paradigm for robot policy learning. Autoregressive VLAs (e.g., RT-2, OpenVLA) generate actions via next-token prediction, while diffusion-based policies (e.g., Diffusion Policy) model multimodal action distributions through a noise-denoising process. However, autoregressive VLAs suffer from imprecise action generation and slow inference, whereas diffusion models inherently lack reasoning and language understanding capabilities. Unifying the reasoning power of autoregressive models with the robust, high-frequency action generation of diffusion models presents a critical open challenge.

## Limitations & Research Problem
- Autoregressive VLAs discretize continuous actions into fixed-size tokens, disrupting action coherence and precision
- Next-token prediction is inherently inefficient for real-time robotic control (e.g., OpenVLA runs at only 5Hz)
- Diffusion-based policies generate robust actions but lack language reasoning capabilities for semantically complex tasks
- Naively combining autoregressive reasoning with diffusion action generation leaves an implicit gap where reasoning signals do not effectively guide policy learning
- Existing methods exhibit poor generalization to visual changes (distractors, novel backgrounds) and unseen objects in zero-shot settings

## Contributions
- Proposed Diffusion-VLA (DiVLA), a unified end-to-end framework integrating autoregressive reasoning with diffusion-based action generation
- Designed a reasoning injection module using Feature-wise Linear Modulation (FiLM) to directly inject self-generated reasoning embeddings into the diffusion policy network, enabling explicit reasoning-guided policy learning
- Built upon a pre-trained VLM (Qwen2-VL), preserving vision-language understanding and conversational capabilities while mapping action tokens to the diffusion model via a projection layer
- Leveraged GPT-4o to automatically transform robot datasets (e.g., Droid) into reasoning-augmented training data
- Achieved state-of-the-art results across multi-task learning, factory sorting, zero-shot bin picking (63.7% on 102 unseen objects), and bimanual table bussing on real robots, outperforming Diffusion Policy, OpenVLA, Octo, and TinyVLA
- DiVLA-2B achieves 82Hz inference on a single A6000 GPU; DiVLA-7B reaches 42Hz, which is 8x faster than OpenVLA at the same model size
- Scalable model family (2B, 7B, 72B parameters) demonstrating consistent generalization improvements with increased scale

## Methodology
- **Vision encoding**: SigLIP encodes images into dense visual features, compressed into a fixed number of visual embeddings via a Transformer; multi-view inputs are supported by sharing the SigLIP backbone and concatenating outputs
- **Language-reasoning backbone**: Qwen2-VL serves as the VLM backbone, autoregressively generating reasoning tokens (task decomposition and explanation) followed by action tokens
- **Projection layer**: A two-layer MLP with LayerNorm projects action tokens from the VLM's final embedding layer into the diffusion model's input dimension space
- **Diffusion action head**: Standard Diffusion Policy design with randomly initialized weights; generates continuous action sequences through noise-denoising; an appended MLP layer maps outputs to the robot's joint space
- **Reasoning injection module**: Extracts the final embedding of the tokenized reasoning output and injects it into diffusion policy network layers via FiLM conditioning; reasoning serves as an auxiliary contextual signal that modulates the policy network without dominating the primary decision-making flow
- **Training objective**: Joint optimization of diffusion loss $L_{diff}$ and next-token prediction loss $L_{ntp}$, with total loss $L = L_{diff} + \alpha L_{ntp}$ ($\alpha=10$)
- **Pretraining data**: DiVLA-2B/7B pretrained on the Droid dataset; DiVLA-72B pretrained on OXE + Droid; GPT-4o is used to automatically generate reasoning annotations for data lacking language labels
- **Fine-tuning strategy**: LoRA applied to fine-tune the VLM; visual encoder is frozen; adaptation to new embodiments requires only replacing the final MLP layer
