# Perception-based Quantitative Runtime Verification for Learning-enabled Cyber-Physical Systems

## Topic
Perception-based Runtime Verification

## Background
Deep neural networks (DNNs) are increasingly deployed in safety-critical applications such as autonomous driving, where failures under unknown uncertainties can endanger human lives. Existing verification approaches for Learning-enabled Cyber-Physical Systems (Le-CPS) operate predominantly at design time, relying on predefined dynamical models and a global view, and provide only qualitative results (Yes/No/Unknown). This paper proposes the first perception-based quantitative runtime verification framework that uses ProbStar reachability to compute collision probabilities in real time.

## Limitations & Research Problem
- **Limitation:** Current Le-CPS verification methods only run at design time with predefined plant models and finite preselected scenarios, producing only qualitative verification results (safe/unsafe/unknown) without quantifying the likelihood or severity of potential failures. They also assume structured environments and cannot adapt to dynamically changing, unstructured real-world conditions.
- **Problem:** How to perform quantitative runtime verification of Le-CPS safety in dynamic, unstructured environments using only perception data, computing collision probabilities in real time while accounting for perception, sensing, and actuation uncertainties?

## Contributions
- First perception-based quantitative runtime verification approach for Le-CPS, combining perception-based modeling with probabilistic star (ProbStar) reachability
- Successful deployment and validation on a real F1Tenth autonomous driving testbed across multiple driving scenarios (rear-end collisions, side collisions, lane following, opposing traffic)
- Comprehensive evaluation of accuracy and timing performance: collision probability for the next 100 control time steps computed in 0.25s on NVIDIA Jetson NX and 0.05s on a reference laptop

## Methodology
- **Perception-based Runtime Modeling:** A probabilistic perception network (YOLO object detection + Monte Carlo Dropout pose estimation) estimates moving obstacle poses as a multivariate Gaussian distribution N(μ_p, σ_p²), capturing both aleatoric and epistemic uncertainty
- **Linearized Motion Model:** A modified kinematic bicycle model is linearized into a discrete state-space model X_{k+1} = A_k X_k, introducing directional components φ_x, φ_y to handle angular nonlinearities
- **Probabilistic Initial Conditions:** Perception, sensing, and actuation uncertainties are transformed into probabilistic initial state distributions using Taylor expansion for error propagation, yielding a standardized initial ProbStar Θ_0
- **ProbStar Reachability Analysis:** Reachable sets Θ_k are computed recursively from the initial ProbStar Θ_0; collision constraints are defined via half-space intersection based on Minkowski differences of vehicle bounding polytopes, and the probability of each ProbStar satisfying the collision constraint is computed in parallel
- **Quantitative Verification Algorithm:** Distinguishes modeling timestep dt_m from reachability timestep dt_r (dt_m can be 10-1000x smaller than dt_r); at each dt_r step, collision probability is computed; also supports verification-guided collision avoidance by evaluating collision probability changes under different steering angles and braking forces
