# Interpretable End-to-End Neurosymbolic RL Agents

> Grandien, Delfosse & Kersting (2024) — arXiv:2410.14371 — TU Darmstadt

## 主题
Object-Centric Interpretable RL

## 背景
Deep RL agent 普遍依赖 shortcut learning，导致在略有不同的环境中泛化能力差，且其 black-box 特性使决策过程难以解释和调试。为应对此问题，基于 object-centric state 的 symbolic 方法被提出，其中 SCoBots（Successive Concept Bottleneck Agents）框架通过 interpretable concept bottleneck 将策略分解为可审查的中间步骤。然而，此前 SCoBots 仅在 ground truth object detection 下被验证，各组件也未被端到端整合。

## 现有局限与研究问题
- **Limitation:** 现有 SCoBots 框架依赖 ground truth object detection（由 OCAtari 提供），各组件（object extraction、relation extraction、action selection）未在无监督条件下端到端集成，限制了实际部署能力。
- **Problem:** 如何构建一个完全端到端的、使用无监督训练组件的 neurosymbolic RL agent，使其在保持 interpretability 的同时达到可竞争的 performance？

## 贡献
- 首次实现端到端训练的 SCoBot，所有组件均采用 unsupervised 训练，无需 ground truth object detection。
- 将 SPACE+MOC（object representation learning）、k-means classification、object tracking、relation extraction 和 ECLAIRE（policy distillation via rule extraction）整合为完整 pipeline。
- 在多个 Atari 游戏（Pong、Boxing、Skiing）上分别评估各组件，验证了框架的 interpretability 与 performance 潜力。
- 证明 modular 架构允许逐步升级组件，但也揭示了 error accumulation 问题。

## 方法论
- **整体架构（SCoBots pipeline）：** 将 policy 分解为三步：Object Extractor → Relation Extractor → Action Selector，每一步产生 interpretable concept bottleneck (ICB)。
- **Object Extractor：**
  - 使用 SPACE（VAE-based）架构配合 MOC（Motion and Object Continuity）训练方案，从原始图像中无监督提取 object bounding box 与 encoding。
  - K-means clustering 对 object encoding 进行无监督分类。
  - 简单 centroid-based tracking 算法推断跨帧 object identity，获取 position history 和 speed 等时序属性。
- **Relation Extractor：** 对提取的 object properties 应用确定性 relational functions（如 Euclidean distance、speed），输出 scalar relational concept vector 作为 action selector 的输入。
- **Action Selector：**
  - 先用 PPO 在 relational concept 上训练 neural policy。
  - 再通过 ECLAIRE rule extraction 将 neural policy 蒸馏为 IF-THEN rule set policy，实现最终的 interpretability。
- **实验设置：** 在 OCAtari 的 Pong、Boxing、Skiing 环境上评估；object extractor 在三个游戏上测试，action selector 在 Pong 和 Boxing 上测试；对比了 ground truth 与 SPACE+MOC input、neural 与 rule set policy、pruned 与 unpruned relational concepts 等多种配置。

## 关键结果
- Object extraction：Boxing 和 Pong 的 F-score 较高，Skiing 因 classifier 混淆（树被误分为 player）表现较差。
- Action selector：在 Pong 上，SPACE+MOC input + rule set policy 可达平均 reward 14.4（ground truth neural 为 ~17-19）；Boxing 上可达 51.8。
- Rule set policy 在特定配置下性能接近 neural policy，证明了 interpretability 与 performance 可兼得。
- Modular 设计允许组件独立升级，但 error accumulation 是主要瓶颈。

## 局限性
- 依赖训练图像包含所有 object 变体及 optical flow motion data 的强假设。
- 当前仅提取 location 和 class 属性，缺少 orientation 等高级属性。
- ECLAIRE 生成的 rule set 规则数量多、前提条件复杂，interpretability 仍有提升空间。

## 未来方向
- 用 YOLO 等统一检测跟踪模型替换 object extractor，或探索 SlotAttention、CutLER 等替代方案。
- 优化 ECLAIRE 超参数以生成更简洁的 rule set；探索 alternative policy distillation methods。
- 扩展到更多游戏和 3D 环境，测试框架的通用性。
