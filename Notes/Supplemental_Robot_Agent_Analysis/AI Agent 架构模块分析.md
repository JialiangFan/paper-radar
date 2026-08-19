---
imported_title: "AI Agent Architecture Module Analysis"
imported_from: "/Users/jfan/ND/看论文/robot_agent/AI Agent 架构模块分析.md"
imported_reason: "Useful for distinguishing VLA policy, monitor, tools, and controller modules."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# AI Agent 架构模块分析

> 基于 Claude Code (Anthropic) 和 Hermes Agent (Nous Research) 等开源项目的架构分析，总结现代 AI Agent 的核心模块。

## 概览

现代 AI Agent 系统通常由以下 **8 大核心模块** 组成：

```
┌─────────────────────────────────────────────────────┐
│                   用户交互层 (UI/CLI)                  │
├─────────────────────────────────────────────────────┤
│              核心 Agent 循环 (Agent Loop)              │
├──────┬──────┬──────┬──────┬──────┬──────┬───────────┤
│ 工具  │ 权限  │ 记忆  │ 上下文 │ 模型  │ 技能  │ 多Agent │
│ 系统  │ 系统  │ 系统  │ 管理  │ 交互  │ 系统  │  协作   │
├──────┴──────┴──────┴──────┴──────┴──────┴───────────┤
│              基础设施层 (配置/认证/遥测)                 │
└─────────────────────────────────────────────────────┘
```

---

## 1. 核心 Agent 循环 (Agent Loop)

**这是 Agent 的心脏。** 一个持续运行的循环，负责接收用户输入、调用模型、执行工具、返回结果。

### 基本流程

```
用户输入 → 组装系统提示 → 调用 LLM → 解析响应
    ↑                                    ↓
    │                             文本响应 / 工具调用
    │                                    ↓
    └──── 返回结果 ←── 执行工具 ←── 权限检查
```

### Claude Code 实现
- **核心文件**: `src/query.ts` (785KB) — 整个 Agent 的主循环
- **QueryEngine**: `src/QueryEngine.ts` — 会话生命周期管理器
- 采用 **流式架构 (Streaming-First)**，逐 token 返回结果
- 支持自动压缩 (auto-compaction)，当 token 接近上限时自动摘要旧消息
- 内置重试逻辑，指数退避 (2s → 2min)

### Hermes Agent 实现
- **核心文件**: `run_agent.py` (AIAgent 类) + `environments/agent_loop.py`
- 默认最大 90 次工具调用迭代
- 支持父子 Agent 共享迭代预算
- 采用标准 OpenAI tool calling 协议

### 关键设计点
| 设计问题 | 典型方案 |
|---------|---------|
| 何时停止循环？ | `stop_reason != "tool_use"` 或达到迭代上限 |
| 如何处理并发工具？ | 分析工具安全性，安全的工具并行执行 |
| 上下文溢出怎么办？ | 自动压缩/摘要旧对话 |
| 错误如何恢复？ | 重试 + 凭证轮换 + 降级 |

---

## 2. 工具系统 (Tool System)

**Agent 的能力边界由工具决定。** 没有工具的 Agent 只是一个聊天机器人。

### 工具接口设计

每个工具通常需要实现：

```
Tool {
  name              // 工具名称
  description       // LLM 可读的描述
  inputSchema       // JSON Schema 参数定义
  validateInput()   // 输入验证
  checkPermissions()// 权限检查
  call()            // 执行逻辑
  isReadOnly()      // 是否只读（影响并发策略）
  isDestructive()   // 是否破坏性操作
}
```

### 工具分类

| 类别 | Claude Code 示例 | Hermes Agent 示例 |
|------|-----------------|-------------------|
| **文件操作** | FileReadTool, FileEditTool, FileWriteTool | file_tools, file_operations |
| **搜索发现** | GlobTool, GrepTool | session_search_tool |
| **命令执行** | BashTool | terminal_tool (6种后端) |
| **网络访问** | WebFetchTool, WebSearchTool | web_tools |
| **代码执行** | — | code_execution_tool |
| **浏览器** | — | browser_tool (Browserbase) |
| **视觉** | (FileReadTool 支持图片) | vision_tools |
| **记忆** | (内置 auto-memory) | memory_tool |
| **子Agent** | AgentTool | 内置 subagent delegation |
| **外部协议** | MCPTool (40+ 动态工具) | mcp_tool |

### MCP (Model Context Protocol) — 工具系统的扩展协议

MCP 是一个关键的扩展机制，允许 Agent 动态加载外部工具：

- **Claude Code**: 支持 stdio / SSE / HTTP / WebSocket / SDK 传输
- **Hermes Agent**: 同样支持 MCP 服务器集成
- 工具命名规则: `mcp__<server>__<tool>`

### 关键设计点
- **工具注册**: 静态注册 (代码内置) + 动态注册 (MCP/插件)
- **并行执行**: 只读工具可安全并行，破坏性工具串行执行
- **结果存储**: 工具结果持久化以供后续引用

---

## 3. 权限与安全系统 (Permission & Security)

**Agent 能力越强，安全控制越重要。**

### Claude Code 的权限流水线

```
工具调用请求
    ↓
输入验证 (validateInput)
    ↓
Pre-Hook (用户自定义 shell 命令)
    ↓
权限规则匹配 (alwaysAllow / alwaysDeny / alwaysAsk)
    ↓
交互式确认 (无匹配规则时询问用户)
    ↓
工具级权限检查 (checkPermissions)
    ↓
执行工具
```

**核心能力**:
- 文件系统沙箱 (路径验证)
- 危险命令检测 (如 `rm -rf`, `git push --force`)
- YOLO 分类器 — ML 模型自动判断是否安全
- 权限拒绝追踪与审计

### Hermes Agent 的安全机制

- **命令审批**: 基于 allowlist 的危险操作检测
- **路径安全**: 目录遍历防护、越狱防护
- **提示注入检测**: 扫描配置文件中的注入模式、隐藏 Unicode、隐藏 div

### 关键设计点
| 层级 | 防护内容 |
|------|---------|
| 输入层 | 参数验证、Schema 校验 |
| 命令层 | 危险命令模式匹配 |
| 文件层 | 路径沙箱、遍历防护 |
| 网络层 | URL 白名单/黑名单 |
| 用户层 | 交互式确认、权限记忆 |

---

## 4. 记忆系统 (Memory System)

**让 Agent 能跨会话学习和积累知识。**

### 记忆类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **短期记忆** | 当前对话上下文 | 消息历史 |
| **工作记忆** | 当前任务状态 | 任务板、计划 |
| **长期记忆** | 跨会话持久化 | 用户偏好、项目知识 |
| **外部记忆** | 第三方存储 | 向量数据库、文件系统 |

### Claude Code 实现
- **基于文件的记忆**: `~/.claude/projects/<hash>/memory/` 目录
- **MEMORY.md 索引**: 所有记忆的目录文件
- **记忆分类**: user / feedback / project / reference
- **自动记忆**: 对话中自动提取值得记住的信息

### Hermes Agent 实现
- **Memory Manager**: 编排内置 + 外部记忆提供者
- **内置记忆**: MEMORY.md / USER.md 文件
- **插件系统**: 支持 5+ 种外部记忆后端
  - Honcho (辩证用户建模)
  - RetainDB (向量召回)
  - Holographic (分布式记忆)
- **记忆生命周期钩子**:
  - `prefetch()` — 每轮开始前召回相关记忆
  - `sync_turn()` — 每轮结束后持久化
  - `on_pre_compress()` — 压缩前提取洞察
  - `on_session_end()` — 会话结束时萃取

### 关键设计点
- 记忆应该是**结构化的** (分类、索引、可搜索)
- 需要**衰减机制** (过时的记忆应被更新或删除)
- **读取时验证** (记忆可能已过时，需对照当前状态)

---

## 5. 上下文管理 (Context Management)

**LLM 的上下文窗口是有限的，如何高效利用是关键。**

### 上下文压缩策略

```
完整对话历史
    ↓
超过 token 阈值？ ──否──→ 直接使用
    ↓是
裁剪旧工具结果 (低成本，无需 LLM)
    ↓
保护头部消息 (系统提示 + 首次交互)
    ↓
保护尾部消息 (最近 ~20K tokens)
    ↓
中间部分用 LLM 摘要 → 压缩后继续
```

### Claude Code 的三种策略
1. **Auto-Compact**: token 超限时自动摘要旧消息
2. **Snip-Compact**: 删除僵尸消息 (无用的中间结果)
3. **Context-Collapse**: 重构上下文结构

### Hermes Agent 的压缩参数
- 最小摘要: 2,000 tokens
- 摘要比率: 压缩内容的 20%
- 上限: 12,000 tokens
- 支持迭代更新之前的摘要

### 系统提示组装

Agent 的系统提示并非静态文本，而是动态组装：

```
系统提示 = 基础身份
        + 工具描述列表
        + 记忆上下文
        + 技能索引
        + 权限规则
        + 平台特定提示
        + 安全扫描结果
```

---

## 6. 模型交互层 (Model Interaction)

**Agent 与 LLM 的通信协议和适配。**

### 多模型支持

| 特性 | Claude Code | Hermes Agent |
|------|------------|--------------|
| 主要协议 | Anthropic Messages API | OpenAI Chat Completions |
| 备用协议 | — | Anthropic / Codex Responses |
| 模型数量 | Claude 系列 | 200+ (via OpenRouter) |
| 流式传输 | ✅ Delta streaming | ✅ Streaming |
| Token 计费 | 内置计数 | 内置估算 + 缓存感知 |

### 错误处理与容错

Hermes Agent 的错误分类体系值得借鉴：

| 错误类型 | 处理策略 |
|---------|---------|
| 认证失败 | 凭证轮换 |
| 限流 (429) | 指数退避 + 冷却 |
| 服务过载 | 备用提供者 |
| 上下文溢出 | 自动压缩 |
| 模型不存在 | 降级到备选模型 |
| 格式错误 | 重试 + 修正 |

### 凭证池 (Hermes Agent 特色)
- 每个提供者多个凭证
- 池策略: fill_first / round_robin / random / least_used
- 自动检测耗尽 (429/402) 并冷却

---

## 7. 技能与扩展系统 (Skills & Extensions)

**让 Agent 的能力可组合、可分享。**

### 技能 (Skill) 的概念

技能是**可复用的提示模板 + 工具组合**，用于完成特定类型的任务。

```yaml
# 技能文件结构 (以 Hermes Agent 为例)
---
name: paper-review
description: 以文献综述专家视角总结学术论文
platforms: [cli, telegram]
conditions:
  - "用户提到论文"
  - "用户要求阅读/审阅"
---
# 技能内容 (Markdown)
你是一个文献综述专家...
```

### 扩展机制对比

| 机制 | Claude Code | Hermes Agent |
|------|------------|--------------|
| **MCP 协议** | ✅ 核心扩展方式 | ✅ 支持 |
| **技能系统** | ✅ 文件级技能 | ✅ YAML + Markdown |
| **插件系统** | ✅ 版本化插件 | ✅ 记忆插件 |
| **Hooks** | ✅ Shell 命令钩子 | — |
| **自定义命令** | 80+ 斜杠命令 | 斜杠命令 |

### Hermes Agent 的自我改进循环

```
复杂任务 → 成功完成 → 自动提取为技能
                    → 存入技能库
                    → 下次类似任务直接调用
```

这是一个独特的设计：Agent 通过使用不断积累能力。

---

## 8. 多 Agent 协作 (Multi-Agent)

**复杂任务需要多个 Agent 分工协作。**

### Claude Code 的多 Agent 模式

| 模式 | 说明 |
|------|------|
| **default** | 进程内，共享对话 |
| **fork** | 子进程，独立消息，共享文件缓存 |
| **worktree** | 隔离的 git worktree + fork |
| **remote** | 远程容器/桌面端 |

### Swarm 模式 (实验性)

```
主导 Agent (Lead)
  ├── 队友 A → 认领任务 1
  ├── 队友 B → 认领任务 2
  └── 队友 C → 认领任务 3

共享: 任务板、消息收件箱
隔离: 消息历史、文件缓存、工作目录
```

### Agent 间通信
- **Claude Code**: SendMessageTool (点对点消息)
- **Hermes Agent**: 父子 Agent 共享迭代预算 + delegation hooks

---

## 总结对比

| 模块 | Claude Code | Hermes Agent |
|------|------------|--------------|
| **语言** | TypeScript (React/Ink) | Python |
| **Agent Loop** | 流式、单循环 | 标准 tool-calling |
| **工具数量** | 40+ 内置 | 40+ (59 文件) |
| **权限系统** | 多层流水线 + ML 分类器 | Allowlist + 路径安全 |
| **记忆** | 文件记忆 + 分类索引 | 插件化记忆 (5+ 后端) |
| **上下文管理** | 3 种压缩策略 | 迭代摘要 |
| **模型支持** | Claude 系列 | 200+ 模型 |
| **多 Agent** | fork/worktree/swarm | 子Agent delegation |
| **扩展性** | MCP + 插件 + 技能 + Hooks | MCP + 插件 + 技能 |
| **部署** | CLI / 桌面 / IDE | CLI / Telegram / Discord / Slack / WhatsApp |

### 设计 AI Agent 的核心原则

1. **Agent Loop 是核心** — 循环的健壮性决定了 Agent 的可靠性
2. **工具即能力** — 没有工具的 Agent 只是聊天机器人
3. **安全不可妥协** — 能力越大，权限控制越重要
4. **记忆创造连续性** — 跨会话记忆让 Agent 真正"认识"用户
5. **上下文是稀缺资源** — 智能压缩是必须的工程能力
6. **可扩展性** — MCP 等协议让 Agent 能力无限延伸
7. **多 Agent 是趋势** — 复杂任务需要分工协作

---

*分析来源: [Claude Code](https://github.com/anthropics/claude-code) v2.1.88, [Hermes Agent](https://github.com/nousresearch/hermes-agent)*
*创建时间: 2026-04-13*
