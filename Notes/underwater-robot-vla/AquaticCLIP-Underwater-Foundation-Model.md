# AquaticCLIP - Vision-Language Foundation Model for Underwater Scenes

## 主题
Underwater vision-language foundation model

## 背景
水下生态系统受到过度捕捞、沿海开发和气候变化的严重威胁，aquatic scene understanding 对海洋生物学家进行物种监测和生物多样性保护至关重要。Vision-Language Models (VLMs) 如 CLIP 在通用领域的 zero-shot 任务上取得了巨大成功，但因水下成像存在低能见度、运动模糊、颜色畸变和缺乏大规模 paired image-text 数据，将其迁移到 aquatic 域仍极具挑战。

## 现有局限与研究问题
- **Limitation:** 现有水下 VLM 工作（如 MarineGPT、MarineInst）数量稀少，且依赖纯图像数据集或仅覆盖单一任务（segmentation/QA），缺乏大规模、领域特定的 image-text paired dataset；通用 CLIP 在水下场景下表现较差，因为预训练语料中几乎不包含 marine semantics。
- **Problem:** 如何在不依赖人工标注的前提下，构建大规模水下 image-text 数据集，并设计一种能够同时利用 visual 与 textual context 互相引导的 contrastive 预训练框架，使 VLM 能在 zero-shot 与 fine-tuned 设置下泛化到分类、检测、分割、计数等多种 aquatic downstream tasks。

## 贡献
- 构建并发布了 **2 million underwater image-text paired dataset**，数据来源涵盖 YouTube、Netflix、National Geographic、Marine Twitter、Fishes of Australia、Corals of the World 以及 1200 本海洋生物学教材，使用 MarineGPT 在 image-level 与 instance-level 上自动生成增强 caption，并通过 textual description cleaning 模块过滤噪声。
- 提出 **AquaticCLIP**，一种 dual-encoder contrastive 预训练框架，包含两个新颖的轻量模块：**Prompt-Guided Vision Encoder (PGVE)** 渐进聚合 patch features，以及 **Vision-Guided Text Encoder (VGTE)** 将视觉上下文注入文本表征，以进行 cross-modal 对齐。
- 在 zero-shot 与 fine-tuned 场景下进行了广泛评估，覆盖 marine species classification (MAI、SAI)、fine-grained fish/coral classification (FishNet、FNOI、LSF、CSC、CC)、object detection (FishNet、DeepFish、Brackish、URPC)、instance/semantic segmentation 与 object counting，全面超越 SOTA VLM (CoOp、MaPLe、GPT-4V、BLIP2、MarineGPT、MarineInst) 与 vision-only 模型 (ConvNeXt、ViT-L、AquaticVision DINOv2)。

## 方法论
- **Dataset Construction:** 从异质源采集 2M aquatic 图像，每 50 帧抽取关键帧，去除 motion blur 与无关图像；使用 PDF-Figures 2.0 提取教材 figures + captions，并人工核验对齐。
- **Unsupervised Caption Generation:** 利用冻结的 MarineGPT (frozen ViT + Q-former) 在 image-level 产生整体描述；结合 MRegionCLIP + MarineDet 进行实例检测，每个实例再用 MarineGPT 生成 instance-level caption。
- **Textual Description Cleaning Module (TDCM):** 将生成的描述拆分为 k-keywords，计算每个 keyword 与图像 embedding 的 cosine similarity，保留 top-p% 最相关的 keyword 与 ground-truth caption 拼接得到 enriched description C_i。
- **Prompt-Guided Vision Encoder (PGVE):** 输入图像被分为 n_p 个 patches，由冻结的 ViT-B/16 image encoder Φ_v 编码为 patch embeddings；引入一组 learnable prompts Q_i 作为 query，对 patch features 做 cross-attention 渐进融合，再经 MLP + softmax 得到 attention 权重 a_i(j)，最终聚合为 image-level feature f_i。
- **Vision-Guided Text Encoder (VGTE):** 将清洗后的 caption 通过 CLIP text encoder Φ_t 得到 T_i；将 patch features P_i 与 learned prompts E_i 拼接为 keys/values，T_i 作为 query 进行 vision-guided attention，残差更新得到富含视觉上下文的 text feature。
- **Cross-Modal Contrastive Loss:** 采用对称 InfoNCE 损失 L_cont = L_i2t + L_t2i，温度 τ 可学习，使配对 (f_i, T_i) 在 embedding 空间中靠近，非配对样本相互推远。
- **Training:** 在 4 张 A100 上用 Adam (lr=1e-4, weight decay=1e-5)，batch size 512，训练 80 epochs；fine-tune 四个组件 (image encoder, text encoder, PGVE, VGTE)，prompt 数 n_r=20。
- **Zero-shot Inference:** 将类别名套入 prompt template ("An image of {class}.") 编码为 text features，对测试图像计算余弦相似度并取最大者作为预测；同样的 backbone 经轻量 fine-tuning 即可支持 detection (AquaticDet)、segmentation 与 counting (AquaticOC)。
- **Ablations:** 系统验证了 PGVE、VGTE、TDCM 以及 image-level vs instance-level captions 对最终性能的贡献，在 6 个独立数据集上 F1 提升均显著 (例如 CSC 96.80% 准确率、96.40% F1)。
