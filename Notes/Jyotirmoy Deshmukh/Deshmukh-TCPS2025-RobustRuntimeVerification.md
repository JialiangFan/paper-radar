# Distributionally Robust Predictive Runtime Verification

- **Title:** Distributionally Robust Predictive Runtime Verification under Spatio-Temporal Logic Specifications
- **Authors:** Yiqi Zhao, Emily Zhu, Bardh Hoxha, Georgios Fainekos, Jyotirmoy V. Deshmukh, Lars Lindemann
- **Venue:** ACM Transactions on Cyber-Physical Systems (TCPS), 2025
- **Year:** 2025
- **Affiliations:** University of Southern California; Toyota NA R&D


## 主题
在分布偏移条件下进行 STL 属性的鲁棒预测性运行时验证

## 背景
运行时验证（runtime verification）在系统运行过程中监控其行为是否满足形式化规约。预测性运行时验证（predictive runtime verification）更进一步，基于当前观测预测未来轨迹是否满足规约，从而在违规发生前发出预警。然而，预测模型在部署环境与训练环境存在分布偏移时可能给出错误预测。

## 现有局限与研究问题
- **Limitation:** 现有预测性运行时验证方法假设训练和部署数据来自相同分布，在分布偏移下验证保证失效；基于点估计的预测方法忽略预测不确定性；缺乏对分布偏移的量化分析和鲁棒性保证。
- **Problem:** 如何设计在分布偏移条件下仍能提供可靠保证的预测性运行时验证方法？

## 贡献
- 提出分布鲁棒（distributionally robust）的预测性运行时验证框架
- 使用 Wasserstein 距离定义分布偏移的不确定集（ambiguity set）
- 提供 STL 满足概率的鲁棒下界估计，在最坏情况分布偏移下仍有效
- 结合在线学习更新分布估计，实现自适应验证

## 方法论
- **分布鲁棒优化：** 定义 Wasserstein ambiguity set B_ε(P̂) = {P : W(P, P̂) ≤ ε}，其中 P̂ 为经验分布，ε 为允许的偏移半径。求解 inf_{P ∈ B_ε} P[ρ(φ, s) ≥ 0]，即最坏情况下的 STL 满足概率
- **鲁棒满足概率：** 利用 Wasserstein 对偶定理，将无穷维优化问题转化为有限维凸优化问题。鲁棒满足概率 = 标准满足概率 - 修正项（反映分布偏移的影响）
- **在线更新：** 随着运行时收集新数据，使用滑动窗口更新经验分布 P̂ 和偏移半径 ε 的估计。ε 的选择基于有限样本浓度不等式（concentration inequality）
- **STL 监控集成：** 将鲁棒概率估计与标准 STL 在线监控器结合，输出三值判定：满足（鲁棒概率 > 阈值）、违反（鲁棒概率 < 阈值）、未确定
- **评估：** 在自适应巡航控制和自动紧急制动系统上测试，方法在分布偏移场景中保持高验证可靠性，而标准方法出现大量误判
