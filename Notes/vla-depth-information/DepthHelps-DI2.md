# Depth Helps: Improving Pre-trained RGB-based Policy with Depth Information Injection

## 主题
Depth injection for RGB policy

## 背景
3D 感知能力对可泛化的机器人操作至关重要，但当前基于 foundation model 的操作 policy 大多只用 RGB 输入，缺乏 3D 感知，在 fine-grained manipulation 上表现受限。直接训练 RGB-D policy 又依赖深度传感器、部署受限。本文针对"已有大量训练好的 RGB-based policy、且现实中多为 RGB-only 场景"这一现状，提出用最少量对齐的 RGB-D 数据，把 depth 的空间先验注入到预训练 RGB policy 中，推理时仍只用 RGB。基线模型采用在 Calvin 上预训练的 RoboFlamingo (VLM 架构)，benchmark 为 LIBERO。

## 现有局限与研究问题
- **Limitation:** 主流 robotic foundation policy 只依赖 RGB，缺乏 3D/depth 感知，fine-grained 操作受限；而直接做多模态 RGB-D policy 或 cross-modal distillation 的方法，在 manipulation 这种时序任务里会产生 sequential accumulative errors（深度预测误差随时间步累积），且常因偏重模态间知识迁移而忽视操作任务本身需求，导致 RGB-only 部署时性能反而下降。
- **Problem:** 如何用最少量的对齐 RGB-D 数据，把 depth 蕴含的空间先验注入到一个已训练好的 RGB-based policy 中，使其在推理阶段仅靠 RGB 输入就获得接近 RGB-D 的 3D 感知与操作精度？

## 贡献
- 提出 Depth Information Injection (DI²) 框架：用 RGB-Depth 数据微调 policy，但部署/推理时仅依赖 RGB 图像，增强预训练 RGB policy 的 3D 感知能力。
- 设计 Depth Completion Module (DCM) 与 Depth-Aware Codebook (DAC) 两个核心模块，分别负责"从 RGB 预测 depth 特征/注入空间先验"和"离散化去噪、抑制累积误差"。
- 在 LIBERO 仿真 benchmark 与真实世界（Franka Emika Panda + Intel D435）四任务上验证有效性；RGB-only 主实验平均成功率 63.15%，较 RGB-RF 基线 57.95% 提升约 5.2pp（约 9% 相对提升），Long Horizon 套件优势最大（36.40% vs 24.20%）。

## 方法论
- **整体机制（训练用 RGB-D、推理纯 RGB）**：训练时模型输入 RGB-D，动作由 `a_t = π(VLM(f_text, f_rgb, f_depth))` 给出。推理时不再有真实 depth，只用 f_text、f_rgb，以及由 DCM 从 RGB 预测、再经 DAC 量化得到的虚拟 depth 特征，三者一起喂进 VLM 得到动作。即 depth 以"特征"形式进入模型，而非显式深度图。
- **Depth Completion Module (DCM)**：让模型在没有 depth 输入时也能恢复深度的空间信息。RGB 与 depth 各自送入同一个冻结的 ViT 提特征，再分别用独立 projection 层得到 f_rgb 和 f_depth。借鉴 Perceiver Resampler，引入 k 个可学习 token P ∈ R^{k×d} 显式存储空间先验：以 RGB 特征 f_rgb 作为 query，把 P 与 f_rgb 拼接构成 key/value，经多层 cross-attention + FFN 融合，最终输出即预测的 depth 特征 f̂_depth = DCM(f_rgb, P)。P 编码了训练/测试场景共有的统计特性，使模型可从 RGB 推断与操作相关的 depth。
- **Depth-Aware Codebook (DAC)**：解决时序操作中深度预测误差累积、与真实 depth 轨迹偏差变大的问题。定义码本 Z ∈ R^{N×d}（N=512），对 DCM 预测的连续 depth 特征做最近邻量化 f̃_depth = q(f̂_depth | Z) = z_k（取与码字欧氏距离最近者）。码本相当于训练集 depth 特征的聚类中心，比原始连续特征更鲁棒、能过滤模态特定噪声。为避免 codebook collapse，借鉴 CVQ-VAE：每次迭代对每个码字按使用频次做 running-average 更新并对不常用码字用 anchor 向量重初始化（λ=0.99）。
- **三阶段训练**：① Warm-up——用收集到的 RGB+depth 联合训练 imitation policy（loss 为动作 L2，depth 分支与预训练 RGB 模型联合优化）。② Align——去除对真实 depth 的依赖：用 warm-up 得到的感知 encoder，借成对 RGB-D 数据训练 DCM，loss `L_dcm = ||DCM(P, sg(f_rgb)) − sg(f_depth)||²`（sg 为 stop-gradient），把 3D 先验蒸馏进 DCM。③ Codebook——冻结 depth 分支，仅用 MSE 训练码本，配合 running-average 重初始化防坍缩。
- **量化增益**：在 RGB-D 上界实验中 Ours 63.95% vs RGB-RF 57.95%（+6pp）；切到 RGB-only 时 Ours 仅降至 63.15%（降幅最小），而 RGB-D-RF 从 61.25% 崩到 15.65%（严重依赖真实 depth）。消融显示 DCM 贡献最大（去掉 DCM 改用 MLP，平均仅 36.95%；DCM+DAC 全开 63.15%），DAC 主要提升 Goal/Spatial/Long Horizon 并降低 action prediction error。真实世界四任务同样验证 RGB-only 下仍保持优秀表现。
