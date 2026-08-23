# Agentic LLM Planning via Step-Wise PDDL Simulation

**arXiv:** [2603.06064v1](http://arxiv.org/abs/2603.06064v1)
**Date:** 2026-03-06
**Authors:** Kai Göbel, Pierrick Lorang, Patrik Zips, Tobias Glück
**Keywords:** LLM planning, PDDL

---

## 相关主题
- [[literature_review]] — Theme 2 + Theme 4 交叉
- 与 [[PDDL-Instruct]] 直接相关

## 核心创新点
提出 **PyPDDLEngine**，将 PDDL 仿真引擎通过 Model Context Protocol (MCP) 暴露给 LLM，LLM 以逐步交互式搜索进行规划——每次选择一个动作、观测状态、可重置重试。

## 主要方法
- 开源 PDDL 仿真引擎 PyPDDLEngine
- LLM 通过 MCP 接口进行工具调用式规划
- 在 102 个 IPC Blocksworld 实例上评估

## 关键发现
| 方法 | 成功率 | Token 成本 |
|------|--------|-----------|
| Fast Downward | 85.3% | — |
| 直接 LLM 规划 | 63.7% | 1x |
| Agentic LLM (PyPDDLEngine) | 66.7% | 5.7x |

> Agentic 增益仅 +3%，且 token 成本高 5.7 倍。LLM 产生的短计划更像**训练数据记忆**而非真正的规划。

## 核心结论
> **Agentic 增益取决于环境反馈的性质**：编码代理受益于外部信号（编译错误、测试失败），但 PDDL 的逐步反馈是自我评估的，缺乏外部验证。

## 与 PDDL-Instruct 的关系
- PDDL-Instruct 通过**训练时**集成 VAL 验证器解决了这个问题
- PyPDDLEngine 的结果进一步证实：**纯推理时的 agentic 方法不够**，需要训练时的内化（如 PDDL-Instruct）或外部验证信号
