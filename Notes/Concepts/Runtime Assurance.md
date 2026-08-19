# Runtime Assurance

A system architecture that supervises an advanced controller and can switch, intervene, or filter to preserve safety.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2017_Fisac_GeneralSafetyFramework|GeneralSafetyFramework]] | CBF Reachability | Fisac et al. provide a foundational HJ reachability safety framework that supervises arbitrary learning controllers with least-restrictive intervention. |
| [[2024_Quartey_LIMP|LIMP]] | Language Specified Constraints | LIMP grounds complex natural-language robot instructions into symbolic specifications and motion-planning behavior that can be checked before execution. |
| [[2018_Wabersich_PredictiveSafetyFilter|PredictiveSafetyFilter]] | Action Shielding Safety Filters | Predictive safety filters turn an unsafe learning controller into a safe closed-loop system by modifying proposed inputs only when needed. |
| [[2023_Liu_SiriusMonitor|SiriusMonitor]] | Runtime Monitoring Assurance | This paper learns a runtime monitor from trustworthy deployments to predict future failures and reduce human supervision load. |
| [[2017_Alshiekh_Shielding|Shielding]] | Action Shielding Safety Filters | This foundational shielded RL paper synthesizes reactive shields from temporal-logic safety specifications. |
| [[2021_Brunke_SafeLearningRobotics|SafeLearningRobotics]] | CBF Reachability | This survey unifies safe learning-based control and safe RL for robotics, emphasizing uncertainty-aware safety certification. |
| [[2024_Kim_ContinuousShields|ContinuousShields]] | Action Shielding Safety Filters | This paper extends shielding toward continuous state and action spaces with realizability checks. |
| [[2023_Hsu_SafetyFilterUnified|SafetyFilterUnified]] | Action Shielding Safety Filters | This paper provides a modular view of safety filters across CBF, reachability, MPC, and data-driven families. |
| [[2025_Zhang_RoboSafe|RoboSafe]] | Embodied AI Safety | RoboSafe proposes executable safety logic and predictive reasoning for embodied agents facing hazardous instructions. |
| [[2021_Chen_SimplexDrive|SimplexDrive]] | Runtime Monitoring Assurance | Simplex-Drive applies a runtime assurance architecture with an advanced learned controller, verified baseline controller, and mode manager. |
| [[2024_Vardal_LearningRuntimeMonitors|LearningRuntimeMonitors]] | Runtime Monitoring Assurance | This paper proposes learning safety monitors for ML components when ground truth is unavailable at runtime. |
| [[2024_Betzer_DigitalTwinRV|DigitalTwinRV]] | Runtime Monitoring Assurance | This paper uses a digital twin as a runtime verification watchdog for autonomous mobile robots under uncertainty. |
| [[2025_Guo_CaStL|CaStL]] | Language Specified Constraints | CaStL translates natural-language constraints into formal planning specifications. |
| [[2026_Yuan_ContextualRuntimeMonitors|ContextualRuntimeMonitors]] | Runtime Monitoring Assurance | This paper formulates monitor selection for AI controller ensembles as a contextual monitoring problem. |
