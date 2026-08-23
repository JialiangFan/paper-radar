# Octo: An Open-Source Generalist Robot Policy

- **Title:** Octo: An Open-Source Generalist Robot Policy
- **Authors:** Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al.
- **Venue:** arXiv preprint (arXiv:2405.12213)
- **Year:** 2024
- **Affiliations:** UC Berkeley, Stanford University, Carnegie Mellon University, Google DeepMind


## Topic - Open-Source Generalist Robot Policy

## Background
Large policies pretrained on diverse robot datasets hold the promise of transforming robotic learning: instead of training new policies from scratch, generalist robot policies (GRPs) can be finetuned with only a small amount of in-domain data. However, building a truly general-purpose robot model presents unique challenges, requiring handling of diverse robot embodiments, sensor setups, action spaces, task specifications, and compute budgets. Prior models such as RT-1-X, RT-2-X, and RoboCat have made progress toward this goal, but remain limited in input flexibility, finetuning adaptability, and open-source accessibility.

## Limitations & Research Problem
- **Limitation:** Existing generalist robot policies (e.g., RT-1-X, RT-2-X) constrain downstream users to a predefined and restrictive set of input observations (e.g., a single camera stream), preventing flexible adaptation to new sensor configurations.
- **Limitation:** Prior models lack support for effective finetuning to new observation and action spaces; switching the observation or task specification requires re-initializing large components of the pretrained model.
- **Limitation:** The largest and best-performing generalist robot models (e.g., RT-2-X with 55B parameters) are not publicly available, hindering community research and reproducibility.
- **Limitation:** Prior architectures predominantly use large ResNet-style visual encoders fused with comparatively small transformers, limiting scalability when training on large, diverse multi-embodiment datasets.
- **Problem:** How to design an open-source, flexible, and scalable generalist robot policy that supports diverse sensory inputs and action spaces while enabling efficient finetuning to new robot setups?

## Contributions
- Introduced Octo, an open-source transformer-based generalist robot policy pretrained on 800k robot trajectories from the Open X-Embodiment dataset, the largest robot manipulation dataset to date.
- Designed a modular transformer architecture with block-wise attention masking and readout tokens, enabling flexible addition or removal of observation inputs and action outputs without modifying pretrained parameters.
- Supported both language instruction and goal image task conditioning, with flexible switching during finetuning.
- Employed a diffusion-based action head to predict continuous, multi-modal action distributions via action chunking, significantly outperforming MSE and discretized action prediction methods.
- Conducted extensive experiments across 9 robot setups at 4 institutions, demonstrating effectiveness in zero-shot multi-robot control and data-efficient finetuning, outperforming the next best baseline by 52% on average in finetuning evaluations.
- Fully open-sourced model checkpoints (Octo-Small 27M, Octo-Base 93M), training pipeline, finetuning scripts, and data loaders, providing reproducible research infrastructure for the community.
- Performed systematic ablation studies on model architecture, training data, training objective, and model scale, providing design guidance for future generalist robot policies.

## Methodology
- **Architecture:** Adopted a "transformer-first" design consisting of three components: (1) input tokenizers that convert language instructions (via pretrained t5-base encoder) and image observations (via shallow CNN) into token sequences; (2) a transformer backbone that processes task and observation token sequences using block-wise causal attention masking for modularity; (3) learned readout tokens passively aggregate information from the sequence, whose embeddings are decoded into actions by a lightweight diffusion action head.
- **Modular adaptation mechanism:** The block-wise attention structure of the transformer allows adding new observation tokens (e.g., force-torque inputs) or new action heads (e.g., joint position control) during finetuning, requiring only new positional embeddings, lightweight encoders, or new head parameters while fully retaining pretrained weights.
- **Training data:** Curated 25 datasets from the Open X-Embodiment dataset spanning multiple robot embodiments and scenes, with weighted sampling to balance data diversity and scale, doubling the weight for more diverse datasets and down-weighting highly repetitive ones.
- **Training objective:** Used a conditional diffusion decoding head (based on the DDPM objective) with a learned denoising network that performs K-step denoising on a Gaussian noise vector to generate actions, using a cosine noise schedule. Only one forward pass of the transformer backbone is required; the multi-step denoising is carried out entirely within the lightweight diffusion head.
- **Training details:** Provided two model variants, Octo-Small (ViT-S scale, 27M) and Octo-Base (ViT-B scale, 93M); trained with AdamW optimizer, inverse square root decay learning rate schedule, batch size 2048 on a TPU v4-128 pod for 300k steps (~14 hours); used 2-frame observation history and hindsight goal relabeling for data augmentation.
- **Finetuning recipe:** Applied a unified recipe using ~100 target domain demonstrations, 50k steps with cosine decay learning rate, completable in under 5 hours on a single NVIDIA A5000 GPU, accommodating new observations (force-torque), new action spaces (joint position), and new robot embodiments (bimanual manipulation).
