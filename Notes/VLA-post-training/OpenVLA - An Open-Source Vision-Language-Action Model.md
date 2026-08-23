# OpenVLA: An Open-Source Vision-Language-Action Model

- **Title:** OpenVLA: An Open-Source Vision-Language-Action Model
- **Authors:** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, et al.
- **Venue:** arXiv preprint (arXiv:2406.09246)
- **Year:** 2024
- **Affiliations:** Stanford University, UC Berkeley, Toyota Research Institute, Google DeepMind, Physical Intelligence, MIT


## 主题 - 开源视觉-语言-动作模型

## 背景
大规模预训练的vision-language model (VLM)已展现出强大的泛化能力，而将其微调为vision-language-action model (VLA)可直接生成机器人控制动作，为通用型机器人操作策略提供了新范式。然而，现有VLA（如RT-2-X）均为闭源模型，且缺乏针对新任务高效微调VLA的系统性研究。OpenVLA在此背景下提出，旨在构建首个完全开源的通用型VLA，并探索参数高效微调策略。

## 现有局限与研究问题
- **Limitation:** 现有VLA模型（RT-2、RT-2-X、RFM-1等）均为闭源，模型架构、训练流程和数据配比缺乏透明度，阻碍了学术研究与社区复现。
- **Limitation:** 先前工作未系统探索将VLA高效微调至新机器人、新环境和新任务的方法，尤其缺乏在消费级GPU上部署VLA的实践指南。
- **Limitation:** 通用型机器人策略（如RT-1-X、Octo）参数量较小且未利用Internet-scale预训练，在面对干扰物和语义泛化任务时表现不佳。
- **Problem:** 如何构建一个开源、可微调、且性能优于闭源模型的通用型VLA？
- **Problem:** 如何利用LoRA和量化等技术使VLA的训练和推理在消费级硬件上可行？

## 贡献
- 提出OpenVLA，一个7B参数的开源VLA，基于Prismatic VLM（融合DINOv2与SigLIP的双视觉编码器 + Llama 2 7B backbone），在970k真实机器人演示数据（Open X-Embodiment）上微调。
- 在29个任务、多种机器人平台（WidowX、Google Robot）上，OpenVLA以7B参数超越55B参数的闭源RT-2-X，绝对成功率提高16.5%。
- 首次系统研究VLA的高效微调策略，包括full fine-tuning、frozen vision、sandwich fine-tuning和LoRA，发现LoRA（rank=32）以仅1.4%的可训练参数即可匹配full fine-tuning性能，且可在单张A100 GPU上10-15小时完成。
- 验证4-bit量化推理可在不损失性能的前提下将GPU显存需求从16.8GB降至7.0GB，使消费级GPU部署成为可能。
- 完全开源模型权重、训练代码、微调notebook及PyTorch训练流水线。

## 方法论
- **模型架构：** 采用Prismatic-7B VLM作为backbone，包含(1)双视觉编码器（DINOv2提供空间特征 + SigLIP提供语义特征，channel-wise拼接），(2) 2层MLP projector将视觉特征映射至语言嵌入空间，(3) Llama 2 7B作为LLM backbone生成动作token。
- **动作离散化：** 将连续动作空间的每个维度均匀离散化为256个bin（基于训练数据第1至第99百分位数），动作token覆写Llama tokenizer中最不常用的256个token，以next-token prediction目标训练，仅对动作token计算cross-entropy loss。
- **训练数据：** 从Open X-Embodiment数据集中筛选含第三人称视角的单臂末端执行器操作数据集，采用Octo的数据混合权重平衡embodiment、任务和场景多样性，最终覆盖970k轨迹。
- **关键设计决策：** (1)选择Prismatic VLM而非LLaVA或IDEFICS-1，因其融合视觉编码器在语言grounding任务上提升35%；(2)采用224x224分辨率（384x384无性能增益但训练时间增3倍）；(3)微调视觉编码器（与VLM训练中冻结编码器的惯例相反）；(4)训练27个epoch直至action token accuracy超过95%；(5)学习率2e-5。
- **训练基础设施：** 64张A100 GPU，batch size 2048，训练14天（21,500 A100-hours）。推理时以bfloat16精度需15GB显存，在RTX 4090上约6Hz。
- **微调评估：** 在Franka Emika Panda平台上以10-150条演示微调，对比Diffusion Policy、Octo等方法，OpenVLA在7类任务上取得最高平均成功率，尤其在需要语言grounding的多指令任务上优势显著。
