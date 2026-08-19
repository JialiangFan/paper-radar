# State-Space Safety

Safety properties stated over robot or environment state variables, including position, velocity, force, torque, joint limits, and set invariance.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Hu_VLSA_AEGIS|VLSA_AEGIS]] | VLA Safety | AEGIS wraps VLA actions in a plug-and-play control-barrier-function safety constraint layer to reduce collisions without retraining the base policy. |
| [[2017_Fisac_GeneralSafetyFramework|GeneralSafetyFramework]] | CBF Reachability | Fisac et al. provide a foundational HJ reachability safety framework that supervises arbitrary learning controllers with least-restrictive intervention. |
| [[2017_Ames_CBF_QP|CBF_QP]] | CBF Reachability | This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller. |
| [[2020_Shao_RTS|RTS]] | Action Shielding Safety Filters | RTS uses precomputed forward reachable sets to safeguard continuous-control trajectories selected by an RL policy. |
| [[2018_Wabersich_PredictiveSafetyFilter|PredictiveSafetyFilter]] | Action Shielding Safety Filters | Predictive safety filters turn an unsafe learning controller into a safe closed-loop system by modifying proposed inputs only when needed. |
| [[2024_Xie_SafeMPCFeedback|SafeMPCFeedback]] | Human in the Loop | This paper learns implicit safety constraints for MPC from sparse human directional corrections. |
| [[2025_Bajcsy_SparseHumanSafety|SparseHumanSafety]] | Human in the Loop | The paper uses sparse human feedback and conformal prediction to learn when robot behavior should be considered unsafe. |
| [[2023_Ji_SafetyGymnasium|SafetyGymnasium]] | Benchmarks Evaluation | Safety-Gymnasium standardizes SafeRL tasks, constraints, and algorithms for evaluating reward-constraint trade-offs. |
| [[2018_Dalal_SafeExploration|SafeExploration]] | Action Shielding Safety Filters | Dalal et al. introduce a safety layer that projects continuous actions to satisfy linearized constraints during exploration. |
| [[2017_Alshiekh_Shielding|Shielding]] | Action Shielding Safety Filters | This foundational shielded RL paper synthesizes reactive shields from temporal-logic safety specifications. |
| [[2019_Ames_CBFTheory|CBFTheory]] | CBF Reachability | This tutorial-style paper organizes CBF theory and applications for optimization-based safety-critical control. |
| [[2026_Ahmed_TAILSafe|TAILSafe]] | Runtime Monitoring Assurance | TAIL-Safe learns an empirical safe set for imitation policies and applies a recovery mechanism when proposed actions leave that set. |
| [[2023_Yu_LanguageToRewards|LanguageToRewards]] | Language Specified Constraints | Language to Rewards uses LLMs to translate instructions and corrections into reward functions for low-level skill synthesis. |
| [[2025_Markgraf_ActionProjection|ActionProjection]] | Action Shielding Safety Filters | This paper analyzes projection-based safety filters and clarifies when to treat projection as part of the policy or the environment. |
| [[2024_Kim_ContinuousShields|ContinuousShields]] | Action Shielding Safety Filters | This paper extends shielding toward continuous state and action spaces with realizability checks. |
| [[2021_Herbert_ScalableHJ|ScalableHJ]] | CBF Reachability | This paper learns approximations to Hamilton-Jacobi reachability to improve scalability of formal safety guarantees. |
| [[2022_Lederer_ElasticJointCBF|ElasticJointCBF]] | CBF Reachability | The paper shows how CBF safety can be robustified for elastic-joint robots with uncertain dynamics. |
| [[2020_Robey_LearningCBF|LearningCBF]] | CBF Reachability | This paper learns CBFs from demonstrations, reducing the need to hand-design safe-set functions. |
| [[2023_Yuan_ConBaT|ConBaT]] | CBF Reachability | ConBaT brings CBF-inspired safety into transformer policy learning. |
| [[2024_Betzer_DigitalTwinRV|DigitalTwinRV]] | Runtime Monitoring Assurance | This paper uses a digital twin as a runtime verification watchdog for autonomous mobile robots under uncertainty. |
| [[2023_Zhao_GUARD|GUARD]] | Benchmarks Evaluation | GUARD provides a generalized benchmark for comparing SafeRL algorithms under diverse constraints and tasks. |
| [[2019_Ray_SafetyGym|SafetyGym]] | Benchmarks Evaluation | Safety Gym helped standardize constrained RL evaluation for safe exploration. |
| [[2023_McPherson_SharedSafetyConstraints|SharedSafetyConstraints]] | Language Specified Constraints | This paper learns safety constraints shared across tasks from demonstrations, such as avoiding breaking plates regardless of the current goal. |
