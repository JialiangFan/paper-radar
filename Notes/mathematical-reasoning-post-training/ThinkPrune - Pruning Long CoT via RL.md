# ThinkPrune - Pruning Long CoT via RL

## 主题
RL-based CoT length pruning

## 背景
大语言模型（LLMs）通过 inference-time scaling 和 reinforcement learning（RL）训练出 long chain-of-thought（CoT）能力（如 DeepSeek-R1、OpenAI o1），在数学、代码等推理任务上取得显著性能提升。然而，这些 long-CoT LLMs 在推理时产生大量冗余、低效的思考步骤——例如在 MATH500 上 DeepSeek-R1-Distill-Qwen-1.5B 平均生成超过 15,000 个 token，而许多问题不足 1,000 个 token 就能解决。现有的 budget-forcing 方法通过强制 early exit 来限制生成长度，但这种方式并未让模型真正学会压缩推理，导致在低 budget 下性能大幅下降。

## 现有局限与研究问题
- **Limitation:** 现有 budget-forcing 方法（如 S1）在 token budget 耗尽时强制截断推理过程并直接输出答案，模型未能自适应地压缩推理链，导致在紧张 budget 下性能严重下降，且 length-performance tradeoff 远未达到最优。
- **Problem:** 能否通过 fine-tuning 让 long-CoT LLM 主动剪枝其推理长度，同时将性能损失最小化？剪枝后 length-performance tradeoff 如何？推理链中哪些步骤最容易被剪掉？

## 贡献
- 提出 ThinkPrune，一种简单有效的基于 RL 的 CoT 长度剪枝方法，无需修改 reward function，仅通过在训练时加入 length clipping 约束实现长度压缩
- 提出 iterative length pruning 策略，通过多轮逐渐收紧 token limit 的 RL 训练，相比 one-shot 剪枝更好地保持模型性能
- 在 DeepSeek-R1-Distill-Qwen-1.5B 上将平均生成长度从 10,355 压缩至 3,574 tokens，平均精度几乎不变甚至略有提升；在 AIME 数据集上长度减半仅损失 2% 性能
- 对推理行为变化的深入分析：剪枝后模型减少了犹豫/自我修正步骤（"Wait", "But wait", "Alternatively"），同时保留了核心计算推理步骤，推理可读性（perplexity）几乎不变

## 方法论
- **RL with Length Clipping:** 采用与 DeepSeek-R1 相同的 GRPO 训练框架，唯一修改是在 reward 计算前将模型输出截断至长度上限 L。截断后若无法提取正确答案则 reward 为 0，迫使模型在 L tokens 内完成推理和作答。训练时同时在 system prompt 中明确告知模型 token 上限。
- **Iterative Length Pruning:** 设定目标长度 L*，从较宽松的 L1 开始，依次收紧至 L2 > ... > L*，每轮在上一轮最优 checkpoint 基础上继续 RL 训练。每轮以 AIME22/23 为验证集，选取满足"相对精度下降不超过 10%"条件中平均输出长度最短的 checkpoint 作为下一轮起点。
- **实验设置:** 使用 AIME-AMC 历史题目共 2470 条训练数据；评估模型包括 DeepSeek-R1-Distill-Qwen-1.5B（unsaturated）、DeepScaleR-1.5B-Preview（saturated）、QwQ-32B（saturated）；评估集包括 MATH-500、AIME24、AMC23、OlympiadBench；使用 Verl RL 框架，batch size 128，每题 16 rollouts。
- **推理行为分析:** 通过统计关键词频率（"Wait", "double-check", "Therefore" 等）和用 GPT-4o 对推理链进行问题解决阶段分割，定量分析剪枝前后推理行为的变化。
