# USIM and U0: A Vision-Language-Action Dataset and Model for General Underwater Robots

**arXiv:** [2510.07869](http://arxiv.org/abs/2510.07869)
**Date:** 2025-10-09
**Authors:** Junwen Gu, Zhiheng Wu, Pengxuan Si, Shuang Qiu, Yukai Feng, Luoyang Sun, Laien Luo, Lianyi Yu, Jian Wang, Zhengxing Wu
**Keywords:** underwater VLA, simulation dataset, binocular vision, multimodal sensor fusion, BlueROV2, diffusion transformer

---

## 相关主题
- [[literature_review]] — 水下机器人 VLA 模型
- 与 [[UnderwaterVLA - Dual-brain Vision-Language-Action Architecture for Autonomous Underwater Navigation]] 的关系：同为水下 VLA 开创性工作，但本文侧重大规模仿真数据集构建与端到端模型训练，UnderwaterVLA 侧重零样本实机部署与分层架构

## 核心创新点
构建首个大规模水下 VLA 数据集 USIM（561K+ 帧，1852 条轨迹，覆盖 9 种场景 20 种任务），并提出 U0 模型——基于 GR00T N1.5 骨干网络，融合双目视觉与多模态传感器（压力、IMU、DVL），引入卷积-注意力感知增强模块（CAP）解决水下视觉退化问题，在 20 种任务上实现 80% 平均成功率。

## 主要方法
- **USIM 数据集**：基于 Stonefish 仿真器构建，使用 BlueROV2 平台在 9 种水下场景（海底、水下管道、工业水池、太阳能充电站、湖泊、开放海面、水下工厂、现代沉船、古代沉船）中采集 20 种任务的示范数据。包含 12 种抓取任务、2 种管道巡检、2 种沉船扫描、2 种避障导航、1 种动态跟踪、1 种运输任务。训练集 526K 帧 / 1752 轨迹，测试集 35K 帧 / 100 轨迹，采样频率 10Hz，总时长约 15.6 小时。
- **数据模态**：双目相机图像、压力传感器、IMU、多普勒速度计（DVL）、推进器 PWM 信号、机械臂关节角度、自然语言指令。
- **U0 模型架构**：基于 GR00T N1.5（3B 参数）预训练骨干。视觉图像和语言指令通过各自编码器处理后送入 VLM，传感器数据和机器人动作数据送入扩散 Transformer（Diffusion Transformer）进行动作生成。
- **卷积-注意力感知增强模块（CAP）**：针对水下视觉严重退化问题设计的辅助训练模块。处理流程：VLM 提取双目图像特征 -> 卷积层处理（带掩码避免填充伪影）-> 通道注意力生成权重 -> 加权特征池化 -> MLP 输出目标位置预测。训练时使用 MSE 损失作为辅助任务（L = L_action + alpha * L_CAP），推理时可关闭，零额外计算开销。
- **目标位姿表示**：采用机器人中心坐标系，计算目标与机器人间的相对位姿 p_t2r = (R_r^T R_t, R_r^T(t_t - t_r))，更好地捕获水下动态运动特征。
- **训练细节**：总批大小 1024，训练 5000 步，数据按 LeRobot 规范格式化。

## 关键发现
> 预训练 GR00T N1.5 直接部署到水下场景完全失败（0% 成功率），动作误差约为微调模型的 10 倍，表明陆地人形机器人预训练与水下应用之间存在巨大的领域差距。双目视觉在微调后一致优于单目视觉，而 CAP 模块在单目条件下增益更显著（弥补缺乏深度信息的不足）。

## 实验设置
- **离线评估**：在测试集上计算动作误差（e_action），对比 GR00T N1.5 原始模型、GR00T 微调模型和 U0 模型，分别在单目和双目配置下评估
- **在线闭环测试**：非抓取任务（7 种任务，每种 10 次）和移动抓取任务（5 种任务，每种 5 次）
- **仿真平台**：Stonefish 仿真器，支持流体动力学、碰撞物理、视觉退化效果模拟，通过 ROS 集成实现自动化数据采集

## 结论/性能
- **离线动作误差**：U0 双目 0.0593（最优），相比 GR00T 微调双目 0.0619 降低 4.2%；U0 单目 0.0730，相比 GR00T 微调单目 0.0791 降低 7.7%
- **在线成功率**：U0 双目在非抓取任务上平均 **80% 成功率**
- **移动抓取**：U0 双目平均目标距离 0.2752m，相比 GR00T 微调 0.3492m 降低 **21.2%**
- 管道巡检误差 0.1065，沉船扫描误差 0.1004，红色圆柱抓取误差 0.0448
- **局限性**：仅在仿真中验证，未进行实机测试；数据集仅限单一平台（BlueROV2）；深水场景感知能力有限，未融合声呐等模态；移动抓取仍有提升空间
