# USIM and U0: A Vision-Language-Action Dataset and Model for General Underwater Robots

## Topic
Large-scale underwater VLA dataset (USIM) and model (U0) for general-purpose underwater robot manipulation and navigation, built on the Stonefish simulator with BlueROV2.

## Background
Vision-Language-Action models have demonstrated remarkable capabilities in terrestrial robotics, but their application to underwater domains has been severely limited by the lack of large-scale training datasets and the unique challenges of underwater perception (visual degradation, turbidity, limited lighting). Existing underwater robotics datasets are small-scale and task-specific, while pre-trained VLA models trained on land-based data fail completely when deployed underwater (0% success rate), revealing a significant domain gap that necessitates dedicated underwater datasets and model adaptations.

## Limitations & Research Problem
- **Limitation:** No large-scale VLA dataset exists for underwater robotics, preventing effective training and benchmarking of underwater VLA models
- **Limitation:** Pre-trained terrestrial VLA models (e.g., GR00T N1.5) exhibit catastrophic failure in underwater domains due to fundamental differences in physics, perception, and control
- **Limitation:** Standard visual encoders are insufficient for underwater environments where severe visual degradation (turbidity, lighting) compromises perception accuracy
- **Problem:** How to build a comprehensive underwater VLA dataset and model that can handle diverse underwater tasks with multimodal sensor fusion and robust perception under degraded visual conditions

## Contributions
- USIM: first large-scale underwater VLA dataset with 561K+ frames from 1,852 trajectories across 9 scenarios and 20 tasks, totaling 15.6 hours of BlueROV2 interactions at 10Hz
- U0: a VLA model built on GR00T N1.5 (3B parameters) with binocular vision and multimodal sensor fusion (pressure, IMU, DVL, thruster PWM, manipulator joint angles)
- Convolution-Attention Perception Enhancement (CAP) module that improves target localization under degraded visual conditions as an auxiliary training task with zero inference overhead
- Robot-centric target pose representation that better captures dynamic underwater motion characteristics
- Demonstrated 80% success rate across diverse underwater tasks and 21.2% improvement in mobile grasping distance over baselines

## Methodology
- **USIM Dataset Construction**: Built on the Stonefish physics simulator with BlueROV2 platform. 9 underwater environments (seabed, subsea pipeline, industrial pool, solar charging station, lake, open sea surface, underwater factory, modern shipwreck, ancient shipwreck). 20 tasks including 12 grasping tasks, 2 pipeline inspections, 2 shipwreck scanning, 2 obstacle-avoidance navigation, 1 dynamic tracking, 1 transport. Data collected at 10Hz via ROS integration with parallel automated collection pipeline. Split: 526K frames (1,752 trajectories) training, 35K frames (100 trajectories) testing. Modalities: binocular camera images, pressure, IMU, DVL, thruster PWM, manipulator joint angles, language instructions.
- **U0 Model Architecture**: Foundation is pre-trained GR00T N1.5 (3B parameters). Visual images and language instructions processed through respective encoders into a VLM. Additional sensor modalities (pressure, IMU, DVL) and robot action data fed into a diffusion transformer for action generation. Binocular imagery provides enhanced 3D perception. Robot-centric coordinate system for target representation: p_t2r = (R_r^T R_t, R_r^T(t_t - t_r)).
- **CAP Module**: Addresses underwater visual degradation. Pipeline: VLM extracts stereo image features, convolutional layers process with masking (avoiding padding artifacts), channel-wise attention generates weights, weighted features pooled through MLP for target location prediction. Trained with MSE loss as auxiliary task (L = L_action + alpha * L_CAP). Disabled at inference time -- zero computational overhead. Greater benefit in monocular settings where it compensates for lack of depth information.
- **Training Configuration**: Batch size 1024, 5000 training steps. Data formatted per LeRobot specification. Thruster PWM signals normalized, combined with manipulator joint angles for action representation. Separate training runs for monocular and binocular configurations.
- **Experimental Setup**: Offline evaluation on held-out test set measuring action error (e_action). Online closed-loop testing: 7 non-grasping tasks (10 trials each) and 5 mobile grasping tasks (5 trials each). Baselines: GR00T N1.5 pre-trained (0% success -- total failure), GR00T fine-tuned on USIM, U0 in both monocular and binocular configurations. Results: U0 binocular achieves 80% average success rate on non-grasping tasks, 0.0593 action error (best overall), 21.2% distance reduction in mobile grasping (0.2752m vs 0.3492m baseline).
