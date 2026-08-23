# Formal Methods x Robot Learning: Comprehensive Literature Survey (2023-2026)

## Table of Contents
1. [Surveys and Overviews](#1-surveys-and-overviews)
2. [Control Barrier Functions & Certificate-Based Methods](#2-control-barrier-functions--certificate-based-methods)
3. [Shielding & Runtime Verification](#3-shielding--runtime-verification)
4. [Temporal Logic Constraints for Robot RL](#4-temporal-logic-constraints-for-robot-rl)
5. [Lyapunov-Based Neural Control](#5-lyapunov-based-neural-control)
6. [Reachability Analysis & Verified Safety](#6-reachability-analysis--verified-safety)
7. [Safe Diffusion & Foundation Model Methods](#7-safe-diffusion--foundation-model-methods)
8. [Constrained MDP / Policy Optimization](#8-constrained-mdp--policy-optimization)
9. [Safe Sim-to-Real Transfer](#9-safe-sim-to-real-transfer)
10. [LLM-Controlled Robots with Formal Guarantees](#10-llm-controlled-robots-with-formal-guarantees)

---

## 1. Surveys and Overviews

### 1.1 "Revisiting Formal Methods for Autonomous Robots: A Structured Survey"
- **Year:** 2025
- **Venue:** arXiv (2509.20488)
- **Scope:** 181 papers reviewed on formal methods for robotic autonomous systems
- **Key Contribution:** Categorizes FM approaches/formalisms for specification and verification of robotic systems; investigates FM in the context of sub-symbolic AI-enabled robotic systems
- **Formal Guarantee Type:** Meta-survey of specification, verification, and synthesis techniques
- **Robot Domain:** General autonomous robots
- **Post-training vs. Training:** Covers both design-time verification and runtime monitoring

### 1.2 "A Survey of Safe Reinforcement Learning Methods in Robotics"
- **Authors:** Yuen Xie et al.
- **Year:** 2025
- **Venue:** ITM Web of Conferences (CSEIT 2025)
- **Key Contribution:** Taxonomizes safe RL into three categories: (1) control theory-based, (2) formal method-based, (3) constrained optimization-based
- **Formal Guarantee Type:** Comparative analysis of guarantee types
- **Robot Domain:** General robotics
- **Post-training vs. Training:** Covers both

### 1.3 "Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning"
- **Authors:** Lukas Brunke, Melissa Greeff, et al.
- **Year:** 2022 (Annual Reviews, highly cited through 2025)
- **Venue:** Annual Review of Control, Robotics, and Autonomous Systems
- **Key Contribution:** Comprehensive taxonomy of safe learning: learning-based control with uncertain dynamics, RL with safety/robustness, and formal certification of learned policies
- **Formal Guarantee Type:** Multiple (Lyapunov, barrier, reachability, CMDP)
- **Robot Domain:** General robotics

### 1.4 "A Review of Safe Reinforcement Learning: Methods, Theories and Applications"
- **Year:** 2024 (updated version)
- **Venue:** arXiv (2205.10330v5)
- **Key Contribution:** Comprehensive review of SafeRL methods, theory, and applications
- **Formal Guarantee Type:** CMDP constraints, Lyapunov, barrier certificates

### 1.5 "Safe Learning for Contact-Rich Robot Tasks: A Survey from Classical Learning-Based Methods to Safe Foundation Models"
- **Year:** 2025
- **Venue:** arXiv (2512.11908)
- **Key Contribution:** Reviews safety mechanisms integrated into learning for physical contact tasks; covers safe RL and model-based safety strategies for contact-rich scenarios
- **Robot Domain:** Manipulation with contact
- **Post-training vs. Training:** Covers both; explicitly discusses foundation model safety

### 1.6 "Hamilton-Jacobi Reachability in Reinforcement Learning: A Survey"
- **Year:** 2024
- **Venue:** arXiv (2407.09645)
- **Key Contribution:** Surveys the intersection of HJ reachability and RL; how reachable sets verify safety and supervise training of RL policies
- **Formal Guarantee Type:** Hamilton-Jacobi reachability (rigorous mathematical framework)
- **Robot Domain:** General autonomous systems

### 1.7 "A Review On Safe Reinforcement Learning Using Lyapunov and Barrier Functions"
- **Year:** 2025
- **Venue:** arXiv (2508.09128)
- **Key Contribution:** Focused review on Lyapunov and barrier function approaches to safe RL
- **Formal Guarantee Type:** Lyapunov stability, CBF safety

### 1.8 "A Survey of Safe Reinforcement Learning and Constrained MDPs"
- **Year:** 2025
- **Venue:** arXiv (2505.17342)
- **Key Contribution:** Technical survey on single-agent and multi-agent safety in RL via CMDPs
- **Formal Guarantee Type:** CMDP constraint satisfaction

### 1.9 "Safe Control with Learned Certificates: A Survey of Neural Lyapunov, Barrier, and Contraction Methods"
- **Year:** 2022 (updated 2024)
- **Venue:** arXiv (2202.11762)
- **Key Contribution:** Surveys certificate-based methods that simultaneously learn a control policy and a certificate proving soundness
- **Formal Guarantee Type:** Lyapunov, barrier, contraction certificates

### 1.10 "A Survey of Constraint Formulations in Safe Reinforcement Learning"
- **Year:** 2024
- **Venue:** IJCAI 2024
- **Key Contribution:** Classifies constraint formulations used in safe RL
- **Formal Guarantee Type:** Multiple constraint types

### 1.11 "Deep Reinforcement Learning for Robotics: A Survey of Real-World Successes"
- **Authors:** Chen Tang et al.
- **Year:** 2025
- **Venue:** Annual Review of Control, Robotics, and Autonomous Systems
- **Key Contribution:** Modern evaluation of DRL successes in real-world robotics, identifies key success factors and underexplored areas
- **Robot Domain:** Broad (manipulation, locomotion, navigation)

---

## 2. Control Barrier Functions & Certificate-Based Methods

### 2.1 "GCBF+: A Neural Graph Control Barrier Function Framework for Distributed Safe Multi-Agent Control"
- **Authors:** Songyuan Zhang, Oswin So, Kunal Garg, Chuchu Fan (MIT)
- **Year:** 2024/2025
- **Venue:** IEEE Transactions on Robotics (T-RO) 2025
- **Key Method:** Graph Neural Networks parameterize candidate Graph CBFs and distributed control policies; directly takes LiDAR point clouds as input
- **Formal Guarantee Type:** Control Barrier Function (CBF) safety certificates for multi-agent systems
- **Robot Domain:** Multi-robot (Crazyflie drones, up to 1024 agents)
- **Post-training vs. Training:** Training from scratch with safety certificates; the learned GCBF serves as a post-deployment safety filter
- **Results:** Outperforms hand-crafted CBF methods by 20%, RL methods by 40%

### 2.2 "Verification of Neural Control Barrier Functions with Symbolic Derivative Bounds Propagation"
- **Authors:** Hu et al.
- **Year:** 2025
- **Venue:** ICML 2025 (Proceedings of Machine Learning Research, v270)
- **Key Method:** Symbolic derivative bounds propagation for efficient verification of pre-trained neural CBFs
- **Formal Guarantee Type:** Formal verification of CBF conditions along the barrier boundary
- **Robot Domain:** Multiple robot dynamics
- **Post-training vs. Training:** Post-training verification of pre-trained CBFs

### 2.3 "How to Train Your Neural Control Barrier Function: Learning Safety Filters for Complex Input-Constrained Systems"
- **Authors:** So, Serlin et al. (MIT REALM)
- **Year:** 2024
- **Venue:** arXiv / conference
- **Key Method:** Policy neural CBFs -- learn CBFs via value function of nominal policy; addresses high relative degree systems with input constraints
- **Formal Guarantee Type:** CBF safety filter guarantees
- **Robot Domain:** High-dimensional systems with input constraints
- **Post-training vs. Training:** Training a safety filter (can be applied post-training as a filter on any policy)

### 2.4 "CN-CBF: Composite Neural Control Barrier Function for Safe Robot Navigation in Dynamic Environments"
- **Year:** 2025
- **Venue:** arXiv (2603.06921)
- **Key Method:** Composite neural CBF for dynamic environments
- **Formal Guarantee Type:** CBF safety guarantees
- **Robot Domain:** Robot navigation in dynamic environments

### 2.5 "CRABS: Co-trained Barrier Certificate for Safe Reinforcement Learning"
- **Authors:** Luo, Ma et al.
- **Year:** 2021 (NeurIPS), cited heavily through 2024
- **Venue:** NeurIPS 2021
- **Key Method:** Iteratively co-trains barrier certificates, dynamics models, and policies via adversarial training; regularization encourages larger certified safe regions
- **Formal Guarantee Type:** Barrier certificate (zero training-time violations)
- **Robot Domain:** Continuous control (simulated)
- **Post-training vs. Training:** Training from scratch with safety during training

### 2.6 "Probabilistic Safety Guarantees for Learned Control Barrier Functions"
- **Year:** 2025
- **Venue:** Mathematics (MDPI), 14(3):516
- **Key Method:** PAC learning with Lipschitz-constrained neural networks; explicit probabilistic bounds relating NN approximation error to safety failure probability
- **Formal Guarantee Type:** Probabilistic safety certificates via PAC bounds
- **Robot Domain:** Human-robot collaborative optimization (MPC-based)
- **Post-training vs. Training:** Post-training probabilistic certification

### 2.7 "SHIELD: Safety on Humanoids via CBFs In Expectation on Learned Dynamics"
- **Year:** 2025
- **Venue:** arXiv (2505.11494)
- **Key Method:** CBFs computed in expectation over learned dynamics models for humanoid robots
- **Formal Guarantee Type:** CBF safety in expectation
- **Robot Domain:** Humanoid robots
- **Post-training vs. Training:** Post-training safety layer on learned dynamics

### 2.8 "Model-Free Safe Reinforcement Learning Through Neural Barrier Certificate"
- **Year:** 2023
- **Venue:** ResearchGate / conference
- **Key Method:** Neural barrier certificates without requiring a dynamics model
- **Formal Guarantee Type:** Barrier certificate safety
- **Robot Domain:** Continuous control

---

## 3. Shielding & Runtime Verification

### 3.1 "Shields for Safe Reinforcement Learning"
- **Year:** 2025
- **Venue:** Communications of the ACM (CACM)
- **Key Method:** Shields as runtime monitors computed offline from formal safety specifications and abstract environment models; prevents unsafe actions at runtime
- **Formal Guarantee Type:** Provable safety via reactive synthesis from formal specifications
- **Robot Domain:** General RL agents (applicable to robotics)
- **Post-training vs. Training:** Both -- shields during training and deployment
- **Results:** Orders-of-magnitude reduction in safety violations; accelerated learning

### 3.2 "Realizable Continuous-Space Shields for Safe Reinforcement Learning"
- **Authors:** Kim et al.
- **Year:** 2024
- **Venue:** NSF PAR / conference
- **Key Method:** SMT-guided reactive synthesis over LTLt for continuous state/action spaces; runtime action correction via constrained optimization
- **Formal Guarantee Type:** Formal shield realizability in continuous domains
- **Robot Domain:** Continuous control (first shield for continuous spaces)
- **Post-training vs. Training:** Both training-time and deployment-time shielding

### 3.3 "Runtime Verification-Based Safe MARL for Multi-Robot Systems"
- **Year:** 2024
- **Venue:** Big Data and Cognitive Computing (MDPI), 8(5):49
- **Key Method:** Safety-Constrained Markov Game (SCMG) verified with rPATL (probabilistic alternating-time temporal logic with rewards); guides Safety-Constrained Policy Optimization (SCPO)
- **Formal Guarantee Type:** Runtime verification of temporal logic properties
- **Robot Domain:** Multi-robot warehouse systems
- **Post-training vs. Training:** Training with runtime verification guidance

### 3.4 "Safe Reinforcement Learning via Adaptive Robust Model Predictive Shielding"
- **Year:** 2025
- **Venue:** ScienceDirect (Computers & Chemical Engineering)
- **Key Method:** Adaptive MPC-based shielding for RL
- **Formal Guarantee Type:** MPC-based robust safety guarantees
- **Robot Domain:** Process control / robotics

### 3.5 "Towards Robust Shielded RL: The Fear Field Framework"
- **Year:** 2025
- **Venue:** ScienceDirect (Engineering Applications of AI)
- **Key Method:** Adaptive constraints and exploration via "fear fields" for shielded RL
- **Formal Guarantee Type:** Shielding with adaptive safety constraints
- **Robot Domain:** General RL

### 3.6 "Safe-ROS: An Architecture for Autonomous Robots"
- **Year:** 2025
- **Venue:** arXiv (2511.14433)
- **Key Method:** Safety architecture for ROS-based robots
- **Formal Guarantee Type:** Architectural safety guarantees
- **Robot Domain:** ROS-based autonomous robots

### 3.7 "Runtime Verification of DRL-Based Mission-Critical Control"
- **Year:** 2024
- **Venue:** DiVA Portal (thesis/report)
- **Key Method:** Runtime monitoring of deep RL controllers
- **Formal Guarantee Type:** Runtime verification of mission-critical properties
- **Robot Domain:** Mission-critical systems

### 3.8 "Combining Model Checking and Runtime Verification for Safe Robotics" (DRONA)
- **Authors:** Seshia et al. (Berkeley)
- **Year:** Earlier work, still relevant
- **Key Method:** Combines offline model checking with online runtime monitoring using STL
- **Formal Guarantee Type:** Model checking + runtime verification
- **Robot Domain:** Reactive robotics

---

## 4. Temporal Logic Constraints for Robot RL

### 4.1 "Reinforcement Learning with Soft Temporal Logic Constraints Using Limit-Deterministic Generalized Buchi Automaton"
- **Year:** 2024
- **Venue:** ScienceDirect
- **Key Method:** Relaxed LTL constraints via Generalized Buchi Automaton; allows partial satisfaction and motion plan revision
- **Formal Guarantee Type:** Soft LTL satisfaction guarantees
- **Robot Domain:** Robot motion planning
- **Post-training vs. Training:** Training from scratch with TL constraints

### 4.2 "TGPO: Temporal Grounded Policy Optimization for Signal Temporal Logic Tasks"
- **Year:** 2025
- **Venue:** arXiv (2510.00225)
- **Key Method:** Dense reward design under augmented state spaces for STL tasks; addresses the challenge that STL satisfaction is checked over full trajectories
- **Formal Guarantee Type:** STL specification satisfaction
- **Robot Domain:** Robotics control tasks
- **Post-training vs. Training:** Training from scratch with STL objectives

### 4.3 "Funnel-Based Reward Shaping for Signal Temporal Logic Tasks in RL"
- **Year:** 2023/2024
- **Venue:** IEEE (10354421)
- **Key Method:** Funnel functions for tractable RL with robust STL satisfaction in continuous state space
- **Formal Guarantee Type:** Robust STL satisfaction
- **Robot Domain:** Continuous control
- **Post-training vs. Training:** Training from scratch

### 4.4 "Reinforcement Learning under Temporal Logic Constraints as a Sequence Modeling Problem"
- **Year:** 2023
- **Venue:** Robotics and Autonomous Systems
- **Key Method:** Frames TL-constrained RL as sequence modeling
- **Formal Guarantee Type:** LTL constraint satisfaction
- **Robot Domain:** Robotics
- **Post-training vs. Training:** Training from scratch

### 4.5 "Constrained Hierarchical Deep RL with Differentiable Formal Specifications"
- **Year:** 2023
- **Venue:** OpenReview (under review ICLR)
- **Key Method:** Hierarchical RL with differentiable formal specifications as constraints
- **Formal Guarantee Type:** Differentiable formal specification satisfaction
- **Robot Domain:** Hierarchical control tasks

### 4.6 "Safe Reinforcement Learning under Temporal Logic with Reward Design and Quantum Action Selection"
- **Year:** 2023
- **Venue:** Scientific Reports (Nature)
- **Key Method:** Combines TL reward design with quantum-inspired action selection for safety
- **Formal Guarantee Type:** Temporal logic safety specifications
- **Robot Domain:** General control

### 4.7 "Reinforcement Learning with Timed Constraints for Robotics Motion Planning"
- **Year:** 2025
- **Venue:** arXiv (2601.00087)
- **Key Method:** Timed temporal constraints for motion planning
- **Formal Guarantee Type:** Timed constraint satisfaction
- **Robot Domain:** Robot motion planning

### 4.8 "RESTL: RL Guided by Multi-Aspect Rewards for STL Transformation"
- **Year:** 2025
- **Venue:** arXiv (2511.08555)
- **Key Method:** RL with multi-aspect dense reward signals to transform natural language to STL specifications
- **Formal Guarantee Type:** STL specification generation
- **Robot Domain:** NL-to-formal-spec translation

### 4.9 "Formal Methods in Robot Policy Learning and Verification" (STL-Controlled Decision Transformers)
- **Year:** 2024
- **Venue:** OpenReview / FMR Workshop at ICRA 2024
- **Key Method:** Decision transformers controlled by STL specifications; outperforms pure behavior cloning
- **Formal Guarantee Type:** STL specification satisfaction
- **Robot Domain:** 2D maze navigation, Push-T manipulation, simulated robot navigation
- **Post-training vs. Training:** Training with formal specification guidance

---

## 5. Lyapunov-Based Neural Control

### 5.1 "Lyapunov-stable Neural Control for State and Output Feedback: A Novel Formulation"
- **Authors:** Dai et al. (MIT)
- **Year:** 2024
- **Venue:** arXiv (2404.07956)
- **Key Method:** Co-learns NN controllers + Lyapunov certificates using fast empirical falsification and strategic regularizations; first Lyapunov-stable output feedback with NN observers
- **Formal Guarantee Type:** Formal Lyapunov stability over region-of-attraction; post-training verification via strong verifier (SMT/MIP)
- **Robot Domain:** Nonlinear dynamical systems
- **Post-training vs. Training:** Training with cheap adversarial attacks, then post-training verification with strong verifier

### 5.2 "Stability-Certified Reinforcement Learning: A Control-Theoretic Perspective"
- **Year:** 2023-2024
- **Venue:** Berkeley technical report
- **Key Method:** RL with stability certification from control theory
- **Formal Guarantee Type:** Lyapunov stability certificates
- **Robot Domain:** Control systems

### 5.3 "Certified Neural Network Control Architectures: Methodological Advances"
- **Year:** 2025
- **Venue:** Mathematics (MDPI), 13(10):1677
- **Key Method:** Three research thrusts: theoretical foundations, computational tools (ReachNN), cross-domain validation; synthesis of barrier Lyapunov functions with neural approximators
- **Formal Guarantee Type:** Lyapunov stability + barrier safety for human-in-the-loop systems
- **Robot Domain:** Assistive robotics, safety-critical control
- **Post-training vs. Training:** Both training and post-training verification

### 5.4 "Adaptive RBF Neural Network Control with Lyapunov Stability for Industrial Robots"
- **Year:** 2025
- **Venue:** Scientific Reports (Nature)
- **Key Method:** Lyapunov-stability-guaranteed local model adaptive RBF neural network; no need for exact plant model
- **Formal Guarantee Type:** Lyapunov stability guarantees
- **Robot Domain:** Industrial manipulators
- **Post-training vs. Training:** Online learning with stability guarantees

---

## 6. Reachability Analysis & Verified Safety

### 6.1 "Safe Multi-Agent RL via Approximate Hamilton-Jacobi Reachability"
- **Year:** 2024
- **Venue:** Journal of Intelligent & Robotic Systems
- **Key Method:** Approximate HJ reachability for multi-agent RL safety
- **Formal Guarantee Type:** Hamilton-Jacobi reachability safety sets
- **Robot Domain:** Multi-agent robotic systems
- **Post-training vs. Training:** Safety filter during training

### 6.2 "Generalizing Safety Beyond Collision-Avoidance via Latent-Space Reachability Analysis"
- **Year:** 2025
- **Venue:** arXiv (2502.00935)
- **Key Method:** Reachability analysis in latent space; generalizes safety beyond just collision avoidance
- **Formal Guarantee Type:** Reachability-based safety in latent representations
- **Robot Domain:** General robotics
- **Post-training vs. Training:** Post-training safety analysis

### 6.3 "Patching Approximately Safe Value Functions Using Local HJ Reachability Analysis"
- **Authors:** Sander Tonkens et al. (Herbert lab)
- **Year:** 2024
- **Venue:** CDC 2024
- **Key Method:** Locally "patches" invalid safety filter approximations from learning-based methods (e.g., neural CBFs) using rigorous HJ reachability
- **Formal Guarantee Type:** Rigorous HJ reachability guarantees patched onto learned approximations
- **Robot Domain:** Autonomous systems
- **Post-training vs. Training:** **Post-training** patching/correction of learned safety filters

### 6.4 "Back to Base: Hands-Off Learning via Safe Resets with Reach-Avoid Safety Filters"
- **Year:** 2025
- **Venue:** L4DC 2025
- **Key Method:** Time-varying reach-avoid value function as safety filter; ensures robot can always "return to base" during online RL
- **Formal Guarantee Type:** Reach-avoid safety guarantees
- **Robot Domain:** Online robot learning
- **Post-training vs. Training:** Safety during online fine-tuning/learning

### 6.5 "Reachability Barrier Networks: Learning HJ Solutions for Smooth and Flexible CBFs"
- **Year:** 2025
- **Venue:** arXiv (2505.11755)
- **Key Method:** Learns Hamilton-Jacobi solutions as smooth CBFs
- **Formal Guarantee Type:** HJ reachability + CBF
- **Robot Domain:** Control systems

### 6.6 "Provably Safe Deep RL for Robotic Manipulation in Human Environments"
- **Authors:** Thumm et al.
- **Year:** 2022 (ICRA), cited through 2025
- **Venue:** ICRA 2022
- **Key Method:** Shielding via fast reachability analysis of humans and manipulators; ISO-verified human safety; manipulator stops before human is in range
- **Formal Guarantee Type:** ISO-verified reachability-based safety (provable)
- **Robot Domain:** Robot manipulation with human co-workers
- **Post-training vs. Training:** Both -- shield during training and deployment

### 6.7 "Safe Networked Robotics with Probabilistic Verification"
- **Year:** 2023
- **Venue:** arXiv (2302.09182)
- **Key Method:** Probabilistic verification for networked robotic systems
- **Formal Guarantee Type:** Probabilistic safety verification
- **Robot Domain:** Networked multi-robot systems

---

## 7. Safe Diffusion & Foundation Model Methods

### 7.1 "SafeDiffuser: Safe Planning with Diffusion Probabilistic Models"
- **Authors:** Xiao, Wang et al.
- **Year:** 2025
- **Venue:** ICLR 2025
- **Key Method:** Embeds finite-time diffusion invariance (safety constraints via CBFs) into the denoising diffusion procedure
- **Formal Guarantee Type:** CBF-based safety constraints embedded in diffusion process
- **Robot Domain:** Maze planning, legged locomotion, 3D manipulation
- **Post-training vs. Training:** **Post-training** -- modifies the diffusion sampling/denoising process with safety constraints; does not retrain the diffusion model

### 7.2 "Towards Safe Robot Foundation Models Using Inductive Biases"
- **Year:** 2025
- **Venue:** arXiv (2505.10219)
- **Key Method:** Geometric inductive biases + safety layer placed after foundation policy; enforces action constraints ensuring safe state transitions
- **Formal Guarantee Type:** Safety constraints via inductive biases and post-policy safety layer
- **Robot Domain:** General robot foundation models
- **Post-training vs. Training:** **Post-training safety layer** on foundation model

### 7.3 "Modular Safety Guardrails Are Necessary for Foundation-Model-Enabled Robots in the Real World"
- **Year:** 2025
- **Venue:** arXiv (2602.04056)
- **Key Method:** External modularity separates safety enforcement from foundation models; internal modularity decomposes safety into specialized mechanisms
- **Formal Guarantee Type:** Architectural safety guarantees (modular guardrails)
- **Robot Domain:** Foundation-model-enabled robots
- **Post-training vs. Training:** **Post-training** modular safety architecture

### 7.4 "Constrained Diffusers for Safe Planning and Control"
- **Year:** 2025
- **Venue:** arXiv (2506.12544)
- **Key Method:** Constraint mechanisms for diffusion-based planners
- **Formal Guarantee Type:** Constrained diffusion generation
- **Robot Domain:** Planning and control

---

## 8. Constrained MDP / Policy Optimization

### 8.1 "Constrained Policy Optimization (CPO)"
- **Authors:** Achiam et al. (CMU/Berkeley)
- **Year:** 2017, foundational and still heavily used
- **Venue:** ICML 2017
- **Key Method:** First policy search algorithm for CMDPs guaranteeing constraint satisfaction throughout training for arbitrary policy classes (including NNs)
- **Formal Guarantee Type:** CMDP constraint satisfaction guarantee
- **Robot Domain:** General (widely applied to robotics)

### 8.2 "IPO: Interior-point Policy Optimization under Constraints"
- **Year:** 2024
- **Venue:** AAAI
- **Key Method:** Logarithmic barrier functions as penalty for constraint accommodation; zero penalty when satisfied, negative infinity when violated
- **Formal Guarantee Type:** Interior-point constraint enforcement
- **Robot Domain:** General constrained RL

### 8.3 "Guided Constrained Policy Optimization for Dynamic Quadrupedal Robot Locomotion"
- **Year:** 2020 (RAL), still relevant
- **Venue:** IEEE Robotics and Automation Letters
- **Key Method:** CMDP framework for quadrupedal locomotion with model-based control constraints
- **Formal Guarantee Type:** CMDP constraint satisfaction
- **Robot Domain:** Quadrupedal robots

### 8.4 "State-wise Constrained Policy Optimization"
- **Year:** 2024
- **Venue:** OpenReview
- **Key Method:** State-level (rather than trajectory-level) constraint enforcement in policy optimization
- **Formal Guarantee Type:** State-wise safety constraints
- **Robot Domain:** General RL / robotics

### 8.5 "Incentivizing Safer Actions in Policy Optimization for Robotics"
- **Year:** 2025
- **Venue:** IJCAI 2025
- **Key Method:** Incentive mechanisms for safer action selection in policy optimization
- **Formal Guarantee Type:** Safety incentives in optimization
- **Robot Domain:** Robotics

### 8.6 "Multi-Robot Hierarchical Safe RL with Uniformly Ultimate Boundedness Constraints"
- **Year:** 2025
- **Venue:** Scientific Reports (Nature)
- **Key Method:** Hierarchical safe RL with UUB (uniformly ultimate boundedness) constraints
- **Formal Guarantee Type:** UUB stability constraints
- **Robot Domain:** Multi-robot systems

---

## 9. Safe Sim-to-Real Transfer

### 9.1 "Sim-to-Lab-to-Real: Safe RL with Shielding and Generalization Guarantees"
- **Authors:** Turchetta, Krause et al. (Princeton Safe Robotics Lab)
- **Year:** 2023 (Artificial Intelligence Journal)
- **Venue:** Artificial Intelligence (Elsevier)
- **Key Method:** Three-stage pipeline: (1) sim training with shielding, (2) lab fine-tuning with safety constraints, (3) real deployment with certified generalization; provides performance and safety certificates before deployment
- **Formal Guarantee Type:** Generalization certificates + shielding safety guarantees
- **Robot Domain:** Safety-critical robotic deployment
- **Post-training vs. Training:** **Both** -- safety during training AND certification before deployment (a form of post-training verification)

### 9.2 "Safe Model-Based RL with Uncertainty-Aware Reachability Certificate (DRC)"
- **Year:** 2023
- **Venue:** arXiv (2210.07553)
- **Key Method:** Distributional Reachability Certificate (DRC) to address model uncertainties; characterizes robust persistently safe states; safe RL framework resolves DRC constraints
- **Formal Guarantee Type:** Reachability certificate under model uncertainty
- **Robot Domain:** Model-based control with sim-to-real gap
- **Post-training vs. Training:** Training with uncertainty-aware safety

### 9.3 "Bayesian Optimization with Safety Constraints: Safe and Automatic Parameter Tuning in Robotics"
- **Year:** 2021/2023
- **Venue:** Machine Learning (Springer)
- **Key Method:** Bayesian optimization with safety constraints for parameter tuning; carefully explores parameter space to maximize performance while guaranteeing safety with high probability
- **Formal Guarantee Type:** Probabilistic safety guarantees via Bayesian optimization
- **Robot Domain:** Robot parameter tuning
- **Post-training vs. Training:** **Post-training** fine-tuning with safety constraints

---

## 10. LLM-Controlled Robots with Formal Guarantees

### 10.1 "Safe LLM-Controlled Robots with Formal Guarantees via Reachability Analysis"
- **Authors:** Ahmad Hafez et al.
- **Year:** 2025
- **Venue:** arXiv (2503.03911)
- **Key Method:** Data-driven reachability analysis for LLM-controlled robots; in each iteration: LLM generates plan -> compute reachable sets -> if unsafe, adjust plan or execute failsafe maneuver
- **Formal Guarantee Type:** Reachability-based formal verification of LLM-generated plans
- **Robot Domain:** Autonomous navigation, task planning
- **Post-training vs. Training:** **Post-training** safety wrapper on LLM planner -- does NOT retrain the LLM

### 10.2 "Enhancing Reliability in LLM-Integrated Robotic Systems: A Unified Approach to Security and Safety"
- **Year:** 2025
- **Venue:** arXiv (2509.02163)
- **Key Method:** Unified security and safety framework for LLM-robot integration
- **Formal Guarantee Type:** Security + safety guarantees
- **Robot Domain:** LLM-integrated robots

---

## Summary Table: Methods by Formal Guarantee Type

| Guarantee Type | Representative Papers | Strength of Guarantee |
|---|---|---|
| **CBF (Control Barrier Function)** | GCBF+, SafeDiffuser, SHIELD, CN-CBF, CRABS | Forward invariance of safe set (deterministic) |
| **Lyapunov Stability** | Lyapunov-stable Neural Control, Certified NN Architectures | Convergence to equilibrium + stability |
| **HJ Reachability** | HJ-RL Survey, Patching with HJ, Safe LLM Robots | Exact characterization of backward reachable sets |
| **Shielding / Runtime Verification** | Shields for Safe RL, Continuous-Space Shields, RV-MARL | Runtime enforcement of formal specs |
| **Temporal Logic (LTL/STL)** | TGPO, Funnel STL, STL Decision Transformers | Task specification satisfaction |
| **CMDP Constraints** | CPO, IPO, State-wise CPO | Expected constraint satisfaction |
| **Probabilistic / PAC** | PAC-CBF, Bayesian Safe Opt, Probabilistic Verification | High-probability safety bounds |
| **Reachability Certificates** | DRC, Sim-to-Lab-to-Real | Robust safety under uncertainty |

## Summary Table: Post-Training vs. Training-Time Methods

| Category | Papers |
|---|---|
| **Post-training safety filters/wrappers** | SafeDiffuser, Safe LLM Robots, GCBF+ (filter mode), Shields, Modular Guardrails, Safe Robot FM with Inductive Biases |
| **Post-training verification** | Verification of Neural CBFs (symbolic), Lyapunov post-training verification, Patching with HJ Reachability, Probabilistic CBF certification |
| **Safety during training** | CRABS, CPO, Shielded RL, RV-MARL, Soft TL constraints, Funnel STL, Sim-to-Lab-to-Real |
| **Safety during online fine-tuning** | Back to Base (reach-avoid filters), Bayesian Safe Optimization, DRC |
| **Both training + deployment** | Sim-to-Lab-to-Real, Provably Safe Deep RL for Manipulation, Shields for Safe RL |

---

## Key Observations for Post-Training / Fine-Tuning Research

1. **Post-training safety layers are a growing trend**: SafeDiffuser, Safe Robot Foundation Models with Inductive Biases, Modular Safety Guardrails, and Safe LLM Robots all add safety as a modular layer AFTER training the base policy/model.

2. **Verification after training is cheaper than training with verification**: The Lyapunov-stable Neural Control work explicitly shows that cheap adversarial attacks during training + strong post-training verification (SMT/MIP) is more practical than expensive verification during training.

3. **HJ Reachability patching is a compelling post-training approach**: Tonkens et al. (CDC 2024) show that approximate/learned safety filters can be "patched" post-training with rigorous HJ reachability analysis.

4. **Foundation model safety is an open problem**: Multiple 2025 papers note that current robot foundation models lack formal safety guarantees and that post-training safety mechanisms (guardrails, filters, reachability analysis) are essential.

5. **The sim-to-real gap creates a natural post-training stage**: Sim-to-Lab-to-Real explicitly introduces a certification step between training and deployment.

6. **CBFs and shielding are the most mature post-training safety techniques**: They can be applied as runtime filters on any policy without retraining.
