# Reachability Analysis

Formal computation of states from which a system can remain safe or avoid unsafe sets under dynamics and disturbances.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2024_Santos_LanguageSafetyFeedback|LanguageSafetyFeedback]] | Language Specified Constraints | This paper is a direct prototype for grounding natural-language safety feedback into online-updated reachability safety controllers. |
| [[2017_Fisac_GeneralSafetyFramework|GeneralSafetyFramework]] | CBF Reachability | Fisac et al. provide a foundational HJ reachability safety framework that supervises arbitrary learning controllers with least-restrictive intervention. |
| [[2020_Shao_RTS|RTS]] | Action Shielding Safety Filters | RTS uses precomputed forward reachable sets to safeguard continuous-control trajectories selected by an RL policy. |
| [[2021_Brunke_SafeLearningRobotics|SafeLearningRobotics]] | CBF Reachability | This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification. |
| [[2023_Hsu_SafetyFilterUnified|SafetyFilterUnified]] | Action Shielding Safety Filters | This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families. |
| [[2021_Herbert_ScalableHJ|ScalableHJ]] | CBF Reachability | This paper learns approximations to Hamilton-Jacobi reachability to improve scalability of formal safety guarantees. |
