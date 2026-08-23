# Avi: A 3D Vision-Language Action Model Architecture generating Action from Volumetric Inference

## 主题
3D point cloud VLA model

## 背景
Vision-Language-Action (VLA) 模型近年备受关注，但绝大多数 VLA 仅在 2D image 输入上端到端训练，并把机器人决策当作直接预测 robot-specific 的 action tokens。Avi 主张换一条路：在 3D point cloud 上原生操作，基于已有的 3D Multi-modal LLM（ShapeLLM-Omni，Qwen-2.5 VL backbone + 3D VQ-VAE）做 volumetric inference，把决策重述为「语言条件下的 3D 几何推理」，再用经典几何变换（ICP + inverse kinematics）导出动作。

## 现有局限与研究问题
- **Limitation:** 现有 VLA 主要基于 2D 视觉，对 depth、物体几何、细粒度空间关系的推理是间接且易出错的；同时它们直接生成 robot-specific action tokens，绑定到特定 morphology 与 scene 设置，泛化性与可复现性差。
- **Problem:** 能否构建一个原生在 3D 表征（point cloud）上操作的 VLA，把动作生成从「language-to-action」改成「language-to-geometry」——预测被操纵物体的目标后置状态（点云），从而获得对 occlusion、相机位姿变化、视角变化更鲁棒且与机器人形态无关的行为？

## 贡献
- 提出 **AVI（Action from Volumetric Inference）** 架构：用 3D MLLM 通过 volumetric reasoning 预测目标点云（delta point cloud），再经几何变换求动作，而非直接生成 action tokens。关键转变是「不在历史 action tokens 上训练，只用历史 depth/point cloud」，把焦点从 language-to-action 移到 language-to-geometry，提供更强的空间 grounding。
- 提出 **Location Quantization for 3D MLLMs**：一种把空间信息离散化的通用技术，让预训练 3D MLLM 能在 object level（而非仅 scene level）泛化。具体把每个分割物体的质心位置（X/Y/Z 各 256 bins → 768 个 position tokens）与 scale（128 bins → 128 个 scale tokens）量化为新词表 token（共扩展 896 个 token），克服 ShapeLLM-Omni 原本只在单物体在线 3D 资产上训练、难以处理多物体机器人场景的瓶颈。
- 在 LIBERO 抽屉关闭任务上给出初步结果：Avi 在场景间（Scene 5 → Scene 10，物体数变化）保持鲁棒，成功率优于 ResNet-RNN/ResNet-T/ViT-T/Diffusion Policy 等基线（Scene 10 上 0.90，基线最高 0.70），展示对 domain shift 的鲁棒性。

## 方法论
- **整体流水线（language-to-geometry）**：输入是场景的 3D point cloud（由 stereo reconstruction 得到，不用 2D 图像）。① 用 Segment Anything (SAM) 做 2D 分割并几何提升到 3D，把场景点云 P 切成各物体的不相交子集 P_k；② 对每个物体做 location quantization，得到离散描述子 ℓ_k=(x_k,y_k,z_k,s_k)（量化质心 + 量化尺度），转成 location tokens 附加到物体表征；③ 文本指令 T 与几何模态被各自的 encoder（f_text, f_3D）映射进共享 latent space Z；④ 3D MLLM 自回归地预测下一/目标 3D 体素状态，经 VQ-VAE decoder 还原为体素网格再转回点云。
- **3D 表征如何进入模型**：核心是冻结的 3D VQ-VAE encoder，把 64×64×64 的体素形状映射成 8192 个离散 latent token（来自学习到的 codebook C）。MLLM（基于 Qwen-2.5 7B VL）的 token 可来自三类词表：文本词表 V_text（Qwen-2.5）、ShapeLLM-Omni 预训练的 3D codebook V_3D、以及新增的 position/scale 位置词表 V_loc。联合分布按自回归 p(z)=∏ p(z_i | z_<i) 分解，使模型既条件于过去几何 token，也条件于语言指令与量化空间上下文——即在统一离散 token 空间里做 language-to-geometry generation。
- **从 volumetric inference 到 action**：给定指令 T 与当前点云 P_t，模型预测目标点云 P̂_{t+1} ≈ P_t + ΔP（ΔP 是学到的、受 prompt 条件的空间变化，即图 1 中绿色 voxel 表示的「下一时刻」预测）。随后用 **Iterative Closest Point (ICP)** 在源点云与目标点云间求最小化对齐误差 min_{R,t} Σ‖R x_i + t − y_i‖² 的刚体变换 (R∈SO(3), t∈ℝ³)，把该变换施加到末端执行器位姿 (X,Y,Z)，再经 inverse kinematics 解出并执行机器人关节动作。动作完全由几何变换导出，因而 morphology-agnostic。
- **训练数据与阶段**：在 LIBERO 数据集（Robosuite 环境，Franka Panda，含同步 RGB-D 观测与本体感受状态）上微调，实验选取 drawer-closing 任务的 50 个示范。硬件为单张 NVIDIA A6000 (48GB)。微调用 **LoRA**：仅在注意力层最后 K 层的 Q/K/V 投影插入低秩适配矩阵，扫描 rank r∈{4,8,16,32,64}、LoRA_α=2r；SAM encoder 与 VQ-VAE 全程冻结，dropout p=0.05 以在小数据下正则化。新增 896 个 token 的 embedding 随机初始化，原词表 embedding 保留以维持预训练知识。每个样本训练约 100 epoch。
- **局限与未来**：当前显式生成下一帧点云、无法做长时域高层规划；自回归 transformer 与 VQ-VAE tokenization 对精度要求高（cross-entropy loss 偶尔生成错位点云导致 ICP 求出错误变换）。未来方向包括 unfreeze VQ-VAE 提供更丰富监督、引入 3D diffusion-policy / diffusion-style loss 替代 cross-entropy、以及整合更强的 3D MLLM（如 SpatialVerse）。
