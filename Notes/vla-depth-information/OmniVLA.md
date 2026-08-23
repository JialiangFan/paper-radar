# OmniVLA: Physically-Grounded Multimodal VLA with Unified Multi-Sensor Perception for Robotic Manipulation

## 主题
Multi-sensor VLA manipulation

## 背景
Vision-language-action (VLA) 模型靠大规模视觉-语言预训练在机器人操作上有很强的泛化与指令跟随能力，但绝大多数 VLA 只吃 RGB 相机输入，无法完成需要超出可见光感知的任务（如找冷饮、隔箱看物、衣物下找响铃手机）。OmniVLA 把 infrared (thermal)、mmWave radar、acoustic microphone array 等 beyond-RGB 传感器统一接入 VLA，让机器人具备 physically-grounded 的空间智能。

## 现有局限与研究问题
- **Limitation:** 现有 VLA 大多只支持 RGB，缺乏非可见光线索；直接把原始传感器流喂给以 RGB 为主训练的 VLA backbone 会导致性能与数据效率都很差；为每种传感器单独训练 encoder 需要海量数据，且专用融合架构难以泛化到多样传感器；传感器数据相比 web 级图文对极度稀缺。
- **Problem:** 如何用一种数据高效、对硬件无依赖、可复用预训练视觉编码器的统一方式，把异构多传感器信息接入 VLA 并 spatially grounded 到目标物体上以指导操作？

## 贡献
- 提出 OmniVLA，据作者称是首个统一 infrared / mmWave / acoustic 多传感器、实现超出 RGB 感知能力的 VLA 操作模型。
- 提出 **sensor-masked image**：把传感器信息以彩色 mask 形式叠加到 RGB 图像上的统一表示，spatially grounded 且语义对齐，能复用预训练视觉编码器、提供跨传感器/分辨率/硬件的统一接口、提升学习效率。
- 给出轻量 OmniVLA 架构并做大量真实世界实验；开源（github.com/GuoHeyu/OmniVLA）。

## 方法论
**关于 depth/3D 信息（用户关注点）**：本文的核心并非 depth，而是 beyond-RGB 多传感器。depth 仅作为硬件传感套件的一部分（depth camera 与 RGB、IR、mmWave、6-mic 阵列同装），RGB 提供"标准视觉感知"，论文未给 depth 设计专门注入机制；"depth 增强 VLA 空间-时序理解"只在 related work 引用 [16]-[20] 提及。真正注入模型的 3D/物理线索是把 **mmWave / acoustic 经 delay-and-sum beamforming 算成 azimuth–elevation 热力图**（公式 1），从而获得与 RGB 一致的 2D 空间映射（间接编码方位/遮挡后物体位置），thermal 本身已是 raster 图像。

**两部分流水线：**
1. **Sensor-masked image 生成（off-the-shelf，不训练，异步后台运行）**：
   - 预处理：所有原始测量统一转成 camera-like 2D 空间表示——thermal 直接是 (u,v) raster；mmWave/acoustic 用 beamforming 得到 azimuth-elevation 热图。
   - 分割：把 task 文本 + RGB 送 VLM（GPT-4o）生成分割关键词 prompt（如 "red block/drink"、"black phone"），再用 Grounded SAM 2（SAM2 + Grounding DINO）出 0-1 mask（公式 2）。prompt 任务开始时生成、低频后台更新，VLM 延迟不影响实时控制。
   - 叠加融合：各传感器图先与 RGB 做一次性 Calibration（旋转+裁剪）粗对齐，再在 mask 区域做 alpha 混合（公式 3，默认 α=1，即 mask 区域完全用传感器信息上色）。
2. **多传感器 VLA 架构（基于 SmolVLA，默认）**：
   - sensor-masked image 送入**冻结的预训练 vision encoder**（与 RGB 共用）→ 每个传感器接一个独立 MLP projector 投影成对齐 token → 与语言 token（经 tokenizer）拼接 → LLM backbone → 接 diffusion/flow-matching 的 Action Expert 生成 action chunk（公式 4）。架构灵活，可按部署场景只用单个传感器。

**训练阶段：**
- **基础训练（主）**：从预训练 SmolVLA 权重开始；**冻结 vision encoder**；用预训练 RGB projection 层权重**初始化每个传感器的 MLP projector**（把已建立的视觉特征映射当强先验，使模型快速适应 sensor-masked image）；然后用采集的演示数据**co-fine-tune** 传感器 MLP + 解冻的 backbone。8×A100，~14h / 50K 步，batch 32；推理 15 预测/秒（RTX 4090）。
- **多传感器预训练 + 少样本适应（泛化实验）**：先用 800 episode 混合语料（thermal/mmWave/acoustic 各 200 + 通用 pick-and-place 200）预训练，再用 **25 episode** 对 unseen 任务做 few-shot 适应。

**相比纯 RGB / raw-sensor 的量化增益：**
- 平均任务成功率 **84%**，对比 VLA-RGB 25%（**+59%**）、VLA-RAW（原始传感图、无叠加）56%（**+28%**）；任务分 0.90 vs 0.55 / 0.73。
- 数据效率：sensor-masked 仅需约 **50%** 训练 episode 即可达到 raw-sensor 同等成功率（Fig 6）。
- 泛化（Table III / Fig 7）：unseen 任务上比 OmniVLA-Base(+59%) 和 Pretrained VLA-RAW(+28%) 平均更高，单任务最多 +68%；分解为 Stage1（选对目标，受益于空间对齐）+ Stage2（完成操作，受益于多传感器预训练先验）。
- backbone 可换：换 Pi0 也 work（64% 平均），SmolVLA 因预训练于 lerobot 机械臂数据集表现更好。
