# MarineGym: A High-Performance Reinforcement Learning Platform for Underwater Robotics

## Topic
GPU-accelerated reinforcement learning simulation platform for underwater unmanned vehicles (UUVs), providing standardized benchmarking with domain randomization for sim-to-real transfer.

## Background
Existing underwater simulation environments suffer from limited RL compatibility, low training efficiency, and lack of standardized benchmarks for reproducible research. Traditional platforms like DAVE, Stonefish, and HoloOcean operate at only 10-1,000 FPS with limited parallelization, creating a bottleneck for large-scale RL training that requires millions of environment interactions. The underwater robotics community lacks the equivalent of what Isaac Gym/Sim provides for terrestrial and aerial robots.

## Limitations & Research Problem
- **Limitation:** Current underwater simulators (DAVE, Stonefish, HoloOcean) are CPU-bound, achieving only ~100-1,000 FPS with ~10 parallel environments, making large-scale RL training impractical. No existing platform provides standardized RL tasks across diverse UUV morphologies.
- **Problem:** How to build a GPU-accelerated, RL-native simulation platform for underwater robotics that supports diverse vehicle morphologies, realistic hydrodynamics, domain randomization, and standardized benchmarking -- all at speeds enabling practical deep RL training.

## Contributions
- First GPU-accelerated RL platform specifically designed for underwater robotics, achieving 250,000 FPS on a single RTX 3060 with 8,000+ parallel environments (250x faster than existing platforms)
- Custom hydrodynamic plugin integrated with NVIDIA Isaac Sim's PhysX engine, decomposing dynamics into rigid-body (PhysX) and hydrodynamic (PyTorch GPU tensors) components based on Fossen's equations of motion
- Five diverse UUV models spanning three propulsion paradigms: multirotor (BlueROV 6-thruster, BlueROV Heavy 8-thruster), rudder-propeller (LAUV, iAUV), and tiltrotor hybrid (HAUV)
- Three actuator dynamics models: zero-order (direct mapping), first-order (differential equation), and neural-network-driven (learned nonlinear mapping from experimental data)
- Modular domain randomization toolkit covering physical properties, simulation settings, actuator parameters, and environmental factors with uniform, Gaussian, and custom sampling distributions
- Three standardized RL tasks: station-keeping, trajectory tracking, and docking, benchmarked with DDPG, PPO, SAC, TD3, and DQN

## Methodology
- **Hydrodynamic Simulation**: Decomposes Fossen's equation of motion into rigid-body dynamics (handled by PhysX) and hydrodynamic effects (added mass, damping, Coriolis/centripetal forces, restoring forces -- computed via custom GPU-accelerated PyTorch plugin). This separation enables leveraging PhysX parallelism while maintaining hydrodynamic fidelity.
- **Visual Rendering**: Isaac Sim's real-time ray-tracing engine simulates underwater optical physics including spectral attenuation and color distortion characteristic of underwater environments.
- **Domain Randomization**: Four randomization categories -- (1) physical properties (mass, inertia, center of gravity), (2) simulation settings (fluid density, added mass matrix, damping coefficients), (3) actuator parameters (time constant, force constant, installation position), (4) environmental factors (current velocity/direction, external payload). Training ranges: mass 0.8-1.2x, current velocity 0.0-0.5 m/s, payload 0.0-0.3x nominal.
- **UUV Models**: Five vehicles with YAML-based configuration and URDF specifications: BlueROV (6 thrusters, full 6-DOF), BlueROV Heavy (8 thrusters, enhanced maneuverability), LAUV (rudder-propeller, optimized for cruising), iAUV (Zhejiang University, underactuated), HAUV (tiltrotor hybrid for air-sea missions).
- **RL Tasks**: Station-keeping (maintain pose under disturbances), trajectory tracking (follow helical/Lissajous curves), docking (precise landing on underwater platform under flow disturbances).
- **Experimental Setup**: Benchmarked on NVIDIA RTX 3060 GPU. Compared against DAVE (parallelized and standard), Stonefish, and HoloOcean. Evaluated all 5 UUV models across 3 tasks with and without domain randomization. Test environments include in-distribution (Env1) and out-of-distribution (Env2, e.g., 1.4x mass, 0.8 m/s current -- beyond training range). RL algorithms: DDPG, PPO, SAC, TD3, DQN.
- **Key Results**: (1) 250,000 FPS vs ~1,000 FPS for parallelized DAVE (250x speedup). (2) Domain randomization reduces station-keeping error by 95.8% in-distribution and 92.3% out-of-distribution. (3) Underactuated vehicles (LAUV, iAUV) require 2x training steps and show significant performance degradation under strong currents. (4) 8-thruster platforms show minimal robustness loss under disturbances.
- **Limitations**: No real-world deployment validation; simplified underwater visual characteristics; hydrodynamic model based on analytical Fossen equations rather than CFD.
