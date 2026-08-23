# VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning

- **Title:** VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning
- **Authors:** Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, Ziwei Wang
- **Venue:** arXiv preprint (arXiv:2505.18719)
- **Year:** 2025
- **Affiliations:** Tsinghua Shenzhen International Graduate School (Tsinghua University), Nanyang Technological University


## Topic - Scalable RL for VLA Models

## Background
Large Vision-Language-Action (VLA) models trained via imitation learning on large-scale human demonstrations have shown strong performance across diverse robotic manipulation tasks, yet they suffer from out-of-distribution (OOD) failures due to limited state coverage in offline data. Reinforcement learning (RL), as an exploration-based paradigm, offers a principled way to overcome this limitation by training on online-collected data with unlimited state coverage. Recent successes of RL in enhancing LLM reasoning (e.g., DeepSeek-R1, GRPO) suggest that similar test-time scaling benefits may transfer to robotics, motivating this work.

## Limitations & Research Problem
- VLA models rely on offline imitation learning with limited visited states, causing execution failure in OOD scenarios at test time
- Traditional RL from scratch suffers from data inefficiency, requires extensive reward engineering, and is restricted to low-dimensional state spaces, small-scale networks, and single-task settings
- Robotic manipulation environments provide naturally sparse rewards (binary signals only upon task completion), hindering policy optimization for long-horizon tasks
- No unified algorithmic and systematic framework exists for applying trajectory-level RL to large-scale auto-regressive VLAs
- Core question: Can RL-based test-time scaling benefits, as observed in LLMs, be achieved in robotic manipulation?

## Contributions
- Proposes VLA-RL: the first unified framework that systematically applies online RL to pretrained auto-regressive VLAs, formulating general robotic manipulation trajectories as multi-modal multi-turn conversations
- Introduces the Robotic Process Reward Model (RPRM): a vision-language model fine-tuned to provide reward densification via automatically extracted pseudo reward labels, eliminating the need for manual annotation
- Identifies and validates critical implementation details for training stability and efficiency: curriculum selection strategy, GPU-balanced vectorized environments, batch decoding, and critic warmup
- Achieves state-of-the-art results on 40 LIBERO benchmark tasks using OpenVLA-7B, surpassing the strongest SFT baseline by 4.5% and matching the commercial model pi_0-FAST, with only 48 GPU hours of RL training
- Provides preliminary evidence of inference scaling laws in robotics: performance consistently improves with increased test-time computation

## Methodology
- **Problem formulation**: Formalizes auto-regressive VLA manipulation as an MDP where the state space is the Cartesian product of image space and text token sequences, and the action space consists of discrete token sequences output by VLAs; optimized via PPO with clipped objective and GAE
- **Rollout phase**: Merges updated LoRA weights with the original checkpoint for inference; the agent interacts with the environment to collect trajectories; action log-probabilities are decomposed as the sum of token-level log-probabilities
- **Robotic Process Reward Model**: Reformulates reward modeling as a next-token prediction problem; trained on an autonomous pseudo reward label generation pipeline — (1) Milestone Segmentation: segments trajectories into subtasks based on significant gripper openness changes; (2) Progress Labeling: assigns positive pseudo-rewards at keyframes where end-effector velocity approaches zero
- **Reward densification**: Final reward is the direct sum of the environment's sparse reward and the RPRM-predicted reward, providing more frequent and informative learning signals
- **Curriculum selection strategy**: Adaptive task sampling with probability proportional to exp((0.5 - s_j) / tau), prioritizing tasks near the 50% success rate frontier of the agent's current capabilities
- **Critic warmup**: Pre-trains the value network exclusively for several iterations using trajectories collected by the imitation-pretrained policy before joint policy-value optimization begins, preventing noisy early value estimates from derailing policy gradients
- **GPU-balanced vectorized environments**: Each GPU worker is assigned its own subset of vectorized environments, with an all_reduce operation aggregating environmental states across workers to balance GPU memory consumption
- **Infrastructure**: vLLM-accelerated inference, PyTorch FSDP for distributed training, bfloat16 precision, OpenRLHF-style architecture with 1 dedicated inference GPU and G-1 training GPUs
