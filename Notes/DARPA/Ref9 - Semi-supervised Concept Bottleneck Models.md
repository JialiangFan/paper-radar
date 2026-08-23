# Semi-supervised Concept Bottleneck Models

## Research Problem
How to train concept bottleneck models with minimal concept annotations by jointly addressing semi-supervised concept labeling and concept-saliency spatial alignment.

> Hu, L., Huang, T., Xie, H., Gong, X., Ren, C., Hu, Z., Yu, L., Ma, P., & Wang, D. (2024). Semi-supervised Concept Bottleneck Models. arXiv:2406.18992v3.

## 主题

Semi-supervised Interpretable Concept Learning

## 背景

Concept Bottleneck Models (CBMs) 通过引入人类可理解的 concept bottleneck layer，为黑箱深度学习模型提供基于概念的可解释性，在分类任务中先预测 concept labels 再据此做出最终分类决策。然而，CBM 的训练严重依赖由专家标注的高质量 concept annotations，获取成本高昂且耗时。现有的无监督方法（如 Label-free CBM）虽然摆脱了标注依赖，但过度依赖 GPT-3 等大语言模型生成概念集，存在可靠性不足、缺乏 concept evaluation metrics、以及"完全无标注"假设过于理想化等问题。

## 现有局限与研究问题

- **Limitation 1:** 传统 CBMs 需要完整的 expert concept annotations，标注成本极高，限制了实际应用场景的规模化部署。
- **Limitation 2:** 现有 CBM 方法中 concept saliency maps 与 input saliency maps 经常出现 misalignment，即模型预测的 concept 并未对应到图像中真正相关的特征区域，削弱了可解释性的可信度。
- **Limitation 3:** 无监督 CBM 方法依赖 LLMs 生成 concepts，可靠性差且无法利用少量已有标注数据。
- **Problem:** 如何在仅有少量 concept labels 的 semi-supervised 设定下，同时实现高精度的 concept prediction 和 concept-input alignment，使 CBM 在数据稀缺场景下仍保持良好的分类性能与可解释性？

## 贡献

- 提出 SSCBM (Semi-supervised Concept Bottleneck Model) 框架，首次在统一框架中同时解决 semi-supervised concept annotation 和 concept-saliency alignment 两个问题。
- 设计基于 KNN 的 pseudo labeling 策略，利用 labeled data 的 cosine similarity 为 unlabeled data 分配高质量 pseudo concept labels（即 c_img），简洁高效。
- 提出 Image-Textual Semantics Alignment 模块：通过计算 concept embeddings 与 image feature maps 之间的 concept heatmaps，生成基于 alignment 的 pseudo concept labels（即 c_align），并引入 alignment loss 优化两类 pseudo labels 的一致性，解决 concept-saliency misalignment 问题。
- 在 CUB、AwA2、WBCatt、7-point 四个数据集上的实验表明，仅使用 10% labeled data，SSCBM 的 concept accuracy 和 task accuracy 平均仅比 fully supervised 最优 baseline 低 2.44% 和 3.93%。

## 方法论

- **整体架构：** 基于 Concept Embedding Model (CEM) 构建，包含 feature extractor (backbone, e.g., ResNet50)、embedding generator、concept bottleneck layer、label predictor 四个核心模块。
- **Labeled data 处理：** 输入经 backbone 提取 latent representation h，送入 embedding generator 生成 concept embeddings，经 FC + sigmoid 得到 predicted concept vector c_hat，与 ground truth concept labels 计算 binary cross-entropy concept loss (L_c)；label predictor 基于 c_hat 预测类别，计算 task loss (L_task)。
- **Unlabeled data - Pseudo Labeling (c_img)：** 使用 visual encoder 提取 image features，计算 unlabeled sample 与所有 labeled samples 的 cosine distance，选取 k-nearest neighbors，以归一化距离倒数为权重加权平均其 concept labels，生成 pseudo concept labels c_img。
- **Unlabeled data - Concept Heatmap & Alignment Label (c_align)：** 利用 visual encoder 的 feature map V (H x W x m) 与每个 concept embedding c_i^m 计算 cosine similarity heatmap H_i；对 heatmap 进行 average pooling 得到 concept score vector s；通过 threshold 将 s 二值化为 alignment pseudo label c_align。
- **Alignment Loss：** 计算 c_img 与 c_align 之间的 binary cross-entropy，即 L_align = BCE(c_img, c_align)，促使 concept encoder 同时从 pseudo labels 和 image-concept alignment 中学习。
- **总体损失函数：** L = L_task + lambda_1 * L_c + lambda_2 * L_align，其中 lambda_1 和 lambda_2 为平衡可解释性与准确率的超参数。
- **评估指标：** Concept accuracy、task accuracy、concept saliency map 可视化、test-time intervention 实验验证可解释性。
