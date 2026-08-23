# Underwater Object Detection - From Traditional to LVLM Survey

## 主题
UOD challenges, traditional to LVLMs

## 背景
水下目标检测 (UOD) 对海洋生物多样性监测、生态保护、AUV/ROV 自主作业等海洋应用至关重要，但水下成像存在光衰减、散射、色偏、噪声、低对比度等固有问题，加之标注数据稀缺与小目标/遮挡频发，使得传统及现代检测框架难以达到稳定可靠的性能。近年来 LVLMs (大视觉语言模型) 在 VQA、图像描述、目标定位等任务上的成功，为弥补 UOD 在数据、泛化与多模态推理上的短板提供了新思路。本综述系统梳理了 UOD 从传统图像处理方法到深度学习再到 LVLMs 的演进路径。

## 现有局限与研究问题
- **Limitation:** 现有 UOD 综述多聚焦于传统/深度学习方法，对 LVLMs 在水下场景的潜力探讨不足；现有检测方法难以同时应对图像退化、小目标、类不平衡、域偏移以及 AUV 嵌入式平台的实时性约束；公开数据集 (RUOD, DUO, URPC, UDD, Brackish 等) 普遍存在样本量小、类别失衡、标注噪声、多样性欠缺等问题。
- **Problem:** 如何系统性地刻画 UOD 面临的多维挑战，并探索 LVLMs (含合成数据生成与高效微调) 在数据稀缺、域偏移、定位精度与实时部署等难题上的可行解？

## 贡献
- 将 UOD 挑战系统性归纳为五大类：图像质量退化、目标相关、数据相关、计算与处理、检测方法局限，并对应梳理传统与现代解决方案，给出统一的挑战-方案分类法 (Taxonomy)。
- 首次将 LVLMs (CLIP、Florence-2、BLIP-2、Flamingo、GPT-4V、Qwen2-VL、LLaMA 3.2-vision、DeepSeekVL2、MoE-LLaVA、InternLM-XComposer2-4KHD、CoLLaVO、PIN 等) 引入 UOD 综述视角，分别讨论其在图像质量增强、目标检测、数据合成、实时计算与定位精度五个方向的应用潜力。
- 通过两个案例研究验证 LVLMs 落地路径：(i) 用 DALL-E 3 生成合成水下图像并配合 OpenCV 增强 (色彩迁移、雾化、模糊) 扩充 Roboflow100 数据集，YOLO11 在混合数据集上 mAP@50 由 0.793 提升至 0.796、mAP@50-95 由 0.501 提升至 0.505、Recall 由 0.714 提升至 0.736；(ii) 用 LoRA 高效微调 Florence-2 LVLM 用于 UOD。
- 总结三点核心 insight：现有 UOD 仍无法充分应对图像退化和小目标；LVLM 合成数据有潜力但需进一步提升真实感；LVLMs 的实时部署仍是开放问题。

## 方法论
- **结构化文献综述法**：基于 DUO 公共数据集示意图直观呈现典型水下退化样例，并建立"挑战-方案-案例-未来方向"的层次化分类树 (Fig. 1)。
- **挑战分类**：Image Quality Degradation (环境效应/噪声失真)、Target-Related (小目标/遮挡/动态场景)、Data-Related (数据量不足/类不平衡/标签噪声/域偏移)、Computational & Processing (实时/预处理/迁移学习)、Detection Methodology (Bounding Box / 尺度变化)。
- **解决方案演进梳理**：图像处理 (增强/复原/融合) → 图像合成 (GAN/Diffusion) → 目标检测 (小目标、Bounding Box 优化、尺度处理、实时检测、类不平衡、图像质量、域偏移)。
- **LVLM 路线图**：列举主流 LVLMs 及其能力 (Table 6)，对应五类 UOD 挑战展开机理分析 — 增强图像质量、改进目标检测、合成数据缓解数据稀缺/不平衡、MoE-Tuning / InternLM-XComposer2-4KHD 实现实时与高分辨率推理、PIN (Positional Insert) 实现冻结 VLM 上的零样本定位。
- **案例研究 1 (Synthetic Data Augmentation)**：DALL-E 3 文本生图 + 图生图 (sea urchin / scallop / starfish / sea cucumber 4 类) → OpenCV 增强 (美学/色彩迁移/Gaussian blur/蓝绿雾化) → Roboflow 人工标注 1200 张 → 与 RF100 7600 张组合为 8800 张 → YOLO11 训练并对比；用 PSNR/SSIM 评估增强质量，并从 quality / diversity / complexity 三个维度讨论合成数据的优劣。
- **案例研究 2 (Florence-2 + LoRA fine-tuning)**：以 Florence-2 LVLM 为基线，使用 LoRA 高效微调验证其在 UOD 上的可适配性。
- **未来方向**：自动标注、提示工程提升合成真实感、面向 AUV/ROV 的轻量化 LVLM 部署、跨域泛化与鲁棒性研究。
