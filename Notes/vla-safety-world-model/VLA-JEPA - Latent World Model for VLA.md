# VLA-JEPA - Enhancing Vision-Language-Action Model with Latent World Model

> 作者: Jingwen Sun et al. (2026, arXiv 2602.10098)

## 主题

Leakage-free JEPA pretraining for VLA

## 背景

在互联网规模的无标注视频上预训练 VLA 策略很有吸引力，因为机器人动作标注数据昂贵且覆盖面窄。为此出现了一批 latent-action pretraining 方法（LAPA、UniVLA、villa-X、Genie 系列等），先从视频中学出 latent action 与状态转移结构，再迁移到下游控制。本文指出这类目标函数普遍仍锚定在 pixel 层面，学到的并不是控制真正需要的 action-relevant state transition semantics。

## 现有局限与研究问题

- **Limitation:**
  - **Pixel 层监督偏向外观而非动作**：直接预测未来像素或压缩帧间差分，监督信号被纹理、光照、背景杂乱、视角变化主导；这些因子方差大但可控性低，容易预测却与策略需要掌握的自由度关系薄弱。
  - **真实视频放大 noisy motion**：人类视频/野外视频中相机运动与非因果的背景变化可能强于交互引起的状态变化，导致 latent action 退化成「delta-frame 噪声运动编码器」。
  - **信息泄漏使 latent action 塌缩为 shortcut**：不少 pipeline 把当前观测和未来观测送进同一模块，或让未来上下文影响 latent 变量，latent action 于是直接编码「未来本身」，语义为空——能对上训练损失，但不是有意义的控制因子。
  - **多阶段训练复杂脆弱**：representation pretraining → latent-action learning/alignment → policy learning 的三段式流程带来工程复杂度与阶段间不一致。
  - 已有缓解手段（optical-flow 约束、object-centric 先验）把 latent action 偏向手工设计的视觉先验，换环境后容易系统性失效。
- **Problem:** 如何在不做 pixel 重建、不引入未来信息泄漏、且只用单阶段预训练的前提下，让 VLA 从无动作标注视频中学到真正 action-relevant 的隐空间状态转移（latent world model），并把它有效迁移到下游机器人控制？

## 贡献

- 系统分析 latent-action pretraining 的四类失效模式（pixel-tethered 目标、真实视频噪声运动、未来信息泄漏、多阶段脆弱性），把问题归结为「隐式锚定在 pixel variation」这一共同根因。
- 提出 VLA-JEPA：JEPA 式的 **leakage-free state prediction** 预训练框架——target encoder 只用未来帧构造监督目标，student 路径（VLM backbone）只看当前观测，未来帧永不作为输入，从设计上堵死 shortcut。
- 在 latent 空间而非 pixel 空间做预测对齐，得到对相机运动与无关背景变化更鲁棒的 dynamics abstraction。
- 把流程简化为「JEPA 预训练 + action-head 微调」的两步 recipe，去掉了以往 latent-action pipeline 的多阶段复杂度与辅助模块。
- 支持人类视频与机器人数据的统一（cross-domain）训练：人类视频只用 alignment loss，机器人数据用 alignment + action prediction 联合目标。
- 在 LIBERO、LIBERO-Plus、SimplerEnv 与真机 Franka 上验证：LIBERO 平均成功率 97.2（最高），LIBERO-Plus 平均 79.5（7 个扰动维度中 5 个最佳），真机 ID 与 object-layout OOD 均优于 π₀ / π₀.₅。

## 方法论

- **Backbone**：Qwen3-VL（Qwen3 + SigLIP-2）作为核心 VLM；引入两组可学习特殊 token `<latent_i>`（第 i 个时间步的 latent action）与 `<action>`（动作条件），每个 `<latent_i>` 在输入序列中复制 K 次以支持变长 latent action 编码。
- **World state encoder**：用冻结的 self-supervised **V-JEPA2** encoder 对每个视角编码，再按视角拼接成统一的 world state $s_{t_i} = \|_v F(I_{v,t_i})$——多视角统一表示而非单视角。
- **Latent action 生成**：VLM 只接收初始时刻 $t_0$ 的多视角观测与语言指令 $\ell$，输出 $z_{t_i} = p^{VLM}_\theta(\langle latent_i\rangle \mid \{I_{j,t_0}\}, \ell)$；未来帧从不进入 VLM 输入端。
- **Latent world model**：自回归 Transformer 世界模型 $\hat{s}_{t_{i:i+1}} = p^{WM}_\theta(s_{t_{0:i}}, z_{t_{0:i}})$ 预测下一段 latent 状态 chunk；注意力机制为 time-causal——同一时间步内 latent token 与 world state token 双向全注意力，跨时间步严格因果、屏蔽未来。
- **训练目标（JEPA 对齐）**：$\mathcal{L}_{WM} = \sum_k \mathbb{E}[\hat{s}_{t_k} - s_{t_k}]$。论文从 JEPA/ELBO 角度解释：冻结 target encoder $F(\cdot)$ 带 stop-gradient 且输出确定性 embedding，KL 项消失，ELBO 退化为 latent 空间的重建损失。teacher-forcing 联合优化 WM 与 VLM。
- **动作头**：conditional flow matching。以 $z_a = p^{VLM}(\langle action\rangle \mid I_{t_0}, \ell, \langle latent_i\rangle)$ 为条件，学习速度场 $v_\theta(a_t, t\mid z_a)$ 拟合线性插值诱导的目标流；推理时从噪声积分得到动作轨迹 $\hat a_{0:H}$。总目标 $\mathcal{L} = \mathcal{L}_{FM} + \beta\mathcal{L}_{WM}$。
- **数据与实现**：人类视频用 Something-Something-v2（220K 段）做 latent world model 预训练，机器人端用 Droid（76K 轨迹）；下游在 LIBERO（约 2K 演示）、Fractal/BridgeV2（SimplerEnv）、真机 100 条演示上微调；8×A100。
- **关键消融**：(1) 去掉人类视频后 LIBERO-Plus 从 79.5 掉到 62.9，且人类视频比例越高各扰动维度成功率越高——说明人类视频主要增强既有技能的鲁棒性（如失败后重新张开夹爪再抓，repeated grasping）而非引入新的动作执行能力；(2) 未来视频 horizon $T\in\{4,8,16\}$，$T=8$ 平均最好，$T$ 太小信息不足、太大引入冗余；(3) 注意力可视化显示 VLA-JEPA 的 latent action token 聚焦机械臂、手与被操作物体，而 LAPA 注意力弥散（泄漏导致 latent action 退化为目标图像的压缩表示）、UniVLA 过度偏向语义而关注无关背景。

## 与 STL×VLA 主线的关联

这篇提供了一个可用的「前瞻信号源」：latent world model 在推理链路里显式预测未来 latent world state chunk $\hat s_{t_{i:i+1}}$（horizon 约 4–16 帧），原则上可以在动作真正执行前对预测状态求值，这正是 runtime verification / predictive monitoring 需要的 lookahead。但论文本身完全没往这个方向走——世界模型只作为预训练与联合微调的辅助对齐目标，推理时不用于监控，也没有任何时序规范、安全约束或量化安全指标；LIBERO / LIBERO-Plus / SimplerEnv 度量的都只是 success rate，鲁棒性是靠分布扰动（camera/light/background/layout/noise 等 7 维）间接刻画的，属于 distributional robustness 而非 specification compliance。

论文中唯一与安全直接相关的是真机实验的定性观察：π₀.₅ 指令跟随更准但「position control frequently violates the safety boundaries of the robot arm」导致执行失败，而 VLA-JEPA 抓错物体更多、却 rarely breaches the robot arm's safety constraints——这恰好是一个「任务正确性 vs 安全约束满足」权衡的实例，但作者只是顺带提及，既没定义安全谓词也没统计违约率，正好是 STL 可以形式化并量化的空白。

留给 STL×VLA 的空间有两处：其一，V-JEPA2 latent 状态不可解释，要把 STL 原子谓词（距离、接触、越界、力/速度阈值）落到这个隐空间，需要额外的 predicate probe / grounding head，或改用可解释的状态通道；其二，人类视频带来的 repeated grasping 属于隐式 recovery 行为，与 STL 里「违约后在有界时间内恢复」的时序模式天然对应，但论文只在附录做了案例展示，没有可验证的时序保证。
