# Semantic Safety

Safety properties expressed in language or semantic categories, such as hazards, fragile objects, people, tools, or forbidden activities.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Zhang_SafeVLA|SafeVLA]] | VLA Safety | SafeVLA treats safety alignment for VLA policies as a constrained learning problem rather than relying on inherited LLM/VLM harmlessness. |
| [[2026_Chen_HazardArena|HazardArena]] | VLA Safety | HazardArena exposes semantic safety failures where the same physical action is safe or unsafe depending on context. |
| [[2024_Santos_LanguageSafetyFeedback|LanguageSafetyFeedback]] | Language Specified Constraints | This paper is a direct prototype for grounding natural-language safety feedback into online-updated reachability safety controllers. |
| [[2025_Ying_AGENTSAFE|AGENTSAFE]] | Embodied AI Safety | AGENTSAFE benchmarks whether embodied VLM agents comply with or refuse hazardous instructions across perception, planning, and execution. |
| [[2023_Brohan_RT2|RT2]] | VLA Models | RT-2 popularized the VLA formulation by co-training web-scale vision-language models and robotic action prediction through action tokenization. |
| [[2026_Li_VLASafetySurvey|VLASafetySurvey]] | VLA Safety | This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem. |
| [[2023_Ren_KnowNo|KnowNo]] | Human in the Loop | KnowNo uses conformal prediction to calibrate when an LLM-based robot planner should ask for human help under ambiguity. |
| [[2024_Quartey_LIMP|LIMP]] | Language Specified Constraints | LIMP grounds complex natural-language robot instructions into symbolic specifications and motion-planning behavior that can be checked before execution. |
| [[2024_Agia_Sentinel|Sentinel]] | Runtime Monitoring Assurance | Sentinel separates fast action-consistency failures from slower task-progress failures for runtime monitoring of generative robot policies. |
| [[2023_Huang_VoxPoser|VoxPoser]] | Language Specified Constraints | VoxPoser turns language and visual grounding into 3D value maps that guide closed-loop robot trajectories. |
| [[2025_Lu_ISBench|ISBench]] | Embodied AI Safety | IS-Bench evaluates interactive safety, including risks that emerge from an agent's own intermediate actions rather than only from the initial instruction. |
| [[2023_Driess_PaLME|PaLME]] | VLA Models | PaLM-E injects embodied visual and state observations into a large language model for multimodal embodied reasoning. |
| [[2024_Xie_BadRobot|BadRobot]] | Embodied AI Safety | BadRobot shows that language-level jailbreaks can produce physically unsafe embodied behavior, including mismatches between verbal refusal and executed action. |
| [[2024_Robey_RoboPAIR|RoboPAIR]] | Embodied AI Safety | RoboPAIR adapts jailbreak search to LLM-controlled robots and demonstrates that unsafe physical actions can be elicited across access regimes. |
| [[2024_Duan_AHA|AHA]] | Runtime Monitoring Assurance | AHA fine-tunes a VLM to detect and explain manipulation failures, turning failure recognition into a reusable monitor signal. |
| [[2025_Tang_GeoManip|GeoManip]] | Language Specified Constraints | GeoManip treats geometric constraints inferred from language and object-part relations as a general interface for robot manipulation. |
| [[2026_Li_EmbodiedAISafetySurvey|EmbodiedAISafetySurvey]] | Embodied AI Safety | This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems. |
| [[2022_Ahn_SayCan|SayCan]] | VLA Models | SayCan combines language-model planning scores with learned affordance scores so plans are both semantically plausible and executable. |
| [[2023_Huang_GroundedDecoding|GroundedDecoding]] | Language Specified Constraints | Grounded Decoding constrains LLM-generated action sequences using grounded environment models during decoding. |
| [[2025_Su_ReSem3D|ReSem3D]] | Language Specified Constraints | ReSem3D uses MLLMs and vision foundation models to build hierarchical 3D spatial constraints from language and RGB-D observations. |
| [[2024_Chen_CoPa|CoPa]] | Language Specified Constraints | CoPa uses foundation models to infer spatial constraints between object parts and solve open-world manipulation tasks. |
| [[2022_Liang_CodeAsPolicies|CodeAsPolicies]] | Language Specified Constraints | Code as Policies shows that LLM-generated programs can compose perception and control APIs for embodied tasks. |
| [[2023_Yu_LanguageToRewards|LanguageToRewards]] | Language Specified Constraints | Language to Rewards uses LLMs to translate instructions and corrections into reward functions for low-level skill synthesis. |
| [[2024_Cheang_GR2|GR2]] | VLA Models | GR-2 pretrains on web-scale video and fine-tunes for video generation and action prediction in robot manipulation. |
| [[2025_Peng_FailSafeVLA|FailSafeVLA]] | VLA Safety | FailSafe targets failure detection and recovery for VLA manipulation policies rather than only offline evaluation. |
| [[2025_Wang_VLAFool|VLAFool]] | VLA Safety | VLA-Fool studies multimodal perturbations across text, vision, and grounding that cause unsafe or incorrect VLA behavior. |
| [[2026_Wang_VLAReasoningFaithfulness|VLAReasoningFaithfulness]] | VLA Safety | This paper probes whether VLA driving-model reasoning faithfully reflects entities and actions relevant to safety. |
| [[2025_Zhang_RoboSafe|RoboSafe]] | Embodied AI Safety | RoboSafe proposes executable safety logic and predictive reasoning for embodied agents facing hazardous instructions. |
| [[2025_Son_PhysicalSafetyLLMs|PhysicalSafetyLLMs]] | Embodied AI Safety | This paper diagnoses physical safety failures in LLM decision making for embodied contexts. |
| [[2025_Schotschneider_RuntimePerceptionSurvey|RuntimePerceptionSurvey]] | Runtime Monitoring Assurance | This survey categorizes runtime monitors for DNN perception by monitoring inputs, internal representations, and outputs. |
