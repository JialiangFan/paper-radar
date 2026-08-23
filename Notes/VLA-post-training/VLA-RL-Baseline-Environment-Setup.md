# VLA RL Baseline 环境与训练需求

## 1. LIBERO Benchmark

### 简介
LIBERO 是 VLA RL 领域的标准 benchmark，基于 robosuite + MuJoCo 物理引擎构建。包含多个 task suite：
- **LIBERO-Spatial**: 空间推理任务（简单）
- **LIBERO-Object**: 物体识别任务（简单）
- **LIBERO-Goal**: 目标导向任务（中等）
- **LIBERO-Long**: 长 horizon 多阶段任务（难，**推荐用于实验**）
- **LIBERO-90**: 90 个任务的多任务泛化（难，**推荐用于实验**）

### GitHub
- 官方仓库: https://github.com/Lifelong-Robot-Learning/LIBERO
- HuggingFace fork: https://github.com/huggingface/lerobot-libero

### 安装
```bash
conda create -n libero python=3.8.13
conda activate libero
git clone https://github.com/Lifelong-Robot-Learning/LIBERO.git
cd LIBERO
pip install -r requirements.txt
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 \
    --extra-index-url https://download.pytorch.org/whl/cu113
pip install -e .
```

### 技术栈
```
LIBERO (benchmark/task 层)
  └── robosuite (机器人仿真框架)
       └── MuJoCo (物理引擎)
```

---

## 2. Baseline 代码仓库

| 方法 | GitHub | 基础模型 | RL 算法 |
|---|---|---|---|
| SimpleVLA-RL | https://github.com/PRIME-RL/SimpleVLA-RL | OpenVLA-OFT (7B) | GRPO |
| RIPT-VLA | https://github.com/Ariostgx/ript-vla | OpenVLA-OFT / QueST | RLOO + PPO |
| VLA-RL | https://github.com/ (清华, 待确认) | OpenVLA (7B) | PPO |
| VLA-RFT | https://github.com/OpenHelix-Team/VLA-RFT | VLA-Adapter + Flow Matching | GRPO |
| FPO | 待确认 | Pi0 (Flow Matching) | PPO-style (FPO) |

---

## 3. 硬件需求

### 仿真环境运行（仅 LIBERO）
- 任意 NVIDIA GPU 即可
- 设置 headless 渲染: `export MUJOCO_GL=egl`

### VLA RL 训练

| 方法 | 最低 GPU | 推荐 GPU | 显存/卡 |
|---|---|---|---|
| **RIPT-VLA** (需求最低) | 3× A5000 | 4× A5000/A100 | 24-80 GB |
| **VLA-RL** | 4× A100 | 多卡 A100 | 80 GB |
| **SimpleVLA-RL** | 4× A100 | 8× A800 | 80 GB |
| **VLA-RFT** | 4× A800 | 4× A800 | 80 GB |

### 为什么需要这么多 GPU
1. **VLA 模型 7B 参数** — 单卡放不下完整模型 + optimizer states
2. **并行 Rollout** — RL 需要同时跑多条轨迹，每条都需要 VLA 推理
3. **推理+训练分离** — 通常 1 张卡专做 rollout 推理（vLLM），其余卡做梯度更新

---

## 4. 训练时间

| 方法 | RL 训练步数 | 预估 GPU Hours | 预估墙钟时间 (推荐配置) |
|---|---|---|---|
| **RIPT-VLA** | ~15 次迭代 (低数据) / ~500 步 | ~10-20 h | **半天** (4× A5000) |
| **VLA-RL** | 10,000 步 | **48 GPU hours** (论文明确) | ~6h (8卡) / ~12h (4卡) |
| **SimpleVLA-RL** | ~200-300 RL 步 | ~20-50 h (估计) | ~半天到一天 (8× A800) |
| **VLA-RFT** | 400 步 (RL 部分) | 极短 (但 world model 预训练 150K 步另算) | 几小时 |

### 时间瓶颈分析
```
一次 RL 迭代 ≈
  Rollout (占 80%+ 时间):
    VLA 推理 (~150ms/步) × 512步/轨迹 × 64条轨迹
  Reward 计算 (极快)
  Policy Gradient 更新 (较快)
```

---

## 5. 推荐复现路线

### 第一选择: RIPT-VLA（最容易上手）
- 硬件需求最低: 3-4× A5000 24GB 即可
- 训练最快: 15 次迭代就有明显效果
- 代码开源且文档清晰
- 支持 tokenized 和 regression 两种 action head
- 安装: 参考 https://github.com/Ariostgx/ript-vla

### 第二选择: SimpleVLA-RL（效果最好）
- LIBERO SOTA (99.1%)
- 基于 veRL 框架，工程实现更成熟
- 但需要 8× A800 80GB
- 安装: 参考 https://github.com/PRIME-RL/SimpleVLA-RL/blob/main/SETUP.md

### SFT Baseline: OpenVLA-OFT
所有 RL 方法都基于 OpenVLA-OFT 做 post-training，需要先获取 SFT checkpoint：
- OpenVLA: https://github.com/openvla/openvla
- OpenVLA-OFT: Stanford 发布的优化微调版本
- 训练: 64× A100, 14 天 (预训练); 微调用 LoRA 单卡 A100 即可

---

## 6. 关键依赖库

| 库 | 用途 | 版本建议 |
|---|---|---|
| PyTorch | 深度学习框架 | 2.4.0+ (RL 训练) / 1.11 (LIBERO 仿真) |
| vLLM | 加速 VLA 推理 (rollout 阶段) | 最新版 |
| veRL | RL 训练框架 (SimpleVLA-RL 使用) | v0.2-v0.3 |
| Flash Attention 2 | 加速 transformer attention | 最新版 |
| FSDP | 分布式训练 | PyTorch 内置 |
| robosuite | 机器人仿真 | LIBERO 指定版本 |
| MuJoCo | 物理引擎 | 2.1+ |

---

## 7. 备注

- LIBERO 的 Python 版本要求 (3.8.13) 和 RL 训练框架 (3.10+) 不同，可能需要两个 conda 环境
- 设置 headless 渲染: `export MUJOCO_GL=egl` 和 `export CUDA_VISIBLE_DEVICES=0`
- Safety-CHORES benchmark (SafeVLA 提出) 是安全约束实验的目标环境: https://github.com/PKU-Alignment/SafeVLA

---

*创建时间: 2026-03-30*
*用途: VLA Post-Training 研究的环境搭建与 baseline 复现参考*
