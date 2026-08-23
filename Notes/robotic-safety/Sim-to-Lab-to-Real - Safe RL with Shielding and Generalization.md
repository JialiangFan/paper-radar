# Sim-to-Lab-to-Real: Safe RL with Shielding and Generalization Guarantees

## 主题
Safe Sim-to-Real Transfer RL

## 背景
RL训练的策略在真实世界部署时性能常急剧下降（sim-to-real gap），不安全行为在仿真中可能无关紧要，但在真实环境中可能导致严重后果。现有sim-to-real方法（如domain randomization）并未显式考虑安全问题。

## 现有局限与研究问题
- **Limitation:** 传统sim-to-real方法不提供性能或安全性的泛化保证；传统性能保证方法需要对系统不确定性有显式描述（如驱动噪声边界），但在高维视觉输入的真实系统中这通常不可行
- **Problem:** 如何系统性地弥合sim与real之间的安全差距，并在真实部署前提供性能和安全的可证明保证？

## 贡献
- 提出三阶段框架Sim-to-Lab-to-Real：在Sim阶段训练多样性策略，在Lab阶段安全fine-tune并认证
- Sim-to-Lab转移：通过HJ可达性分析训练backup safety policy，使用shielding机制在探索时过滤不安全动作，减少4%-77%的安全违规
- Lab-to-Real转移：应用PAC-Bayes Control框架，提供策略在unseen环境中性能和安全的泛化下界
- 将HJ可达性分析与PAC-Bayes结合，将泛化界提升40%

## 方法论
- 双策略设置：性能策略优化任务reward，backup策略基于Safety Bellman Equation（HJ可达性）训练
- Shielding: 当safety state-action value function预测不可避免的安全违规时，backup策略覆盖性能策略
- PAC-Bayes框架：训练条件化于latent variable z的策略分布，Sim阶段训练prior，Lab阶段fine-tune posterior
- 在两种室内导航环境和真实Unitree四足机器人上验证
