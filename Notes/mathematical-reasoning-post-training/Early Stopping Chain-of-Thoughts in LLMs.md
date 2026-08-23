# Early Stopping Chain-of-Thoughts in LLMs

## 主题
Early stopping CoT reasoning（推理时提前终止 chain-of-thought 生成）

## 背景
Reasoning LLM（如 OpenAI o 系列、DeepSeek R1、QwQ）通过生成长 chain-of-thought（CoT）来解决复杂问题，但冗长的推理轨迹导致 inference 成本极高。研究表明 LLM 在得出正确答案后仍频繁 overthink，持续产生冗余步骤。如何在保留 CoT 准确性的同时压缩推理长度，成为 efficient reasoning 领域的核心挑战。

## 现有局限与研究问题
- **Limitation:** 现有 output-side efficient reasoning 方法（如 Speculative Rejection、Early Stop Self-Consistency）要求并行解码或辅助 reward model，增加了系统复杂度，且无法直接适用于单条推理轨迹。
- **Problem:** 何时可以安全地中止一条推理轨迹而不损害最终答案质量？即能否在单条轨迹上、无需额外模型的条件下检测 CoT 的收敛时机。

## 贡献
- 提出 **ES-CoT**（Early-Stop CoT），首个基于 run-jump test 的 inference-time 提前终止方法，无需额外 reward model、并行解码或 retraining。
- 经验与理论双重验证：step answers 单调收敛于最终答案，且 run length（连续相同 step answer 的长度）在收敛时出现统计显著的突增（jump）。
- 在 5 个数学/逻辑推理 benchmark（AIME24、GPQA、MATH500、Minerva、OlympiadBench）和 3 个 LLM（QwQ-32B、Qwen3-8B、DeepSeek-R1-Distill-Llama-8B）上，ES-CoT 平均减少约 **41%** 的 inference tokens，同时保持与标准 CoT 相当的精度。
- ES-CoT 可与 self-consistency prompting 无缝结合（ES-CoT+SC），在进一步节省 token 的同时还可提升准确率。

## 方法论
- **Step answer 定义：** 在每个推理步骤 $t$ 结束时，向 LLM 追加 prompt "The final answer is"，记录模型当前输出作为 step answer $x_t$。
- **Run sequence：** 将连续输出相同答案的步骤计为一次 run，记录各 run 的长度序列 $R = \langle r_1, r_2, \ldots \rangle$。
- **Run-jump test（核心停止准则）：** 计算差分序列 $D = \langle d_1, \ldots, d_{n-1} \rangle$，$d_i = r_{i+1} - r_i$。若最新差分 $d_{n-1} \geq d_{\min}$，且 t-test 表明 $d_{n-1}$ 显著大于历史差分 $d_{1:n-2}$，则立即终止生成，输出当前 step answer。
- **超参数：** 最小差分阈值 $d_{\min}$（默认 10，用于防止过早停止）；t-test 显著性水平 p-value（默认 0.05）。
- **理论保证：** 在最终答案为确定性（Assumption 1）且 step answer 概率单调增加（Assumption 2）的条件下，Theorem 1 给出 ES-CoT 误差的上界，证明 run length 越大误差越趋近于 0。
- **与 self-consistency 的结合：** 在多条采样轨迹上分别应用 ES-CoT，再用 majority voting 决定最终答案，兼顾效率与鲁棒性。
