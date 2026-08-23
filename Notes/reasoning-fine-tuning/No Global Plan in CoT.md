# No Global Plan in Chain-of-Thought: Uncover the Latent Planning Horizon of LLMs

**arXiv:** [2602.02103v1](http://arxiv.org/abs/2602.02103v1)
**Date:** 2026-02-02
**Authors:** Liyan Xu, Mo Yu, Fandong Meng, Jie Zhou
**Keywords:** LLM planning, CoT analysis

---

## 相关主题
- [[literature_review]] — Theme 4: CoT 推理的有效性分析与改进
- 与 [[Chain of Thoughtlessness]] 构成互补的分析视角

## 核心创新点
通过 **Tele-Lens** 探测方法揭示 LLMs 的隐性规划是**短视且局部的**（myopic horizon），主要进行增量性转变而非精确的全局规划。

## 主要方法
- 开发 Tele-Lens 针对隐藏状态的探测方法
- 在多任务域分析隐性规划范围
- 提出用少量 CoT 点表征整体路径不确定性的策略
- 演示自动识别 CoT bypass 的可行性

## 关键发现
1. LLMs 呈现**"近视式"推理**——主要进行增量性转变
2. 少量 CoT 点即可有效表征整条路径的不确定性
3. 可以在**不降低性能**的前提下实现 CoT bypass 的自动识别

## 与 Chain of Thoughtlessness 的关系
| 论文 | 核心结论 | 分析层面 |
|------|---------|---------|
| Chain of Thoughtlessness | CoT 是模式匹配，非算法推理 | 行为层面（输出分析） |
| **No Global Plan** | LLM 隐性规划是短视的 | 表征层面（隐藏状态探测） |

两篇论文从不同角度印证了同一结论：LLM 缺乏真正的全局规划能力。

## 启发
支持了 SPIRAL/RAP 等引入外部搜索结构的必要性——如果 LLM 内部缺乏全局规划，那么必须通过外部搜索机制来弥补。
