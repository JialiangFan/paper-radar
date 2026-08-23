# Revel: NS-RL with Formally Verified Exploration

## 主题
Verified Safe RL Exploration

## 背景
Safe exploration 是 reinforcement learning 中的核心难题：在自动驾驶、机器人等安全关键应用中，即使极小概率的 unsafe action 也可能导致严重后果，因此需要在 worst-case inputs 下保证 agent 行为安全。现有 safe RL 方法（如 Constrained Policy Optimization）多基于概率性安全约束，无法提供形式化的 worst-case guarantee；而基于 formal verification 的 shielding 方法虽能提供可证明安全性，但仅适用于 finite action space，且使用固定不变的 static shield，在 continuous control 场景下过度保守、限制学习性能。此外，在 learning loop 内反复对 neural network 进行 formal verification 的计算成本极高，难以实际应用。

## 现有局限与研究问题
- **Limitation 1:** 基于概率约束的 safe RL 方法（如 CPO）无法保证 worst-case safety，在训练过程中仍然频繁违反安全约束。
- **Limitation 2:** 已有 verified exploration 方法依赖预先构造的 static shield，不随学习过程更新，在 continuous state/action space 中表现保守且次优。
- **Limitation 3:** 在 learning loop 中直接对 neural network policy 进行 formal verification 在计算上不可行（单个网络的验证即可能耗时数十分钟）。
- **Problem:** 如何设计一个支持 continuous state/action space、兼容 deep policy gradient 方法、且保证每一个中间 policy 在 worst-case 下都可证明安全的 RL 框架？

## 贡献
- 提出 REVEL (Reinforcement learning with verified exploration) 框架，首次实现在 continuous state/action space 中使用 deep policy representation 和 policy gradient 方法的同时保证 formally verified safe exploration。
- 设计 neurosymbolic policy 表示：policy $h(s) = \text{if } (P^\#(s, f(s)) \subseteq \phi) \text{ then } f(s) \text{ else } g(s)$，其中 $f$ 为 neural network（正常模式），$g$ 为 piecewise linear symbolic shield，$\phi$ 为 inductive invariant 构成的 safety monitor。Shield 和 monitor 以可高效验证的 symbolic 形式表达，避免对 neural network 的直接验证。
- 提出基于 functional mirror descent 的学习算法，包含三步迭代：(i) Lift -- 将 symbolic shield 提升至 neurosymbolic 空间；(ii) Update -- 在 neural policy space 中执行 approximate policy gradient；(iii) Project -- 通过 imitation learning 将更新后的 policy 投影回 safe symbolic shield 空间。整个过程无需 neural network verification。
- 提供理论分析，证明在合理假设下 REVEL 的 regret bound 为 $O(\sigma\sqrt{1/T} + \epsilon + \beta + L_J\zeta)$，其中 shield 介入频率 $\zeta$ 越低则 regret 越小。
- 在 10 个 continuous control benchmark 上实验验证：REVEL 在 8/10 任务中实现零安全违规（DDPG 和 CPO 均有大量违规），同时在 7/10 任务中性能与 DDPG 相当或更优，并显著优于 static shielding 方法。

## 方法论
- **Neurosymbolic Policy 表示：** 定义两个 policy class -- symbolic class $\mathcal{G}$（piecewise linear policy，可高效验证）和 neurosymbolic class $\mathcal{H} \supseteq \mathcal{G}$（形如 $(g, \phi, f)$ 的 blended policy）。Safety monitor $P^\#(s, f(s)) \subseteq \phi$ 检查 neural action 是否保持系统在 inductive invariant $\phi$ 内；若通过则执行 neural action $f(s)$，否则回退至 verified shield $g(s)$。
- **Formal Verification via Abstract Interpretation：** 使用 abstract interpretation 构造 inductive invariant $\phi$（一组 hyperinterval 形式的 abstract state），证明在 worst-case dynamics $P^\#$ 下系统不会到达 unsafe states $S_U$。验证仅针对 symbolic shield $g$，完全避免对 neural network 的验证。
- **Lift 步骤：** 将当前 shield $g_t$ 及其 invariant $\phi_t$ 提升为 neurosymbolic policy $(g_t, \phi_t, g_t)$，neural component 初始化为通过 DAgger 模仿 $g_t$ 训练的网络。此步骤天然安全，因为安全性仅依赖 $g$ 和 $\phi$。
- **Update 步骤：** 对 neurosymbolic policy $(g, \phi, f)$ 执行 policy gradient 更新，仅修改 neural component $f$（$g$ 和 $\phi$ 保持不变），产生新 policy $(g, \phi, f - \eta\nabla_\mathcal{F}J(h))$。由于 shield 和 monitor 不变，更新后 policy 仍可证明安全。
- **Project 步骤（Algorithm 2）：** 通过 cutting plane 方法迭代细化 shield：每次选取一个 region 并分裂，用 IMITATESAFELY 子程序在每个子区域内通过 constrained projected gradient descent 合成新的 safe linear policy，使其模仿 neurosymbolic policy 的行为同时保证验证可行性。最终返回 Bregman divergence 最小的 shield 及其对应的新 invariant。
- **IMITATESAFELY 子程序：** 将安全模仿问题转化为一系列 constrained supervised learning 问题，交替执行 gradient update 和 projection（投影到 safe linear policy 参数空间的 hyperinterval 约束内），使用 abstract interpretation 验证每个 hyperinterval 内的所有 controller 均安全。
- **实验设置：** 10 个 benchmark（mountain-car, road, road-2d, noisy-road, noisy-road-2d, obstacle, obstacle2, pendulum, acc, car-racing），对比 DDPG、CPO、static shielding 三个 baseline。REVEL 在所有 benchmark 上实现零训练安全违规，性能在多数任务上与无安全约束的 DDPG 相当，训练时间中 shield synthesis 占约 87%。
