# Deterministic World Models for Verification of Closed-loop Vision-based Systems

## Topic
Vision-based System Verification

## Background
Closed-loop vision-based control systems are increasingly deployed in safety-critical domains, relying on end-to-end controllers to process images and operate physical plants. Verifying such systems faces two fundamental challenges: the difficulty of accurately modeling complex visual environments, and the computational scalability bottleneck caused by high-dimensional images. Recent work uses generative world models (e.g., cGANs) as camera surrogates, but their reliance on stochastic latent variables introduces unnecessary overapproximation error for verification.

## Limitations & Research Problem
- **Limitation:** Existing cGAN-based world models use stochastic latent variables to generate image diversity, but these latent variables lack physical interpretability, making it inherently difficult to define valid input bounds for reachability analysis. Widening latent bounds causes reachable sets to explode with excessive overapproximation error. Meanwhile, symbolic techniques are limited to highly structured environments and cannot handle dynamic, complex scenes.
- **Problem:** How to build a verifiable world model without stochastic latent variables that integrates seamlessly with star-based reachability analysis and provides rigorous safety guarantees for closed-loop vision-based systems?

## Contributions
- Proposes the Deterministic World Model (DWM) that maps physical system states directly to images, eliminating uninterpretable stochastic latent variables and ensuring precise, physically meaningful input bounds
- Designs a dual-objective training loss: image reconstruction loss (weighted MSE emphasizing semantically important regions) + controller difference loss (ensuring generated images produce control actions consistent with real images)
- First adoption of Star/ImageStar-based reachability analysis for verification of closed-loop vision-based systems, constraining DWM input dimensions to physical state dimensions for scalability
- Uses conformal prediction to establish statistical upper bounds on trajectory deviation between the world model and the real system, transferring verification results from the surrogate to the real system

## Methodology
- **DWM architecture:** Implements a state-to-image decoder g_θ: S → I with fully connected layers followed by transposed convolution layers, taking low-dimensional physical states (e.g., position, velocity) as input and producing high-dimensional grayscale images (e.g., 96x96)
- **Training loss:** Total loss L(θ) = L_rec(I, Î) + λL_ctrl(I, Î), where L_rec uses pixel-intensity-based weighted MSE (high weight w_h for dark regions/objects, low weight w_l for bright background), and L_ctrl = ||C(Î) - C(I)||² enforces control behavior consistency
- **Star-set reachability analysis:** Represents initial state uncertainty as Star set S_0 = {s = c_0 + V_0α | C_0α ≤ d_0, l_0 ≤ α ≤ u_0}; propagates layer-by-layer through DWM and CNN controller (exact mapping for affine layers, sound over-approximation via StarV for nonlinear activations); outputs an ImageStar capturing the complete envelope of all admissible generated images
- **Closed-loop verification pipeline:** At each time step, propagates current state set R_t through DWM to produce ImageStar I_img, then through CNN controller to compute control action set U, uses PyBDR to compute next reachable state set R_{t+1} = R_dyn(R_t, U_t), iterating to obtain a finite-time reachable tube
- **Conformal prediction transfer:** Defines trajectory-based non-conformity scores, computes statistical upper bounds from a calibration dataset, guaranteeing with probability 1-α that the real system trajectory is contained within an expanded version of the world model's reachable tube
- **Experimental validation:** Evaluated on CartPole, MountainCar, and Pendulum (OpenAI Gym benchmarks), showing DWM produces significantly tighter reachable sets and higher F1 verification accuracy compared to latent-variable baselines
