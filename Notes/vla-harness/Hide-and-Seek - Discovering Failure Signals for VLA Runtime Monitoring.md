# Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring

> arXiv: 2605.30834 | 年份: 2026

## 主题
Coarsely supervised VLA failure detection

## 背景
Vision-Language-Action (VLA) 模型能让机器人follow自然语言指令并泛化到多样任务，但在真实部署中仍会出现 execution failures，例如一次细微的 grasp 失败若未被察觉，可能级联成掉落物品甚至更高代价的后果。因此在执行过程中实时检测失败（runtime monitoring）是 embodied system 稳健部署的关键环节。本文作者来自 University of Wisconsin–Madison 与 Georgia Institute of Technology，把 failure detection 建模为一个只有 trajectory-level 标签的 coarsely supervised learning 问题。

## 现有局限与研究问题
- **Limitation:** 现有失败检测方法在两个维度上受限。(1) *Supervision cost*：step-level 失败标注昂贵且难以规模化，需要专家在 long-horizon、stochastic 的轨迹上标出精确的错误时间戳；近期工作 SAFE 通过把 trajectory-level 标签均匀赋给所有 timestep 来回避标注，但这会把 failure onset 之前的正常动作误标为失败，引入大量 label noise。(2) *Computational practicality*：基于 action resampling 的多采样方法与外部 VLM judge 推理开销巨大，难以满足实时部署；OOD-based 方法在 unseen 任务上泛化差；多数先前方法还是为固定任务上的 specialist policy 设计的。
- **Problem:** 在**没有任何 step-level 标注**、仅有 trajectory-level 成功/失败标签的条件下，如何学到一个轻量、可实时运行的 fine-grained failure detector，使其能够定位 failure-indicative action 并在合适时机报警（Definition 3.1，Coarsely Supervised Failure Detection）？

## 贡献
- 提出 **Hide-and-Seek**：一个轻量的 runtime failure detection 框架，首次把 coarsely supervised learning 与 embodied failure detection 建立联系，仅凭 trajectory-level 监督即可发现 failure-indicative actions。
- 设计双粒度 contrastive objective：在轨迹之间（inter-trajectory）与轨迹之内（intra-trajectory）同时区分 failure-indicative 与 non-failure actions，把粗粒度的轨迹标签转化为**时间结构化**的 failure signal。
- 在 LIBERO、VLABench 两个仿真 benchmark 与真实机器人平台上，跨 OpenVLA、π0、π0.5 三种代表性 VLA policy（覆盖 autoregressive 与 flow-matching 两种范式）做系统评测，在 seen / unseen 任务上均达到 SOTA，并给出实用的 accuracy–timeliness trade-off。

## 方法论
- **问题形式化**：每个 timestep 从 VLA 的 action token / action head 提取内部 action embedding $h_t \in \mathbb{R}^d$，rollout 轨迹记为 $\tau = (h_1,\dots,h_T)$，只有轨迹级标签 $y(\tau)\in\{0,1\}$。检测器 $f_\phi$ 为 sigmoid 输出的序列模型，把前缀 $\tau_{\le t}$ 映射为 failure score $s_t \in [0,1]$。
- **Inter-trajectory contrastive loss（式 2）**：margin-based loss，要求 failure trajectory 中**最具失败指示性**的那一步得分高于 success trajectory 中最像失败的 hardest false-positive 步（如短暂犹豫或已成功恢复的笨拙中间姿态），margin 为 $m_r$。该目标不假设失败发生在何处，而是自适应地"seek"出隐藏的失败信号。
- **Intra-trajectory contrastive loss（式 3）**：定义 proxy failure onset $t_{\text{onset}} = \arg\max_t (s_t - s_{t-1})$（分数上升最陡处），要求 post-onset 平均分超过 pre-onset 平均分，margin 为 $m_o$，从而在无时间标注的情况下塑造时间上的分数动态。附录 C.1 显示该 proxy 与人工标注 onset 高度接近。
- **总目标（式 4）**：$\mathcal{L} = \mathcal{L}_{\text{inter}} + \lambda \mathcal{L}_{\text{intra}}$。
- **实现细节**：backbone 默认为单层 LSTM；autoregressive policy（OpenVLA）跨层与自由度平均 embedding，flow-matching policy（π0/π0.5）在最后一步 denoising 的 velocity prediction head 之前抽 hidden state 并对齐 action chunk；用窗口大小 $w$ 的非重叠 sliding-window average pooling 降低时间冗余。
- **Runtime monitoring via Conformal Prediction（式 5）**：用 one-sided functional conformal prediction 在 held-out 的 $C$ 条成功轨迹上标定 time-varying 阈值 $\zeta_t = \mu_t + b_t$，在 exchangeability 假设与显著性水平 $\alpha$ 下保证成功 rollout 的 trajectory-level false alarm rate 有界；首个 $s_t \ge \zeta_t$ 的时刻即 detection time。
- **评测指标**：balanced accuracy (bACC，主指标)、weighted accuracy (wACC)、time-weighted accuracy (TWA，同时惩罚过晚检测)；结果在 $\alpha \in \{0.15, 0.20, 0.25\}$ 上平均、3 个随机种子上平均。共对比 12 个 action-based baseline，分 OOD-based（Mahalanobis、Cosine k-NN、PCA-KMeans、RND、LogpZO）、multi-sampling（Cluster Entropy、EigenScore、STAC、ACE，每步 $N=10$ 采样）、classifier-based（SAFE-LSTM、SAFE-MLP）与 token uncertainty-based（Entropy、NLL，仅 OpenVLA）四类。

## 实验与关键数字
- **LIBERO-10（Table 1）**：OpenVLA（成功率 51.0%）上 Hide-and-Seek 取得 seen bACC 0.852 / wACC 0.853 / TWA 0.660，unseen 0.834 / 0.828 / 0.663，全面优于所有 baseline；π0（成功率 84.2%）上 seen 0.885 / 0.926 / 0.693，unseen 0.892 / 0.921 / 0.705。
- **OOD 方法的泛化缺陷**：Mahalanobis 在 OpenVLA 上 bACC 从 seen 的 67.0% 跌到 unseen 的 51.3%。
- **VLABench（Table 2）**：π0.5（成功率 40.3%）上 seen bACC 0.856 / wACC 0.827 / TWA 0.662，unseen 0.713 / 0.709 / 0.608；相对最强的 SAFE-MLP，seen 上 +6.8% bACC、+8.1% TWA，unseen 上 +7.2% bACC、+10.8% TWA。
- **真实机器人（Table 3，UFactory xArm 6 + Intel RealSense D435，π0.5）**：CUBE 任务成功率 61.2%，KITCHEN 63.7%。Hide-and-Seek 在四个设定下均取得最佳 TWA：CUBE seen 0.966 bACC / 0.852 TWA、unseen 0.914 / 0.800；KITCHEN seen 0.968 / 0.863、unseen 0.972 / 0.876。在 unseen CUBE 上相对 SAFE-MLP 提升 +11.7% bACC、+15.0% TWA；SAFE-MLP 在 seen CUBE 上达 99.2% bACC 但 unseen 跌至 79.7%，稳定性远逊。多采样方法因推理开销过大被排除在真机实验之外。
- **对比 VLM-based runtime monitor（Table 6）**：以 Qwen3-VL-8B-Instruct 在 LIBERO-10 + OpenVLA 上做逐帧成功/失败判定，bACC 0.712、单步延迟 2.343 s；Hide-and-Seek bACC 0.843、延迟 0.001 s（单张 NVIDIA A6000），即 **+13.1% bACC** 且速度快 **2,000×** 以上。
- **对比 uniform trajectory-level labeling（Fig. 4a）**：+19.4% bACC（OpenVLA）、+18.6% bACC（π0）。
- **Loss 组件消融（Table 5）**：仅 $\mathcal{L}_{\text{inter}}$ 已达 0.825（OpenVLA）/ 0.856（π0），分别超过最强 baseline SAFE-MLP +2.6% / +2.1%；仅 $\mathcal{L}_{\text{intra}}$ 退化至 0.579 / 0.601；两者结合为 0.843 / 0.888（相对仅 inter 再 +1.8% / +3.2%）。
- **Backbone 消融（Table 4）**：LSTM 0.843 / 0.888，GRU 0.834 / 0.893，Transformer 0.804 / 0.824，MLP 0.765 / 0.743；带时间上下文的 backbone 显著优于 per-step MLP。
- **超参敏感性（Fig. 4b/4c）**：margin 扫描中各配置 bACC 相对均值波动 <4%，最佳为 $m_r=1.0, m_o=0.5$（88.8% bACC）；窗口大小 OpenVLA 最优 $w=4$、π0 最优 $w=8$（与 π0 的 action chunk / replanning interval 对齐）。
- **Accuracy–timeliness trade-off（Fig. 3）**：在 $\alpha \in [0.01, 1.0]$ 上扫描操作点，Hide-and-Seek 的曲线在 OpenVLA 与 π0 上都最靠近左上角；参考的 failure onset 由 GPT-5.2 在录制视频上标注。
