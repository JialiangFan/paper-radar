# OmniVLA: Physically-Grounded Multimodal VLA with Unified Multi-Sensor Perception for Robotic Manipulation

## Topic
Multi-sensor VLA manipulation

## Background
Vision-language-action (VLA) models generalize well on robotic manipulation thanks to large-scale vision-language pretraining, but most consume RGB camera input only, which prevents them from tasks requiring beyond-visible perception (e.g., grabbing a cold drink, seeing through a closed box, finding a ringing phone buried under clothes). OmniVLA unifies beyond-RGB sensors — infrared (thermal), mmWave radar, and an acoustic microphone array — into a VLA so the robot gains physically-grounded spatial intelligence.

## Limitations & Research Problem
- **Limitation:** Most VLAs only support RGB and lack non-visible cues. Naively feeding raw sensor streams into an RGB-trained VLA backbone yields poor performance and data efficiency; training a separate encoder per sensor needs huge amounts of data, and hardware-specific fusion architectures fail to generalize across diverse sensors. Sensor data is also far scarcer than web-scale image-text pairs.
- **Problem:** How to integrate heterogeneous multi-sensor information into a VLA in a data-efficient, hardware-agnostic way that reuses the pretrained vision encoder and keeps sensor cues spatially grounded on target objects to guide manipulation?

## Contributions
- OmniVLA, claimed to be the first VLA unifying infrared / mmWave / acoustic sensing to enable manipulation beyond RGB perception.
- **Sensor-masked image**: a unified representation that overlays sensor information onto the RGB image as colored masks — spatially grounded and semantically aligned — enabling reuse of pretrained vision encoders, a uniform interface across sensors/resolutions/hardware, and improved learning efficiency.
- A lightweight OmniVLA architecture with extensive real-world evaluation; open-sourced (github.com/GuoHeyu/OmniVLA).

## Methodology
**On depth/3D information (the reader's focus):** This paper is not centered on depth but on beyond-RGB multi-sensor fusion. A depth camera is merely part of the hardware sensor suite (mounted alongside RGB, IR, mmWave, and a 6-mic array); RGB provides the "standard visual perception," and the paper gives no dedicated depth-injection mechanism — "depth enhancing VLA spatio-temporal understanding" is only cited in related work ([16]-[20]). The 3D/physical cues actually injected come from converting **mmWave / acoustic data into azimuth–elevation heatmaps via delay-and-sum beamforming** (Eq. 1), giving a 2D spatial mapping consistent with RGB (indirectly encoding bearing / occluded-object location); thermal is already a raster image.

**Two-part pipeline:**
1. **Sensor-masked image generation (off-the-shelf, not trained, runs asynchronously in background):**
   - Preprocessing: all raw measurements are turned into a camera-like 2D spatial representation — thermal is already a raster over (u,v); mmWave/acoustic use beamforming to produce azimuth-elevation heatmaps.
   - Segmentation: a VLM (GPT-4o) takes the task text + RGB to generate segmentation-keyword prompts (e.g., "red block/drink", "black phone"), then Grounded SAM 2 (SAM2 + Grounding DINO) produces a 0-1 mask (Eq. 2). Prompts are generated at task start and updated at low frequency in the background, so VLM latency does not affect real-time control.
   - Overlay/blending: each sensor image is roughly aligned to RGB by a one-time Calibration (rotation + cropping), then alpha-blended within the mask region (Eq. 3, default α=1, i.e., the masked region is fully recolored with sensor information).
2. **Multi-sensor VLA architecture (built on SmolVLA by default):**
   - The sensor-masked image goes into a **frozen pretrained vision encoder** (shared with RGB) → each sensor has its own MLP projector producing aligned tokens → concatenated with language tokens (from the tokenizer) → LLM backbone → a diffusion/flow-matching Action Expert generating an action chunk (Eq. 4). The setup is flexible — a single sensor can be used depending on deployment.

**Training stages:**
- **Base training (primary):** start from pretrained SmolVLA weights; **freeze the vision encoder**; **initialize each sensor's MLP projector from the pretrained RGB projection layer** (using established visual feature mappings as a strong prior so the model adapts quickly to sensor-masked images); then **co-fine-tune** the sensor MLPs together with the unfrozen backbone on collected demonstrations. 8×A100, ~14h / 50K steps, batch 32; inference ~15 predictions/sec on an RTX 4090.
- **Multi-sensory pretraining + few-shot adaptation (generalization experiment):** pretrain on an 800-episode mixed corpus (200 each for thermal/mmWave/acoustic + 200 generic pick-and-place), then adapt to unseen tasks with only **25 episodes** of few-shot finetuning.

**Quantitative gains vs RGB-only / raw-sensor:**
- Average task success **84%**, vs VLA-RGB 25% (**+59%**) and VLA-RAW (raw sensor images, no overlay) 56% (**+28%**); task scores 0.90 vs 0.55 / 0.73.
- Data efficiency: sensor-masked images reach raw-sensor-level success with only ~**50%** of the training episodes (Fig. 6).
- Generalization (Table III / Fig. 7): on unseen tasks, outperforms OmniVLA-Base (+59%) and Pretrained VLA-RAW (+28%) on average, up to +68% on a single task; decomposed into Stage 1 (select the right target, benefiting from spatial alignment) + Stage 2 (complete manipulation, benefiting from multi-sensory pretraining priors).
- Backbone-swappable: also works with Pi0 (64% avg); SmolVLA performs better thanks to its lerobot-arm pretraining.
