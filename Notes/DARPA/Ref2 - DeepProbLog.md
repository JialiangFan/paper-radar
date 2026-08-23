# DeepProbLog: 神经概率逻辑编程

## Research Problem
How to fully integrate deep neural networks with probabilistic logic programming through minimal syntactic extension (neural predicates), enabling end-to-end differentiable learning across perception, logic, and probability.

> Manhaeve, R., Dumančić, S., Kimmig, A., Demeester, T., & De Raedt, L. (2019). Neural Probabilistic Logic Programming in DeepProbLog. *arXiv:1907.08194v2*. (Extended version of NeurIPS 2018 spotlight)

## 主题
Neural Probabilistic Logic Programming

## 背景
AI 任务大致可分为需要低级感知（如图像识别）和高级推理（如逻辑演绎）两类。深度学习在感知方面表现卓越，但在推理上远不如逻辑和概率方法。概率逻辑编程（如 ProbLog）将逻辑与概率统一，而神经符号 AI 试图将神经网络与符号推理结合。然而，现有方法要么仅将逻辑作为正则化约束、要么限于非递归无环逻辑程序，未能实现神经网络、逻辑和概率三者的完全集成。DeepProbLog 提出应同时集成神经网络与两大推理框架——逻辑和概率，且纯神经、纯逻辑和纯概率方法应为其特例。

## 现有局限与研究问题
- **Limitation 1:** 现有神经符号方法（如 Neural Theorem Provers, Logic Tensor Networks）主要通过在欧几里得空间中编码逻辑项来近似逻辑推理，不支持概率推理和感知，且通常限于非递归无环逻辑程序。
- **Limitation 2:** "逻辑作为正则化"方法（如 Semantic Loss, DL2）将逻辑约束编码为损失函数的正则化项，无法直接进行逻辑推理或概率推断。
- **Limitation 3:** 神经程序归纳方法（如 ∂4, NPI, TerpreT）使用神经网络填充程序模板中的空洞，但缺乏概率语义支持，且面临长程序追踪的可扩展性问题。
- **Problem:** 如何设计一个框架，通过对 ProbLog 的最小扩展（引入神经谓词），实现神经网络与概率逻辑编程的完全集成，保留 ProbLog 的完整语义、推理和实现，同时支持端到端梯度训练？

## 贡献
- 提出 DeepProbLog，通过引入**神经标注析取（neural annotated disjunction, nAD）**和**神经事实（neural fact）**两种构造，以最小语法扩展将深度神经网络集成到概率逻辑编程语言 ProbLog 中。
- 语义完全继承 ProbLog：将 nAD 实例化为普通标注析取（用神经网络输出替换概率），保留 ProbLog 的可能世界语义和加权模型计数（WMC）推理。
- 基于**代数 ProbLog (aProbLog)**和**梯度半环（gradient semiring）**实现端到端学习：梯度半环的元素为元组 (p, ∇p)，通过算术电路（AC）上的半环运算同时计算概率和梯度，再通过链式法则将梯度传播到神经网络参数。
- 统一支持四种能力：(i) 符号与子符号表示与推理，(ii) 程序归纳（program induction），(iii) 概率逻辑编程，(iv) 深度学习从示例中学习。
- 通过 9 组实验（T1-T9）全面验证：MNIST 加法（单/多位数、带监督不足、带噪声标签）、程序归纳（Forth 加法/排序/WAP）、概率+深度学习（硬币分类、扑克牌游戏）。

## 方法论
- **语言设计：** DeepProbLog 程序由概率事实集 F、神经标注析取（nAD）集 N 和规则集 R 组成。nAD 形如 `nn(m_r, I, O, d) :: r(I, O)`，其中 `m_r` 标识神经网络模型，I 为输入变量序列，O 为输出变量，d 为输出域。接地后，nAD 通过前向传播神经网络实例化为普通标注析取。
- **推理（Inference）：** 与 ProbLog 四步推理一致——(1) 接地（backward chaining 确定相关基规则），(2) 重写为命题逻辑公式，(3) 知识编译为 SDD（Sentential Decision Diagram），(4) 转换为算术电路（AC）并计算 WMC。DeepProbLog 唯一额外步骤是在接地后用神经网络前向传播实例化 nAD 的概率。
- **学习（Learning）：** 采用 learning from entailment 设定，目标为最小化查询成功概率与期望概率之间的损失（通常为负对数似然）。关键创新在于使用**梯度半环**：半环元素为 (p, ∇p) 元组，加法 ⊕ 和乘法 ⊗ 分别对应概率求和/乘积及其梯度的链式法则传播。AC 上的半环计算同时得到 P(q) 及 ∂P(q)/∂p_i；然后通过链式法则 dL/dθ_k = (∂L/∂P(q)) · Σ_i (∂P(q)/∂p̂_i) · (∂p̂_i/∂θ_k) 将梯度从逻辑层传播至神经网络参数。AC 可缓存以避免重复编译。
- **实验设置：**
  - **T1-T4（逻辑推理+深度学习）：** MNIST 数字加法任务。T1 为单位数加法，T2 为多位数加法（复用 T1 的神经谓词），T3 为三图像约束任务（需熵正则化防止模式崩溃），T4 为带噪声标签（显式建模噪声概率）。对比基线为直接分类 19/199 种可能和的 CNN。
  - **T5-T7（程序归纳）：** 基于 differentiable Forth (∂4) 的程序框架，用神经网络填充程序空洞。T5 为 Forth 加法，T6 为冒泡排序，T7 为自然语言数学应用题。DeepProbLog 在排序任务上优于 ∂4（可扩展至更长序列）。
  - **T8-T9（概率编程+深度学习）：** T8 为硬币分类（远程监督学习潜在表示），T9 为简化扑克游戏（同时学习卡牌识别和概率参数）。
  - 实现基于 ProbLog2 + PyTorch，Adam 优化器（神经网络）+ SGD（逻辑参数）。
