# Constraint Grounding

Translation of high-level language or visual semantics into concrete constraints over state, action, geometry, or controller variables.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2024_Santos_LanguageSafetyFeedback|LanguageSafetyFeedback]] | Language Specified Constraints | This paper is a direct prototype for grounding natural-language safety feedback into online-updated reachability safety controllers. |
| [[2024_Quartey_LIMP|LIMP]] | Language Specified Constraints | LIMP grounds complex natural-language robot instructions into symbolic specifications and motion-planning behavior that can be checked before execution. |
| [[2023_Huang_VoxPoser|VoxPoser]] | Language Specified Constraints | VoxPoser turns language and visual grounding into 3D value maps that guide closed-loop robot trajectories. |
| [[2024_Xie_SafeMPCFeedback|SafeMPCFeedback]] | Human in the Loop | This paper learns implicit safety constraints for MPC from sparse human directional corrections. |
| [[2025_Tang_GeoManip|GeoManip]] | Language Specified Constraints | GeoManip treats geometric constraints inferred from language and object-part relations as a general interface for robot manipulation. |
| [[2022_Ahn_SayCan|SayCan]] | VLA Models | SayCan combines language-model planning scores with learned affordance scores so plans are both semantically plausible and executable. |
| [[2023_Huang_GroundedDecoding|GroundedDecoding]] | Language Specified Constraints | Grounded Decoding constrains LLM-generated action sequences using grounded environment models during decoding. |
| [[2025_Su_ReSem3D|ReSem3D]] | Language Specified Constraints | ReSem3D uses MLLMs and vision foundation models to build hierarchical 3D spatial constraints from language and RGB-D observations. |
| [[2024_Chen_CoPa|CoPa]] | Language Specified Constraints | CoPa uses foundation models to infer spatial constraints between object parts and solve open-world manipulation tasks. |
| [[2022_Liang_CodeAsPolicies|CodeAsPolicies]] | Language Specified Constraints | Code as Policies shows that LLM-generated programs can compose perception and control APIs for embodied tasks. |
| [[2023_Yu_LanguageToRewards|LanguageToRewards]] | Language Specified Constraints | Language to Rewards uses LLMs to translate instructions and corrections into reward functions for low-level skill synthesis. |
| [[2020_Robey_LearningCBF|LearningCBF]] | CBF Reachability | This paper learns CBFs from demonstrations, reducing the need to hand-design safe-set functions. |
| [[2023_McPherson_SharedSafetyConstraints|SharedSafetyConstraints]] | Language Specified Constraints | This paper learns safety constraints shared across tasks from demonstrations, such as avoiding breaking plates regardless of the current goal. |
| [[2025_Guo_CaStL|CaStL]] | Language Specified Constraints | CaStL translates natural-language constraints into formal planning specifications. |
