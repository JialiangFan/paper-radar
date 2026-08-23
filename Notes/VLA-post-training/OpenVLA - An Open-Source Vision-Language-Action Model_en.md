# OpenVLA: An Open-Source Vision-Language-Action Model

- **Title:** OpenVLA: An Open-Source Vision-Language-Action Model
- **Authors:** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, et al.
- **Venue:** arXiv preprint (arXiv:2406.09246)
- **Year:** 2024
- **Affiliations:** Stanford University, UC Berkeley, Toyota Research Institute, Google DeepMind, Physical Intelligence, MIT


## Topic - Open-source generalist robot VLA

## Background
Large pretrained vision-language models (VLMs) have demonstrated strong generalization capabilities, and fine-tuning them into vision-language-action models (VLAs) enables direct generation of robot control actions, offering a new paradigm for generalist robot manipulation policies. However, existing VLAs such as RT-2-X are closed-source, and there has been no systematic investigation into efficiently fine-tuning VLAs for new tasks and robot setups. OpenVLA addresses these gaps by introducing the first fully open-source generalist VLA and exploring parameter-efficient fine-tuning strategies.

## Limitations & Research Problem
- **Limitation:** Existing VLA models (RT-2, RT-2-X, RFM-1, etc.) are closed-source, lacking transparency in model architecture, training procedures, and data mixture, which hinders academic research and community reproducibility.
- **Limitation:** Prior work has not systematically explored methods for efficiently fine-tuning VLAs to new robots, environments, and tasks, particularly lacking practical guidance for deploying VLAs on consumer-grade GPUs.
- **Limitation:** Prior generalist robot policies (RT-1-X, Octo) have relatively small parameter counts and do not leverage Internet-scale pretraining, leading to poor performance on tasks with distractors and semantic generalization.
- **Problem:** How to build an open-source, fine-tunable generalist VLA that outperforms closed-source counterparts?
- **Problem:** How to leverage LoRA and quantization to make VLA training and inference feasible on consumer hardware?

## Contributions
- Introduces OpenVLA, a 7B-parameter open-source VLA built on Prismatic VLM (dual visual encoder fusing DINOv2 and SigLIP + Llama 2 7B backbone), fine-tuned on 970k real-world robot demonstrations from Open X-Embodiment.
- Outperforms the 55B-parameter closed-source RT-2-X by 16.5% absolute success rate across 29 tasks on multiple robot platforms (WidowX, Google Robot), with 7x fewer parameters.
- Provides the first systematic study of efficient fine-tuning strategies for VLAs, including full fine-tuning, frozen vision, sandwich fine-tuning, and LoRA. LoRA (rank=32) matches full fine-tuning performance while training only 1.4% of parameters, completable in 10-15 hours on a single A100 GPU.
- Demonstrates that 4-bit quantized inference preserves performance while reducing GPU memory from 16.8GB to 7.0GB, enabling deployment on consumer-grade GPUs.
- Fully open-sources model weights, training code, fine-tuning notebooks, and the PyTorch training pipeline.

## Methodology
- **Model architecture:** Uses Prismatic-7B VLM as the backbone, consisting of (1) a dual visual encoder (DINOv2 for spatial features + SigLIP for semantic features, concatenated channel-wise), (2) a 2-layer MLP projector mapping visual features to the language embedding space, and (3) Llama 2 7B as the LLM backbone for generating action tokens.
- **Action discretization:** Each dimension of the continuous action space is uniformly discretized into 256 bins (based on the 1st to 99th percentile of training data). Action tokens overwrite the 256 least-used tokens in the Llama tokenizer. Training uses a standard next-token prediction objective with cross-entropy loss computed only on action tokens.
- **Training data:** Curated from Open X-Embodiment, filtered to single-arm end-effector manipulation datasets with at least one third-person camera view. Octo's data mixture weights are adopted to balance embodiment, task, and scene diversity, covering 970k trajectories total.
- **Key design decisions:** (1) Prismatic VLM chosen over LLaVA and IDEFICS-1 due to its fused visual encoder yielding 35% improvement on language grounding tasks; (2) 224x224 resolution adopted (384x384 showed no performance gain but 3x training cost); (3) vision encoder is fine-tuned during VLA training (contrary to the VLM convention of freezing it); (4) training runs for 27 epochs until action token accuracy exceeds 95%; (5) learning rate of 2e-5.
- **Training infrastructure:** 64 A100 GPUs, batch size 2048, 14 days of training (21,500 A100-hours). Inference at bfloat16 precision requires 15GB VRAM, running at approximately 6Hz on an RTX 4090.
- **Fine-tuning evaluation:** Fine-tuned on Franka Emika Panda with 10-150 demonstrations per task. Compared against Diffusion Policy, Octo, and other baselines, OpenVLA achieves the highest average success rate across 7 task categories, with particularly strong advantages on diverse multi-instruction tasks requiring language grounding.
