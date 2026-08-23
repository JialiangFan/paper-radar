# RLVR Implicitly Incentivizes Correct Reasoning

## 主题
RLVR Incentivizes Correct LLM Reasoning

## 背景
DeepSeek-R1 的成功引发了学界对 Reinforcement Learning with Verifiable Rewards (RLVR) 的广泛关注，该范式通过 GRPO 算法让 LLM 基于 answer correctness 的二元反馈进行 free exploration，从而提升 chain-of-thought (CoT) 推理能力。然而，社区对 RLVR 是否真正增强了推理能力存在争议：一种流行假说认为所有正确推理路径已存在于 base model 中，RLVR 仅提升了 sampling efficiency 而非扩展 reasoning capacity。本文系统性地回应了这一争论，论证 RLVR 能隐式地激励正确推理。

## 现有局限与研究问题
- **Limitation:** 先前研究发现 post-RLVR 模型的 Pass@1 提升但 Pass@K 未超越 base model，由此推断 RLVR 不扩展推理能力边界；但 Pass@K 指标本身存在缺陷，base LLM 可能通过错误 CoT 碰巧猜中答案（spurious guesses），导致该指标高估 base model 的推理能力。
- **Problem:** 是否应将"RLVR 仅提升采样效率"视为根本性结论，还是应重新审视与之矛盾的实验发现？RLVR 究竟能否从理论和实证层面真正扩展 base LLM 的推理能力边界？

## 贡献
- 提出 CoT-Pass@K 指标，同时验证最终答案和中间推理步骤的正确性，揭示 RLVR 在数学和代码任务上均扩展了 reasoning capability boundary。
- 建立理论框架（Theorem 1），基于 Logic Prior 假设证明 GRPO 梯度隐式地增加正确 CoT 的生成概率、降低错误 CoT 的概率，即使 reward 仅基于 answer correctness。
- 分析 RLVR 训练动态，发现模型从训练早期即开始激励正确推理，P(CC|CA) 持续提升，且该能力可泛化至未见测试集。
- 通过 SFT 实验验证 RLVR 生成的 CoT 质量持续改善，SFT 在 RLVR CoT 数据上可近似复现 post-RLVR 模型的泛化性能。

## 方法论
- **CoT-Pass@K 指标设计：** 采用 LLM-as-a-CoT-Judge 范式（DeepSeek-R1-0528-Qwen3-8B 作为 verifier），对每条 CoT 进行多次独立验证，使用 any-correct、all-correct、majority-correct 三种聚合策略以降低 false positive/negative。
- **理论分析：** 引入 Logic Prior 假设——正确 CoT 比错误 CoT 具有更高的导致正确答案的概率（α > β），在此条件下证明 GRPO advantage 对正确 CoT 期望为正、对错误 CoT 期望为负，从而 policy gradient 单调递增正确 CoT 的生成概率。
- **实证验证：** 基于 DAPO（Qwen2.5-32B base, 17k 数学训练集）复现 GRPO 训练，在 AIME 2024/2025、MATH-500、AMC23、Minerva 等数学 benchmark 及 LiveCodeBench 多版本代码 benchmark 上评估 Pass@K 与 CoT-Pass@K。
- **训练动态分析：** 追踪训练过程中 P(CA) 和 P(CC|CA) 的演化，验证正确推理从早期即被激励，并观察泛化到测试集的趋势。
- **CoT 质量评估：** 在相同 base model 上以不同训练阶段的 RLVR CoT 数据进行 SFT，通过 post-SFT 模型在测试集上的 Pass@1 和 CoT-Pass@K 表现间接衡量 CoT 数据质量。

> **Title:** Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs
> **Authors:** Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye, Zhirong Wu, Yang Wang, Zhijian Xu, Xiao Liang, Junjie Li, Ziming Miao, Jiang Bian, Mao Yang
> **Venue:** arXiv:2506.14245
> **Year:** 2025
> **Affiliations:** Microsoft Research Asia, Peking University, CUHK, UCLA