# Underwater Diffusion Attention Network with CLIP Joint Learning

## 主题
CLIP-Guided Diffusion Underwater Enhancement

## 背景
水下图像因光吸收、散射、色偏与雾化等复杂退化而严重受损，直接影响 AUV 的目标检测、识别与场景理解等下游视觉任务。现有扩散类增强方法严重依赖合成的成对数据集，存在领域偏移与泛化能力差的问题；而对预训练扩散模型进行微调又容易破坏其先验知识，产生失真的伪增强结果。论文来自 King Fahd University of Petroleum and Minerals（Shaahid 与 Behzad，arXiv 2505.19895，2025年5月）。

## 现有局限与研究问题
- **Limitation:** 基于扩散模型的水下图像增强（UIE）通常依赖合成的成对数据，引入分布偏差；微调过程会损坏 CLIP/扩散模型的空中（in-air）自然图像先验，导致灾难性遗忘与失真增强；另外 CLIP 用于 UIE 时面临提示词对抽象退化（雾化、低对比度）描述不精确、相似提示得分差异大等不稳定问题。
- **Problem:** 如何在无需大量真实成对水下参考图的前提下，构建一个既保留空中自然图像先验、又能针对局部退化进行可控增强、并实现视觉-文本语义一致性的扩散增强框架？

## 贡献
- 提出 UDAN-CLIP：将图到图扩散模型与对比视觉-语言（CLIP）联合学习相结合的水下扩散注意力网络，以 CLIP-UIE 为基线进行扩展。
- 引入基于 VLM 的分类器，通过 CoOp/CLIP-LIT 风格的可学习提示（in-air 与 underwater 各 77 token）作为分类器引导，在微调过程中保留空中自然图像先验，缓解灾难性遗忘。
- 设计空间注意力模块，对骨干（ResNet-101）输出的特征图生成 1 通道空间注意力掩码，针对雾化、低对比度、浑浊等局部退化进行强化对齐。
- 提出新的 CLIP-Diffusion 联合损失 L_UDAN-CLIP，将像素级扩散噪声预测损失与基于 UDAN-CLIP 编码器的感知/语义对齐项加权融合（λ1=0.6，λ2=0.4），平衡像素保真度、感知质量与语义一致性。
- 在 T200、Color-Checker7 与 C60 等数据集的全参考与无参考指标上验证：T200 上 PSNR 27.949、SSIM 0.952、UCIQE 0.654 均超过 CLIP-UIE、DM_underwater、UDAformer、UIEC²-Net 等 SOTA。

## 方法论
- **数据合成（UIE-air）:** 使用 Reinhard 等的 CIELAB 色彩迁移，将 iNaturalist 2021 的空中图像迁移到随机选定的水下模板，生成成对（合成水下，空中真值）数据集 UIE-air，用于扩散模型的预训练。
- **预训练阶段:** 在 UIE-air 上训练条件扩散模型 ε_θ(x_t,y,t)，学习"水下退化→空中自然"的先验映射（损失 L2 噪声预测）；T=2000 步，线性噪声调度 1e-6→1e-2。
- **多条件分类器引导:** 微调时引入两个条件 y1（源水下图像，UIE-ref/SUIM-E/UIEB）与 y2（in-air 自然域），按贝叶斯展开得分函数 ∇log p(x_t|y1,y2)=∇log p(x_t)+λ∇log p(y1|x_t)+(1-λ)∇log p(y2|x_t)，并以 ε_θ(x_t,y1,y2,t) 形式融合分类器梯度引导反向扩散。
- **提示学习分类器:** 冻结 CLIP-UIE 主干，使用 CoOp 思想训练 in-air 与 underwater 两组可学习提示（N=77 token），用二元交叉熵区分两类图像，以避免人工提示词不稳定问题。
- **空间注意力模块:** 对 ResNet-101 主干输出 F∈R^{B×1024×H×W} 通过卷积+sigmoid 生成空间注意力掩码 A，元素相乘得到 F'=A⊙F，再用自适应注意力池化得到全局描述符 φ(I)，与文本嵌入做余弦相似度对齐，重点强化雾化/浑浊区域。
- **联合视觉-文本对齐与 CLIP-Diffusion 损失:** 将 L_classifier（基于优化提示的对比 softmax 项）作为额外引导加入噪声预测，并定义 L_UDAN-CLIP = λ1·L1(ε,ε_θ(x)) + λ2·D_CLIP(f_θ(x),f_θ(x_target))，在 UIEB+SUIM-E 上微调（800+1525 训练对），在 T200 测试，并以 ColorChecker7、C60 验证泛化。
