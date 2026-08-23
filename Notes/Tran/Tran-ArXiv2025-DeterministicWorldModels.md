# Deterministic World Models for Verification of Closed-loop Vision-based Systems

## 主题
Vision-based System Verification

## 背景
闭环 vision-based control systems 日益应用于安全关键领域，这类系统依赖端到端控制器处理图像并操控物理设备。验证此类系统面临两大挑战：准确建模复杂视觉环境的困难性，以及高维图像带来的计算可扩展性瓶颈。近期研究使用 generative world models（如 cGAN）作为摄像头替代模型，但其依赖 stochastic latent variables 引入了不必要的验证过近似误差。

## 现有局限与研究问题
- **Limitation:** 现有基于 cGAN 的 world model 使用 stochastic latent variables 来生成图像多样性，但 latent variables 缺乏物理可解释性（lack physical interpretability），难以定义有效的输入边界用于 reachability analysis；同时扩大 latent bounds 会导致 reachable sets 急剧膨胀，引入过大的 overapproximation error。符号化方法（symbolic techniques）则受限于高度结构化的环境，无法处理动态复杂场景。
- **Problem:** 如何构建一个无需 stochastic latent variables 的可验证 world model，使其能与 star-based reachability analysis 无缝集成，并为闭环 vision-based systems 提供严格的安全保证？

## 贡献
- 提出 Deterministic World Model (DWM)，直接将系统物理状态映射为图像，消除不可解释的 stochastic latent variables，确保输入边界精确且具有物理意义
- 设计双目标损失函数：image reconstruction loss（加权 MSE，重点关注语义重要区域）+ controller difference loss（确保生成图像产生与真实图像一致的控制动作）
- 首次将 Star/ImageStar-based reachability analysis 应用于闭环 vision-based systems 的验证，将 DWM 输入维度限制为物理状态维度以解决可扩展性问题
- 使用 conformal prediction 建立 world model 与真实系统之间轨迹偏差的统计上界，将 surrogate system 的验证结果转移到真实系统

## 方法论
- **DWM 架构：** 采用 state-to-image decoder g_θ: S → I，由全连接层后接转置卷积层构成，输入为低维物理状态（如位置、速度），输出为高维灰度图像（如 96×96）
- **训练损失：** 总损失 L(θ) = L_rec(I, Î) + λL_ctrl(I, Î)，其中 L_rec 使用基于像素强度的加权 MSE（暗区域/物体赋予高权重 w_h，亮背景赋予低权重 w_l），L_ctrl = ||C(Î) - C(I)||² 约束控制行为一致性
- **Star-set 可达性分析：** 用 Star set S_0 = {s = c_0 + V_0α | C_0α ≤ d_0, l_0 ≤ α ≤ u_0} 表示初始状态不确定性集合；逐层传播通过 DWM 和 CNN 控制器（affine layers 精确映射，nonlinear activation layers 使用 StarV 的 sound over-approximation）；输出 ImageStar 表示所有可能生成图像的完整包络
- **闭环验证流程：** 在每个时间步，将当前状态集 R_t 通过 DWM 生成 ImageStar I_img，再通过 CNN 控制器计算控制动作集 U，使用 PyBDR 计算下一步 reachable state set R_{t+1} = R_dyn(R_t, U_t)，迭代得到有限时间 reachable tube
- **Conformal prediction 转移保证：** 定义轨迹偏差的 non-conformity scores，使用校准数据集计算统计上界，以概率 1-α 保证真实系统轨迹包含在 world model reachable tube 的扩展范围内
- **实验验证：** 在 CartPole、MountainCar、Pendulum 三个 OpenAI Gym benchmarks 上验证，DWM 相比 latent-variable baseline 生成更紧致的 reachable sets 和更高的 F1 verification accuracy
