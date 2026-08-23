# ThinkPRM - Process Reward Models That Think

## 主题 / Topic
CoT-based process reward model（基于思维链的过程奖励模型）

**论文信息**
- 作者：Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng, Moontae Lee, Honglak Lee, Lu Wang
- 机构：University of Michigan, LG AI Research, University of Illinois Urbana-Champaign, Mila
- arXiv：2504.16828v5，2025年12月
- 代码：https://github.com/mukhal/thinkprm

---

## 背景 / Background

- 大语言模型（LLM）在推理任务中越来越依赖 test-time scaling，即在推理阶段投入更多计算资源来提升性能。
- Process Reward Model（PRM，过程奖励模型）是 test-time scaling 的关键组件，用于对解题方案中每个步骤进行评分，从而引导 Best-of-N selection（最优解选择）和 verifier-guided beam search（验证器引导的束搜索）。
- 传统的 discriminative PRM（判别式过程奖励模型）将验证任务视为分类问题，直接输出每一步的正确/错误得分。
- Generative verification（生成式验证）的早期工作（如 LLM-as-a-Judge、GenRM）尝试将验证视为语言生成任务，产生简短的 chain-of-thought（CoT）再作出判断。

---

## 现有局限与研究问题 / Limitations & Research Problem

**判别式 PRM 的局限：**
1. 训练需要大量的 step-level annotations（步骤级标注），成本高昂——例如 PRM800K 数据集包含约 712K 条步骤标注。
2. 不利用语言模型本身的生成能力，训练成本高且可解释性差。
3. 推理阶段使用 fixed compute（固定计算量），无法随 test-time compute 动态扩展。

**现有生成式验证方法（LLM-as-a-Judge / GenRM）的局限：**
1. 对 instruction wording（指令措辞）高度敏感，轻微改动可导致 F1 分数波动 3-4 分。
2. 产生大量 invalid judgments（无效判断）——模型输出中缺乏可提取的最终标签（如 \boxed{yes}/\boxed{no}）。
3. 存在严重的 overthinking（过度思考）和 infinite looping/repetition（无限循环/重复）问题，验证链超出 token 预算而无法终止。
4. GenRM 仅限于 short CoT，限制了其 test-time scaling 能力。
5. 通用 LLM 经常无法识别推理错误，作为验证器表现差于专用奖励模型。

**核心研究问题：**
- 如何构建数据高效（data-efficient）的 PRM，使其能够通过生成长 CoT 来进行 step-by-step 验证，同时支持 test-time compute scaling？

---

## 贡献 / Contributions

1. **提出 ThinkPRM**：一种生成式 process reward model，通过生成扩展的 verification chain-of-thought（验证思维链）来逐步验证解题方案中的每一步。
2. **极高的数据效率**：仅使用约 1% 的 PRM800K 步骤标注（约 8K 条）进行训练，却显著优于在全量数据上训练的 discriminative PRM。
3. **全面超越 baselines**：
   - 在 ProcessBench、MATH-500、AIME '24 等多个 benchmark 上超过 LLM-as-a-Judge 和 discriminative verifiers。
   - 在 out-of-domain 评估中（GPQA-Diamond、LiveCodeBench），比在完整 PRM800K 上训练的判别式验证器分别高出 8% 和 4.5%。
   - 在相同 token 预算下，比 LLM-as-a-Judge 提升 test-time scaling 效率 7.2%（在 ProcessBench 子集上）。
4. **泛化能力强**：虽然仅在数学数据上训练，但能泛化至科学推理（GPQA-Physics）和代码生成（LiveCodeBench）等 out-of-domain 任务。
5. **支持双维度 scaling**：
   - Parallel scaling：对同一验证步骤采样 K 条独立 verification CoTs，取平均分。
   - Sequential scaling：通过触发短语（如 "Let's verify again"）促使模型对初始验证进行 self-correction（自我修正）。

---

## 方法论 / Methodology

### 核心思路
将验证任务视为生成任务：给定一道题目和一个多步骤解答，模型生成一段扩展的 chain-of-thought，逐步分析每个解题步骤是否正确，最终输出每步的 \boxed{correct}/\boxed{incorrect} 标签。

### 数据收集流程（Rejection Sampling Finetuning）

**Step 1 - 采样 verification chains：**
- 使用 QwQ-32B-Preview 作为采样模型，针对 PRM800K 数据集中的每个 problem-prefix pair 生成多条 verification CoTs。
- Prompt 要求模型逐步审核解答，为每步给出 critique 并输出 \boxed{correct}/\boxed{incorrect}。

**Step 2 - 基于 process labels 的过滤（关键）：**
- 保留满足以下条件的 CoTs：
  (i) 包含可提取的步骤级决策标签（格式正确）；
  (ii) 每步的判断与 PRM800K 中的 gold process labels 一致；
  (iii) CoT 长度在最大 token 预算内（避免过度思考）。
- 约 20% 的初始样本满足条件，最终收集约 1K 条高质量 verification CoTs（对应约 8K 个步骤标注）。
- 论文通过消融实验证明，基于 process-level 过滤显著优于基于 outcome-level（最终答案对错）的过滤。

**训练数据统计（1K 数据集）：**
- 正确解答 486 条（48.6%），错误解答 514 条（51.4%）
- 步骤标注：正确步骤 7474 条（92.3%），错误步骤 625 条（7.7%）
- 验证链平均长度：1037 tokens

### 训练细节

**训练模型：**
- R1-Distill-Qwen-1.5B、R1-Distill-Qwen-7B、R1-Distill-Qwen-14B（full fine-tuning）
- QwQ-32B-Preview（LoRA fine-tuning，rank=32，α=16）

**训练方式：**
- 在过滤后的 1K 条 verification CoTs 上进行 supervised fine-tuning（监督微调）。
- 1.5B 模型训练约 30 分钟，14B 模型训练约 1.5 小时（单张 A100 80GB 或 RTX A6000 48GB GPU）。
- 特殊 token `<think>` 和 `</think>` 用于标识验证推理过程。

### 推理阶段评分

- 模型生成最多 8192 tokens 的 verification chain。
- 强制解码字符串 "Is the solution correct?"，使用 P("yes") / (P("yes") + P("no")) 作为最终解答得分。
- 针对 parallel scaling，对 K 条独立 verification CoTs 的分数取平均。
- 针对 sequential scaling，使用触发短语引导模型重新检查验证，实现 self-correction。

### LLM-as-a-Judge 的问题分析（RQ1）

实验发现，直接将推理模型用作 LLM-as-a-Judge 进行过程验证存在以下问题：
- **高无效输出率**：R1-Qwen-1.5B 无效标签率高达 53.2%，即超过一半的输出无法提取判断结果。
- **Overthinking 与 infinite looping**：准确验证的 CoTs 通常较短（<3K tokens），而不准确的验证 CoTs 呈现出长尾分布，在 7K-8K tokens 处剧增，反映了过度思考和循环问题。
- **对指令敏感**：指令措辞轻微变化可导致 F1 分数波动 3-4 分。

### 主要实验结果

**ProcessBench（验证准确性）：**
- ThinkPRM-14B 在 OlympiadBench 和 OmniMath 上的 F1 分别达 87.3 和 85.7，远超同底座 LLM-as-a-Judge（72.8/67.8）。
- 训练数据量约为 DiscPRM（判别式 PRM）的 1/100，但验证准确率更高。

**Best-of-N 选择（MATH-500、AIME '24）：**
- ThinkPRM-14B 在所有 sampling budget 下均优于或持平于 DiscPRM 和 LLM-as-a-Judge。

**Verifier-guided beam search（MATH-500）：**
- ThinkPRM-1.5B（使用 8K 步骤标注）超过 LLM-as-a-Judge 和 DiscPRM，甚至超过使用更多训练数据的 RLHFFlow-Deepseek-PRM（off-the-shelf PRM）。

**Out-of-domain 泛化（GPQA-Physics、LiveCodeBench）：**
- ThinkPRM-14B 在 Best-of-N 下超过 DiscPRM-14B 约 8%（GPQA-Physics）和 4.5%（LiveCodeBench）。
- 判别式 PRM 在 domain shift 下表现脆弱，而生成式 PRM 更具鲁棒性。

### 关键消融实验

1. **Long CoT vs. Short CoT 训练**：在长 CoT 上训练的 ThinkPRM 比在压缩后的短 CoT 上训练的版本高出 20+ F1 分，证明扩展推理对验证至关重要。
2. **Process-based 过滤 vs. Outcome-based 过滤**：基于步骤级标签过滤的数据明显优于仅基于最终答案对错过滤的数据。
3. **Monte Carlo 自动标注**：使用 Monte Carlo rollouts 自动生成步骤标签（Math-shepherd 数据集）的 ThinkPRM-1.5B 与使用人工标注的版本性能相当，说明训练流程对标注来源具有鲁棒性。
4. **长推理链泛化**：虽然仅在短解答上训练，ThinkPRM 可泛化至包含 backtracking 的长推理链（如 Qwen3-1.7B 思考模式输出）。

### 局限性

- **过度自信（Overconfidence）**：生成式 PRM 的分数可能聚集在极端值（接近 0 或 1），难以得到校准的概率估计。
- **步骤标签干扰（Step Label Interference）**：对前期步骤的错误判断会影响后续步骤的验证（自回归特性导致的误差传播）。
- **额外推理开销**：生成 verification CoT 比判别式分类引入更多计算成本，但论文认为性能收益足以抵消这一开销。
