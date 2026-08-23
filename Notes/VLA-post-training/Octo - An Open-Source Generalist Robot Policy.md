# Octo: An Open-Source Generalist Robot Policy

- **Title:** Octo: An Open-Source Generalist Robot Policy
- **Authors:** Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al.
- **Venue:** arXiv preprint (arXiv:2405.12213)
- **Year:** 2024
- **Affiliations:** UC Berkeley, Stanford University, Carnegie Mellon University, Google DeepMind


## 主题 - Open-Source Generalist Robot Policy

## 背景
大规模预训练策略在多样化机器人数据集上的训练，有望从根本上改变机器人学习范式：无需从零训练新策略，通用机器人策略（Generalist Robot Policy, GRP）只需少量领域内数据即可微调适配新任务。然而，构建真正通用的"general-purpose robot model"面临独特挑战，需要处理不同的robot embodiment、sensor配置、action space、任务规范和计算资源。现有模型如RT-1-X、RT-2-X和RoboCat虽取得进展，但在输入灵活性、微调适配性和开源可及性方面仍存在显著不足。

## 现有局限与研究问题
- **Limitation:** 现有generalist robot policy（如RT-1-X、RT-2-X）将用户限制在预定义且受限的输入observation集合中（如单一camera stream），无法灵活适配新的sensor配置。
- **Limitation:** 现有模型缺乏对新observation space和action space的有效finetuning支持，切换任务规范或observation类型需要重新初始化模型的大部分参数。
- **Limitation:** 最大规模、性能最优的generalist robot model（如RT-2-X, 55B参数）未向公众开放，阻碍了社区的研究与复现。
- **Limitation:** 现有模型多采用ResNet-style大型visual encoder配合较小transformer的架构，在大规模多样化数据集上的scalability受限。
- **Problem:** 如何设计一个开源、灵活且可扩展的generalist robot policy，使其能够支持多样化的sensor输入与action space，并可高效微调适配新的robot setup？

## 贡献
- 提出Octo，一个基于transformer的开源generalist robot policy，在Open X-Embodiment数据集的800k robot trajectory上预训练，是迄今最大规模的robot manipulation数据集。
- 设计了模块化的transformer架构，通过block-wise attention masking和readout token机制，支持灵活添加或移除observation输入和action输出，无需修改预训练参数即可适配新的sensor和action space。
- 支持language instruction和goal image两种任务条件方式，且可在finetuning阶段灵活切换。
- 采用diffusion-based action head预测连续、多模态的action distribution，以"action chunking"方式预测未来多步动作序列，显著优于MSE和离散化action prediction方法。
- 在4个机构的9种robot setup上进行了广泛实验，验证了Octo在zero-shot multi-robot控制和data-efficient finetuning方面的有效性，平均finetuning性能超出次优基线52%。
- 完全开源模型checkpoint（Octo-Small 27M, Octo-Base 93M）、训练pipeline、finetuning脚本和数据加载器，为社区提供可复现的研究基础设施。
- 系统性地进行了model architecture、training data、training objective和model scale的ablation study，为未来generalist robot policy的设计提供指导。

## 方法论
- **架构设计：** 采用"transformer-first"架构，由三部分组成：(1) input tokenizer将language instruction（通过预训练t5-base编码）和image observation（通过浅层CNN编码）转换为token序列；(2) transformer backbone处理task token和observation token序列，通过block-wise causal attention mask实现模块化；(3) readout token被插入序列中被动聚合信息，其embedding经由lightweight diffusion action head解码为action。
- **模块化适配机制：** Transformer的block-wise attention结构允许在finetuning时添加新的observation token（如force-torque输入）或新的action head（如joint position控制），仅需新增positional embedding、轻量级encoder或新head参数，完全保留预训练权重。
- **训练数据：** 从Open X-Embodiment数据集中筛选25个子数据集，包含多种robot embodiment和scene，通过加权采样平衡数据多样性与规模，对多样化数据集加倍权重，并对重复性过高的数据降权。
- **训练目标：** 使用conditional diffusion decoding head（基于DDPM目标），通过learned denoising network对Gaussian noise向量进行K步去噪生成action，采用cosine noise schedule，仅需transformer backbone单次前向传播，多步去噪在轻量级diffusion head内完成。
- **训练细节：** 提供Octo-Small（ViT-S规模，27M）和Octo-Base（ViT-B规模，93M）两种变体；使用AdamW optimizer、inverse square root decay学习率调度、batch size 2048，在TPU v4-128 pod上训练300k步（约14小时）；使用2帧observation history和hindsight goal relabeling进行数据增强。
- **Finetuning策略：** 统一采用约100条target domain demonstration、50k步cosine decay学习率训练，可在单张NVIDIA A5000 GPU上5小时内完成，适配新observation（force-torque）、新action space（joint position）和新robot embodiment（双臂操作）。
