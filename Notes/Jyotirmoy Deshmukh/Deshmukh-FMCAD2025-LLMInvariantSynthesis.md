# Guiding Likely Invariant Synthesis on Distributed Systems with Large Language Models

- **Title:** Guiding Likely Invariant Synthesis on Distributed Systems with Large Language Models
- **Authors:** Jyotirmoy V. Deshmukh et al.
- **Venue:** FMCAD 2025 (Formal Methods in Computer-Aided Design)
- **Year:** 2025
- **Affiliations:** University of Southern California


## 主题
利用LLM引导分布式系统的可能不变量合成，实现协作式neuro-symbolic不变量发现

## 背景
分布式系统的正确性验证依赖于发现系统不变量（invariant），但手工编写不变量需要深厚的专业知识。自动化不变量合成是形式化验证的核心挑战之一。传统方法基于模板或数据驱动，但在分布式系统中面临谓词空间爆炸问题。

## 现有局限与研究问题
- **Limitation:** 传统模板方法需要预定义谓词模板，覆盖范围有限；纯数据驱动方法可能生成不够紧凑或不安全的不变量；直接使用LLM（如GPT-o3）端到端生成不变量质量不稳定。
- **Problem:** 如何结构化地利用LLM的语义理解能力来辅助不变量合成，同时保持形式化验证的严谨性？

## 贡献
- 提出PSyn系统，将LLM作为"谓词提示器"（predicate prompter）集成到不变量合成循环中
- LLM负责建议原子谓词，形式化验证工具负责检查和精化，实现neuro-symbolic协作
- 显著优于GPT-o3等纯LLM基线方法
- 在soundness、tightness和safety三个关键指标上全面提升不变量质量

## 方法论
- **协作架构：** LLM不直接生成最终不变量，而是在迭代循环中建议候选原子谓词；形式化验证器检查这些谓词的有效性，并通过反例引导LLM精化建议
- **反例引导精化：** 当候选不变量不满足要求时，系统生成反例反馈给LLM，引导其调整谓词建议。这种迭代过程逐步收敛到高质量不变量
- **Chain-of-Thought提示：** 实验表明，链式思维提示比few-shot学习更有效地引导LLM理解不变量合成的语义需求
- **评估：** 在多个分布式系统协议上评估，PSyn在soundness（不变量为真）、tightness（不变量足够强）和safety（可推导安全属性）三个维度上均优于基线
