# GeoPT - Scaling Physics Simulation via Lifted Geometric Pre-Training

## Topic
Geometric Pre-Training for Physics Simulation

## Background
Neural simulators have emerged as efficient surrogates for classical numerical solvers, accelerating physics simulation across scientific discovery and engineering design. However, achieving industrial-fidelity accuracy is bottlenecked by the prohibitive cost of generating high-fidelity training data (e.g., a single DrivAerML sample costs 6.1×10⁴ CPU-hours). While abundant 3D geometries are freely available from public repositories, self-supervised pre-training on static geometry alone ignores dynamics and can even lead to negative transfer on downstream physics tasks.

## Limitations & Research Problem
- **Limitation:** Neural simulator training relies heavily on solver-generated labeled data, where per-sample computational cost scales sharply with geometry and physics complexity, severely limiting scalability.
- **Limitation:** Existing self-supervised pre-training methods (e.g., predicting SDF or vector distance) operate only within the native geometry space, ignoring the geometry-dynamics coupling. The learned representations fundamentally misalign with those required for downstream physics tasks (the geometry-physics gap).
- **Limitation:** Existing physics foundation models (e.g., Poseidon, DPOT, P3D) still rely on large-scale physics simulation data for pre-training and are restricted to specific physics families on regular grids, failing to generalize to industrial-scale simulations.
- **Problem:** How to pre-train neural simulators solely on abundant unlabeled geometry data such that the learned representations capture geometry-dynamics coupling, enabling faster convergence and improved accuracy with fewer physics labels?

## Contributions
- Proposes **dynamics-lifted geometric pre-training**: augmenting geometry with randomly sampled synthetic velocity fields to lift pre-training from the native geometry space to a joint geometry-dynamics space, enabling dynamics-aware self-supervision without physics labels.
- Introduces **GeoPT**, a unified pre-trained model for general physics simulation, pre-trained on over one million samples from 10,000+ ShapeNet geometries, applicable to aerodynamics, hydrodynamics, crash simulation, and beyond.
- Demonstrates consistent improvements across 5 industrial-fidelity benchmarks: 20-60% reduction in physics data requirements, up to 2× faster convergence, and favorable scaling with both model size and data volume.
- Provides theoretical justification showing that GeoPT pre-training is equivalent to solving a collisionless transport equation with sticking boundaries, learning a universal physics prior satisfying mass conservation.

## Methodology
- **Core idea — Lifted Pre-Training:** Downstream physics simulation depends on coupled geometry G and dynamics conditions S, yet geometry pre-training only involves G. GeoPT bridges this gap by augmenting each geometry with randomly sampled per-point synthetic velocities v ~ Unif(B^C), constructing particle trajectories under geometry boundary constraints, and extending supervision from static geometric features (vector distance) to dynamic feature trajectory sequences h_G(x_{0:τ}).
- **Pre-training objective:** Model F_θ receives query position x, geometry G, and velocity field V, predicting the vector distance sequence along the trajectory: L^pre_lifted = E[||F_θ(x; G, V) - h_G(x_{0:τ})||²]. Default discretization uses τ=2 steps with 100 dynamic fields per geometry.
- **Pre-training data:** Uses ShapeNet (Chang et al., 2015) subsets of cars, airplanes, and watercraft (~13,000 geometries), sampling 32,768 volume points and 4,096 surface points per shape, generating ~1.35M samples (~5TB). Geometric features computed via FCPW-accelerated ray-triangle intersection in ~3 days on 80 CPU cores.
- **Fine-tuning adaptation:** Replaces random velocity fields with task-specific velocity fields V_S (e.g., freestream velocity for aerodynamics, impact direction for crash), enabling a unified interface across diverse physics domains.
- **Backbone:** Adopts Transolver (Wu et al., 2024) as the default architecture-agnostic backbone, with Base (3M), Large (7M), and Huge (15M) parameter configurations.
- **Experimental setup:**
  - **Benchmarks:** DrivAerML (car aerodynamics), NASA-CRM (aircraft aerodynamics), AirCraft (flight aerodynamics), DTCHull (ship hydrodynamics), Car-Crash (crash simulation), plus extended Radiosity task
  - **Baselines:** From-scratch Transolver, Geometry-Only Pre-Training (vector distance/SDF prediction), Geometry-Only Conditioning (Hunyuan3D VAE encoder), other backbones (Galerkin Transformer, GNOT, UPT, Transolver++)
  - **Metrics:** Relative L2 error; focus on data efficiency (data saving) and convergence acceleration
