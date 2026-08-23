# StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing

> arXiv: 2604.05014 | 年份: 2026

## 主题
Modular unified VLA codebase

## 背景
构建通用具身智能体需要同时整合感知、语言理解与动作生成，这正是 Vision-Language-Action (VLA) 模型试图解决的核心问题。当前 VLA 研究已形成两大家族：VLM-based methods（复用语言模型的表征能力做 action decoding）与 world-model-based methods（用生成式架构联合建模动作分布与未来观测）。然而两条路线基本各自独立发展，代码库、接口假设与评测协议互不兼容，形成作者所称的 VLA 研究 "Tower of Babel"，使得系统性比较、复现与设计选择的权衡分析都难以进行。

## 现有局限与研究问题
- **Limitation:** 碎片化体现在三个层面——architecture 层面动作解码设计各异（autoregressive tokenization、parallel regression、diffusion、flow matching），难以横向比较；system 层面各方法发布时与模型架构、数据处理、训练流水线紧耦合，组件无法跨项目复用；evaluation 层面结果报告在互不重叠的 benchmark 子集上、协议不一致，公平比较不可行。作者将根因归结为 "缺乏统一的 VLA 系统抽象"。
- **Limitation:** 已有开源代码库（如 GR00T N1、π0 的发布代码）大多是 method-specific 的，不支持 (i) 跨不同 action-decoding paradigm 的模块化组合、(ii) 跨异构数据源的可复用训练、(iii) 跨 benchmark 与 embodiment 的标准化评测与部署。
- **Problem:** 是否存在一个统一抽象，能让 VLM-based 与 world-model-based 两类 VLA 同时落在同一套数据管线、训练循环与评测协议之下，从而实现 backbone 与 action head 各自独立替换的受控比较？

## 贡献
- 提出 **StarVLA**，一个开源 VLA 研究平台，核心设计为 **backbone–action head decomposition**：共享的 vision-language backbone 编码场景与指令，可插拔的 action head 将表征映射为电机指令，两者通过标准化契约实现 **bidirectional modularity**（任一侧可独立替换而不影响另一侧及周边基础设施）。
- 在该抽象下实现四种代表性范式：**StarVLA-FAST**（FAST tokenizer + autoregressive 离散动作 token）、**StarVLA-OFT**（轻量 MLP 并行回归连续动作，L1 loss）、**StarVLA-π**（layer-wise cross-DiT flow-matching action expert，迭代去噪）、**StarVLA-GR00T**（dual-system：VL backbone 为 System 2 慢推理，DiT flow-matching 模块为 System 1 快动作生成）。VLM backbone（Qwen3-VL）与 world-model backbone（Cosmos-Predict2）均作为 drop-in 替代支持。
- 将 cross-embodiment learning 与 multimodal co-training 抽象为 **paradigm-agnostic 的可复用训练配置**，而非方法专属的附加模块；所有 recipe 对全部范式一致生效。
- 通过统一的 server–client 测试接口集成多个主流 benchmark（LIBERO、SimplerEnv、RoboTwin 2.0、RoboCasa-GR1、BEHAVIOR-1K 等，Table 1 记为 7 个），同一接口同时支持仿真评测与真机部署，无需改动代码。
- 提出 **generalized VLA perspective**：实证表明 VLM-based 与 world-model-based 方法并非本质不同的范式，而是共享结构框架下 auxiliary signal 形式（language-aligned reasoning vs. future observation prediction）的变体。

## 方法论
- **统一 policy 形式化**：将 VLA 建模为 π(a_{t:t+k}, y_aux | x_≤t, ℓ)，其中 x_≤t 为多模态观测历史（视觉/深度/触觉/本体感觉），ℓ 为语言指令，a_{t:t+k} 为 k 步 action chunk，y_aux 为可选辅助输出。训练目标统一为 L = L_action + L_aux。Direct VLA 令 L_aux = 0；VLM-based VLA 的 L_aux 为 language-aligned 目标（子任务规划、空间 grounding、结构化推理）；WM-based VLA 的 L_aux 为未来观测预测。
- **统一 I/O 接口**：所有模块继承同一基类，暴露 `forward({raw images, str, ...}) → loss dict`（训练入口）与 `predict_action({raw images, str, ...}) → {normalized_actions, ...}`（推理入口）。训练输入直接镜像真机部署时的原始观测而非重度预处理的 dataloader 张量，以最小化 train/test distribution mismatch，作者称之为 *deployment-time invariant* 契约。
- **组合式框架**：每个 VLA 方法拆为 VL backbone + pluggable action head 两部分，通过 YAML 声明式配置装配（先加载 backbone，再挂载 action head）。
- **训练范式**：(1) robot-only SFT（`train_starvla.py`，支持全参微调与 `trainer.freeze_modules` 选择性冻结、多参数组不同学习率、bfloat16 autocast、梯度累积/裁剪、cosine schedule）；(2) multi-objective co-training（`train_starvla_cotrain.py`，双 dataloader 每步两次 forward/backward，VLM loss 由 `trainer.loss_scale.vlm` 缩放）；(3) cross-embodiment co-training（`datasets.vla_data.data_mix` 指定 (dataset, weight, robot type) 三元组，运行时物化为 `LeRobotMixtureDataset`）；(4) RL fine-tuning 为规划中项（与 RLinf 项目合作，尚未开放）。分布式基于 PyTorch + Accelerate + DeepSpeed。
- **评测与部署**：checkpoint 由 `baseframework.from_pretrained()` 加载并托管为轻量 WebSocket policy server，benchmark evaluator 可运行在独立 conda 环境中通过 msgpack 客户端交互；benchmark 差异隔离在 `model2libero_interface.py`、`model2simpler_interface.py`、`model2robotwin_interface.py` 等适配文件中（图像 resize、读取 `dataset_statistics.json` 反归一化、action ensembling、sticky gripper 与 delta/absolute 转换）。真机部署时机器人控制器扮演 client 角色，模型服务不变。
- **generalist 训练设置**：在 LIBERO、SimplerEnv、RoboTwin 2.0、RoboCasa-GR1 的合并训练集上联合训练单一模型，learning rate 1×10⁻⁴，total batch size 256，避免任务专属 action head，用统一 padding 将低自由度动作扩展到共享的 32 维动作向量。

## 实验与关键数字
- **LIBERO**（4 个 suite，10 tasks × 50 episodes = 500 trials/suite，8×A100，per-device batch 16）：Qwen3-VL-4B backbone 下仅训 30K 步（9.54 epochs）即达 FAST 95.4 / OFT 96.6 / π 95.7 / GR00T 96.5（平均成功率 %）。对比 OpenVLA-OFT 需 175K 步（223 epochs）达 97.1，StarVLA-OFT 以 **6× 更少步数、23× 更少 epoch** 达到 96.6；π0+FAST 85.5、GR00T-N1.5（20K 步）86.5 均明显更低。换成 Cosmos-Predict2-2B backbone 后表现相当（OFT 95.8 / π 95.5 / GR00T 95.2，全部 ≥95.2），表明抽象对不同 VL backbone 均可泛化。
- **SimplerEnv**（16×A100，每个设置完整重跑官方评测 5 次取均值）：WidowX Visual Matching 上 Qwen3-VL-4B 最高平均 65.3%（StarVLA-GR00T，20K 步），Cosmos-Predict2-2B 最高 61.6%；对比 π0 27.1、π0-FAST 48.3、GR00T-N1.5 61.9、SpatialVLA 42.7、Magma 35.8。Google Robot 上 StarVLA-OFT 达 Visual Matching 平均 76.0（此前最佳 CogACT 74.8）、Variant Aggregation 平均 70.2（SpatialVLA 70.7）。
- **RoboCasa-GR1**（24 tasks，单一模型联合训练，每任务 50 rollouts，共 250 rollouts 报告口径）：StarVLA-OFT 48.8% 最优，StarVLA-GR00T 47.8%，StarVLA-π 43.9%，离散的 StarVLA-FAST 仅 39.0%；对比 π0.5 37.0%、GR00T-N1.6 47.6%。即 OFT 比 π0.5 高 11.8 个百分点，说明该 benchmark 上 action head 选择影响显著（39.0 → 48.8）。
- **RoboTwin 2.0**（50 tasks × 2 setups × 100 episodes = 10,000 trials，48×A100，150K 步）：clean/randomized 成功率 StarVLA-GR00T 88.0/88.5、StarVLA-OFT 88.2/88.3、StarVLA-π 88.1/88.8、StarVLA-FAST 72.5/83.2；对比 π0 65.9/58.4、π0.5 82.7/76.8、X-VLA 72.9/72.8、LingBot-VLA 88.6/86.7。
- **Multimodal co-training**（基于 StarVLA 的 ST4VLA 研究）：vanilla VLA 仅动作微调会在 20K 步内使 RefCOCO-g grounding 掉到接近随机水平。vanilla co-training 相对 vanilla VLA 带来 +4.1% Google Robot VM 与 +6.4% WidowX；spatially pretrained 变体进一步达到 Google Robot VM/VA 84.6/75.9、WidowX 73.2，同时保持 RefCOCO-g IoU@0.5 = 71.2、RoboRefIt Acc@0.5 = 74.3，多模态理解 MME 1411 / MMVet 23.3 / TextVQA 28.6 / POPE 86.2（vanilla VLA 基线为 Google Robot 66.1/63.5、WidowX 54.7）。
- **Generalist（跨 benchmark 联合训练单一模型）**：LIBERO 平均 97.8、WidowX 70.2、Google VA 73.8、Google VM 79.3、RoboTwin clean* 88.7 / random* 87.8、RoboCasa-GR1 57.3。其中 RoboCasa-GR1 从最佳 specialist 的 48.8% 提升到 57.3%，其余 benchmark 与 specialist 基本持平。
- **计算效率**（StarVLA-GR00T + Qwen3-VL-4B，RoboCasa-GR1，A100 80GB，wall-clock per 100K steps）：单节点 8×A100 下 per-GPU batch 从 2 增到 24，step latency 0.703 → 2.404 s/step（3.4×），sample throughput 22.7 → 79.9 samples/s，GPU 利用率 74% → 96%。多节点固定 per-GPU batch = 8：8 GPUs 0.735 s/step、87.0 samples/s；32 GPUs 0.899 s/step、284.7 samples/s（81.9% scaling eff.）；256 GPUs 0.931 s/step、2200.0 samples/s、scaling efficiency 79.1%。即跨节点通信引入一次性延迟开销（0.735 → ~0.93 s/step），但超过 32 GPUs 后并行效率稳定在 79–80%，可放心扩展到数百卡。
- **集成 benchmark 规模参考**：LIBERO 130 tasks / 50 demos per task / ~6.5K 轨迹；LIBERO-Plus 10,030 个 test-only 任务，覆盖 7 类扰动因子与 21 个 low-level 组件；RoboCasa-GR1 24 tasks / ~1,000 demos each / ~24K 轨迹；RoboTwin 2.0 50 tasks / 每任务 50 clean + 500 randomized demos / 27.5K 轨迹；BEHAVIOR-1K 1,000 项日常活动、50 个交互场景、>9,000 个物体，BEHAVIOR Challenge 提供 10,000 条遥操作演示（超过 1,200 小时）；CALVIN 4 个环境、34 个任务、ABC→D 设置下 1,000 条长度为 5 的任务序列。
