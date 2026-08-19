# Control Barrier Functions

Control-theoretic certificates that enforce forward invariance of a safe set through inequality constraints on controls.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Hu_VLSA_AEGIS|VLSA_AEGIS]] | VLA Safety | AEGIS wraps VLA actions in a plug-and-play control-barrier-function safety constraint layer to reduce collisions without retraining the base policy. |
| [[2017_Ames_CBF_QP|CBF_QP]] | CBF Reachability | This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller. |
| [[2019_Ames_CBFTheory|CBFTheory]] | CBF Reachability | This tutorial-style paper organizes CBF theory and applications for optimization-based safety-critical control. |
| [[2021_Brunke_SafeLearningRobotics|SafeLearningRobotics]] | CBF Reachability | This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification. |
| [[2023_Hsu_SafetyFilterUnified|SafetyFilterUnified]] | Action Shielding Safety Filters | This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families. |
| [[2022_Lederer_ElasticJointCBF|ElasticJointCBF]] | CBF Reachability | The paper shows how CBF safety can be robustified for elastic-joint robots with uncertain dynamics. |
| [[2020_Robey_LearningCBF|LearningCBF]] | CBF Reachability | This paper learns CBFs from demonstrations, reducing the need to hand-design safe-set functions. |
| [[2025_Yang_CBFRL|CBFRL]] | CBF Reachability | CBF-RL uses CBF filtering during training so policies internalize safety and may deploy without an online filter. |
| [[2023_Yuan_ConBaT|ConBaT]] | CBF Reachability | ConBaT brings CBF-inspired safety into transformer policy learning. |
