# Motion Planning for Automata-based Objectives using Efficient Gradient-based Methods

- **Title:** Motion Planning for Automata-based Objectives using Efficient Gradient-based Methods
- **Authors:** Anand Balakrishnan, Merve Atasever, Jyotirmoy V. Deshmukh
- **Venue:** IROS 2024 (IEEE/RSJ International Conference on Intelligent Robots and Systems)
- **Year:** 2024
- **Affiliations:** University of Southern California


## 主题
将符号自动机编码为矩阵算子（automaton matrix operator），利用矩阵半环代数实现自动微分，从而用梯度方法高效求解基于自动机目标的运动规划问题

## 背景
运动规划中使用时序逻辑（如STL、LTL）描述复杂任务规约（如按顺序到达区域、避开障碍）。现有两大类方法：(1) 基于自动机的方法，将规约编译为自动机并分解为子问题，但面临自动机状态爆炸；(2) 基于优化的方法，直接优化STL鲁棒度，但需要存储完整信号历史，且min/max导致梯度消失。

## 现有局限与研究问题
- **Limitation:** 基于STL鲁棒度的梯度方法需要存储完整轨迹历史，无法扩展到长时间窗口任务；MILP方法对非线性系统和长horizon不可行；自动机方法和优化方法分属两个阵营，互不兼容。
- **Problem:** 如何统一自动机的结构化分解优势和梯度优化的高效性，同时避免对完整信号历史的依赖？

## 贡献
- 定义 **automaton matrix operator** A(x)：将符号自动机的转移函数编码为矩阵半环上的矩阵运算，每个输入状态 x 映射为一个 |Q|×|Q| 的权重转移矩阵
- 轨迹的自动机权重表示为矩阵连乘：w_A(ξ) = α^T A(x₀) A(x₁) ... A(x_l) β，天然支持自动微分框架（PyTorch）的反向传播
- 提出使用 (max, +) 半环（tropical semiring）替代 (min, max) 半环，缓解梯度消失问题
- 支持开环规划（直接优化控制序列）和闭环MPC（receding horizon），自动机状态通过 memoization 高效传递
- 在三个场景上验证：reach-avoid、顺序到达、自适应巡航控制（ACC）

## 方法论
- **矩阵半环编码：** 对符号自动机 A = (Σ, Q, Q₀, Q_F, Δ)，定义矩阵算子 A(x)_{ij} = λ(x, Δ(qᵢ, qⱼ))，其中 λ 是将布尔谓词映射到半环值的广义权重函数。整条轨迹的接受度通过矩阵连乘计算，利用半环代数的结合律实现高效计算
- **两种半环对比：**
  - (min, max) 半环：语义上等价于布尔接受，但min操作在梯度优化中易陷入局部最优
  - (max, +) 半环（tropical）：用加法替代min，梯度性质更好，实验中收敛速度快约10倍
- **开环规划（Algorithm 1）：** 给定初始状态，直接用梯度上升优化控制序列 u，目标为最大化 w_A(ξ)
- **闭环MPC（Algorithm 2）：** 每步用开环规划求解短horizon最优控制，执行第一步后更新自动机状态 q_t（通过 memoization），避免重新计算完整历史
- **关键优势：** 自动机结构天然编码了任务历史（哪些子目标已完成），无需像STL方法那样存储完整信号历史。这使得长horizon闭环控制成为可能——STLCG和MILP方法在此类任务上不可行
- **评估：** 与STLCG（STL计算图）和MILP方法对比。(max,+)自动机在开环中迭代次数比STLCG少10-15倍；在闭环中，只有自动机方法能处理长horizon顺序任务（STLCG/MILP无法编码）

## 关键洞察
- 自动机的状态本身就是对"任务进展"的压缩表示，不需要像STL那样回溯完整历史来判断规约满足情况
- 矩阵连乘的形式天然兼容自动微分框架，无需任何特殊的可微化处理
- (max, +) tropical semiring 在优化景观上优于 (min, max)，因为加法操作保留了所有输入的梯度贡献，而min/max只传播极值方向的梯度
