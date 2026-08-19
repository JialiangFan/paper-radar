# Action Shielding

A runtime layer that blocks, masks, projects, or replaces proposed actions that would violate a safety specification.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Hu_VLSA_AEGIS|VLSA_AEGIS]] | VLA Safety | AEGIS wraps VLA actions in a plug-and-play control-barrier-function safety constraint layer to reduce collisions without retraining the base policy. |
| [[2026_Chen_HazardArena|HazardArena]] | VLA Safety | HazardArena exposes semantic safety failures where the same physical action is safe or unsafe depending on context. |
| [[2026_Li_VLASafetySurvey|VLASafetySurvey]] | VLA Safety | This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem. |
| [[2017_Fisac_GeneralSafetyFramework|GeneralSafetyFramework]] | CBF Reachability | Fisac et al. provide a foundational HJ reachability safety framework that supervises arbitrary learning controllers with least-restrictive intervention. |
| [[2017_Ames_CBF_QP|CBF_QP]] | CBF Reachability | This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller. |
| [[2020_Shao_RTS|RTS]] | Action Shielding Safety Filters | RTS uses precomputed forward reachable sets to safeguard continuous-control trajectories selected by an RL policy. |
| [[2018_Wabersich_PredictiveSafetyFilter|PredictiveSafetyFilter]] | Action Shielding Safety Filters | Predictive safety filters turn an unsafe learning controller into a safe closed-loop system by modifying proposed inputs only when needed. |
| [[2026_Li_EmbodiedAISafetySurvey|EmbodiedAISafetySurvey]] | Embodied AI Safety | This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems. |
| [[2018_Dalal_SafeExploration|SafeExploration]] | Action Shielding Safety Filters | Dalal et al. introduce a safety layer that projects continuous actions to satisfy linearized constraints during exploration. |
| [[2017_Alshiekh_Shielding|Shielding]] | Action Shielding Safety Filters | This foundational shielded RL paper synthesizes reactive shields from temporal-logic safety specifications. |
| [[2019_Ames_CBFTheory|CBFTheory]] | CBF Reachability | This tutorial-style paper organizes CBF theory and applications for optimization-based safety-critical control. |
| [[2021_Brunke_SafeLearningRobotics|SafeLearningRobotics]] | CBF Reachability | This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification. |
| [[2026_Ahmed_TAILSafe|TAILSafe]] | Runtime Monitoring Assurance | TAIL-Safe learns an empirical safe set for imitation policies and applies a recovery mechanism when proposed actions leave that set. |
| [[2025_Markgraf_ActionProjection|ActionProjection]] | Action Shielding Safety Filters | This paper analyzes projection-based safety filters and clarifies when to treat projection as part of the policy or the environment. |
| [[2024_Kim_ContinuousShields|ContinuousShields]] | Action Shielding Safety Filters | This paper extends shielding toward continuous state and action spaces with realizability checks. |
| [[2023_Hsu_SafetyFilterUnified|SafetyFilterUnified]] | Action Shielding Safety Filters | This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families. |
| [[2025_Yang_CBFRL|CBFRL]] | CBF Reachability | CBF-RL uses CBF filtering during training so policies internalize safety and may deploy without an online filter. |
| [[2021_Chen_SimplexDrive|SimplexDrive]] | Runtime Monitoring Assurance | Simplex-Drive applies a runtime assurance architecture with an advanced learned controller, verified baseline controller, and mode manager. |
