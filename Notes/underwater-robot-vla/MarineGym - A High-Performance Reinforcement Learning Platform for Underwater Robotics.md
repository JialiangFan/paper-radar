# MarineGym: A High-Performance Reinforcement Learning Platform for Underwater Robotics

**arXiv:** [2503.09203](http://arxiv.org/abs/2503.09203)
**Date:** 2025-03-12
**Authors:** Shuguang Chu, Zebin Huang, Yutong Li, Mingwei Lin, Ignacio Carlucho, Yvan R. Petillot, Canjun Yang
**Keywords:** underwater robotics, reinforcement learning, GPU-accelerated simulation, domain randomization, Isaac Sim

---

## 相关主题
- [[literature_review]] — 水下仿真平台

## 核心创新点
提出首个专为水下机器人设计的 GPU 加速强化学习平台 MarineGym，基于 NVIDIA Isaac Sim 构建自定义水动力学插件，在单张 RTX 3060 上实现 250,000 FPS 的仿真速度（较传统平台提升 250 倍），支持 8,000+ 并行环境实例，并提供 5 种 UUV 模型、3 类标准化 RL 任务和模块化域随机化工具包，为水下 RL 研究建立了可复现的基准测试框架。

## 主要方法
- **GPU 加速水动力学仿真**: 将水下机器人动力学分解为刚体分量（PhysX 引擎处理）和水动力学分量（基于 Fossen 运动方程的 PyTorch 张量 GPU 计算），涵盖附加质量、阻尼矩阵、科里奥利效应和恢复力矩
- **Isaac Sim 集成**: 利用实时光线追踪引擎模拟水下光学物理特性，包括光谱衰减和水下环境特有的颜色失真
- **5 种 UUV 模型**: BlueROV（6 推进器）、BlueROV Heavy（8 推进器）、LAUV（舵-螺旋桨）、iAUV（浙大开发，欠驱动）、HAUV（倾转旋翼混合空水飞行器），均支持 YAML 配置和 URDF 格式
- **3 种执行器模型**: 零阶（直接映射）、一阶（微分方程捕捉加减速动态）、神经网络驱动（从实验数据学习非线性映射，捕捉摩擦和阻尼效应）
- **域随机化工具包**: 涵盖物理属性（质量、惯性、重心）、仿真设置（流体密度、附加质量矩阵、阻尼系数）、执行器参数（时间常数、力常数、安装位置）、环境因素（水流速度/方向、外部载荷），支持均匀分布、高斯分布和自定义分段采样
- **预定义 RL 任务**: 定点保持（环境扰动下维持目标姿态）、轨迹跟踪（跟随时变 3D 轨迹如螺旋线、利萨如图形）、对接（水下平台精确自主着陆）
- **基准 RL 算法**: 实现了 DDPG、PPO、SAC、TD3、DQN 等多种算法用于对比评估

## 关键发现
> 域随机化在分布外条件下可实现高达 64% 的误差降低；欠驱动模型（LAUV、iAUV）所需训练步数为全驱动设计的 2 倍；在强海流条件下，8 推进器的重型平台（BlueROV Heavy、HAUV）性能退化最小，而欠驱动平台则面临显著挑战。

## 结论/性能
- **仿真速度**: 250,000 FPS（RTX 3060），8,200 并行环境；传统平台 DAVE 约 1,000 FPS（10 环境），Stonefish/HoloOcean 约 100 FPS
- **域随机化效果 - 定点保持**: DR 训练后误差从 1.637m 降至 0.036m（Env1，改善 95.8%），从 1.898m 降至 0.147m（Env2，改善 92.3%）
- **域随机化效果 - 轨迹跟踪**: 误差从 0.093m 降至 0.047m（Env1，改善 49.5%）
- **域随机化效果 - 对接**: 误差从 0.241m 降至 0.088m（Env2，改善 63.5%）
- **局限性**: 缺乏真实世界部署验证，水下视觉特性仍为简化模拟
