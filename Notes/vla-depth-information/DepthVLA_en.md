# DepthVLA: Enhancing Vision-Language-Action Models with Depth-Aware Spatial Reasoning

## Topic
Depth-aware spatial reasoning VLA

## Background
Vision-Language-Action (VLA) models, built on pretrained Vision-Language Models (VLMs), inherit strong language grounding and cross-task generalization and have become a leading paradigm for robotic manipulation. However, VLMs are weak at 3D spatial reasoning (insensitive to object shape and fine geometry), so VLA performance degrades on tasks requiring precise spatial understanding—grasping small objects, precise operation, collision avoidance. DepthVLA extends the π0 mixture-of-transformers (MoT) framework by explicitly adding a pretrained depth expert for geometric perception.

## Limitations & Research Problem
- **Limitation:** Existing VLAs rely on extensive action-data pretraining to ground VLMs in 3D space, which is inefficient, poorly scalable, and still insufficient for accurate spatial understanding. External-depth approaches (e.g., SpatialVLA generating pseudo point clouds with an off-the-shelf depth estimator) are essentially workarounds—the depth module is not optimized end-to-end with the VLA, capping performance. Generative-world-model and Chain-of-Thought (CoT) approaches either lack explicit 3D knowledge or must autoregressively generate hundreds of spatial tokens, incurring >2 s inference latency.
- **Problem:** How can recent advances in 3D perception (monocular depth / 3D foundation models) be leveraged to enhance VLAs with explicit, end-to-end fine-grained spatial reasoning **without sacrificing inference speed**?

## Contributions
- **DepthVLA architecture:** A novel VLA integrating a pretrained depth prediction expert into a mixture-of-transformers framework, enabling explicit spatial reasoning while preserving semantic grounding from the VLM.
- **Per-expert pretraining strategy:** The MoT design lets each expert (VLM and depth) be pretrained separately on diverse datasets beyond embodied action data, improving training efficiency and scalability.
- **Extensive real-world + simulation validation:** Significantly outperforms SOTA across real-robot, LIBERO, and Simpler benchmarks—78.5% vs 65.0% (real-world progress), 94.9% vs 93.6% (LIBERO), 74.8% vs 58.8% (Simpler)—with gains concentrated on tasks demanding spatial reasoning (grasping accuracy, collision avoidance).

## Methodology
- **Three-expert MoT structure:** Extends π0's two experts (VLM + action expert) with an independent depth expert—
  - **VLM expert:** Paligemma-3B encodes image(s) and language instruction `l` for semantic and open-vocabulary perception (vision via SigLIP).
  - **Depth expert:** an encoder-decoder. Encoder is DINOv2-L, **initialized from Depth Anything V2** to inherit strong 3D priors from a large-scale depth foundation model; the decoder mirrors the VLM transformer structure with a linear head for depth output. Uses the same backbone as the VLM but with **separate weights and dimensions**.
  - **Action expert:** a flow-matching action expert trained from scratch, taking proprioception and noise, outputting a k-step continuous action chunk.
- **How depth/3D enters the model (core):** Rather than feeding only a final depth map, the action expert **attends to the depth expert's intermediate-layer features at every layer**, exploiting rich geometric representations (not low-dimensional depth outputs) to generate actions. All three experts **share the same attention layers**, but a **block-wise mask** governs information flow: VLM tokens and depth tokens attend only to themselves (preserving pretrained abilities), while action tokens attend to all streams (VLM + depth + proprio + noise). Actions are thus conditioned jointly on language, visual, and spatial-geometric cues.
- **Where depth acts / training stages:** Two stages—
  1. **Per-expert pretraining:** the depth expert is first pretrained on diverse 3D datasets (WildRGB-D, Scannet, Scannet++, HyperSim) on a monocular depth prediction task using a **scale-invariant log loss** (`L_si = sqrt((1/n)Σy² − λ((1/n)Σy)²)`, `y = log d̂ − log d`, λ=0.5) to acquire robust spatial reasoning; the VLM inherits Paligemma pretraining. Depth is decoupled from action here, allowing massive non-embodied 3D data.
  2. **End-to-end VLA training:** trained on embodied action data via imitation learning (maximizing `log π_θ`) plus a **flow-matching loss** `L_flow`; the **depth prediction loss is retained**, giving a final objective `L = L_si + L_flow` that jointly optimizes spatial reasoning and action generation end-to-end. Each benchmark is then fine-tuned for 4k–30k steps.
- **Efficiency:** Adds only 600M parameters over the π0 baseline (300M DINOv2 encoder + 300M depth decoder), 8.0 GB vs 6.7 GB VRAM, 210 ms vs 190 ms per step. Because actions are predicted in 1-second chunks (16 steps on a 15 Hz platform), the extra latency is negligible—the key advantage over CoT-style methods (>2 s).
- **Ablation findings:** (i) depth-expert pretraining, (ii) retaining depth loss during VLA training, and (iv) the block-wise mask are all necessary; (iii) freezing the depth expert barely hurts (its learned spatial representation is robust/universal, easing deployment without GT depth); (v) **predicting depth beats directly inputting GT depth** (94.9% vs 93.3%), attributed to modality competence—self-predicting depth avoids over-reliance on external signals and integrates geometric reasoning more effectively into the shared representation space.
- **Limitation:** monocular depth prediction is ill-posed and can fail on tiny edges, transparent/texture-less objects; future work may explore multi-view depth or pointmap prediction.
