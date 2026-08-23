# Survey on Safe Robot Control via Learning

## 主题
Safe Robot Control Learning

## 背景
现代社会高度依赖机器人系统，涉及航空航天、汽车、能源、医疗等众多行业。当控制目标涉及安全时，必须防止系统进入违反安全约束的状态。经典控制理论和Deep RL分别代表了控制方法谱系的两端。

## 现有局限与研究问题
- **Limitation:** 经典控制方法依赖精确的数学模型，对复杂非线性系统建模困难；纯数据驱动方法缺乏安全保证
- **Problem:** 如何在真实机器人上学习高性能控制策略，同时维持稳定性、避障、过驱动预防等多种安全属性

## 贡献
- 从经典控制到Deep RL的完整谱系角度综述安全机器人控制学习方法
- 涵盖model-free vs model-based、myopic vs predictive、discrete vs continuous等多个分类维度
- 讨论嵌入式系统硬件和软件层面保持安全的实际考量
- 补充了软件工程视角的安全性讨论，如LTL (Linear Temporal Logic)规约和混合自动机

## 方法论
- 按控制器类型分类：PID（myopic/model-free）、MPC（predictive/model-based）、LQR等
- 涵盖系统辨识、Lyapunov稳定性分析、可达性验证等核心技术
- 讨论Zonotopes等几何工具在可达性证明中的应用
