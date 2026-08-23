# SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning

- **Title:** SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning
- **Authors:** Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, et al.
- **Venue:** arXiv preprint (arXiv:2509.09674)
- **Year:** 2025
- **Affiliations:** Tsinghua University, Shanghai AI Lab, Shanghai Jiao Tong University, Peking University, The University of Hong Kong


## Topic - RL Framework for VLA Models

## Background
Vision-Language-Action (VLA) models have become a dominant paradigm for robotic manipulation, typically trained via large-scale pretraining followed by supervised fine-tuning (SFT) on expert trajectories. However, SFT requires costly human-operated robot trajectory data that is scarce and difficult to scale. Recent breakthroughs in Large Reasoning Models (e.g., DeepSeek-R1) have demonstrated that reinforcement learning (RL) with simple outcome rewards can substantially enhance step-by-step reasoning, motivating the exploration of analogous approaches for VLA models.

## Limitations & Research Problem
- **Data scarcity**: High-quality human-operated robot trajectories required for SFT are prohibitively expensive to collect, severely limiting scalability
- **Poor generalization**: SFT-trained VLA models degrade significantly on unseen tasks, environments, or objects, particularly in compositional, long-horizon, and distribution-shifted settings
- **Unique challenges of RL for VLAs**: Unlike LLMs, VLA rollouts require multi-round interactive sampling with the environment, which is substantially slower and more costly; traditional robot RL methods rely on hand-crafted process rewards with poor transferability
- **Core research question**: Can RL enhance VLA models' capacity to generate accurate actions step by step, analogous to its success in improving LLM reasoning?

## Contributions
- Proposed SimpleVLA-RL, an efficient end-to-end online RL framework for VLA models built upon veRL, featuring VLA-specific interactive trajectory sampling, scalable parallel multi-environment rendering, and optimized loss computation
- Adopted a simple binary outcome reward (1 for task success, 0 for failure), avoiding complex process reward engineering while maintaining scalability and cross-environment applicability
- Introduced three exploration-enhancing strategies: Dynamic Sampling (filtering all-success/all-failure groups), Clip Higher (asymmetric clipping range [0.8, 1.28]), and Higher Rollout Temperature (T=1.6), each yielding 10-15% performance improvements
- Achieved SoTA on LIBERO (99.1% average), with +30.6 and +30.5 gains on RoboTwin 1.0 and 2.0 respectively, surpassing all baselines
- Demonstrated RL's effectiveness in overcoming data scarcity: with only one demonstration trajectory plus RL, LIBERO-Long success rate improved from 17.3% to 91.7%, even surpassing full 500-trajectory SFT
- Discovered the "pushcut" phenomenon: during RL training, the policy autonomously discovers novel manipulation strategies absent from demonstration data (e.g., pushing instead of grasp-move-place), paralleling the "Aha Moment" in DeepSeek-R1
- Sim-to-real experiments showed that simulation-trained RL policies transfer effectively to the real world, improving average success rate from 17.5% to 38.5%

## Methodology
- **Base model**: Built on OpenVLA-OFT (LLaMA2-7B backbone) with discrete action token output, naturally compatible with PPO-like RL algorithms for probability distribution sampling and policy gradient computation
- **Interactive VLA Rollout**: Unlike LLM single-pass generation, VLA rollout requires environment interaction at each timestep for updated observations, enabling closed-loop control; synchronous multi-environment parallel rendering accelerates sampling
- **Outcome Reward Modeling**: Trajectory-level binary reward (success=1, failure=0), uniformly propagated to all action tokens in the trajectory, avoiding task-specific reward engineering
- **Training objective**: GRPO algorithm with KL divergence regularization removed (following DAPO), eliminating the need for a reference model, reducing memory consumption, and encouraging broader exploration
- **Dynamic Sampling**: Filters groups with uniform rewards during rollout to ensure non-zero advantage estimates and stable gradients
- **Experimental setup**: Evaluated on LIBERO (long-horizon multitask), RoboTwin 1.0 (bimanual), and RoboTwin 2.0 (domain randomization) benchmarks; trained on 8x NVIDIA A800 80GB GPUs
- **Failure mode analysis**: RL fails completely when the SFT model has zero initial capability (no successful trajectories means no positive reward signal); model prior capability is positively correlated with RL effectiveness, with a minimum competence threshold required
