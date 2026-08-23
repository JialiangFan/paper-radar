# OceanGym: A Benchmark Environment for Underwater Embodied Agents

**arXiv:** [2509.26536](http://arxiv.org/abs/2509.26536)
**Date:** 2025-09-30
**Authors:** Yida Xue, Mingjun Mao, Xiangyuan Ru, Yuqi Zhu, Baochang Ren, Shuofei Qiao, Mengru Wang, Shumin Deng, Xinyu An, Ningyu Zhang, Ying Chen, Huajun Chen
**Keywords:** underwater embodied agents, benchmark, multimodal LLM, autonomous underwater vehicle, signal temporal logic

---

## 相关主题
- [[literature_review]] — 水下感知与基准测试

## 核心创新点
OceanGym 是首个面向水下具身智能体的综合性基准测试平台，基于 Unreal Engine 5.3 与 HoloOcean 物理仿真构建约 800m x 800m 的高保真海洋环境，涵盖 8 个任务域，并提出以 POMDP 为核心的多模态 LLM 统一智能体框架，集成感知、记忆与序列决策能力，首次系统性揭示了当前 MLLM 在水下极端条件下与人类专家之间的巨大性能差距。

## 主要方法
- **高保真仿真环境**: 基于 Unreal Engine 5.3 和 HoloOcean 构建，空间约 800m x 800m，支持两种深度（浅水 50m 高照明 / 深水 500m 低能见度），包含逼真的海洋基础设施资产（油管、沉船、飞机残骸、电气设备、风力发电站等），智能体通过六方向（前/后/左/右/上/下）同步 RGB 与声纳传感器感知环境
- **统一智能体框架 (POMDP)**: 将水下导航建模为部分可观测马尔可夫决策过程，包含多模态感知处理模块（RGB + 声纳融合）、滑动窗口记忆架构（应对动态水下环境和部分可观测性）、以及 MLLM 参数化的离散动作策略（方向移动与旋转控制）
- **八大任务域**: 分为感知任务（多视角感知、上下文感知）和决策任务（沉船探测、飞机残骸搜索、采矿机器人定位、油桶搜索、电气设备检测、管道巡检、风电站评估、对接操作），所有任务均在浅水和深水两种条件下评估
- **多模型评估**: 系统评估了 GPT-4o-mini、Gemini、Qwen2.5-VL-7B 等主流 MLLM，以人类专家表现为基准

## 关键发现
> 在深水低能见度条件下，最优模型 GPT-4o-mini 的决策成功率仅为 14.8%，而人类专家在同等条件下可达 69.6%；浅水条件下最优模型成功率为 18.4%，人类为 100%。感知任务中 Qwen2.5-VL-7B 浅水准确率 57.12%，深水骤降至 28.48%。尤为关键的是，虽然人类专家在融合声纳数据后性能一致提升，但 MLLM 对声纳数据的利用"有限且不一致"，暴露了当前架构在非标准视觉模态融合上的根本缺陷。

## 结论/性能
- 感知任务: Qwen2.5-VL-7B 浅水 57.12%，深水 28.48%（人类接近 100%）
- 决策任务: GPT-4o-mini 浅水 18.4%，深水 14.8%（人类浅水 100%，深水 69.6%）
- MLLM 与人类专家存在 43-85 个百分点的巨大差距
- 声纳数据融合: 人类一致受益，MLLM 表现有限且不稳定
- 记忆转移: 跨任务转移比任务内转移更稳定，尤其在深水条件下
- 主要失败模式: 感知错误导致导航失误、长时间任务中记忆退化（循环导航、方向混乱）
- 智能体能力初期随经验提升，但很快达到平台期，表明内在探索与长期规划能力不足
