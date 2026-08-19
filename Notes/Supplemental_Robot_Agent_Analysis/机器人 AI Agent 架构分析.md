---
imported_title: "Robot AI Agent Architecture Analysis"
imported_from: "/Users/jfan/ND/看论文/robot_agent/机器人 AI Agent 架构分析.md"
imported_reason: "Useful for the safety-agent workflow slide and agent/component framing."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# 机器人 AI Agent 架构分析

> 对比通用 AI Agent (Claude Code, Hermes Agent) 与机器人 AI Agent (OpenClaw/ROSClaw) 的架构差异，梳理机器人 Agent 的核心模块。

## 核心观点

机器人 Agent 比通用 Agent **简单很多**，但有一些**独有的模块**（感知、安全、硬件抽象）。

---

## 通用 Agent 模块的取舍

| 通用 Agent 模块 | 机器人需要？ | 原因 |
|----------------|------------|------|
| 文件编辑/搜索工具 | ❌ 不需要 | 机器人不写代码 |
| 权限交互式确认 | ❌ 大幅简化 | 实时控制不能等用户确认 |
| 上下文压缩 (3种策略) | ⚠️ 简化 | 对话短，但感知数据量大 |
| MCP/插件扩展 | ❌ 不需要 | 工具就是固定的硬件能力 |
| 多 Agent 协作 | ⚠️ 视场景 | 多机器人协作时才需要 |
| 技能/斜杠命令 | ❌ 不需要 | — |
| 记忆系统 | ⚠️ 简化 | 可能需要记住环境/任务，但比通用 Agent 轻量 |

---

## 机器人 Agent 的 5 个核心模块

```
┌─────────────────────────────────────┐
│        Agent Loop (大脑)             │
│   LLM 推理 → 技能选择 → 执行监控     │
├──────────┬──────────┬───────────────┤
│  感知模块  │  技能库   │  安全模块     │
│ Perception│  Skills  │   Safety     │
├──────────┴──────────┴───────────────┤
│        硬件抽象层 (ROS 2 / 直接控制)   │
└─────────────────────────────────────┘
```

---

### 1. Agent Loop — 比通用 Agent 简单得多

通用 Agent 的循环是 `用户输入 → LLM → 工具调用 → 循环`，可能迭代几十次。

机器人 Agent 的循环：

```
感知数据 → LLM 理解场景 → 选择技能 → 执行 → 观察结果 → 下一步
```

**关键简化**：
- 不需要流式 token 输出（机器人不需要逐字显示）
- 工具调用次数少（一个任务通常是几个动作的序列）
- 不需要复杂的上下文压缩（对话轮次少）

**独特挑战**：
- **实时性要求**：LLM 推理延迟可能太高，需要分层 — 高层用 LLM 规划，底层用传统控制器执行
- **闭环控制**：需要持续观察执行结果，不是"调用一次工具就完事"

---

### 2. 感知模块 (Perception) — 通用 Agent 没有的

这是机器人 Agent **独有且最重要**的模块。

```
相机图像 ──→ VLM/视觉模型 ──→ 结构化场景描述 (JSON)
LIDAR点云 ──→ 障碍物检测 ──→ 
关节状态  ──→ 本体感知   ──→ 
```

OpenClaw/ROSClaw 的做法叫 **"bridged grounding"**：
- 用一个 VLM 把相机画面转成文字描述
- 这样即使纯文本 LLM 也能"看到"环境

**设计决策**：
- 直接用多模态模型 (如 GPT-4o/Claude) 处理图像？还是用专门的视觉模型预处理？
- 感知频率是多少？每次决策前拍一张照？还是持续流式感知？

---

### 3. 技能库 (Skill Library) — 本质不同于通用 Agent 的"工具"

通用 Agent 的工具是 `读文件`、`执行命令` 这类**离散操作**，调一次就完成。

机器人的"工具"是**运动技能** — 一段持续执行的控制策略：

```python
# 通用 Agent 的工具 — 调一次就完成
def read_file(path: str) -> str:
    return open(path).read()

# 机器人的"工具" — 需要持续控制直到完成
def pick_up(object_name: str):
    approach(object_name)          # 接近目标
    while not aligned():
        adjust_pose()              # 持续对准
    close_gripper()                # 抓取
    lift()                         # 提起
    verify_grasp()                 # 验证是否抓住了
```

**技能库的设计**：
- 每个技能有**前置条件**和**后置条件**（如 `pick_up` 要求手爪是空的）
- 技能可以是 learned policy（神经网络）或 scripted（硬编码）
- LLM 负责**选择和编排技能**，不负责底层控制

---

### 4. 安全模块 (Safety) — 比通用 Agent 更关键

通用 Agent 的安全是"别删错文件"。机器人的安全是**物理安全**，后果严重得多。

```
LLM 输出动作
    ↓
速度限制检查 (v_max, ω_max)
    ↓
碰撞检测 (自碰撞 + 环境碰撞)
    ↓
关节限位检查
    ↓
力/力矩限制
    ↓
执行
```

ROSClaw 的参数设定：
- `v_max = 1.0 m/s`, `ω_max = 1.5 rad/s` 硬限制
- 接口白名单 — LLM 只能调用预定义的安全接口
- 完整审计日志

**关键原则：安全层不能依赖 LLM 判断，必须是硬编码的规则。**

---

### 5. 硬件抽象层 (Hardware Abstraction)

把具体硬件接口统一成 LLM 能理解的 tool schema：

```
ROS 2 话题/服务  →  Affordance Manifest  →  LLM tool schema

例如:
/cmd_vel (geometry_msgs/Twist)  →  {
  "name": "move",
  "description": "移动机器人",
  "parameters": {
    "linear_x": "前进速度 m/s",
    "angular_z": "旋转速度 rad/s"
  }
}
```

OpenClaw 会**自动**把 ROS 服务/话题定义转成 tool schema，换机器人只需换配置。

---

## 最简可行架构 (MVP)

```
┌──────────────────────────────┐
│  LLM (多模态，直接看图)        │
│  输入: 图像 + 任务描述         │
│  输出: 技能名 + 参数           │
├──────────────────────────────┤
│  技能库 (5-10 个基础技能)      │
│  move, turn, pick, place,    │
│  look_around, wait ...       │
├──────────────────────────────┤
│  安全层 (速度/力矩硬限制)      │
├──────────────────────────────┤
│  ROS 2 / 硬件驱动             │
└──────────────────────────────┘
```

**大概 500-1000 行代码就能跑起来**，比 Claude Code 的几十万行简单两个数量级。

核心就是：LLM 看图说话 → 选技能 → 安全检查 → 执行 → 看结果 → 下一步。

---

## 与通用 Agent 的对比总结

| 维度 | 通用 Agent (Claude Code) | 机器人 Agent |
|------|------------------------|-------------|
| 代码量 | ~100,000+ 行 | ~500-1,000 行 (MVP) |
| 工具数量 | 40+ 且可动态扩展 | 5-10 个固定技能 |
| 循环次数 | 可能几十次 | 通常 < 10 步 |
| 安全重点 | 文件/命令权限 | 物理安全（速度/力/碰撞） |
| 感知 | 无（读文件即可） | 核心模块（视觉/LIDAR/本体感知） |
| 实时性 | 不要求 | 关键要求 |
| 上下文管理 | 复杂（长对话压缩） | 简单（短对话，但感知数据大） |
| 扩展性 | MCP/插件/Hooks | 换硬件 = 换配置 |

---

## 参考项目

- [OpenClaw](https://github.com/openclaw/openclaw) — 自主 AI Agent 平台，支持机器人控制
- [ROSClaw](https://arxiv.org/html/2603.26997) — OpenClaw 的 ROS 2 机器人框架
- [OpenGo](https://github.com/openclaw) — 基于 LLM 的四足机器人 Agent

*创建时间: 2026-04-13*
