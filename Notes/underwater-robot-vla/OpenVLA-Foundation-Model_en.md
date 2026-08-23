# OpenVLA - An Open-Source Vision-Language-Action Model

## Topic
Open-source generalist VLA model

## Background
Vision-Language-Action (VLA) models inject Internet-scale priors into robot control by fine-tuning pretrained visually-conditioned language models (VLMs) on robot trajectories. Prior state-of-the-art VLAs such as RT-2-X show strong generalization, but their weights, training code, and data mixtures are closed, blocking downstream research and adaptation to new robots or tasks.

## Existing Limitations and Research Questions
- **Limitation:** Existing SOTA VLAs are fully closed (no visibility into architecture, training procedure, or data mixture), and there is no established best practice for parameter-efficient fine-tuning and deployment of VLAs on commodity hardware.
- **Problem:** How to build a fully open, state-of-the-art generalist VLA together with a reproducible recipe for efficient fine-tuning and serving on new robots, tasks, and consumer-grade GPUs?

## Contributions
- Releases OpenVLA, a 7B-parameter open-source VLA that beats the 55B closed-source RT-2-X by 16.5% absolute success rate across 29 tasks while using 7x fewer parameters.
- Demonstrates effective fine-tuning of OpenVLA on 7 new manipulation tasks, outperforming from-scratch Diffusion Policy by 20.4% in multi-task, multi-object language-grounded settings.
- First work to validate LoRA low-rank fine-tuning and INT8/INT4 quantization for VLAs, enabling fine-tuning and inference on consumer GPUs (e.g. RTX 4090) without success-rate loss.
- Fully open-sources the 970k-trajectory training dataset, model weights, scalable PyTorch training codebase, and HuggingFace fine-tuning/inference notebooks as community infrastructure for VLA research.

## Methodology
- **Backbone:** Built on the Prismatic-7B VLM, combining a fused SigLIP + DinoV2 visual encoder (semantic + spatial features), a 2-layer MLP projector, and a Llama 2 7B language model backbone; input resolution 224x224.
- **Action tokenization:** Following RT-2, each dimension of the 7-DoF end-effector action is discretized into 256 bins between the 1st and 99th percentile of training actions, and the bins overwrite the 256 least-used tokens in the Llama tokenizer.
- **Training data:** A curated 970k-trajectory subset of Open X-Embodiment, restricted to single-arm manipulation with at least one third-person camera, balanced across embodiments, scenes and tasks using Octo's data mixture weights.
- **Training recipe:** Standard next-token cross-entropy loss applied only on action tokens; vision encoder unfrozen during fine-tuning (critical for fine-grained spatial control); fixed LR 2e-5; 27 epochs until action-token accuracy passes 95%; 64 A100 GPUs for 14 days (~21.5k GPU-hours), batch size 2048.
- **Efficient adaptation:** Provides LoRA fine-tuning, INT8/INT4 quantized inference (~15GB VRAM in bf16, ~6Hz on a single RTX 4090), and a remote VLA inference server for streaming actions to robots without local heavy compute.
