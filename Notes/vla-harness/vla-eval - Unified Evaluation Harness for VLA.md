# vla-eval: A Unified Evaluation Harness for Vision-Language-Action Models

> arXiv: 2603.13966 | 年份: 2026

## 主题
Unified VLA evaluation harness

## 背景
VLA（Vision-Language-Action）模型越来越需要在多个仿真 benchmark 上评测以证明跨环境、跨 embodiment 的泛化能力，但每接入一个 benchmark 都要付出可观的工程成本：各 benchmark 自带独立的 simulator、Python runtime 与资产依赖（LIBERO 需 Python 3.8 + robosuite，ManiSkill2 需 Python 3.10 + SAPIEN，CALVIN 需 Python 3.8 + PyBullet），没有任何单一环境能同时满足全部约束。除依赖冲突外，评测协议本身也常常 underspecified——seed、episode 数、preprocessing 细节多被论文省略。本文沿用语言模型领域 lm-evaluation-harness 的解耦思路，把 model inference 与 benchmark execution 彻底分离。

## 现有局限与研究问题
- **Limitation:** 在 M 个 benchmark 上评测 N 个模型需要重复 M 次接入、且对每个模型独立进行，构成 O(N × M) 的集成负担；对小团队而言全面的多 benchmark 评测不可行。同时协议 underspecified 导致复现依赖对参考实现的逐项人工比对，单个未记录参数即可使成功率波动最高 55 个百分点。
- **Problem:** 能否设计一套统一 harness，使模型只接入一次、benchmark 只接入一次，就自动获得完整的 N × M 交叉评测矩阵（把集成复杂度从 O(N × M) 降为 O(N + M)），同时保证对参考实现的复现保真度并显著压缩 wall-clock 评测时间？

## 贡献
- 开源评测 harness，支持 **14 个仿真 benchmark** 与 **6 个 model server**，基于 Docker 隔离与 WebSocket+msgpack 协议；模型只需实现单个 `predict()`，benchmark 只需实现四方法接口。
- 在 **6 个 VLA codebase × 3 个 benchmark** 上复现已发表分数，并记录此前**未被文档化的坑（undocumented pitfalls）**——其中单个未记录参数可使成功率偏移达 55 pp。
- 模型无关的并行评测方法论（episode sharding + batch inference），实现最高 **47× wall-clock 加速**（LIBERO 2,000 episodes：约 14 h → 约 18 min）；瓶颈在环境步进速率而非模型推理。
- 发布 VLA leaderboard，含 canonical protocol 定义，聚合 **17 个 benchmark 上的 657 条已发表结果**。

## 方法论
- **架构：** client-server 分离，WebSocket 承载 msgpack 二进制序列化。每条消息携带类型（observation / action / episode_start / end）、benchmark 专属 payload、sequence number 与 timestamp。
- **Model server：** 继承 `PredictModelServer`，提供阻塞式 `predict(obs, ctx)`（典型约 50 行），内建自动 action chunking 与可选的 batched inference（`max_batch_size`）。
- **依赖隔离：** model server 通过 PEP 723 inline metadata 声明依赖，`vla-eval serve` 用 `uv run` 自动拉起隔离环境；冲突依赖（CogACT 钉 `transformers==4.40.1` vs. X-VLA 需 `transformers>=4.44`）可共存，与 benchmark 侧的 Docker 隔离同构。
- **Benchmark 接入：** 在专用 Docker 镜像内实现四个方法 `reset` / `step` / `make_obs` / `get_step_result`，依赖全部 pin 死。
- **声明式配置：** 两份 YAML（benchmark + model server）驱动一次评测；全部 Docker 镜像带版本 tag 发布到 ghcr.io，并打包所需资产（scene 文件、纹理、robot description），消除 ad-hoc 资产安装。完整评测仅需两条命令：`vla-eval serve` 与 `vla-eval run`。每次运行产出结构化 JSON，记录 harness 版本、benchmark 配置与 per-episode 指标。
- **并行方法论：** 环境并行用 episode sharding 跨 K 个 Docker 容器；推理并行用 batched forward pass。以 demand/supply 方式调参——λ(K) 为环境吞吐随 shard 数的函数，μ(B) 为模型吞吐随 batch size 的函数，工作点满足 λ(K) < 0.8·μ(B*) 以避免排队堆积。
- **Leaderboard 策划：** 先建立各 benchmark 的 canonical protocol 定义（统一任务子集、指标、split 与可比性约束，因为 SimplerEnv 跨三种不可比机器人配置、CALVIN ABC→D 与 ABCD→D 不可比、LIBERO 论文有报 4 或 5 个 suite 之别）；再由 AI agent（Claude Code with Opus 4.6）经 MCP 工具（arXiv、Semantic Scholar、PDF reader）审阅 1,704 篇论文抽取并归一化结果；最后由人工逐条复核异常与歧义，每条记录带完整 provenance 元数据并通过自动 schema 校验。

## 实验与关键数字
- **规模：** Table I 列出 14 个 benchmark，action space 6D–14D，压缩后 Docker 镜像 4.7 GB（RLBench）至 35.6 GB（RoboCasa）。其中 3 个标为 cross-codebase reproduction verified（SimplerEnv、LIBERO、CALVIN），其余 11 个为 integrated but not yet cross-validated。6 个 model server：CogACT、OpenVLA、OpenVLA-OFT、π0/π0-FAST、GR00T N1、X-VLA。
- **并行加速（LIBERO + CogACT-7B，H100 model server + 独立 benchmark host）：** episode sharding 从 K=1 到 K=50 使环境吞吐提升 **32.6×**（λ: 11.2 → 364.6 obs/s）；batch inference 从 B=1 到 B=16 使 model server 吞吐提升 **2.8×**（μ: 165.2 → 468.2 obs/s）。合并后 2,000 episodes 由约 14 h 降至约 18 min，**47× 加速**。工作点 K*=50 占 B=16 供给容量的 78%；K>80 后环境开销导致吞吐下降。
- **其他 benchmark：** CALVIN 1,000 sequences、16 shards、约 33 min、**16×**（原 8.6 h）；SimplerEnv 288 episodes（3 seeds）、16 shards、约 8.5 min、**12×**（原 1.7 h）。
- **复现矩阵（Table II，ours 与 reported 的 Δ）：** 评测 protocol 为 LIBERO 4 suites × 10 tasks × 50 episodes（共 2,000）、CALVIN ABC→D 1,000 chained sequences、SimplerEnv 4 个 WidowX 任务每任务 24 episodes。LIBERO(%)：OpenVLA 76.2 (−0.3)、π0.5 97.7 (+0.8)、OpenVLA-OFT 96.7 (−0.4)、GR00T N1.6 94.9 (−2.1, 社区 checkpoint)、DB-CogACT 94.7 (−0.2)、X-VLA 97.4 (−0.7)。CALVIN(len)：DB-CogACT 4.02 (−0.04)、X-VLA 4.30 (−0.13)。SimplerEnv(%)：GR00T N1.6 59.7 (−8.0, Google Robot visual matching)、DB-CogACT 63.5 (−6.0)、X-VLA 94.8 (−1.0)。
- **未被记录的坑（undocumented pitfalls）：**
  1. **X-VLA / proprioceptive state source：** 在 LIBERO 上取错本体状态来源，成功率从 97.8% 跌至 42%——单个参数造成 **55 pp** 落差。
  2. **absolute vs. delta action mode：** 两者都是合法 7D 向量、仅从数据无法区分；混淆后位置误差累积、机器人发散，成功率 **0%**。
  3. **OpenVLA-OFT / quaternion-to-axis-angle：** 官方实现不做 antipodal normalization（angle ∈ [0, 2π]，符合 robosuite 约定），而作者初版实现翻转了 w < 0 的四元数（angle ∈ [0, π]）；这一处不匹配使 LIBERO-Goal 从 97% 跌到 83%、LIBERO-Long 从 95% 跌到 56%。
  4. **OpenVLA / 评测期 center crop：** 论文未记载的 center crop（scale = 0.9），省略后损失约 **3 pp**。
  5. **GR00T / end-effector pose 输入：** GR00T 期望 end-effector pose 作为本体输入，但该字段只存在于其内部 simulator fork、官方 SimplerEnv 中没有；缺失时分数从 30–55% 直接掉到 **0%**。补齐必要 patch 后，GR00T 在 SimplerEnv（Google Robot）从 0% 恢复到 59.7%，仍余 −8.0 pp 差距。
  - 以上问题均只能通过与参考实现逐层比对中间值才能发现。
- **Leaderboard 与 cross-benchmark 分析：** 聚合 **657 条结果 / 17 个 benchmark / 509+ configurations**，来源为引用了至少一个被追踪 benchmark 的 **1,704 篇论文**。覆盖分布（Fig. 5，509+ 模型）：**81%（410）只在 1 个 benchmark 上评测**，13%（66）2 个、5%（24）3 个、2%（9）4 个及以上，仅 3 个模型（0.6%）在 5 个及以上；只有 6% 覆盖 3 个及以上 benchmark——说明 cross-benchmark 比较极为稀缺。
- **局限：** 审计仅覆盖 6 个 codebase × 3 个仿真 benchmark，更多 benchmark 与真机迁移待做；leaderboard 结果来自论文抽取而非独立验证；支持指标仅限 task success rate，subtask progress、task efficiency、safety 等更细粒度维度尚未支持。
