---
imported_title: "Pi0.5: A VLA Model with Open-World Generalization"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/Pi0.5 - A VLA Model with Open-World Generalization.md"
imported_reason: "Background for the newer pi-series real-world VLA training line."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Pi0.5: a Vision-Language-Action Model with Open-World Generalization

- **Title:** π₀.5: a Vision-Language-Action Model with Open-World Generalization
- **Authors:** Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, Ury Zhilinsky
- **Venue:** arXiv preprint (arXiv:2504.16054)
- **Year:** 2025
- **Affiliations:** Physical Intelligence


## 主题 - VLA开放世界泛化能力

## 背景
Vision-language-action (VLA) 模型在端到端机器人控制方面取得了显著进展，但其泛化能力主要局限于与训练数据高度匹配的环境。开放世界泛化（即在从未见过的真实家庭中执行复杂、长时间操作任务）仍是物理智能领域的核心挑战。Physical Intelligence 团队基于其前代模型 pi0，提出了 pi0.5，旨在通过异构数据源的co-training实现广泛的真实世界泛化。

## 现有局限与研究问题
- **Limitation:** 现有VLA模型通常仅在与训练数据分布一致的环境中评估，难以泛化到全新场景（如未见过的厨房或卧室）
- **Limitation:** 单纯依靠扩大目标机器人平台的数据采集来覆盖所有可能场景是不可行的（brute-force scaling infeasible）
- **Limitation:** 现有端到端系统难以执行长时间（10-15分钟）、多阶段的灵巧操作任务（如清洁整个厨房）
- **Problem:** 如何设计一种训练框架，使VLA能够从多种异构数据源（不同机器人、语义标注、web数据）中进行知识迁移，实现多层次的开放世界泛化？

## 贡献
- 提出 pi0.5，首个能在全新真实家庭中执行长时间（10-15分钟）、多阶段灵巧操作任务的端到端学习型机器人系统
- 设计了一套heterogeneous co-training框架，整合mobile manipulator数据、non-mobile robot数据、cross-embodiment实验室数据、high-level subtask prediction、verbal instruction以及multimodal web数据
- 提出层次化推理架构（hierarchical inference）：同一模型先预测high-level semantic subtask，再基于subtask生成low-level action chunk
- 通过系统性ablation实验验证了各co-training数据源的贡献，证明cross-embodiment迁移与web数据对泛化至关重要
- 在三个从未见过的真实家庭中验证了 pi0.5 的泛化能力，显著超越 pi0 及其增强版本

## 方法论
- **两阶段训练流程：** Pre-training阶段使用discrete tokens（FAST tokenizer）在所有异构数据上进行标准autoregressive训练（280k steps）；Post-training阶段加入flow matching action expert，使用continuous action表示，专注于mobile manipulation（80k steps）
- **异构数据混合（Pre-training）：** 包括约400小时mobile manipulator家庭数据（MM）、多环境non-mobile robot数据（ME）、cross-embodiment实验室数据（CE）、high-level subtask prediction标注（HL）、以及image captioning/VQA/object localization等multimodal web数据（WD）
- **Post-training数据：** 在MM和ME数据基础上增加verbal instruction示范（VI）和web数据（WD），以保持语义与视觉能力
- **模型架构：** 基于PaLiGemma (2B) VLM backbone + 300M参数的action expert；使用attention mask确保VLM embedding单向流向action expert，避免信息泄漏
- **层次化推理（Hierarchical Inference）：** 推理时模型先通过autoregressive decoding生成high-level subtask文本（如"pick up the plate"），再以此subtask为条件，通过action expert经10步flow matching denoising生成continuous action chunk（horizon=50, 50Hz）
- **Loss函数：** 联合优化cross-entropy loss（text/FAST tokens）与flow matching loss（continuous actions），通过权重参数 alpha 平衡两者
- **泛化性能随训练环境数量提升：** 实验表明从3个到104个训练场景，模型在未见环境中的任务完成度持续提升，且104场景模型性能接近直接在测试环境训练的oracle baseline
