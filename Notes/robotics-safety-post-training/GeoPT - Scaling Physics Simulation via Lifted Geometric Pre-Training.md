

## 主题
Geometric Pre-Training for Physics Simulation

## 背景
神经模拟器（Neural Simulators）作为经典数值求解器的高效替代品，正在加速科学发现和工程设计中的物理仿真。然而，实现工业级精度的瓶颈在于生成高保真训练数据的高昂计算成本（例如 DrivAerML 气动数据集中，单个样本需要 6.1×10⁴ CPU 小时）。虽然海量的 3D 几何数据可从公开仓库免费获取，但在静态几何上进行自监督预训练会忽略动力学信息，反而可能导致下游物理任务的性能下降（negative transfer）。

## 现有局限与研究问题
- **Limitation:** 神经模拟器的训练严重依赖数值求解器生成的标注数据，每个样本的计算成本随几何复杂度和物理精度急剧增长，严重限制了模型的可扩展性。
- **Limitation:** 现有的自监督预训练方法（如预测 SDF、向量距离等）仅在几何的"原生空间"（native space）中学习，忽略了几何与动力学的耦合关系。预训练学到的表示与下游物理任务所需的表示存在根本性不匹配（geometry-physics gap）。
- **Limitation:** 现有物理 Foundation Model（如 Poseidon、DPOT、P3D）仍依赖大量物理仿真数据进行预训练，且局限于特定物理族（如规则网格上的 2D/3D 流体），无法泛化到工业级仿真任务。
- **Problem:** 如何仅利用大量无标注的几何数据进行预训练，使神经模拟器能够学习到反映几何-动力学耦合关系的表示，从而在少量物理标签下加速收敛并提升精度？

## 贡献
- 提出 **Dynamics-Lifted Geometric Pre-Training** 范式：通过为几何数据附加随机采样的合成速度场，将预训练从静态几何的原生空间"提升"（lift）到几何-动力学联合空间，使模型无需物理标签即可学习动力学感知的表示。
- 构建了 **GeoPT**——一个统一的物理仿真预训练模型，在 ShapeNet 的 10,000+ 几何体上预训练超过 100 万个样本，适用于气动、水动力、碰撞仿真等多种下游任务。
- 在 5 个工业级物理仿真 benchmark 上验证，GeoPT 减少 20-60% 的物理数据需求，加速收敛达 2 倍，且在模型规模和数据量上均展现良好的 scaling 特性。
- 从理论角度证明 GeoPT 的预训练等价于求解带粘性边界（sticking boundary）的无碰撞输运方程，揭示其学习的是满足质量守恒的通用物理先验。

## 方法论
- **核心思想——Lifted Pre-Training：** 下游物理仿真依赖几何 G 和动力学条件 S 的耦合，而几何预训练仅涉及 G。GeoPT 通过为每个几何体随机采样合成速度场 V（每点独立采样 v ~ Unif(B^C)），构造粒子在几何边界约束下的运动轨迹，将自监督信号从静态几何特征（向量距离）扩展为沿轨迹的动态几何特征序列 h_G(x_{0:τ})。
- **预训练目标：** 模型 F_θ 接收查询点位置 x、几何 G 和速度场 V，预测轨迹上各时间步的向量距离序列，即 L^pre_lifted = E[||F_θ(x; G, V) - h_G(x_{0:τ})||²]。默认离散化步数 τ=2，每个几何生成 100 组不同的动力学场。
- **预训练数据：** 使用 ShapeNet（Chang et al., 2015）中汽车、飞机、船舶三类共 ~13,000 个几何体，采样 32,768 个体积点和 4,096 个表面点，生成约 130 万个样本（~5TB）。几何特征计算使用 FCPW 加速的光线-三角形求交，80 CPU 核上约 3 天完成。
- **Fine-Tuning 适配：** 将随机速度场替换为任务特定的速度场 V_S（如气动中的来流速度、碰撞中的冲击方向），直接在预训练模型上微调，实现统一接口适配不同物理域。
- **Backbone：** 采用 Transolver（Wu et al., 2024）作为默认骨干网络（architecture-agnostic），支持 Base（3M）、Large（7M）、Huge（15M）三种规模。
- **实验设置：**
  - **Benchmark：** DrivAerML（汽车气动）、NASA-CRM（飞机气动）、AirCraft（飞行器气动）、DTCHull（船舶水动力）、Car-Crash（碰撞仿真），以及扩展的 Radiosity（辐射度）任务
  - **基线：** From Scratch Transolver、Geometry-Only Pre-Training（预测向量距离/SDF）、Geometry-Only Conditioning（Hunyuan3D VAE 编码器）、其他骨干（Galerkin Transformer, GNOT, UPT, Transolver++）
  - **评估指标：** Relative L2 error；关注数据效率（data saving）和收敛速度（convergence acceleration）
