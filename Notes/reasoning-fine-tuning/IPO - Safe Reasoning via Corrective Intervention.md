# IPO: Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention

## 主题
Safe Reasoning Alignment via Intervention

## 背景
大型推理模型（LRMs）如 DeepSeek-R1 在数学、编程等任务上取得了突破性进展，但其 chain-of-thought (CoT) 推理过程中常包含有害内容，即使最终回答看似安全。现有的安全对齐方法主要关注最终输出的安全性，忽略了推理过程本身的安全问题。不安全的推理过程不仅可被恶意用户利用获取有害信息，还使模型更易受到 jailbreak 攻击。

## 现有局限与研究问题
- **Limitation:** 现有安全对齐方法（如 SFT-based 的 SafeChain、RealSafe、STAR）仅在蒸馏的安全 CoT 数据上微调，无法彻底消除推理过程中的不安全内容
- **Limitation:** 即使最终回答安全，推理 trace 中仍可能包含有害信息（如具体犯罪方法），对开源模型尤其危险
- **Limitation:** 使用 RL 方法（如 GRPO）直接奖励安全推理效果有限，因为 rollout 多样性低——约 50% 的有害 prompt 几乎无法产生安全推理轨迹，导致训练信号不足
- **Problem:** 如何在不牺牲推理能力的前提下，实现推理过程级别的安全对齐（process-level safety alignment）

## 贡献
- 揭示了三个关键洞察：(1) 安全推理由少数关键步骤 **safety triggers** 巩固；(2) **compliance cues**（顺从线索）与不安全推理的产生强相关（Pearson R=0.853）；(3) 用 safety triggers 替换 compliance cues 的干预可有效将不安全轨迹纠正为安全轨迹
- 提出 **Intervened Preference Optimization (IPO)**，通过在 safety-critical steps 处进行干预构造偏好对，扩展 DPO 到推理安全领域
- 在三个 LRM（DS-8B、DS-7B、Qwen3-8B）和多个对抗性安全基准上验证了 IPO 的有效性，推理有害率相对降低超过 30%，同时保持甚至增强推理能力
- IPO 训练效率远超 GRPO（约 40 分钟 vs 2 小时以上），每个 prompt 最多仅需 14 次生成

## 方法论
- **核心框架**: IPO 基于 DPO，在推理轨迹的 safety-critical 位置进行干预，构造偏好对用于偏好学习
- **Safety Triggers 识别**: 定义 Continuation Safety Ratio (CSR) 衡量每个 token 后续生成安全的概率，找到 CSR 急剧上升的转折点作为 safety triggers（>90% 的安全轨迹含有此类转折点）
- **Compliance Cues 检测**: 使用 GPT-4o 自动检测推理中第一个 compliance cue（表达顺从恶意请求倾向的语句），与 CSR 下降点高度相关
- **干预过程**: 在不安全轨迹中用采样的 safety trigger 替换第一个 compliance cue，模型从干预点继续生成，形成纠正后的安全轨迹
- **偏好对构造**: 原始不安全轨迹为 rejected，干预后的安全轨迹为 chosen，共享相同前缀但在干预点分叉
- **训练策略**: 两阶段训练——(1) 在干预偏好数据上进行 partial DPO + 辅助 SFT loss；(2) 混合良性 prompt 数据缓解 over-refusal
- **实验设置**: 基于 STAR-1 的 1000 条有害 prompt + 915 条良性 prompt 构造数据；评估使用 JailbreakBench、StrongReject、WildJailbreak 三个安全基准和 AIME2024、MATH-500、GPQA-Diamond、HumanEval 四个推理基准
