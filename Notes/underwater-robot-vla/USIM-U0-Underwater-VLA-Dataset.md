# USIM and U0 - A VLA Dataset and Model for Underwater Robots

## 主题
Underwater VLA dataset and model

## 背景
水下环境对机器人作业提出了独特挑战，包括复杂的 hydrodynamics、有限的能见度和受限的通信。尽管 data-driven 方法已经在地面机器人和特定任务的自主水下机器人上取得进展，但是大规模、高质量的水下数据集仍然稀缺，限制了能够执行多任务的通用 underwater embodied intelligence 的发展。本文基于 Stonefish 仿真器和 BlueROV2 平台，构建了首个面向水下机器人的多任务 Vision-Language-Action 数据集 USIM，并基于该数据集提出通用水下 VLA 模型 U0。

## 现有局限与研究问题
- **Limitation:** 现有水下数据集（如 VAROS、UIEB、AQUALOC、Underwater Caves Sonar Data Set）多为任务特定，主要服务于感知任务，缺乏统一的 VLA 数据；真实海域采集成本高、风险大；现有 underwater simulator（HoloOcean、Dave、FishGym、Stonefish）虽可用，但尚未被用于构建大规模多任务 VLA 数据集；同时，indoor/terrestrial 的 VLA 模型（RT-2、OpenVLA、π0、GR00T N1.5）直接迁移到水下时存在巨大 domain gap，且单目视觉对水下 3D 空间感知能力不足。
- **Problem:** 如何构建可扩展的高质量水下 VLA 数据集，并训练出能够同时处理 visual navigation、obstacle avoidance、inspection、scanning、dynamic tracking 以及 fluid-dynamics-aware mobile manipulation 的通用水下 VLA 模型？

## 贡献
- 构建了 USIM 数据集：基于 Stonefish 仿真器与 BlueROV2 平台，包含 561K frames、1,852 trajectories、约 15.6 小时机器人–环境交互数据，覆盖 9 种场景（seabed、subsea pipeline、industrial pool、solar charging station、lake、open sea surface、underwater factory、modern shipwreck、ancient shipwreck）和 20 个任务（12 个 grasping、2 个 pipeline inspection、2 个 shipwreck scanning、2 个 obstacle-avoidance navigation、1 个 dynamic tracking、1 个 transport），数据按 LeRobot 规范组织。
- 提出 U0 模型：基于 Isaac-GR00T N1.5 backbone（约 3B 参数）的通用水下 VLA 模型，融合 binocular vision、IMU、pressure、DVL、altitude、joint、thruster 等多源传感器，并引入由 VLM 特征引导的 Convolution-Attention-based Perception focus enhancement (CAP) 模块。
- 建立可扩展的 data-to-task 框架：首次系统地联合处理由语言指令引导的多任务水下感知与动作；在 inspection、obstacle avoidance、scanning、dynamic tracking 等任务上达到 80% 平均成功率，在 mobile manipulation 任务中将机器人到目标的距离相比 baseline 减小 21.2%。
- 模型大小适合部署在 NVIDIA Jetson 等 embedded AI 平台，推动水下具身智能的实际落地。

## 方法论
- **仿真环境构建：** 使用 Stonefish simulator 搭建 9 种水下场景，配置带有 manipulator 与 parallel gripper 的 BlueROV2，支持 hydrodynamics、collision、grasping 仿真；通过 Stonefish ROS package 与 ROS 集成，进行 map randomization、sunlight 与 Jerlov water clarity 随机化以增强 visual diversity。
- **数据采集流水线：** 自动化并行采集，PID 控制器负责 ROV 位姿跟踪，MoveIt 负责 grasping 任务的 manipulator 规划与控制，数据以 10 Hz 记录；其中 526K frames / 1,752 trajectories 用于训练，35K frames / 100 trajectories 用于测试。
- **U0 模型架构：** 双系统 dual-system 架构。Vision encoder + projector 处理双目图像，text tokenizer 处理语言指令，两者送入 VLM；ROV state（IMU、pressure、DVL、altitude、joint、thruster）通过 encoder 编码后与 VLM 输出的 action tokens 共同输入 Diffusion Transformer，通过 cross-attention 生成动作；同时 VLM 特征送入 CAP 模块预测 target，作为辅助任务分支，推理时可关闭以避免增加部署延迟。
- **多源传感器融合与动作空间：** 状态空间包含 binocular images、IMU、pressure、DVL；动作空间将 thruster PWM 信号与 manipulator joint angles 归一化拼接；目标位姿采用 robot-centric 表示 p_{t2r} = (R_r^T R_t, R_r^T (t_t - t_r))，缓解对世界坐标系的依赖，符合 egocentric reasoning。
- **CAP 模块：** 输入为来自 binocular VLM 的 token，依次经过 1-D Conv、BatchNorm、ReLU、与 MASK 卷积、channel-wise attention（1-D Conv + BatchNorm + sigmoid）、pooling 与 MLP 输出预测目标，训练时使用 MSE loss L_CAP 与动作损失加权 L = L_action + α L_CAP。
- **训练设置：** Total batch size 1024，训练 5000 步；分别在单目和双目变体上 fine-tune GR00T N1.5 与 U0。
- **评估方案：** 包括 open-loop offline evaluation（35K frames 测试集，对比 GR00T N1.5、GR00T FT、U0 的 e_action 与 e_target，单目/双目两种输入）和 closed-loop online testing（在仿真器中执行 5 个 grasping 任务和 7 个非 grasping 任务，记录成功率与机器人到目标的平均距离）。
