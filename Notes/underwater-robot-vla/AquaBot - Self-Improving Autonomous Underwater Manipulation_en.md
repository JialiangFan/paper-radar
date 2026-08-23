# AquaBot: Self-Improving Autonomous Underwater Manipulation

## Topic
Fully autonomous underwater manipulation system combining behavior cloning with self-learning optimization to surpass human teleoperation performance.

## Background
Underwater robotic manipulation faces significant challenges due to complex fluid dynamics and unstructured environments, which cause most existing manipulation systems to rely heavily on human teleoperation. This reliance on human operators is a major bottleneck -- teleoperation is slow, requires constant human attention, and is limited by communication latency and operator fatigue. Recent advances in imitation learning and self-play optimization offer a path toward autonomous manipulation systems that can learn from human demonstrations and then improve beyond human-level performance.

## Limitations & Research Problem
- **Limitation:** Current underwater manipulation systems depend on human teleoperation due to the difficulty of autonomous control in fluid environments with complex dynamics, poor visibility, and unstructured obstacles. This makes operations expensive, slow, and limited in scale.
- **Problem:** How to build a fully autonomous underwater manipulation system that can learn from limited human demonstrations and then self-improve to surpass human teleoperation performance across diverse real-world tasks.

## Contributions
- AquaBot: a fully autonomous underwater manipulation system that eliminates the need for human teleoperation during deployment
- A two-stage learning pipeline combining behavior cloning from human demonstrations with self-learning optimization that enables the robot to exceed human performance
- Extensive real-world validation across three diverse underwater tasks (object grasping, trash sorting, rescue retrieval), demonstrating 41% speed improvement over human operators
- Open-source release of both hardware designs and software implementation, lowering the barrier to entry for underwater robotics research

## Methodology
- **Behavior Cloning (Stage 1)**: The system first learns a base manipulation policy through behavior cloning from human teleoperation demonstrations. A human operator controls the underwater robot to perform various manipulation tasks, and the resulting state-action trajectories are used to train an initial policy via supervised learning.
- **Self-Learning Optimization (Stage 2)**: Starting from the behavior-cloned policy, the system employs a self-improvement mechanism where the robot autonomously explores and optimizes its policy. This stage enables the robot to discover manipulation strategies that are more efficient than the original human demonstrations, ultimately surpassing human-level performance.
- **System Integration**: AquaBot integrates perception, planning, and control into a cohesive end-to-end autonomous system. The hardware platform is designed for underwater operation with appropriate waterproofing, buoyancy control, and manipulation capabilities.
- **Experimental Setup**: Real-world experiments across three tasks -- (1) object grasping in underwater environments, (2) trash sorting requiring object classification and placement, and (3) rescue retrieval simulating emergency recovery operations. Performance is measured primarily by task completion speed compared to a human teleoperator baseline. All experiments are conducted in real underwater environments, not simulation.
