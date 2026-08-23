# STaR - Bootstrapping Reasoning With Reasoning

## 主题
Self-Taught Reasoning via Bootstrapping

## 背景
近年来研究表明，生成显式的 chain-of-thought rationale 可以显著提升 LLM 在数学推理、常识问答等复杂任务上的表现。然而，诱导模型生成 rationale 的两种主流方法各有缺陷：构建大规模 rationale 数据集需要昂贵的人工标注或依赖受限的模板方法，而 few-shot prompting 虽无需标注数据，但其性能远低于在大数据集上 fine-tune 直接预测答案的模型。因此，如何以低成本、可扩展的方式让模型习得高质量的推理能力，是一个亟待解决的问题。

## 现有局限与研究问题
- **Limitation:** 构建 rationale 数据集依赖大量人工标注，成本高昂且难以扩展；few-shot prompting 生成 rationale 的准确率显著低于在完整数据集上 fine-tune 的模型，二者之间存在难以弥合的性能差距。
- **Problem:** 如何仅从少量 rationale 示例出发，通过迭代式自我学习，让模型自动生成并利用高质量 rationale 来持续提升自身推理能力？

## 贡献
- 提出 STaR（Self-Taught Reasoner），一种 bootstrapping 机制，从少量 few-shot rationale 示例迭代生成大规模 rationale 数据集，无需人工验证新 rationale 的正确性。
- 引入 rationalization 技术：对模型未能正确回答的问题，提供正确答案作为 hint，让模型反向生成 rationale，从而突破纯 rationale generation 的学习瓶颈，加速 bootstrapping 过程。
- 在 arithmetic、CommonsenseQA 和 GSM8K 三个领域进行了系统评估与消融实验，证明 STaR 显著优于直接 fine-tune 预测答案的 baseline，且 6B 参数模型可达到 30x 更大模型的 few-shot 水平。
- 首次提出让 pre-trained LLM 通过迭代利用自身语言建模能力来自我提升推理的技术。

## 方法论
- **Rationale Generation Bootstrapping：** 给定预训练模型 M 和带答案的数据集，使用少量 few-shot rationale 示例 prompt 模型，为每个问题生成 rationale 和答案；仅保留最终答案正确的 rationale，在此过滤后的数据集上 fine-tune 原始模型 M；用新模型重复此过程，迭代直至性能饱和。
- **Rationalization：** 对于模型 rationale generation 失败（答案错误）的问题，将正确答案作为 hint 加入 prompt，引导模型在已知答案的条件下反向生成合理的 rationale；将 rationalization 生成的 rationale（去除 hint）与正常生成的 rationale 合并，共同用于 fine-tuning。
- **理论联系：** STaR 可视为 RL-style policy gradient 的近似——以答案正确性作为 reward，通过 greedy decoding 近似采样、过滤错误 rationale 近似 REINFORCE 梯度估计；rationalization 则相当于从 hint-augmented 分布 p(r|x,y) 进行 off-policy 采样，提供更高效的搜索空间。
- **训练细节：** 使用 GPT-J（6B）作为 base model，每次迭代从原始预训练模型重新训练（避免过拟合），逐步增加 fine-tuning 步数（每轮增加 20%）。

> **Title:** STaR: Self-Taught Reasoner — Bootstrapping Reasoning With Reasoning
> **Authors:** Eric Zelikman, Yuhuai Wu, Jesse Mu, Noah D. Goodman
> **Venue:** arXiv:2203.14465
> **Year:** 2022
> **Affiliations:** Stanford University, Google Research