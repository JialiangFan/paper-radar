# PointVLA: Injecting the 3D World into Vision-Language-Action Models

## Topic
Injecting 3D point clouds into VLA

## Background
Vision-Language-Action (VLA) models excel at robotic manipulation by leveraging large-scale 2D vision-language pretraining, but their reliance on RGB-only inputs limits the 3D spatial reasoning (depth, object manipulation, height) critical for real-world interaction. Retraining with 3D data from scratch is computationally prohibitive and wastes valuable existing 2D robot datasets. PointVLA injects point clouds as a complementary conditioning signal without retraining the pretrained VLA.

## Limitations & Research Problem
- **Limitation:** Most robot foundation models (OpenVLA, π0, DexVLA, etc.) use only 2D visual input and lack 3D spatial information; pure-3D alternatives (3DVLA, 3D Diffusion Policy) either depend on simulation with a sim-to-real gap or require retraining / discarding 2D data, which is expensive and prone to overfitting on scarce 3D data.
- **Problem:** How can sparse 3D point-cloud information be efficiently injected into a pretrained VLA to grant 3D spatial perception, **without retraining and without disrupting** the well-established 2D vision-text representations?

## Contributions
- Propose PointVLA, a framework that injects point clouds into a pretrained VLA **without retraining**: it freezes the VLM backbone and the vanilla action expert and injects 3D geometric features only through a lightweight modular block, minimizing disruption to pretrained representations and mitigating catastrophic forgetting of 2D knowledge.
- Introduce a **skip-block analysis** that systematically identifies which blocks of the action expert can be skipped at inference (i.e., are "less useful"), and injects 3D features only into these non-critical blocks for a good performance/efficiency trade-off.
- Validate on simulation (RoboTwin) and real robots (bimanual UR5e, AgileX), outperforming 2D/3D imitation-learning methods (OpenVLA, Diffusion Policy, DexVLA, DP3, ScaleDP), and demonstrate three unique advantages: few-shot multi-tasking, real-vs-photo discrimination (mitigating object hallucination), and height adaptability.

## Methodology
- **Overall paradigm:** treat the 3D point cloud as a **complementary conditioning signal** rather than a primary input modality, decoupling 3D processing from the core 2D visual encoder to preserve the integrity of pretrained 2D representations. Built on DexVLA: a 2B-parameter Qwen2-VL serves as the VLM "brain", and a 1B-parameter ScaleDP (a diffusion-policy variant with **32 diffusion transformer blocks**) is the action expert.
- **In what form does 3D/depth enter the model:**
  - **Point Cloud Encoder:** a simplified hierarchical convolutional architecture (similar to iDP3); upper conv layers extract low-level features while lower blocks learn high-level scene representations, with max pooling between layers to progressively reduce point density. Features from each conv block are concatenated into a unified multi-level 3D embedding. The authors note pretrained 3D encoders hinder learning in new environments, hence a lightweight self-trained encoder.
  - **Point Cloud Injector (injection-block design):** first transform the channel dimension of the point-cloud embedding to match the action embedding; an **Adapter** compresses the large action embedding to align with the 3D embedding (chunk size 1280 → 128-dim point-cloud emb). For selected blocks, an **MLP adapter** projects the 3D features, which are then injected into the block via an **addition** operation; the injection path is wrapped by **zero-initialized linear layers (Zero Linear)** so the injection is initially zero and does not disturb the original model output.
  - **Where to inject (which blocks):** a skip-block analysis on DexVLA's shirt-folding task — single-block skipping shows the **first 11 blocks are crucial** (skipping any causes a large performance drop), while blocks beyond ~11 (11–31) contribute less; multi-block skipping shows **up to 5 consecutive blocks can be skipped** before failure. Therefore 3D is injected only into these "less critical" blocks, adding only **5 injection blocks** total — lightweight and fast at inference.
- **Why freeze:** (1) training from scratch or fully retraining with 3D data is computationally infeasible and discards valuable 2D data; (2) injection alters the representation of the affected block — to minimize interference with the action expert's pretrained feature space, **the VLM backbone and most of the action expert are frozen**, leaving only the 5 conditioning/injection blocks and the final layers of the action expert (adapted to the embodiment's output) trainable. Keeping the 2D vision-text embeddings intact preserves a reliable information source while reducing overfitting to scarce 3D data.
- **Training:** fine-tuned from DexVLA stage-1 pretrained weights with the VLM set trainable to learn new language instructions, chunk size 50; point clouds collected with a RealSense L515.
- **Quantitative gains (vs RGB-only DexVLA, i.e. the ablation of PointVLA):**
  - Long-horizon packing (bimanual UR5e) average completion length **Avg. Len 2.36 vs DexVLA 1.72** (and far above Octo 0.27 / OpenVLA 0.36 / DP 0.36 / ScaleDP-1B 0.72).
  - Real-vs-photo discrimination success rate **3/3 vs DexVLA 0/3** (OpenVLA/DP/ScaleDP all 0/3), effectively mitigating object hallucination.
  - Height adaptability (trained at 3 mm, tested at 52 mm table height) **5/5 vs all 2D baselines 0/5**.
  - RoboTwin simulation: highest average success rate across tasks under both 20 and 50 demonstrations; notably, adding RGB to the pure-3D DP3 hurts performance, underscoring the necessity of *conditionally* injecting 3D.
