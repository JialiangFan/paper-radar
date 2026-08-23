# RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic

## 主题
VLM Safety Guardrail Framework

## 背景
VLM驱动的具身智能体在执行复杂长horizon任务方面展现出impressive能力，但它们对恶意危险指令极度脆弱（如"把球扔向窗户"）。与纯文本LLM不同，具身智能体可以将不安全指令转化为不可逆的物理行动，造成real-world安全威胁。

## 现有局限与研究问题
- **Limitation:** 现有安全防御方法依赖静态规则过滤器或手工安全提示，无法处理动态、时间依赖和上下文相关的隐式风险（如"打开微波炉"——取决于里面是否有金属叉子）
- **Problem:** 如何在VLM驱动的具身智能体运行时有效防御两类隐式风险——上下文风险（看似安全的动作因环境上下文变危险）和时间风险（单个动作安全但持续执行不安全的序列）？

## 贡献
- 提出RoboSafe：基于可执行谓词逻辑的混合推理安全护栏框架
- 引入Backward Reflective Reasoning：持续反思近期轨迹，推断temporal safety predicates，主动触发replanning
- 引入Forward Predictive Reasoning：基于长期安全记忆中的多模态上下文推理，预测并拦截隐式上下文风险
- 使用Hybrid Long-Short Safety Memory统一两种推理：短期工作记忆(M^S)存储当前轨迹，长期知识记忆(M^L)存储安全经验
- 在三个具身智能体workflow上减少36.8%危险动作，在真实机械臂上验证

## 方法论
- 将具身智能体建模为POMDP，guardrail作为黑盒安全滤波器在推理时拦截动作
- Safety Knowledge Generation：通过知识解耦机制将安全知识分为high-level推理示范ρ_t和low-level可验证谓词Φ_t
- Multi-grained Contextual Retrieval：粗粒度（场景+行为）和细粒度（具体动作）双层检索相关安全经验
- Contextual Logic Verification：将检索到的安全经验转化为可执行Python逻辑谓词，由轻量级interpreter验证
- Temporal Logic：backward推理验证时间安全谓词Ψ_t，检测持续不安全序列并触发replan
