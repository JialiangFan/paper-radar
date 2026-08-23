# DEER - Dynamic Early Exit in Reasoning Models

## 主题
Dynamic early exit reasoning

## 背景
大型推理语言模型（Large Reasoning Models, LRMs）如 DeepSeek-R1 和 GPT-O1 依赖 test-time scaling，通过生成长链式思维（Chain-of-Thought, CoT）来解决复杂任务。然而，过长的 CoT 不仅降低推理效率，还可能引入冗余的 reasoning steps，导致模型从正确路径偏移到错误答案。研究发现约 75% 的样本存在"pearl reasoning"临界点，即在完成全部推理步骤之前就已具备足够信息得出正确答案。

## 现有局限与研究问题
- **Limitation 1:** 现有 LRMs 在 Supervised Fine-Tuning 和 Reinforcement Learning 阶段未能学会动态调整 reasoning length，导致推理时产生过多冗余步骤（overthinking problem）。
- **Limitation 2:** 现有 efficient reasoning 方法（如 TCC、CoD、NoThinking）要么无法泛化到复杂任务，要么以牺牲推理准确率为代价；基于固定启发式的 early exit 策略无法适应每道题的最优退出位置。
- **Problem:** 如何在无需额外训练的前提下，动态识别 LRM 推理过程中的 pearl reasoning 临界点，在模型对试答案置信度足够高时提前终止 CoT 生成，从而同时提升效率与准确率？

## 贡献
- 提出 **DEER**（Dynamic Early Exit in Reasoning），一种无需训练的 plug-and-play 方法，可无缝集成到现有 o1-like LRMs 中。
- 通过监控 **Action Transition Points (ATP)**（语言标记如 "Wait" 或基于 token entropy 的方法）识别推理转换节点作为候选 early-exit 位置。
- 提出 **DEER-PRo**（Parallel and Robust variant），在多个 early-exit 候选点并行进行 answer induction，利用 MAD（Mean Absolute Deviation）校准置信度分数，大幅提升对 prompt 敏感性的鲁棒性。
- 集成 **Branch-Parallel Decoding** 加速策略，通过线性化多分支并行生成和基于置信度的 KV cache 管理，减少 answer induction 带来的额外延迟。
- 在 10 个 reasoning benchmarks（GSM8K、MATH-500、AMC、GPQA、AIME、LiveCodeBench 等）上覆盖 11 个模型（1.5B 到 671B），CoT 长度平均压缩 19.1%–80.1%，准确率提升 0.3%–5.0%。

## 方法论
- **框架概述:** DEER 包含三个核心模块——Reasoning Transition Monitor、Answer Inducer、Confidence Evaluator，协同判断是否在当前节点提前退出。
- **Reasoning Transition Monitor:** 检测推理转换点（ATP）作为 early-exit 候选位置；支持两种策略：(i) 语言标记法（linguistic marker-based），检测 "Wait"、"Alternatively" 等关键词；(ii) 熵值法（entropy-based），计算每个推理步骤首 token 的熵 H(p(·|x<t))，高熵位置表示模型正在"思考分叉"，作为候选退出点。
- **Answer Inducer:** 在检测到 ATP 时，用 "final answer" token（含 \boxed{} 分隔符）替换后续内容，诱导模型立即生成试答案 A = LRM(P, T, I)。
- **Confidence Evaluator:** 计算试答案各 token 最大预测概率的几何平均值作为置信度 C；若 C > λ（阈值设为 0.95），认为已达 pearl reasoning，停止后续推理并输出结论；否则撤销 answer induction，继续推理。
- **DEER-PRo:** 在多个 early-exit 点并行执行 N 次 answer induction（使用不同 prompt），计算校准置信度 C_cali = C_avg − α · C_MAD，用 MAD 惩罚过高的置信度噪声，有效消除模型对 answer inducing prompt 的敏感性。
- **Branch-Parallel Decoding:** 将多分支 answer induction 线性化为单序列并行生成（使用特殊 causal attention mask），同时进行动态 KV cache 管理，使 trial answer 评估与 reasoning chain 生成在时间上重叠，降低额外延迟。
- **实验基准:** 在 DeepSeek-R1-Distill-Qwen 系列（1.5B/7B/14B/32B）、Qwen3 系列（1.7B/4B/8B/14B/32B）、QwQ-32B 上验证；评估指标为 Accuracy (Acc)、Token Number (Tok)、Compression Rate (CR)。
