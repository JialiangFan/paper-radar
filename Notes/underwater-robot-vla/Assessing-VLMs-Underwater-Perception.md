# Assessing VLMs for Underwater Perception

> 作者: Muhammad Yousaf, Aitor Arrieta, Shaukat Ali, Paolo Arcaini, Shuai Wang
> 单位: Simula Research Laboratory / Oslo Metropolitan University / Mondragon University / NII Tokyo / DNV
> 年份: 2026 (arXiv:2602.10655 v3)
> 项目背景: EU InnoGuard 项目，工业伙伴 DNV AS

## 主题
VLM perception evaluation for AUR

## 背景
自主水下机器人 (AUR) 在低能见度、噪声严重的水下环境中执行垃圾收集等任务，传统深度学习感知模块严重依赖稀缺且嘈杂的标注数据，限制了 AUR 软件的可信度。视觉-语言模型 (VLM) 凭借强泛化与上下文推理能力，被视为有潜力的水下感知替代方案，但其性能、不确定性及校准在水下场景下从软件工程视角尚未被系统研究。本工作受工业伙伴 (DNV) 在海事系统保障与风险管理需求驱动，对 VLM 作为 AUR 软件感知模块的可用性进行实证评估。

## 现有局限与研究问题
- **Limitation:** 水下深度学习感知模型依赖稀缺、噪声大的标注数据；同时 VLM 在水下条件下的性能、不确定性、置信度校准缺乏从软件工程角度的系统证据，工业界无法判断其能否安全集成进 ACPS / AUR 软件。
- **Problem:**
  - RQ1 (Performance): VLM 在水下图像分类任务中的表现如何?
  - RQ2 (Uncertainty Quantification): VLM 在水下分类时的不确定性如何度量?
  - RQ3 (Performance-Uncertainty Relationship): 性能与不确定性 / 置信度 / 校准之间的关系如何，怎样指导工程师为 AUR 软件选择 VLM?

## 贡献
- 在 AUR 软件感知模块语境下，对 4 个开源 VLM (InstructBLIP, LLaVA-1.6, DeepSeek-VL2, QWen2.5-VL，均约 7B 参数) 在两个水下数据集 (TrashCan1.0, SeaClear) 上进行系统的零样本经验评估。
- 同时考察性能、置信度、不确定性、校准四个维度的关系，揭示「高置信 / 低不确定 ≠ 高性能」，强调校准比单纯置信度更关键。
- 给出工业可参考的结论: BLIP 与 DeepSeek 综合最佳，BLIP 校准最好；LLaVA 过度自信、校准差，不适合 AUR 关键感知；为 ACPS / 海事工业方提供选型证据。
- 提出面向 AUR 软件工程的 VLM 评估方法学与可复现 replication package。

## 方法论
- **整体架构:** AUR 软件由感知 (VLM) → 规划 → 控制构成，VLM 接收图像 + 文本指令 (识别水下垃圾等四类物体)，输出多标签分类与 token 级 logits 用于不确定性量化 (图 1)。
- **数据集:** TrashCan1.0 (7,212 张) 与 SeaClear (8,610 张)，将原始细标签合并为 Animal / Vegetation / Object / Trash 四类多标签分类任务，强调对未见水下物体的泛化能力。
- **被测模型:** InstructBLIP (ViT)、LLaVA-1.6 (CLIP ViT-L/14)、DeepSeek-VL2 (SigLIP+SAMB)、QWen2.5-VL (重设计 ViT)，统一约 7B 参数；零样本推理、温度=0、单 NVIDIA RTX-5090。
- **Prompt:** 单一 domain-dependent zero-shot 模板，要求 VLM 按 Animals / Vegetation / Objects / Trash 四类输出列表与计数，保证跨模型语义一致与公平比较。
- **评估指标:**
  - 性能 (RQ1): F1 (Macro / Micro)、Jaccard (Macro / Micro)、Precision、Recall，并按 Trash 等关键类逐类评估。
  - 不确定性 (RQ2): 基于 token 级概率的概率型不确定性度量 (置信度分数、熵等) 与校准度量。
  - 性能-不确定性关系 (RQ3): 复用 RQ1/RQ2 指标，分析高性能模型是否同时具备良好校准。
- **核心发现:** BLIP 与 DeepSeek 性能领先，尤其在 Trash 与 Object 类；LLaVA 高置信但校准差 (overconfident)；BLIP 在性能与校准的折中上最适合工业 AUR 部署，说明应将「校准」纳入 VLM 选型核心准则。
