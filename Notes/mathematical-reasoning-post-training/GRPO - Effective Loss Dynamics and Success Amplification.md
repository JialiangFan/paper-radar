# GRPO - Effective Loss, Dynamics, and Success Amplification

## 主题
GRPO Loss Dynamics Analysis

## 背景
Group Relative Policy Optimization (GRPO) 由 DeepSeekMath 提出，通过 Monte Carlo rollouts 估计 advantage 并对 reward 进行 mean+variance whitening，取代了 PPO 中需要单独训练 critic 网络的做法。GRPO 在 DeepSeek-R1 等模型中被广泛用于以 verifiable binary rewards 训练 LLM 的数学推理与代码生成能力。本文从理论角度解析 GRPO 在 binary verifiable rewards 下的 effective loss 结构、策略迭代动力学及 probability of success (PoS) 的收敛行为。

## 现有局限与研究问题
- **Limitation:** GRPO 的 reward whitening 机制在 binary reward 场景下的实际优化效果缺乏理论刻画；不同 KL regularization 方式（reference-only vs. mirror descent vs. two-KL）和 normalization 方式（mean+var vs. mean-only）对 PoS 动力学的影响尚不明确。
- **Problem:** GRPO 是否等价于某种 contrastive loss？其迭代过程中 PoS 如何演化，是否收敛到不动点，且该不动点是否高于初始 reference policy 的成功率（即是否实现 success amplification）？

## 贡献
- 证明 GRPO 在 calibrated binary reward 下等价于一个 adaptive weighted contrastive loss，权重由旧策略的 PoS 决定：低 PoS 时加大对正确样本的激励，高 PoS 时加大对错误样本的惩罚。
- 对多种 GRPO 变体（no-clip GRPO、Mirror GRPO、Dr. GRPO、two-KL mixed）推导出最优策略的 closed-form recursion，表明 PoS 的 logit 按简洁的递推关系演化。
- 证明 PoS 序列收敛到不动点 p*，且在 0 < p_ref < 1 条件下 p* > p_ref，即 GRPO 实现 success amplification；Mirror GRPO (alpha=0) 进一步保证 PoS 单调递增并全局收敛到 1。
- 在 GSM8K + Qwen2.5-0.5B 上实验验证理论预测：reference policy 平均成功率从 21% 提升至 37.5%，PoS 轨迹与 fixed-point iteration 预测吻合。

## 方法论
- **Reward calibration 分析：** 在 binary reward r(q,o) in {0,1} 下，将 GRPO 的 advantage whitening 展开为关于旧策略 PoS p(q) 的显式校准函数，正确答案获得正的 calibrated reward（稀有成功获得更多 credit），错误答案获得负的 calibrated reward（高 PoS 时惩罚更重）。
- **Contrastive loss 等价：** 将 calibrated reward 代入 GRPO 目标函数，证明其等价于以 sqrt((1-p)/p) 和 sqrt(p/(1-p)) 为权重的 contrastive loss，正项鼓励对正确样本提高似然比，负项抑制对错误样本的似然比。
- **最优策略闭式解：** 在概率空间上对 GRPO 目标取最大化，利用凸优化一阶条件得到最优策略 pi_n(o|q) 正比于 pi_ref(o|q) * exp(calibrated reward / beta)。
- **PoS 不动点迭代：** 由最优策略递推得到 PoS 递推 p_n(q) = h(p_{n-1}(q))，其中 h 为 sigmoid 函数复合 logit 与权重函数的映射。利用 Brouwer 不动点定理证明不动点存在，利用导数条件和 Banach 不动点定理分析局部收敛与稳定性。
- **变体对比：** 系统比较六种 GRPO 变体的 PoS 递推与不动点性质（见 Table 1），揭示 mean+var normalization 等价于 mean-only normalization 加 adaptive effective beta。
- **Stabilized GRPO：** 引入 smoothing factor epsilon 避免 p(q)=0 或 1 时方差为零导致的数值不稳定。
- **实验验证：** 在 GSM8K 上用 Qwen2.5-0.5B-Instruct 作为 reference policy，使用 TRL 框架训练，跟踪不同 prompt 上的 PoS 轨迹，验证 fixed-point iteration 行为和 success amplification。

> **Title:** Reinforcement Learning with Verifiable Rewards: GRPO's Effective Loss, Dynamics, and Success Amplification
> **Authors:** Youssef Mroueh
> **Venue:** arXiv:2503.06639
> **Year:** 2025
> **Affiliations:** IBM Research