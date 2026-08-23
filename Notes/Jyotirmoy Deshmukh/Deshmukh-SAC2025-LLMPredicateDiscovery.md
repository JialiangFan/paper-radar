# LLM-guided Predicate Discovery for Formal Methods

- **Title:** LLM-guided Predicate Discovery and Data Augmentation for Learning Likely Program Invariants
- **Authors:** Yuan Xia, Aabha Shailesh Pingle, Deepayan Sur, Jyotirmoy V. Deshmukh, Mukund Raghothaman, Srivatsan Ravi
- **Venue:** SAC 2025 (40th ACM/SIGAPP Symposium on Applied Computing)
- **Year:** 2025
- **Affiliations:** University of Southern California


## 主题
利用大语言模型 (LLM) 辅助形式化方法中的谓词发现过程

## 背景
形式化验证和程序分析中，谓词发现（predicate discovery）是关键步骤——需要找到合适的谓词来构建抽象模型或归纳不变量。传统方法依赖人工设计或模板化搜索，是形式化方法自动化的主要瓶颈之一。大语言模型（LLM）展示了强大的代码理解和推理能力，可能为自动化谓词发现提供新途径。

## 现有局限与研究问题
- **Limitation:** 传统谓词发现方法（如 CEGAR）依赖反例引导的迭代精化，计算开销大且难以扩展；人工谓词设计需要深厚的领域专业知识；现有自动化方法受限于固定模板，难以发现创新性谓词。
- **Problem:** 如何利用 LLM 的语义理解能力自动发现适用于形式化验证的高质量谓词？

## 贡献
- 提出 LLM-guided predicate discovery 框架，结合 LLM 的语义推理和形式化方法的精确验证
- 设计 prompt engineering 策略，引导 LLM 生成候选谓词
- 使用形式化验证作为 LLM 输出的检验器（verifier），形成 LLM-propose + FM-verify 的闭环
- 在多个验证基准上显著减少人工干预

## 方法论
- **LLM 谓词提议：** 给定程序代码和验证目标，构造结构化 prompt 让 LLM 提出候选谓词。prompt 包含程序语义描述、目标属性、以及可选的失败反例
- **形式化验证检验：** 使用 SMT 求解器或模型检查器验证 LLM 提出的谓词是否足以证明目标属性。如果验证失败，提取反例信息
- **迭代精化：** 将验证失败的反例和已发现的有效谓词反馈给 LLM，请求生成更精确的谓词。形成 LLM → Verifier → LLM 的迭代循环
- **多 LLM 集成：** 使用多个 LLM（或同一 LLM 的多次采样）并行提议谓词，增加发现概率。对候选谓词进行去重和排序
- **评估：** 在 SV-COMP 基准和 CPS 验证案例上测试，方法在大部分案例中成功发现充分谓词，减少 80% 以上的人工谓词设计工作
