# Concept Bottleneck Models

## Research Problem
How to make deep learning predictions interpretable and intervenable by routing all decisions through a human-understandable concept layer without sacrificing accuracy.

> Koh, P.W., Nguyen, T., Tang, Y.S., Mussmann, S., Pierson, E., Kim, B., & Liang, P. (2020). Concept Bottleneck Models. *Proceedings of the 37th International Conference on Machine Learning (ICML)*, PMLR 119.

## 主题
Interpretable Concept-Based Prediction Models

## 背景
当前主流的深度学习模型采用 end-to-end 架构，直接从原始输入 (如 pixels) 映射到目标输出 (如疾病严重程度)，缺乏对中间推理过程的可解释性。在医学影像 (如膝关节 X-ray 骨关节炎分级) 和细粒度图像识别 (如鸟类物种鉴定) 等高风险场景中，领域专家需要能够理解模型的推理依据，并在必要时对模型进行干预和纠正。早期基于 concept 的模型曾尝试引入人类可理解的中间表征，但在 predictive accuracy 上远落后于 end-to-end neural networks，导致 accuracy 与 interpretability 之间被认为存在不可调和的 tradeoff。

## 现有局限与研究问题
- **Limitation 1:** End-to-end 模型作为 black box，不支持基于 human-specified concepts 的解释与干预；现有 post-hoc interpretation 方法 (如 linear probes, concept activation vectors) 只能事后近似地恢复 concepts，无法实现对单个 concept 的精确干预 (intervention)。
- **Limitation 2:** 早期 concept bottleneck 方法在 predictive accuracy 上显著低于 standard end-to-end models，且缺乏系统性的 training scheme 比较和 test-time intervention 能力的探索。
- **Problem:** 是否可以构建一种模型，在保持与 end-to-end models 竞争性 task accuracy 的同时，通过 human-interpretable concept bottleneck 实现可解释性和 test-time intervention？不同训练策略对 accuracy-interpretability-intervenability 三者的影响如何？

## 贡献
- 提出 Concept Bottleneck Models (CBMs) 的系统化框架：模型结构为 $x \xrightarrow{g} c \xrightarrow{f} y$，其中 $g$ 将输入映射到 human-specified concepts $c$，$f$ 再从 concepts 预测最终 target $y$，所有预测必须经过 concept bottleneck layer。
- 系统比较了三种训练策略——**Independent** ($g$ 和 $f$ 分别独立训练)、**Sequential** (先训练 $g$，再用 predicted concepts 训练 $f$)、**Joint** (联合优化 concept loss 和 task loss，通过超参数 $\lambda$ 控制权衡)——并证明 CBMs 在 OAI (膝关节骨关节炎 X-ray) 和 CUB (鸟类识别) 两个任务上可达到与 standard end-to-end models 竞争性甚至更优的 task accuracy，同时保持高 concept accuracy。
- 首次系统研究 test-time intervention：领域专家可在推理阶段直接修改 predicted concept values $\hat{c}$，将修正传播到最终预测 $\hat{y}$，显著提升 task accuracy (如 OAI 上仅纠正 2 个 concepts 即可将 RMSE 从 >0.4 降至约 0.3)。
- 证明 CBMs 对 spurious correlations 和 covariate shifts 更具鲁棒性：在 CUB+Places background shift 实验中，bottleneck models 的 task error 显著低于 standard models (约 0.48 vs. 0.63)。
- 提供了在 well-specified linear regression setting 下的理论分析，给出 bottleneck model 相对于 standard model 的 excess error 上界条件 ($k/d$ 小且 $\sigma_Y^2 \gg \sigma_C^2$ 时 bottleneck 更优)。

## 方法论
- **模型架构:** 将任意 end-to-end neural network 改造为 CBM——调整网络某一层的维度为 concept 数量 $k$，添加 intermediate loss 使该层与 human-specified concepts 对齐。对 OAI 使用 pretrained ResNet-18 ($x \to c$) + 3-layer MLP ($c \to y$)；对 CUB 使用 Inception-v3 ($x \to c$) + single linear layer ($c \to y$)。
- **三种训练方案:**
  - *Independent:* $\hat{g}$ 和 $\hat{f}$ 分别独立优化各自的 loss；$\hat{f}$ 在训练时使用 true concepts，但测试时使用 predicted concepts。
  - *Sequential:* 先训练 $\hat{g}$，然后固定 $\hat{g}$，用其 predicted concepts 训练 $\hat{f}$。
  - *Joint:* 联合最小化 $\sum_i [L_Y(f(g(x^{(i)})); y^{(i)}) + \lambda \sum_j L_{C_j}(g_j(x^{(i)}); c_j^{(i)})]$，$\lambda$ 控制 task loss 与 concept loss 的权衡。
- **Test-time intervention:** 在推理阶段，将模型预测的 $\hat{c}_j$ 替换为专家提供的 true value $c_j$，传播至 $\hat{y}$。对 OAI (regression) 直接替换；对 CUB (classification) 通过设置 logits $\hat{\ell}_j$ 为训练分布的 5th/95th percentile 来近似干预。
- **鲁棒性评估:** 构造 CUB+Places 数据集，训练集中每个鸟类物种与特定 background category 关联，测试时 shuffle 背景，验证 CBMs 对 background spurious correlation 的抵抗能力。
- **理论分析:** 在 linear Gaussian setting 下推导 independent bottleneck model 与 standard model 的 asymptotic excess error ratio 上界为 $\frac{k/d \cdot \sigma_Y^2 + \sigma_C^2}{\sigma_Y^2 + \sigma_C^2}$。
