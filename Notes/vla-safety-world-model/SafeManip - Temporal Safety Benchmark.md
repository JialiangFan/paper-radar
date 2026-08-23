# SafeManip - Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation

> 作者: Chengyue Huang, Khang Vo Huynh, Sebastian Elbaum, Zsolt Kira, Lu Feng (2026, arXiv 2605.12386)

## 主题

Temporal safety benchmark for manipulation

## 背景

机器人操作长期以 task success rate 为主要评价指标，但"完成任务"不等于"安全执行"。很多安全失效本质上是 **temporal（时序）** 的——比如机器人接触过生食后又去碰干净餐具、或者在物体尚未完全进入柜子时就松手——这些不是单帧的 unsafe state，而是随执行过程展开才显现的时序违规。现有 safety benchmark 大多用 task-specific hazard label、瞬时碰撞检测或累积轨迹代价来表达安全，无法说清"违反了哪条规则、何时违反、任务是安全完成还是仅仅完成"。

## 现有局限与研究问题

- **Limitation:** 现有 safety benchmark 的安全语义碎片化且不可复用。Hazard-oriented benchmark（SafeBox、ResponsibleRobotBench、IS-Bench）用自然语言或 PDDL 谓词描述电气/火灾/化学/人身风险，不覆盖 grasping、contact、release、containment 这类低层操作事件；execution-oriented benchmark（SafeLIBERO、Safety-CHORES、FailureBench、RedVLA）把安全表达为瞬时谓词、标量 cost 或 red-teaming 目标，而非可复用的时序公式；即便是最接近的 specification-driven 工作（VLA-Arena、SENTINEL），其约束也嵌在任务定义/cost block 里或停留在通用 hazard 规则层面。同时，机器人领域已有的 specification pattern 库偏 mission-level 或 mobility-oriented，缺少面向 manipulation safety 的可复用 property suite。
- **Problem:** 如何把实际操作场景中的安全关切形式化成**可复用、跨任务可实例化、可在有限轨迹上在线监控**的时序属性，并据此把 task completion 与 safe execution 拆开来度量，从而诊断当前 VLA 策略的时序安全失效？

## 贡献

- 提出 **SafeManip**：policy-agnostic 的 property-driven benchmark，由三部分构成——可复用的 LTL_f safety property templates、task-specific predicate bindings、以及把 task success 与 safe execution 分离的评价指标。
- 给出覆盖 **8 类 manipulation safety category** 的 10 条 LTL_f 属性模板：collision & contact safety、grasp stability、release stability、cross-contamination、action onset、mechanism recovery、object containment、enclosure & access。模板写在抽象命题上，可绑定具体 object/fixture/region/skill 后跨任务复用。
- 提出 **finite-trace monitoring protocol**：把 rollout 观测 grounding 成 symbolic predicate trace，在其上评估 LTL_f 属性，输出 property-level 的安全结论（而非二值安全标签或碰撞 cost）。
- 在 RoboCasa 上以 **50 个 RoboCasa365 任务 × 6 个 VLA 策略/训练变体**（π₀、π₀.₅、GR00T N1.5，以及 GR00T-pt / GR00T-to / GR00T-tpt 三个训练变体，每任务 50 rollout）做了大规模实证评估。
- 核心实证发现：**task success 会掩盖时序安全失效**。π₀.₅ 相比 π₀ 成功率从 8.1% 升到 9.3%，violation rate 却从 69.7% 升到 82.8%；大量成功 rollout 属于 success-but-unsafe；违规高度集中在 collision/contact 与 release stability 两类；violation rate 随任务 horizon（atomic → short → medium → long）单调上升，且强烈依赖 manipulation suite。
- 开源代码库（property templates、task bindings、temporal monitors、rollout 处理与评测脚本）：https://github.com/chengyuehuang511/SafeManip

## 方法论

- **规约语言：LTL_f（Linear Temporal Logic over finite traces）**。理由是 manipulation rollout 天然有限（成功/失败/到 horizon 即终止）。命题集 P 为与安全相关的布尔谓词（contact、grasp stability、fixture state、containment、contamination status 等），算子含 ∧/∨/¬ 与 ◯（Next）、U（Until）、□（Always）、◇（Eventually）。
- **属性模板设计**。例如 φ₂: □(ObjGrasped → (StableGrasp U ObjReleased)) 表达抓取稳定性；φ₄: □(Contaminated → (¬CleanContact U Sanitized)) 表达交叉污染的先后顺序约束；φ₆: □(MechHit → ◇(Retract ∧ ◇Recovered)) 表达机构受撞后的回退与恢复。模板取材于 OSHA Technical Manual 的 hazard 视角与 FDA Food Code 的卫生/污染视角，再改写成有限轨迹上可观测的形式，覆盖从每步都要成立的 invariant 到涉及 ordering / recovery / eventual satisfaction 的多步属性。
- **监控管线**。每个时间步查询 simulator 的 state variable、object pose、contact event、gripper state、fixture state 和 task-relevant action signal，计算 Contaminated、EnclosureCleared 等布尔谓词，从而把连续 rollout 转成 symbolic finite trace；每条实例化后的 LTL_f 公式编译成 **DFA**（用 LTLf2DFA），随 trace 在线更新状态，进入 rejecting state 即判定违规，并记录违规时间步、持续时长与所属 property category。
- **任务与策略设定**。RoboCasa 仿真器（提供 articulated fixtures / appliances，并暴露 simulator state 用于 grounding 谓词），50 个 RoboCasa365 任务归为 7 个 manipulation suite（Atomic & Fixture；Beverage；Bread/Breakfast/Reheating；Cooking & Ingredient Prep；Cleaning/Washing/Sanitation；Storage & Organization；Plating/Serving/Portioning）。所有策略均使用外部提供的 checkpoint，作者不做任何训练/微调，六个设定共享同一套 task suite、rollout protocol、monitor 与 metrics。
- **评价指标**。task success rate；rollout-level 与 per-property 的 safety violation rate；把 rollout 分解成 **success-and-safe / success-but-unsafe / fail-but-safe / fail-and-unsafe** 四类结局；以及 unsafe-state exposure rate（rollout 中处于违规状态的时间步占比），用于区分短暂违规与长期不安全行为。
- **探索性分析**。在 GR00T-tpt 上测试两种 safety prompt：短的保守动作提示把成功率从 43.9% 降到 26.4%、violation rate 从 71.8% 降到 69.4%；长的列举式约束提示把成功率压到 6.9%、violation rate 降到 65.1%——说明 prompt-based safety guidance 能诱导保守行为但代价高，作者将系统性 prompt 设计留作 future work。

## 与 STL×VLA 主线的关联

这篇论文把"用 temporal logic 形式化 VLA 安全"这个位置占住了一半：它确实用了形式化时序规约（LTL_f + DFA 在线监控）来评估 VLA 策略，并且证明了 task success 与 temporal safety 是两个不同维度——这为"必须做时序安全约束"提供了强有力的实证背书，可以直接作为 STL×VLA 主线的 motivation 引文。但它留下的空间也很明确：**(1) 只做 evaluation，不做 enforcement**——monitor 只在 rollout 结束或违规时给出判定，不介入策略执行，没有 runtime shielding、没有违规后的修正或重规划；作者自己在 Conclusion 里把"把 property-level safety monitoring signal 融入 safe policy training"列为 future work。**(2) 用 LTL_f 而非 STL**——命题是布尔谓词，没有实值 robustness semantics，因此拿不到可微的违规程度信号，无法直接用于梯度式约束优化或作为 RL reward shaping；STL 的 quantitative semantics 正好补上这一块。**(3) 谓词 grounding 依赖 privileged simulator state**（object pose、contact event、fixture state），作者明确承认迁移到真机需要可靠的感知、接触估计与事件检测——从感知/world model 中估计谓词或 STL 信号是一个开放接口。**(4) 属性是手工模板 + 人工 task binding**，没有从语言指令自动合成规约的环节。综合看，这篇是"STL×VLA"生态位里的 benchmark/measurement 层，把评测基础设施和 failure taxonomy 做好了，而 enforcement（runtime STL shielding）、quantitative robustness、以及 spec-aware training 三条路仍然是开放的。
