# EasyUUV: An LLM-Enhanced Universal and Lightweight Sim-to-Real Reinforcement Learning Framework for UUV Attitude Control

**arXiv:** [2510.22126](http://arxiv.org/abs/2510.22126)
**Date:** 2025-10-25
**Authors:** Guanwen Xie, Jingzehua Xu, Jiwei Tang, Yubo Huang, Zixi Wang, Shuai Zhang, Dongfang Ma, Juntian Qu, Xiaofan Li
**Keywords:** LLM-enhanced control, sim-to-real transfer, reinforcement learning, UUV attitude control, adaptive controller

---

## 相关主题
- [[literature_review]] — LLM 增强水下控制

## 核心创新点
提出首个将多模态大语言模型（LLM）与强化学习和自适应控制相结合的水下无人潜航器（UUV）姿态控制框架 EasyUUV。系统采用三层混合架构：RL 策略生成高层姿态修正、自适应 S 曲面（A-S-Surface）控制器执行底层控制、多模态 LLM 在运行时自适应调节控制器参数，实现了从仿真到真实水域的零样本迁移，并在水池和海试中验证了有效性。

## 主要方法
- **三层混合控制架构**: RL 策略接收 9 维状态向量（当前/目标姿态四元数 + 深度误差），输出 4 维动作（横滚、俯仰、偏航、深度修正），馈入自适应 S 曲面控制器执行底层推力分配。控制律为 sigmoid 函数形式：$u_t = \frac{2}{1+\exp(-\zeta_1 e(t) - \zeta_2 \dot{e}(t))} - 1 + \Delta u(t)$
- **PPO 强化学习训练**: 基于 RSL-RL 库，在 NVIDIA Isaac Lab + MuJoCo 物理引擎中训练，460 个 episode（约 3x10^7 步）在 RTX 4060 上仅需约 130 秒。奖励函数包含姿态对齐项 $r_q = \exp(-|q \cdot q_{des}^*|)$、动作惩罚项和深度跟踪项
- **域随机化**: 浮心-重心偏移（0.075-0.15m 均匀球面）、体积（1.5-3L 均匀分布）、控制器增益（15-30% 变化范围）
- **多模态 LLM 运行时参数调节**: LLM 智能体处理视觉日志和文本传感器数据，自适应调节控制器参数（$\zeta_1$, $\zeta_2$），无需重新训练。LLM 输出受模糊规则约束的调节缩放因子（大幅调整 2x/0.5x，微调 1.5x/0.67x），而非直接生成参数值
- **水动力学建模**: 基于 MuJoCo 惯性盒近似的现象学阻力和粘性力模型；Blue Robotics T200 推进器（16V）采用分段二次拟合：正转 29.54a^2+26.10a-2.44，中性区间 -0.08~0.08，反转区间独立拟合
- **低成本硬件平台**: 约 1000 美元，3D 打印 ABS 外壳 + 铝合金结构，30L 防水舱，<20kg，8 个自定义推进器实现全驱动 6-DOF，ESP32-WROOM 微控制器（100Hz），MPU9250 九轴 IMU + 互补滤波，RS-485 线缆实时通信

## 关键发现
> RL 策略使复合跟踪误差降低 77%（MSE 从 0.452 降至 0.103）；LLM 运行时参数调节在湍流条件下仅需 2 次调整即可将 MSE 降低 78%（从 0.0812 降至 0.0179 rad^2）；小规模域随机化相比大规模域随机化能获得更优的跨域泛化性能；零样本 sim-to-real 迁移在水池和海试中均成功验证。

## 结论/性能
- **RL 增强效果**: 复合误差 MSE 从 0.452（无 RL）降至 0.103（有 RL），改善 77%
- **控制器对比**: A-S-Surface 控制器收敛最快、最终 MSE 最低，显著优于 S-Surface 和 PID
- **域随机化**: 小规模 DR 在正浮力偏移下将 MSE 从 0.0388 降至 0.0087；大规模 DR 反而降低稳定性（0.0110）
- **水池实验**: RL 使偏航+横滚跟踪 MSE 从 0.3836 降至 0.2356，标准差从 0.150 降至 0.080
- **LLM 调节效果**: 湍流条件下 2 次 LLM 调整将 MSE 从 0.0812 降至 0.0179 rad^2（降低 78%）
- **海试**: 在波浪诱导湍流下成功跟踪目标指令，稳态误差趋近于零，验证了零样本域迁移能力
- **局限性**: 仿真保真度受限、LLM 行为非确定性、评估仅限于特定低成本平台和姿态跟踪任务
