# TokenSkip - Controllable CoT Compression

## 主题 / Topic
Controllable CoT compression — 通过 token skipping 实现可控的 Chain-of-Thought 压缩，在保持推理性能的同时降低 CoT token 消耗。

## 背景 / Background
Chain-of-Thought (CoT) prompting 已被证明能有效提升 LLM 在复杂推理任务中的表现。OpenAI o1 和 DeepSeek-R1 等前沿模型进一步表明，扩展推理时的 CoT 序列长度可以持续改善推理性能。然而，由于 LLM 解码的自回归特性，更长的 CoT 输出会导致推理延迟和 key-value cache 内存占用成比例增加；attention 层的二次方计算复杂度进一步加剧了这一负担。当 CoT 序列超过 10,000 tokens 时，计算开销和响应时间的问题尤为突出，严重影响用户体验。

## 现有局限与研究问题 / Limitations & Research Problem
**核心研究问题**："CoT 输出中的每个 token 对最终答案的贡献是否相同？"

**现有方法的局限**：
- **Token-efficient prompts**（如 BeConcise、OnlyNumbers、AbbreWords）：实际压缩率仅达 0.94–0.97，几乎没有效率提升。
- **Length-control prompts**（LC-Prompt）：即使目标设为 0.5，实际压缩率也超过 0.89，无法达到指定比例。
- **Truncation（暴力截断）**：虽然能达到指定压缩比，但推理性能严重下降——在压缩率 0.5 时，GSM8K 准确率下降 79%，MATH-500 下降 21%。
- 现有 token 重要性度量（如 Selective Context）存在位置依赖问题，单向 attention 机制无法全面捕捉 token 的重要性信息。
- 先前研究表明，跳过推理步骤可能与 test-time scaling 相冲突，损害推理性能。

**关键发现**：CoT 输出中 token 的语义重要性存在显著差异。数学公式和关键数值对最终答案贡献更大，而 "so"、"since" 等语义连接词贡献较小。LLM 具备从压缩 CoT 中恢复完整推理过程的能力（CoT Recovery）。

## 贡献 / Contributions
1. **首次探索通过 token skipping 提升 CoT 效率**，基于 LLM CoT 轨迹中 token 语义重要性差异这一发现。
2. **提出 TokenSkip**：一种简单有效的方法，使 LLM 能够跳过 CoT 中的冗余 token，学习关键推理 token 之间的捷径，支持可调压缩比的 CoT 压缩。
3. **实验验证**：在 Qwen2.5-14B-Instruct 上，TokenSkip 在 GSM8K 上将推理 token 减少 40%（313 → 181），性能下降不超过 0.4%；在 MATH-500 上，LLaMA-3.1-8B-Instruct 减少 30% token，性能下降不超过 4%，推理速度提升 1.4×。
4. 训练成本低：仅微调模型 0.2% 的参数（LoRA），训练数据规模与原始训练集相当（GSM8K 7,473 条，MATH 7,500 条），7B 模型约 2 小时，14B 模型约 2.5 小时（双 3090 GPU）。
5. 验证了 TokenSkip 在数学领域外的泛化能力（CommonsenseQA、MMLU-STEM），在 50% token 压缩下无性能损失。

## 方法论 / Methodology

### 核心思路
TokenSkip 的核心洞察：**CoT 中每个推理 token 对推导答案的贡献不同**。通过裁剪低重要性 token 并用压缩 CoT 微调模型，使 LLM 在推理时自动跳过冗余 token。

### Token 重要性度量
采用 **LLMLingua-2**（双向 BERT-like LM）衡量每个 token 的重要性，定义为：

$$I_2(x_i) = P(x_i \mid \boldsymbol{x}_{\leq n}; \boldsymbol{\theta}_{\mathcal{M}_B})$$

即给定完整上下文时，双向语言模型对该 token 的预测概率。相比单向 LM 的 perplexity 度量，双向 attention 避免了位置依赖偏差。

### 三阶段流程

**阶段一：Token Pruning（Token 剪枝）**
- 给定目标 LLM $\mathcal{M}$ 的 CoT 轨迹 $\boldsymbol{c} = \{c_i\}_{i=1}^m$ 和压缩率 $\gamma \in [0,1]$
- 计算每个 CoT token 的重要性 $\{I(c_i)\}_{i=1}^m$，按降序排列
- 以 $\gamma$-分位数 $I_\gamma = Q_\gamma(I(c_1), \ldots, I(c_m))$ 为剪枝阈值
- 保留重要性 $\geq I_\gamma$ 的 token，生成压缩 CoT $\tilde{\boldsymbol{c}} = \{c_i \mid I(c_i) \geq I_\gamma\}$

**阶段二：Training（监督微调）**
- 构建训练数据集 $\mathcal{D}$：对每条 CoT 轨迹以随机采样自压缩比集合 $\{\gamma_0, \ldots, \gamma_z\}$（默认 $\{0.5, 0.6, 0.7, 0.8, 0.9, 1.0\}$）进行剪枝
- 训练样本格式：$\mathcal{Q}\ [\text{EOS}]\ \gamma\ [\text{EOS}]\ \tilde{\boldsymbol{c}}\ \boldsymbol{a}$，将压缩率 $\gamma$ 插入问题后
- 过滤掉答案错误的轨迹以保证数据质量；保留部分原始 CoT 轨迹（$\gamma=1$）以维持推理能力
- 使用 LoRA 进行参数高效微调，最小化压缩 CoT 和答案序列的负对数似然

**阶段三：Inference（推理）**
- 输入格式与训练一致：$\mathcal{Q}\ [\text{EOS}]\ \gamma\ [\text{EOS}]$
- 用户通过指定 $\gamma$ 值（$\gamma \in \{\gamma_0, \ldots, \gamma_z\}$）控制压缩程度
- 模型自回归生成压缩 CoT 和答案，自动跳过低重要性 token 并在关键推理 token 间学习捷径

### 关键实验发现
- **压缩率遵从性**：TokenSkip 的实际压缩率与指定值高度吻合，而 More Ratio 变体在低压缩率（0.3、0.4）下遵从性显著下降
- **Token 重要性分布**：被跳过的 token 重要性分布偏向低值，保留的 token 偏向高值，验证了模型确实学会了丢弃低重要性 token
- **重要性度量对比**：使用 LLMLingua-2 的 TokenSkip 优于 Selective Context，GPT-4o 作为上界表明更好的重要性度量可进一步提升性能
- **长度预算实验**：在相同长度预算下，TokenSkip（$\gamma=0.7$–$0.9$）超越原始 LLM，绝对性能提升 1.3–2.6 个百分点，说明压缩 CoT 格式能更高效地利用推理 token

### 局限性
- 未在更大规模模型（Qwen2.5-32B/72B）上实验，受计算资源限制
- LLMLingua-2 未专门针对数学数据训练，对数值 token 和数学表达式的处理可能不够优化
- 未在长 CoT 模型（如 QwQ-32B-Preview）上测试
