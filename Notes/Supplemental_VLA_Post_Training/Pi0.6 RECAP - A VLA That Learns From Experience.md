---
imported_title: "Pi0.6 RECAP: A VLA That Learns From Experience"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/Pi0.6 RECAP - A VLA That Learns From Experience.md"
imported_reason: "Most relevant prior for real-world experience, corrections, and VLA improvement."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# π*₀.₆: A VLA That Learns From Experience

- **Title:** π*₀.₆: a VLA That Learns From Experience
- **Authors:** Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, ... Sergey Levine, Chelsea Finn, Karol Hausman, et al.
- **Venue:** arXiv preprint (arXiv:2511.14759)
- **Year:** 2025
- **Affiliations:** Physical Intelligence


## 主题 - 通过真实世界经验和强化学习改进VLA

## 背景
VLA模型通过大规模模仿学习（预训练+SFT）获得了灵活的任务执行能力，但要在真实世界中达到实用级别的鲁棒性和速度，仅靠离线演示是不够的。就像人类需要通过反复练习才能精通一项技能，VLA也需要从自主部署的经验中持续学习。然而，将RL应用于大规模flow matching VLA面临三大挑战：(1) 如何设计适用于flow-based模型的可扩展离线RL方法；(2) 如何有效整合异构数据（演示、自主rollout、人工纠正）；(3) 如何在真实世界中设置稀疏、模糊的奖励信号进行RL训练。

## 现有局限与研究问题
- 纯模仿学习的VLA从未观察自身动作后果，存在compounding error和distribution shift问题
- 现有VLA RL方法（PPO/REINFORCE变体）依赖policy gradient，需要tractable log-likelihood，但flow matching模型不提供此项，难以直接应用
- 在线RL（如PPO）在大模型+真实机器人场景下采样效率极低，难以扩展
- AWR等加权回归方法虽可用于离线设置，但会大幅丢弃或降权数据，实质上退化为filtered imitation learning，无法充分利用次优数据
- 真实世界任务的奖励信号天然稀疏（episode级别的成功/失败），且需要人工标注

## 贡献
- 提出**RECAP**（RL with Experience and Corrections via Advantage-conditioned Policies）：一种通用的离线RL框架，使VLA能够从真实世界部署经验中持续自我改进
- 设计**Advantage Conditioning**策略提取方法：训练一个distributional value function估计每个状态-动作对的advantage，将二值化advantage indicator作为额外条件输入VLA（类似classifier-free guidance），避免了对flow matching模型log-likelihood的需求
- 训练**distributional value function**：使用较小VLM backbone（670M Gemma 3），将return离散化为201个bin进行分类预测，支持多任务、多语言条件
- 整合**异构数据源**：演示数据、自主rollout（带成功/失败标签）、专家遥操作纠正（intervention），所有数据统一用于value function和policy训练
- 在真实世界复杂任务上验证：叠衣服（11种衣物）、制作浓缩咖啡（专业咖啡机）、组装纸箱（工厂场景），throughput提升2倍以上，失败率降低约2倍
- 实现工业级持续运行：连续13小时制作咖啡、连续2小时折叠衣物，无需人工干预

## 方法论
- **基础模型 π₀.₆**：基于π₀.₅演进，使用Gemma 3（4B）作为VLM backbone + 860M参数的action expert（flow matching），通过Knowledge Insulation (KI)训练流程端到端联合训练；π*₀.₆在π₀.₆基础上增加advantage indicator条件输入能力
- **RECAP三步迭代流程**：
  1. **数据收集**：在真实机器人上部署VLA，执行自主rollout并标注episode级成功/失败；可选地由专家遥操作者在自主执行过程中提供在线纠正（intervention），纠正动作标记为advantage=positive
  2. **Value Function训练**：使用所有已收集数据（演示+自主数据）训练distributional value function V^π_ref，将归一化的return-to-go离散化为B=201个bin，通过cross-entropy loss训练分类器；value function使用与VLA相同架构但更小的VLM backbone（670M）
  3. **Advantage-conditioned Policy训练**：从value function计算每个(o_t, a_t)的advantage A^π_ref，设定任务相关阈值ε_ℓ（30th percentile），二值化为improvement indicator I_t；将"Advantage: positive/negative"作为文本token注入VLA输入序列，在所有数据上训练VLA同时预测有/无advantage conditioning的动作（类似CFG的unconditional/conditional训练）
- **推理时**：设置I_t = True（advantage: positive），可选使用classifier-free guidance (β>1)进一步增强optimal动作的采样概率
- **奖励设计**：使用极简的episode级稀疏奖励——成功r_T=0，失败r_T=-C_fail，中间步r_t=-1；value function学习预测距成功的剩余步数
- **与PPO/AWR对比**：PPO在off-policy+flow matching设置下不稳定（需极小trust region η=0.01）；AWR通过importance weighting大幅降权次优数据；RECAP通过advantage conditioning在所有数据上训练，同时利用好的和差的经验，效果显著优于两者
- **训练规模**：预训练使用数万小时多机器人演示数据；每轮RECAP收集约300-600条自主轨迹（4台机器人），迭代2轮即可获得显著提升
