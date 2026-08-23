# 3D-VLA: A 3D Vision-Language-Action Generative World Model

## 主题
3D generative world model for embodied action

## 背景
现有 vision-language-action (VLA) 模型大多基于 2D 输入，直接学习从感知到动作的映射，缺乏对 3D physical world 动态与"动作-状态关系"的建模。人类则具备 world model，会先在脑中想象（imagine）未来状态再据此规划动作。本文提出 3D-VLA，把 3D perception、reasoning 和 action 通过一个 generative world model 打通，建立在 3D large language model (3D-LLM) 之上，让具身智能体获得类人的 3D 理解与"先想象目标、再生成动作"的能力。

## 现有局限与研究问题
- **Limitation:** 现有 embodied foundation model（如 RT-2、PALM-E）只学 perception→action 的直接映射，不能 imagine 未来状态、不模拟 world dynamics；现有 embodied 数据集多为 2D 图像/视频，缺少 depth/3D 标注、3D bounding box、goal 状态等用于 3D 推理与规划的信息。
- **Problem:** 如何构建一个建立在 3D 表征上的 human-like world model，使其既能在 3D 场景中 reason/localize，又能 imagine 多模态目标状态（图像/深度/点云），并据此生成机器人动作；以及如何获得带 3D 标注的大规模具身训练数据。

## 贡献
- 提出 **3D-VLA**：一个统一 3D perception、reasoning、action 的 3D vision-language-action 具身基础模型，核心是 generative world model。
- 构建大规模 **3D Embodied Instruction Tuning Dataset**（约 2M 3D-language-action 数据对），从现有机器人/人-物交互数据集中提取并补全 3D 信息，弥补现有具身数据集缺 3D 标注的问题。
- 设计一套 **interaction tokens**（scene / object / location / action 等特殊 token）来增强模型对动态 3D 场景的交互与 grounding 能力。
- 预训练 **embodied diffusion models**（RGBD-to-RGBD、point-to-point）实现 goal image / depth / point cloud 生成，并用一个 **projector** 把这些 diffusion decoder 与 LLM embedding 空间对齐，实现 goal imagination；在多项具身任务（reasoning、多模态目标生成、动作规划）上大幅超过 2D 基线。

## 方法论
- **Backbone（3D 场景表征）：** 建在 3D-LLM 之上，以 BLIP2-FlanT5_XL 为预训练 VLM 起点。不直接用点云网络从头训练，而是沿用 3D-LLM 思路：从 multi-view RGB images 经预训练 VLM 提取 2D 特征，再 lift 成 **3D features**（融合相机内参与位姿，把 RGB-D 投影到 3D point cloud）。3D feature 经 **Q-Former** 编码后送入 LLM。训练时解冻 Q-Former、输入/输出 token embedding 权重。
- **Depth/3D 如何进入模型：** 数据侧——超过 95% 视频数据无 3D 信息，用 **ZoeDepth** 逐帧估计深度，用 **RAFT** 光流保证背景帧间深度一致，从而把 RGB-D lift 成带相机内参/位姿的 3D point cloud；并用 spaCy 解析指令名词 + **Grounded-SAM** 得到 2D mask，lift 到 3D 得到物体 **3D bounding box (AABB)**；动作用数据集提供的 7-DoF。模型侧——3D 信息以"multi-view 提取的 3D feature（经 Q-Former）+ 文本中的 3D token（loc/scene/object）"形式进入 LLM，即 depth 既用于构造 3D 场景表征，也用于生成 3D 标注监督。
- **Interaction tokens：** `<obj></obj>` 标注被操作/指代物体；`<loc0-255>`（6 个 token）表示 3D bounding box 的 AABB；`<scene></scene>` 包裹静态场景 embedding 以表达动态场景；机器人动作用离散 token `<aloc0-255>`、`<arot0-255>`、`<gripper0/1>`（绝对位置/旋转/夹爪开合），动作间以 `<ACT_SEP>` 分隔。
- **Generative world model 与 goal imagination：** 分两步注入生成能力。(1) **预训练 embodied diffusion models**：RGBD→RGBD 用 Stable Diffusion V1.4（把 RGB latent 与 depth latent 拼接作为条件），point→point 用 **Point-E**（加点云条件），以"基于指令编辑初始状态→生成目标状态"的方式训练，得到能 imagine goal image / depth / point cloud 的解码器。(2) **桥接 LLM 与生成（对齐阶段）**：引入 `<image></image>`、`<pcd></pcd>` 等特殊 token，LLM 在这些 token 之间生成给机器人执行的指令与 object/location token；用一个 **transformer-based projector** 把 LLM 的 decoder feature 与 embedding 映射到 diffusion model 空间，从而按指令指定的模态条件生成对应 goal。用 **LoRA** 微调各 diffusion model，只训练新 token embedding、对应输出线性层和整个 projector，同时最小化 LLM loss 与 diffusion denoising loss。
- **与 action 的结合：** goal imagination 产出的 goal state（image/point cloud）可回灌给模型指导 **robot control**——模型先想象目标状态，再结合 3D feature 与定位到的关键物体，输出 7-DoF 动作 token 完成 planning。论文论证：因为利用了 3D 信息能更准确定位关键物体并 imagine 目标状态，reasoning、localization 和 action planning 都优于 2D 基线。
- **训练数据与阶段：** 三阶段——① backbone 训练（在 3D Embodied Instruction Tuning Dataset 上训 3D-VLA base，含 task caption、action prediction、localization、多模态 goal generation 等任务，约 2M 数据对）；② 预训练 embodied diffusion models（RGBD/点云）；③ 对齐阶段（projector + LoRA 把 diffusion 接入 LLM）。数据来源：Open-X Embodiment 中 12 个机器人数据集 + 含深度的 Dobb-E/RH20T + 仿真环境 RLBench/CALVIN + 人-物交互数据（Epic-Kitchens、HOI4D）；语言标注用模板 + ChatGPT 扩写。评测覆盖 Embodied/Task/What-if/Dense QA、localization、RGB/点云 goal 生成、以及 RLBench/CALVIN 上的动作规划。
