# DREAM - Domain-aware Reasoning for Underwater Monitoring

## Topic
VLM-guided underwater monitoring autonomy

## Background
Ocean warming and acidification are increasing mass-mortality risk for temperature-sensitive shellfish such as oysters, motivating long-term, wide-area, low-cost benthic monitoring. Human-diver operations are costly and hazardous, so robotic ROVs are a safer alternative, but existing solutions either rely on tele-operators or on imitation-learning policies tied to one domain. DREAM proposes a Vision-Language-Model (VLM)-guided autonomy framework that injects oceanic domain knowledge into the planning loop to enable persistent, wide-area, low-cost underwater exploration and habitat monitoring.

## Existing Limitations and Research Question
- **Limitation:** Prior underwater monitoring methods are largely imitation-learning based, lack feedback from the outer world, and depend on prior target locations. Recent LLM/VLM systems (OceanPlan, OceanChat, AquaChat++) enable language piloting and multi-AUV coordination but lack robust reasoning, persistent spatial memory, and adaptive replanning.
- **Problem:** How can an underwater robot autonomously and efficiently discover and map objects of interest (oysters, shipwrecks) without prior location information, by combining oceanic domain knowledge with persistent spatial memory?

## Contributions
- A 3-layer architecture (perception, cognitive-aware planning, control) enabling end-to-end monitoring from raw sensing through high-level reasoning down to low-level adaptive control.
- A VLM-based framework that integrates domain knowledge with sequential Chain-of-Thought reasoning to produce persistent monitoring policies that do not rely on object localization priors.
- Real-world deployment on a BlueROV2 demonstrating feasible exploration in marine environments for various objects of interest.
- Open-sourced synthetic environment (Oystersim), real-world dataset, and code to facilitate further underwater robotics monitoring research.
- Empirical results: in oyster monitoring DREAM uses 31.5% less time than the UIVNAV baseline, 23% fewer steps and 8.88% more oysters covered than vanilla VLM. In shipwreck scenes it achieves 100% coverage with no collisions in 27.5% fewer steps, versus 60.23% average coverage for vanilla VLM.

## Methodology
- **Perception module.** A front-facing camera produces RGB, depth, and semantic-segmentation images. Pixels are unprojected to a 3D point cloud, classified by height into target objects (oysters), obstacles, and free space, and ray-cast through the camera FOV to incrementally update a 2D occupancy grid that records explored / unknown / occupied regions and acts as the persistent spatial memory for the VLM.
- **Cognitive-aware planning.** A VLM (GPT-5) receives the RGB, segmentation, depth, and current occupancy map together with a hand-crafted prompt that specifies the mission ("efficiently and comprehensively discover and map all oyster clusters") and a precise completion criterion (green target regions fully enclosed by gray explored cells with no white missed patches). A 6-step Chain-of-Thought scaffold is enforced: (1) distribution analysis from segmentation/occupancy, (2) select current target area, (3) completion check, (4) select next target/frontier, (5) safety and feasibility check using standoff distance, (6) discrete action selection (direction + turn angle + step length). Because VLM inference is slow, it only emits high-level actions instead of low-level commands.
- **Control module.** A planar PD controller tracks setpoints in the body frame; vertical motion is handled by the ROV's depth/altitude hold. State feedback comes from an Invariant EKF (InEKF) and a Cascade Iteratively Preconditioned Gradient (C-IPG) observer fusing IMU and DVL water-relative velocities, providing robust estimates under aggressive yawing or intermittent DVL bottom-lock; "Stop" commands trigger zero-velocity pseudo-measurements to bound drift.
- **Closed loop.** language actions to short setpoint segments to PD tracking, with state supplied by IMU + DVL and continuous-time alignment when the scene allows. Perception (oyster segmentation) and control stability are explicitly decoupled to maintain safety.
- **Experimental setup.** Evaluated in Oystersim across 15 obstacle-laden 40-50 m environments (10 oyster reefs of fringing/string/patch types, 5 shipwreck scenes), with a 200-step cap. Coverage is measured by oyster count for reefs and area for wrecks. Baselines are UIVNAV (zero-shot AI navigation) and a vanilla VLM without CoT (same GPT-5 backbone). Real-world tests use a BlueROV2 with onboard IMU and Waterlinked DVL-A50 in a 12 ft diameter, 5 ft deep tank with oyster shells in a circular arc plus two pipes simulating a wreck, demonstrating real-time end-to-end execution despite cross-currents, tether drag, and surface reflections.
- **Future work.** Plug in DINOv3 features for generalization, train a compact local Mamba-based VLA with pruning and extreme quantization for on-device inference, and extend to 3D cave-like environments.
