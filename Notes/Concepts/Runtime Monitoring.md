# Runtime Monitoring

Inference-time observation of policy inputs, internal signals, outputs, or predicted futures to detect failures before or during execution.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2026_Li_VLASafetySurvey|VLASafetySurvey]] | VLA Safety | This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem. |
| [[2023_Ren_KnowNo|KnowNo]] | Human in the Loop | KnowNo uses conformal prediction to calibrate when an LLM-based robot planner should ask for human help under ambiguity. |
| [[2024_Agia_Sentinel|Sentinel]] | Runtime Monitoring Assurance | Sentinel separates fast action-consistency failures from slower task-progress failures for runtime monitoring of generative robot policies. |
| [[2025_Lu_ISBench|ISBench]] | Embodied AI Safety | IS-Bench evaluates interactive safety, including risks that emerge from an agent's own intermediate actions rather than only from the initial instruction. |
| [[2024_Xie_BadRobot|BadRobot]] | Embodied AI Safety | BadRobot shows that language-level jailbreaks can produce physically unsafe embodied behavior, including mismatches between verbal refusal and executed action. |
| [[2024_Robey_RoboPAIR|RoboPAIR]] | Embodied AI Safety | RoboPAIR adapts jailbreak search to LLM-controlled robots and demonstrates that unsafe physical actions can be elicited across access regimes. |
| [[2024_Duan_AHA|AHA]] | Runtime Monitoring Assurance | AHA fine-tunes a VLM to detect and explain manipulation failures, turning failure recognition into a reusable monitor signal. |
| [[2025_Bajcsy_SparseHumanSafety|SparseHumanSafety]] | Human in the Loop | The paper uses sparse human feedback and conformal prediction to learn when robot behavior should be considered unsafe. |
| [[2026_Li_EmbodiedAISafetySurvey|EmbodiedAISafetySurvey]] | Embodied AI Safety | This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems. |
| [[2023_Liu_SiriusMonitor|SiriusMonitor]] | Runtime Monitoring Assurance | This paper learns a runtime monitor from trustworthy deployments to predict future failures and reduce human supervision load. |
| [[2026_Ahmed_TAILSafe|TAILSafe]] | Runtime Monitoring Assurance | TAIL-Safe learns an empirical safe set for imitation policies and applies a recovery mechanism when proposed actions leave that set. |
| [[2025_Peng_FailSafeVLA|FailSafeVLA]] | VLA Safety | FailSafe targets failure detection and recovery for VLA manipulation policies rather than only offline evaluation. |
| [[2025_Wang_VLAFool|VLAFool]] | VLA Safety | VLA-Fool studies multimodal perturbations across text, vision, and grounding that cause unsafe or incorrect VLA behavior. |
| [[2026_Wang_VLAReasoningFaithfulness|VLAReasoningFaithfulness]] | VLA Safety | This paper probes whether VLA driving-model reasoning faithfully reflects entities and actions relevant to safety. |
| [[2025_Zhang_RoboSafe|RoboSafe]] | Embodied AI Safety | RoboSafe proposes executable safety logic and predictive reasoning for embodied agents facing hazardous instructions. |
| [[2021_Chen_SimplexDrive|SimplexDrive]] | Runtime Monitoring Assurance | Simplex-Drive applies a runtime assurance architecture with an advanced learned controller, verified baseline controller, and mode manager. |
| [[2024_Vardal_LearningRuntimeMonitors|LearningRuntimeMonitors]] | Runtime Monitoring Assurance | This paper proposes learning safety monitors for ML components when ground truth is unavailable at runtime. |
| [[2024_Betzer_DigitalTwinRV|DigitalTwinRV]] | Runtime Monitoring Assurance | This paper uses a digital twin as a runtime verification watchdog for autonomous mobile robots under uncertainty. |
| [[2025_Schotschneider_RuntimePerceptionSurvey|RuntimePerceptionSurvey]] | Runtime Monitoring Assurance | This survey categorizes runtime monitors for DNN perception by monitoring inputs, internal representations, and outputs. |
| [[2020_Mandlekar_HITLTeleoperation|HITLTeleoperation]] | Human in the Loop | This work uses remote human interventions to collect corrective demonstrations for safer and more efficient imitation learning. |
| [[2026_Yuan_ContextualRuntimeMonitors|ContextualRuntimeMonitors]] | Runtime Monitoring Assurance | This paper formulates monitor selection for AI controller ensembles as a contextual monitoring problem. |
