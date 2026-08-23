# DreamGuard: Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model

> arXiv: 2608.05695 | 年份: 2026

## 主题
Risk-aware world model runtime guardrail

## 背景
LLM agent 在开放环境中自主调用外部工具、修改外部状态与用户数据，不安全动作可能造成不可逆后果，因此 runtime guardrail（在动作执行前逐步审查 proposed action 并施加干预）成为关键防线。现有 guardrail 多为 reactive，只评估当前 proposed action 的表面安全性，缺乏对风险如何沿轨迹演化的显式建模。作者指出这留下了 long-horizon risk 的盲区：单看每步都合规的动作（如定位内部文件 → 移入工作区 → 创建公开分享链接）会累积成最终的机密数据泄露。

## 现有局限与研究问题
- **Limitation:** (i) 效率——proactive guardrail 多依赖 LLM 处理完整轨迹历史，受上下文窗口限制且需昂贵的自回归推理，常导致每步多秒级延迟；(ii) 预测与风险判定解耦——先预测未来状态再用独立安全规则/judge 打分，预测本身未针对 risk discrimination 训练，latent state 可能不含识别隐患所需证据；(iii) multi-horizon 风险难以标定——long-horizon 证据在隐患显性化之前很弱，而 immediate-hazard 证据要求在当前动作边界果断干预，两类互补信号需要融合成"早报警但不误报"的干预规则。
- **Problem:** 如何构建一个轻量、可在动作执行前运行的 guardrail，使其 latent dynamics 显式保留 hazardous transition 的证据，并把 immediate-hazard 与 prefix-risk 两个时间尺度的信号标定成 PASS/HOLD/BLOCK 决策？

## 贡献
- 提出 DreamGuard：以轻量 risk-aware world model 为核心的 runtime guardrail，维护固定维度的 recurrent latent state，在动作执行前估计 multi-horizon risk，实现对 immediate hazard 与 long-horizon risk 的 proactive 干预。
- 在四个 agent 安全 benchmark 上系统评测，在缓解 multi-horizon risk、更早干预 long-horizon risk、以及端到端延迟三方面均优于 generic / reactive / proactive 三类 guardrail baseline。
- 补充 online guardrail 评测（真实 agent 执行回路中作为 pre-action hook），验证其在 safety–utility 权衡上的实用性。

## 方法论
- **问题形式化：** guardrail G 在每步 t 接收 x = (e, H_t, a_t)（任务指令、交错的观测-动作前缀、proposed action），输出 d ∈ {PASS, HOLD, BLOCK}；目标是在首个 hazard step t^haz 之前触发 HOLD/BLOCK，同时抑制安全轨迹上的误警。
- **Risk-aware world model：** RSSM 架构，六个组件——sequence model（GRU + LayerNorm，h_t = f(h_{t-1}, z_{t-1}, a_{t-1})）、representation model（后验 z_t ~ q(z_t|h_t,o_t)）、dynamics predictor（先验 ẑ_t ~ p(ẑ_t|h_t)）、observation predictor、immediate-hazard predictor、prefix-risk predictor。后两者基于**预测的后继先验状态** ŝ_{t+1} = (h_{t+1}, ẑ_{t+1}) 打分，从而在执行前完成风险评估。stochastic state 为 factorized categorical + straight-through 梯度。
- **两阶段训练：** ① World model pretraining，L_WM = λ_pred·L_pred + λ_dyn·L_dyn + λ_rep·L_rep；L_pred 在 embedding 空间做 cosine 损失（预测后继观测 embedding 而非原始观测），L_dyn/L_rep 为带 free-bits κ 的反向 stop-gradient KL。② Risk-supervised training，immediate-hazard 用 BCE 监督 y^haz；prefix-risk 用衰减软标签 y^pre = exp(−(t^haz − t − 1)/ρ)（horizon K 内的前驱步），仅部分解冻通往两个 risk predictor 的路径、冻结 GRU core，使 latent dynamics 从"预测通用未来状态"变为"保留风险证据"。
- **Multi-horizon risk estimation：** 对 prefix-risk 分数做 EMA（p^ema，保留持久弱信号）与滑动窗口均值（p^win，保留瞬时上升），构成 temporal evidence state B_t；用有界 noisy-or 融合 S_t = NoisyOr(p^haz, p^ema, p^win)。
- **Split-conformal 校准的干预规则：** p^haz ≥ λ_block → BLOCK；S_t ≥ λ_hold → HOLD；否则 PASS。阈值在 held-out 安全校准轨迹上按轨迹级最大分数的 split-conformal 分位数选取（λ_hold = M_(k)，k = min(⌈(n+1)(1−α)⌉, n)），因而 false-alert 预算是轨迹级可控的；λ_block 用更严格预算同法得到。校准后阈值固定、测试期不变。
- **实现：** frozen Qwen3-4B-Instruct-2507 第 31 层 pooled 特征（2560 维）作为 encoder；deterministic latent 1024、stochastic 32×32；prefix-risk horizon K=3、衰减温度 ρ=1.5；stage-1/stage-2 各 10/12 epoch，batch 8，lr 2e-4，free bits 0.2，单张 H100。

## 实验与关键数字
- **Benchmark 与协议：** SafetyDrift（long-horizon 风险累积）、AgentDojo、Agent Security Bench (ASB)、ASSE-Security（immediate hazard 为主）。仅在 SafetyDrift 上训练与校准，其余三个 benchmark **零样本沿用同一组阈值**。四个 benchmark 统一转成 step-level 格式，由 LLM 预标注 + 两名标注者独立复核确定首个 hazard step。
- **Baselines：** generic（Llama-Guard-4-12B）；reactive（PolicyGuard、GuardAgent、AgentDoG-1.5）；proactive（SafePred、TRACES）。
- **主结果（F1 / SR / FPR %，Latency 秒/次）：** SafetyDrift 96.4 / 96.3 / 3.7 / 0.027；AgentDojo 74.9 / 76.9 / 29.4 / 0.034；ASB 82.1 / 74.2 / 13.6 / 0.023；ASSE-Security 82.9 / 77.2 / 9.8 / 0.016。四个 benchmark 上延迟均为最低，平均端到端 0.025 s/call。
- **跨风险类型稳健性：** TRACES 在 SafetyDrift 达 87.1 F1 但在 ASB 掉到 27.3；PolicyGuard 在 ASSE-Security 达 79.1 F1 但在 SafetyDrift 仅 26.4；DreamGuard 无此断崖式权衡。
- **效率对比：** 比 TRACES 快 3.3×、比 PolicyGuard 快 3.6×、比 GuardAgent 快 250.6×、比 SafePred 快 424.0×。
- **Timing（PHIR / MAS）：** SafetyDrift 96.3 / 3.63（两项均为最佳），AgentDojo 16.8 / 0.33，ASB 17.3 / 0.27（PHIR、MAS 均最佳），ASSE-Security 34.8 / 0.61。
- **Online guardrail：** GPT-5.1 作为 function-calling agent，ASSE-Security online 子集 100 例（48 unsafe / 52 benign），最多 6 步，α = 0.6；DreamGuard 达 Safety Rate 72.92% 且 Utility Rate 90.38%，位于现有 guardrail 构成的 safety–utility 前沿之外。
- **消融（ASSE-Security，Full = F1 82.9 / SR 77.2 / FPR 9.8 / PHIR 34.8 / MAS 0.61）：** w/o recurrent WM → F1 74.7、FPR 升至 73.7（SR 100.0 属过度干预）；w/o successor prediction → F1 76.3、FPR 25.4；w/o hazard predictor → F1 跌至 52.1、PHIR 13.0（降幅最大）；w/o prefix-risk predictor → F1 80.9 但 FPR 24.9、PHIR 25.8；w/o temporal aggregation → F1 77.8、SR 70.1；w/o WM pretraining → FPR 飙至 92.0；w/o risk-supervised training → FPR 仅 2.4 但 SR 64.1、PHIR 9.8、MAS 0.18（过度保守）。
- **局限（作者自述）：** 阈值仅在 SafetyDrift 上校准，面对显著分布漂移时仍可能需要目标域轻量重校准；框架只做"是否干预"，不生成安全的替代动作，触发干预后任务中断代价未被优化。

> 注：本文主体针对 LLM agent（tool-use / prompt-injection 场景），与 VLA harness 的关联是：其"冻结感知编码器 + 轻量 RSSM 预测后继 latent state + 风险监督塑形 + split-conformal 标定的 PASS/HOLD/BLOCK"这套 pre-action 干预骨架，可直接迁移为 VLA 策略执行前的低延迟 runtime monitor，只需把 LLM embedding 换成视觉-本体感知特征、把 hazard 标注换成机器人失效/违规步。
