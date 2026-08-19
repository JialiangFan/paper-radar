---
imported_title: "Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models"
imported_from: "/Users/jfan/ND/看论文/VLA-post-training/papers/Flow Policy Optimization for VLA Models.md"
imported_reason: "Relevant because modern VLAs often use flow/diffusion action heads."
tags:
  - imported-from-previous-vault
  - safe-vla
---

# Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models

- **Title:** Reinforcement Fine-Tuning of Flow-Matching Policies for Vision-Language-Action Models
- **Authors:** Mingyang Lyu, Yinqian Sun, Erliang Lin, Huangrui Li, Ruolin Chen, Feifei Zhao, Yi Zeng
- **Venue:** arXiv preprint (arXiv:2510.09976)
- **Year:** 2025
- **Affiliations:** Institute of Automation, Chinese Academy of Sciences; University of Chinese Academy of Sciences (UCAS); Long-term AI


## 主题 - Flow-matching VLA强化学习微调

## 背景
Vision-Language-Action (VLA) 模型（如OpenVLA、Octo、π₀）通过大规模行为克隆预训练获得了广泛的语义理解和任务执行能力，但其性能受限于离线demonstration数据的质量与覆盖范围。Reinforcement Learning (RL) 为通过在线交互突破imitation learning上限提供了有前景的路径。然而，传统policy gradient方法（如PPO、TRPO）依赖显式policy ratio计算，而flow-matching模型的action likelihood在解析上不可计算，需要求解ODE和Jacobian trace，这使得常规RL方法在计算上不可行。

## 现有局限与研究问题
- Flow-matching策略的log-likelihood不可解析计算，导致importance sampling所需的policy ratio无法直接获取，传统policy gradient方法无法适用
- Reward-weighted supervised learning方法虽规避了likelihood计算，但缺乏主动探索能力，难以发现超越离线数据分布的新行为
- 现有RL for VLA方法（如VLA-RL、ReinFlow、Flow-GRPO）或依赖autoregressive head，或引入stochastic relaxation，尚未在flow-matching架构上实现稳定高效的在线RL
- 稀疏奖励和接触丰富（contact-rich）的操作环境对在线学习的稳定性提出了额外挑战

## 贡献
- 提出Flow Policy Optimization (FPO)框架，通过conditional flow-matching (CFM) objective的per-sample loss变化量构建likelihood-free的policy ratio代理，桥接flow-matching策略与PPO-style更新，绕过显式density estimation和Jacobian计算
- 设计structure-aware credit assignment机制，在action latent space中利用模型训练目标（CFM loss）作为per-sample改进信号，结合clipped surrogate objective实现trust-region控制
- 引入multi-step latent Euler exploration，通过在actor的latent dynamics中进行多步积分生成时序相关的扰动，促进多样性探索
- 采用Q-ensemble critic机制，通过多个Q函数的最小值提供保守value估计，在稀疏奖励环境中增强训练稳定性
- 在LIBERO benchmark和ALOHA Transfer Cube任务上，π₀-FPO以87.2%平均成功率超越OpenVLA、Octo、Diffusion Policy、GRAPE、π₀-FAST等六个强baseline，LIBERO-Long上达到65.3%，ALOHA-sim上超过baseline 1.5倍以上

## 方法论
- **Likelihood-Free Ratio Proxy**：计算同一(state, latent)对在rollout策略与当前策略下的CFM loss差值ΔℓCFM,t，经batch standardization后通过指数映射exp(βz_t)转换为单调的ratio proxy ρ_t，替代不可计算的π_θ/π_θ_old
- **Clipped Surrogate Actor Update**：将ratio proxy ρ_t与GAE advantage Â_t结合，采用PPO-style的clip(ρ_t, 1-ε, 1+ε)·Â_t目标函数，在每个minibatch内standardize advantage并通过ρ_t截断梯度，防止策略崩溃
- **Q-Ensemble Critic**：使用M个action-value函数{Q_ϕᵢ}的集成，temporal-difference target取集成最小值min_i Q(s_{t+1}, x'_{t+1})以抑制过估计偏差，通过Polyak averaging更新target networks，advantage通过GAE从集成最小值V(s)计算
- **Multi-Step Latent Euler Exploration**：从采样的latent x_t⁽⁰⁾出发，沿CFM velocity field v_θ进行K步Euler积分x_t⁽ᵏ⁺¹⁾ = x_t⁽ᵏ⁾ + η·v_θ(x_t⁽ᵏ⁾, τ⁽ᵏ⁾ | s_t)，生成与generative structure对齐的平滑、时序相关的探索扰动
- **Rollout-Update交替训练**：rollout阶段冻结actor参数θ_old收集轨迹并缓存CFM loss至sliding-window buffer；update阶段重新计算当前actor的CFM loss、构建ratio proxy、更新actor和critic ensemble，通过限制buffer大小控制分布偏移
