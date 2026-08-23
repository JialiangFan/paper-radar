# AquaticCLIP: A Vision-Language Foundation Model for Underwater Scene Analysis

**arXiv:** [2502.01785](http://arxiv.org/abs/2502.01785)
**Date:** 2025-02-03
**Authors:** Basit Alawode, Iyyakutti Iyappan Ganapathi, Sajid Javed, Naoufel Werghi, Mohammed Bennamoun, Arif Mahmood
**Keywords:** vision-language model, underwater scene analysis, contrastive learning, zero-shot classification, aquatic foundation model

---

## 相关主题
- [[literature_review]] — 水下感知与基准测试

## 核心创新点
AquaticCLIP 是首个专门面向水下场景分析的视觉-语言基础模型，通过构建 200 万水生图像-文本对数据集，结合提示引导视觉编码器（PGVE）和视觉引导文本编码器（VGTE）的双编码器架构，在零样本水下物种分类、目标检测、语义分割和物体计数等多项任务上大幅超越现有方法（包括 GPT-4V），发表于 IEEE TNNLS。

## 主要方法
- **大规模水生数据集 (200万对)**: 从 YouTube 纪录片（每 50 秒提取唯一帧）、Netflix（《我的章鱼老师》等）、National Geographic、1200 本海洋生物学教科书（PDF-Figures 2.0 提取图表）、Corals of the World、Fishes of Australia、Marine Twitter 等多源异构数据中构建，经人工筛选保留 200 万高质量图像-文本对
- **提示引导视觉编码器 (PGVE)**: 基于冻结的 ViT-B/16-224，利用可学习提示特征通过交叉注意力机制逐步聚合图像块特征，提示作为 Query、图像块特征作为 Key/Value，通过可学习权重矩阵 (W1-W4) 进行注意力融合，优先关注高语义相似度的区域，抑制无关区域
- **视觉引导文本编码器 (VGTE)**: 将图像块特征与学习到的提示拼接作为 Key/Value，文本表征作为 Query，通过视觉引导注意力机制将视觉上下文注入文本表征，增强跨模态对齐
- **无监督描述生成与语义过滤**: 使用 MarineGPT 零样本生成图像级和实例级（MRegionCLIP 检测器辅助）文本描述，通过关键词与图像嵌入的余弦相似度进行语义清洗，保留 top-p% 关键词
- **对称对比学习**: 图像到文本损失 + 文本到图像损失的组合对比学习目标

## 关键发现
> AquaticCLIP 在零样本珊瑚分类 (CC) 数据集上达到 95.3% F1，大幅超越 GPT-4V (87.6%)、BLIP-2 (85.3%)、Fine-tuned CLIP (83.1%) 和 Frozen CLIP (75.2%)；在大规模鱼类数据集 (LSF) 上零样本 F1 达 93.4%；目标检测 (FishNet) mAP50 达 90.3%，超越 MarineInst (85.4%) 和 MRegionCLIP (86.7%)。该模型展示了领域特定预训练在水下视觉任务中的巨大优势。

## 结论/性能
- 零样本物种分类: MAI 87.1%, SAI 92.3% F1
- 零样本细粒度鱼类分类: FishNet 84.2%, FNOI 80.1%, LSF 93.4% F1
- 零样本珊瑚分类: CSC 96.4%, CC 95.3% F1
- 目标检测 (mAP50): FishNet 90.3%, DeepFish 89.1%, Brackish 87.7%, URPC 83.7%
- 线性探测: SAI 94.4%, FishNet 92.3%, LSF 96.1% F1
- 对比基线: 在 CC 数据集上超越 GPT-4V (+7.7%), BLIP-2 (+10.0%), Fine-tuned CLIP (+12.2%)
- 训练配置: 4x A100 GPU, 80 epochs, batch size 512, Adam (lr=1e-4), 20 个可学习提示
