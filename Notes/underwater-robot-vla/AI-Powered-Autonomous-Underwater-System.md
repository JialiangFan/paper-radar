# AI-Powered Autonomous Underwater System for Sea Exploration

## 主题
AI-integrated AUV detection pipeline

## 背景
传统海洋探索受限于高压、低能见度和不可预测的水下环境，人类潜水员单次下潜不足一小时，且数据收集分析耗时数周，导致 70% 的地球表面中仅约 5% 的海洋被充分探索。随着 AI 与自主系统的发展，将计算机视觉、机器学习与自动报告生成整合进自主水下航行器（AUV）成为提升海洋探索效率与安全性的关键路径。本论文提出一个端到端 AI 驱动的 AUV 系统，将 YOLOv12 Nano 检测、ResNet50 特征提取、PCA 降维、K-Means++ 聚类与 GPT-4o Mini LLM 摘要融为单一管线。

## 现有局限与研究问题
- **Limitation:** 现有水下 AI 工作（如 DeepFins、MERLION、MarineInst、MarineGPT）大多聚焦单一环节——或仅做检测、或仅做视觉摘要，缺乏将 YOLO 检测、CNN/PCA 特征处理、K-Means 聚类与 LLM 自然语言报告统一进同一自动化流水线的整合方案；同时领域内 LLM 海洋特异性知识不足，且训练数据存在类别不平衡与图像质量退化问题。
- **Problem:** 如何在算力受限的硬件条件下，构建一个面向 AUV 的端到端 AI 流水线，使其能够实时检测水下目标、对检测结果进行特征级聚类发现潜在新类别，并自动生成结构化的科学报告，从而降低人工潜水风险并加速海洋数据解读？

## 贡献
- 提出首个将 YOLOv12 Nano 检测 + ResNet50 特征提取 + PCA 降维 + K-Means++ 聚类 + GPT-4o Mini LLM 报告整合为单一自动化管线的水下 AI 系统，覆盖从原始视频帧到自然语言科学报告的完整闭环。
- 在合并 DeepFish 与 OzFish 共 55,722 张澳大利亚海域图像（>496 种鱼类、60k+ 实例）上训练评估，YOLOv12 Nano 取得 mAP@0.5 = 0.512、Precision = 0.535、Recall = 0.438，推理速度 2.0–5.5 ms，验证了轻量模型在多样海洋场景下的可用性。
- 通过 PCA 在保留 98% 累积方差的同时将 CNN 特征压缩到 150–900 维，使 K-Means++ 在 687 个检测裁剪中自动确定 27 个有意义聚类，证明无监督聚类可揭示鱼类的形状、光照、姿态等隐含模式，并为发现新物种提供线索。
- 设计针对海洋背景的 LLM 提示模板，将检测裁剪、聚类 HTML、GPS 坐标作为多模态上下文输入 GPT-4o Mini，自动生成包含形状、纹理、栖息地与地理位置的结构化检测/聚类摘要，并通过 Plotly + Dash 在阿拉伯湾场景下完成地图可视化原型。
- 系统化梳理水下 AI 现状（YOLO、CNN、K-Means、LLM 四条线），明确"缺乏端到端整合"的研究空白，并提出针对类别不平衡、维度灾难、本地化海洋 LLM、扩展到海马/虾蟹/植物等多类别以及面向真实部署的模型量化等五条未来方向。

## 方法论
- **系统架构（七大模块）：** Autonomous Vehicle（搭载相机/LiDAR/GPS 等传感器）→ YOLO Object Detection Module → GPS Localization Module → Mapping Module → Image Preprocessing Module（CNN 特征提取）→ K-Means Clustering Module（PCA + Kmeans++）→ Large Language Model API Module（OpenAI GPT-4o Mini），各模块独立运行并把结果缓存到统一 Data Repository 供后续调用。
- **检测阶段：** 采用 YOLOv12 Nano（Ultralytics），引入注意力中心机制，在 NVIDIA RTX 3070 Ti + Ryzen 9 5900X + 32 GB RAM 平台上训练超过 170 小时；将 DeepFish（4,505 帧）与 OzFish（51,217 帧）按 85/15 划分 train/val，统一为 1920×1080 分辨率，以置信度阈值过滤输出边界框与类别概率。
- **特征与降维阶段：** 对每个检测裁剪用 ResNet50 提取深度特征向量并展平；PCA 在两步中使用——一步用于聚类前的特征精炼，另一步用于 2D/3D 可视化，组件数随输入裁剪量自适应（150–900），目标保留 0.98 累积方差；当裁剪数超过 2000 时受硬件限制需调整组件数。
- **聚类阶段：** 使用 K-Means++ 智能初始化加速收敛并提升簇质量，对 687 个检测裁剪聚成 27 簇，通过 Plotly 在 PCA 降维空间内可视化各簇分布，并人工挑选 4 个不同光照/角度/形状的裁剪验证簇分配的相似性与潜在新类别发现能力。
- **LLM 报告阶段：** 通过 OpenAI API 调用 GPT-4o Mini，针对"检测"与"聚类"两类任务设计专用 prompt，将图像裁剪或聚类 HTML 作为附件、GPS 坐标作为辅助输入，生成包含形状、大小、纹理、可识别图案、栖息环境与常见出现地点的结构化摘要；并通过 Plotly + Dash 在阿拉伯湾地图上模拟单/多检测点的真实部署可视化。
- **评估指标：** YOLO 端用 mAP@0.5、Precision、Recall；PCA 用保留组件数与累积解释方差；K-Means 用簇数 k；并辅以 4 段 YouTube 真实水下视频做外部推理验证，置信度从 0.85 到 0.1 区间评估鲁棒性。
