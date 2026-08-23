# Task-Level ILC ↔ icrl-attack：对偶联系与可迁移思路

连接两篇工作：
- [[Task-Level ILC - Dynamic Rope Manipulation]]（CMU, Suresh & Atkeson, arXiv:2602.21302）—— 动态绳索操作的 Task-Level Iterative Learning Control。
- **icrl-attack**（我的 ICLR 2026 投稿：*Vulnerability Analysis of Safe RL via Inverse Constrained RL*）—— 用 ICRL 从专家示范反推安全约束+learner policy，生成对抗攻击诱发 Safe RL 安全违规；无需策略梯度/ground-truth 约束，并给出扰动界估计最优攻击强度。

## 一句话
两者表面隔行（机器人控制 vs Safe RL 攻击），底层是**对偶**：都属于"从示范反推隐藏结构"的 inverse 范式，方向相反（一个让任务成功、一个让任务失败）但结构相同。

## 4 个对偶接触点

1. **从示范反推隐藏结构的 inverse 问题。**
   ILC 用逆模型 M⁻¹（QP）从"任务误差"反推"命令修正"；ICRL 从专家示范反推"隐藏安全约束 + policy"。同一范式，一个反推 dynamics，一个反推 constraint。

2. **critical point ↔ 攻击的关键时刻（最有迁移价值）。**
   ILC 核心洞察："误差/修正应集中在少数临界时刻而非均摊"，实验证明均匀加权会失败。这几乎为 icrl-attack 的 **stealth** 量身定做：把有限扰动预算只砸在最容易触发 cost 违规的 critical states 上，其余时刻不动 → 更隐蔽、budget 更省。可直接做成一个 attack-strength 分配策略或消融。

3. **都刻意避开梯度、走 few-shot。**
   icrl-attack 强调无需策略内部梯度；ILC 也只要逆模型给出的梯度方向大致对就能迭代收敛。**算法迁移**：把当前"一次性生成扰动"升级为 **ILC 式迭代攻击**——每次 rollout 观测 cost 误差，用近似逆模型映射回扰动更新，few-query 内逼近最优攻击。

4. **理论 bound 对偶。**
   icrl-attack 的界回答"多小扰动足以违规"；ILC 的收敛/发散分析（尤其 high-frequency error amplification 导致 divergence）可为"迭代攻击是否稳定收敛"提供现成工具。

## 诚实的边界（别硬套）
- ILC 是 model-based，假设 repeatable dynamics + fixed goal，优化方向是让任务**成功**；icrl-attack 场景是对抗、非重复、要让任务**失败**。
- 所以 ILC 的收敛保证**不能照搬**。但"方向相反、结构相同"恰恰是 related work 里值得点出的对偶关系。

## 一条可落地想法：critical-point-focused iterative attack
1. 用 ICRL 学到的 cost 当 critical-point 选择准则（cost 上升最快的时刻 = critical point）。
2. 只在这些 critical points 施加扰动 → 提升 stealth。
3. 用 ILC 式逆更新迭代放大该点 cost 误差 → few-query、无梯度攻击。

正好扣住 ICLR 论文自称的三个 challenge：无梯度、真实违规（非仅降 reward）、attack strength/stealth。
