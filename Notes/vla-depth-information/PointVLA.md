# PointVLA: Injecting the 3D World into Vision-Language-Action Models

## 主题
Injecting 3D point clouds into VLA

## 背景
Vision-Language-Action (VLA) 模型依靠大规模 2D 视觉-语言预训练在机器人操作上表现出色，但仅用 RGB 输入限制了对真实世界至关重要的 3D 空间推理（depth、object manipulation、height）。用 3D 数据从头重训计算代价高昂，且会浪费已有的大规模 2D robot 数据集。本文提出 PointVLA，在不重训预训练 VLA 的前提下，把 point cloud 作为补充条件信号注入。

## 现有局限与研究问题
- **Limitation:** 现有 robot foundation models（OpenVLA、π0、DexVLA 等）几乎都只用 2D 视觉输入，缺乏 3D 空间信息；而 3DVLA/3D Diffusion Policy 等纯 3D 方案要么依赖仿真存在 sim-to-real gap，要么需要重训/丢弃宝贵的 2D 数据，代价高且易过拟合于稀缺的 3D 数据。
- **Problem:** 如何在**不重训、不破坏**已建立的 2D 视觉-文本表征的前提下，把稀疏的 3D point cloud 信息高效注入预训练 VLA，使其获得 3D 空间感知能力？

## 贡献
- 提出 PointVLA：一个把 point cloud 注入预训练 VLA 的框架，**无需重训**，冻结 VLM backbone 与 vanilla action expert，仅通过轻量模块化 block 注入 3D 几何特征，最小化对预训练表征的扰动、缓解 2D 知识的 catastrophic forgetting。
- 提出 **skip-block analysis**：系统分析 action expert 中哪些 block 在推理时可被跳过（即"less useful"），只把 3D 特征注入这些不关键的 block，兼顾性能与效率。
- 在仿真（RoboTwin）与真机（bimanual UR5e、AgileX）上验证，超越 OpenVLA、Diffusion Policy、DexVLA、DP3、ScaleDP 等 2D/3D imitation learning 方法，并展示三大独特优势：few-shot multi-tasking、real-vs-photo discrimination（缓解 object hallucination）、height adaptability。

## 方法论
- **整体范式**：把 3D point cloud 当作**补充条件信号**（complementary conditioning signal）而非主输入模态，从而解耦 3D 处理与核心 2D 视觉编码器，保留预训练 2D 表征的完整性。基座建立在 DexVLA 上：2B 参数 Qwen2-VL 作为 VLM "brain"，1B 参数 ScaleDP（diffusion policy 变体，含 **32 个 diffusion transformer blocks**）作为 action expert。
- **3D 信息以何种形式进入模型**：
  - **Point Cloud Encoder**：采用简化的分层卷积架构（类似 iDP3），上层卷积提取 low-level 特征、下层卷积学习 high-level 场景表征，层间用 max pooling 渐进降低点云密度，最后把各卷积块的特征拼成一个统一的 multi-level 3D embedding。论文指出预训练 3D encoder 反而会阻碍新环境学习，故用轻量自训 encoder。
  - **Point Cloud Injector（注入 block 设计）**：先把 point-cloud embedding 的通道维变换到与 action expert 的 action embedding 对齐；用 **Adapter** 压缩较大的 action embedding 使其与 3D embedding 对齐（chunk size 1280 → 128 维 point-cloud emb）。对选定的 block，先用一个 **MLP 作为 adapter** 投影 3D 特征，再通过 **addition（加法）** 把 point cloud embedding 注入该 block；注入路径首尾用 **zero-initialized linear layer（Zero Linear）**，使训练初期注入为零、不破坏原模型输出。
  - **注入位置（哪些 block）**：以 DexVLA 的 shirt folding 为案例做 skip-block 分析——单 block 跳过实验发现**前 11 个 block 至关重要**（跳过任一会显著掉点），block 11 之后（约 11–31）贡献较小；多 block 连续跳过实验发现**最多可连续跳过 5 个 block** 才会失败。因此只在这些"less critical" 的 block 注入 3D，总共仅新增 **5 个 injection blocks**，推理时轻量快速。
- **为何冻结**：(1) 把 3D 数据从头训或全量重训计算上不可行，且会丢弃宝贵 2D 数据；(2) 注入会改变被影响 block 的表征——为最小化对 action expert 预训练特征空间的干扰，**冻结 VLM backbone 与 action expert 绝大部分**，只让 5 个 conditioning/injection block 及 action expert 最后几层（适配 embodiment 输出）可训练；保持 2D 视觉-文本 embedding 不变作为可靠信息源，同时缓解对稀缺 3D 数据的过拟合。
- **训练**：用 DexVLA stage-1 预训练权重微调，VLM 设为可训练以学习新语言指令，chunk size 50；用 RealSense L515 采集 point cloud。
- **量化增益（vs 纯 RGB 的 DexVLA，即 PointVLA 的 ablation）**：
  - 长程 packing（bimanual UR5e）平均完成长度 **Avg. Len 2.36 vs DexVLA 1.72**（且全面超过 Octo 0.27 / OpenVLA 0.36 / DP 0.36 / ScaleDP-1B 0.72）。
  - Real-vs-photo discrimination 成功率 **3/3 vs DexVLA 0/3**（OpenVLA/DP/ScaleDP 均 0/3），有效缓解 object hallucination。
  - Height adaptability（训练 3mm、测试 52mm 桌高）**5/5 vs 所有 2D 基线 0/5**。
  - RoboTwin 仿真：在 20 与 50 demonstrations 下跨多任务取得**最高平均成功率**；并观察到纯 3D 模型 DP3 直接加 RGB 反而掉点，凸显"有条件地"注入 3D 的必要性。
