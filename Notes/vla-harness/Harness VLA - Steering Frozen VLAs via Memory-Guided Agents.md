# Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

> arXiv: 2607.08448 | 年份: 2026

## 主题
Memory-guided agent harnessing frozen VLAs

## 背景
语言条件操作（language-conditioned manipulation）同时要求精细的 contact-rich 控制与跨语言、场景、长时序的鲁棒推理。端到端 VLA 模型能从机器人轨迹中直接学到强局部视觉运动技能，但只在其训练轨迹分布内可靠；一旦遇到部署扰动（semantic retargeting、goal re-binding、spatial-layout shift、不稳定局部接触），策略往往重复训练期行为而忽略改变后的指令或场景绑定，单次接触失败即可拖垮整条 monolithic rollout。另一方面，LLM coding agent（Code as Policies、ProgPrompt 及其多模态/agentic 变体）提供互补的语义与组合推理能力，但纯 analytic primitive（IK transport、腕部旋转、夹爪开合等确定性控制器）难以处理不规则抓取、受限放置和 articulated-object 交互。本文把两条路线在 agent harness 视角下做非对称分工。

## 现有局限与研究问题
- **Limitation:** 端到端 VLA 把语言 grounding、长时序组合与底层控制压进单一策略，分布外部署时崩塌（LIBERO-Pro 上 OpenVLA 0.0%、π₀ 0.3%、π₀.₅ 11.0%）；coding agent 侧则倾向于不断扩充 skill library，而 analytic primitive 本身不适合 contact-rich 操作。已有 agentic 工作中，task-specific 执行轨迹很少被表示成可在新空间布局下重新 grounding 的参数化记忆，failure knowledge 也很少被蒸馏成防止重复 empty grasp / false success 的 Global Memory。
- **Problem:** 能否在**不微调 VLA、不在部署期扩充 primitive 词表**的前提下，仅靠 memory-guided agent 对固定 primitive 库的编排，把冻结 VLA 从局部 contact 专家提升为长时序、抗扰动的可靠操作系统？

## 贡献
- 提出 Harness VLA：一个 memory-augmented agentic framework，把冻结 VLA 封装成**单个可重试的 contact-rich primitive**（`VLA_ACT`），与固定的 analytic primitive 组合，在不微调 VLA、不在部署期新增 primitive 的条件下扩展其轨迹分布外能力。
- 给出实证分析，说明为什么**小而固定**的 primitive 库足够：关键不在于加技能，而在于 planner 学会每个 primitive 的 operating range——哪些子问题交给 analytic 控制、何时该调用 `VLA_ACT`、失败接触该如何 re-stage。
- 在标准/扰动 tabletop、家庭厨房、clean-to-randomized 双臂迁移四类 benchmark 上给出强结果：LIBERO-Pro 与 RoboCasa365 分别超过最强相关基线 38.6 与 25.4 个百分点，RoboTwin C2R 达 58.4%，同时保持标准 LIBERO 竞争力。

## 方法论
- **问题形式化**：环境为刚体物理引擎（MuJoCo via Robosuite）；每步观测 o_t = (RGB 图 I_t^rgb, 共配准 metric depth I_t^d, 本体状态 q_t)；任务由自然语言 ℓ 与二值完成谓词 𝒢 定义，仅在 episode 结束给出稀疏成功信号。
- **Agentic execution loop**：把 rollout 建模为高层 planner Π 与物理引擎之间的自回归、turn-based 交互。不设独立层级 tier——冻结 VLA f_θ 与所有确定性 operational-space 控制器统一进入同一个预定义 primitive 库 𝒫。每一轮 Π 读取 o_t、ℓ 与两类记忆检索结果，输出一个结构化 JSON invocation c_t ∈ 𝒫；引擎执行至该 primitive 内部 post-condition 满足，返回 o_{t+1}，直到 𝒢 成立或步数预算耗尽。
- **Harness（运行时契约）**：REPL 式接口，负责暴露 primitive schema、序列化 JSON 决策、执行 primitive、刷新 RGB-D 与本体观测、记录 trace、检索记忆、执行 reset 与预算策略、按 benchmark 谓词检查进度。
- **两阶段生命周期**：
  - *Exploratory Bootstrapping*：在单个 reference seed 上自主试错，此阶段独占 `RESET` 权限与宽松 wall-clock 预算，迭代搜索 staging order、pre-contact pose、`VLA_ACT` 调用时机与 early-return 阈值。成功后把验证过的 primitive 调用序列序列化为 JSONL 存入 **Task Specific Memory**（把具体坐标替换为符号化感知查询，从而跨空间布局可复用）；同时把泛化启发式提炼进持久化 **Global Memory**（success rules，如利用完整任务指令的最优 prompting 策略；failure models，如 empty-grasp 与 false success 识别）。
  - *Deployment Evaluation*：面向未见环境变体（position swap、instruction redirection、多个初始 seed），**完全禁用 `RESET`** 并显著压缩步数预算；planner 检索预计算的 JSONL trace 并用实时 RGB-D 动态 re-ground，参考 Global Memory 确定性执行。论文报告的 benchmark 数字均来自该严格阶段。
- **Unified Primitive Interface（Table 1）**：共享接口含 6 个 analytic primitive + 1 个 VLA primitive——composite 类 `MOVE_TO`、`MOVE_POSE`（世界系笛卡尔目标 / 位姿协变，走内嵌 solver），atomic 类 `ROTATE_WRIST`、`ROTATE_PITCH`、`SET_GRIPPER`、`RELEASE`，以及 `VLA_ACT`；RoboCasa365 额外加 `NAVIGATE_TO`、`MOVE_BASE` 两个移动底盘 primitive 支撑厨房尺度 staging。`RESET` 仅用于 bootstrapping、不计入操作 primitive。primitive 词表在评测前固定，planner **不能**在部署期发明新 primitive。
- **VLA-backed contact primitive**：`VLA_ACT` 接收任务条件 prompt 与 early-return 谓词 τ，冻结 VLA f_θ 持续输出 action chunk 直到 τ 满足或 chunk 预算耗尽，覆盖抓取、受限放置、fixture 驱动、按钮按压、抽屉/门操作、插入等 contact 行为；语义 grounding、空间 re-binding、导航、re-staging 与长时序组合全部留在 planner 侧。
- **Planner backbone**：Codex 与 Claude Code（CC）两种实例，共享同一 harness、记忆接口、primitive 库、冻结 VLA 接口与评测协议，仅 backbone 不同。

## 实验与关键数字
- **设置**：四个 benchmark 家族——LIBERO、LIBERO-Pro（tabletop 扰动）、RoboCasa365（家庭厨房 + 移动底盘）、RoboTwin C2R（双臂 clean-to-randomized 迁移）。`VLA_ACT` 后端分别为 RLinf 发布的 `pi05_libero130_fullshot` π₀.₅-SFT checkpoint（π_RLinf，用于 LIBERO/LIBERO-Pro）、冻结 RLDX-1 RoboCasa checkpoint、post-trained LingBot-VLA（RoboTwin C2R）。
- **标准 LIBERO（Table 2）**：Harness VLA (CC) 总体 96.0%（384/400），Object 100.0%、Spatial 97.0、Goal 94.0、LIBERO-10 93.0；同一冻结 checkpoint π_RLinf 为 95.3%，AtomVLA 97.0。说明可控 primitive 接口未损失 in-distribution 性能。
- **LIBERO-Pro（Table 3，instruction-redirection T + position-swap S，每格 10 tasks × 10 seeds = 100 trials）**：端到端 VLA 大面积崩塌——OpenVLA 0.0、NORA 0.0、π₀ 0.3、MolmoAct 1.5、X-VLA 3.8、AtomVLA 6.3、π₀.₅ 11.0；coding-agent 基线 Cap-X 18.2、RATS 43.8（最强先前基线）。Harness VLA (Codex) 72.1%、(CC) **82.4%**，相对 RATS 提升 **38.6 个百分点**；直接 π_RLinf 基线在同协议下 50.0%，说明增益并非来自冻结 VLA 骨干本身。
- **RoboCasa365（Table 4）**：RLDX-1 task-weighted overall 30.0%；Harness VLA (Codex) 55.4%、(CC) 48.6%，Codex 实例超 RLDX-1 **25.4 个百分点**。分项 Codex：Atomic-Seen 91.6 / Composite-Seen 56.3 / Composite-Unseen 13.8；CC：79.4 / 47.5 / 15.0。基线对比：RLDX-1 60.0/21.3/5.0，WorldDreamer 66.3/26.7/9.0，π₀.₅ 39.6/7.1/1.2，π₀ 34.6/6.1/1.1。仅用 1 个 reference seed 做 bootstrapping，评测用 10 个（Atomic-Seen）/5 个（Composite）held-out seed。
- **零样本 LIBERO-Pro GOAL（Table 5，不检索任何 Task Specific / Global Memory，10 seeds/task）**：Harness VLA (CC) 在 position-swap 达 31.0%（Cap-X 25.6%），在 instruction-redirection 达 79.0%（Cap-X 16.8%）。与 few-shot 对照可分离记忆贡献：指令重定向下语义 re-binding 能力大体保留（79.0% zero-shot vs 87.0% few-shot），但位置扰动下明显下滑（31.0% vs 87.0%），说明空间扰动强烈依赖 bootstrapping 期发现的 task-specific primitive 组织。
- **RoboTwin C2R（Table 6，50 tasks × 5 randomized seeds，零样本 clean-to-randomized 迁移）**：直接 LingBot-VLA 50.4%；Harness VLA (Codex) 58.0%、(CC) **58.4%**。外部基线 GR00T-N1.7 20.7、π₀.₅ 47.9、StarVLA 10.6。
- **Key Finding 2 / 自适应调用（Figure 4）**：以每 episode 允许的最大 `VLA_ACT` 调用次数 k 作横轴——LIBERO-Pro：k=1 已达 52%（超过 frozen-policy 基线 50%），k=2 为 68%，饱和至全 harness 的 82%；RoboCasa365：k=1 为 2%、k=3 为 21%、k=10 为 39%，全 harness 48%（frozen 基线 30%）；RoboTwin C2R：k=1 为 18%、k=2 为 42%、k=3 为 49%，全 harness 58%（frozen 基线 50%）。少数 planner 选择的调用即可超越冻结策略，说明 VLA 调用稀疏但可 re-stage/重试是鲁棒性关键。
- **Key Finding 3 / 完成归因（Figure 6）**：成功 rollout 中触发最终完成谓词的 primitive 类别——LIBERO 家族以 analytic 为主（Spatial 72%/28%、Object 80%/20%、Goal 79%/21%、LIBERO-10 84%/16%，analytic/VLA）；RoboCasa365 与 RoboTwin 终局更依赖 contact 操作（Composite-Seen 40%/60%、Composite-Unseen 17%/83%、Atomic 14%/86%；RoboTwin 50 tasks 34%/66%）。
- **局限（作者自述）**：高层 planner 与底层 VLA 之间是开环反馈；缺少基于环境奖励与人类偏好的联合微调（未来可用 GRPO 等 sample-efficient RL）；缺乏细粒度 image captioning，限制高杂乱长时序任务中的结构推理；可与 ASPIRE 等自动技能发现结合，在保留可审计 primitive 接口的同时准入新技能。
