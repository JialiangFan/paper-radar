# Benchmarks and Evaluation

Task suites, metrics, and protocols for measuring unsafe behavior, constraint violation, and safe task completion.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Zhang_SafeVLA|SafeVLA]] | VLA Safety | SafeVLA treats safety alignment for VLA policies as a constrained learning problem rather than relying on inherited LLM/VLM harmlessness. |
| [[2026_Chen_HazardArena|HazardArena]] | VLA Safety | HazardArena exposes semantic safety failures where the same physical action is safe or unsafe depending on context. |
| [[2025_Ying_AGENTSAFE|AGENTSAFE]] | Embodied AI Safety | AGENTSAFE benchmarks whether embodied VLM agents comply with or refuse hazardous instructions across perception, planning, and execution. |
| [[2024_Kim_OpenVLA|OpenVLA]] | VLA Models | OpenVLA provides an accessible 7B VLA pretrained on diverse robot demonstrations, making it a practical base policy for safety-layer research. |
| [[2026_Li_VLASafetySurvey|VLASafetySurvey]] | VLA Safety | This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem. |
| [[2025_Lu_ISBench|ISBench]] | Embodied AI Safety | IS-Bench evaluates interactive safety, including risks that emerge from an agent's own intermediate actions rather than only from the initial instruction. |
| [[2023_ONeill_OpenXEmbodiment|OpenXEmbodiment]] | VLA Models | Open X-Embodiment standardizes a large multi-robot manipulation dataset and trains RT-X models for cross-embodiment transfer. |
| [[2024_Xie_BadRobot|BadRobot]] | Embodied AI Safety | BadRobot shows that language-level jailbreaks can produce physically unsafe embodied behavior, including mismatches between verbal refusal and executed action. |
| [[2024_Ghosh_Octo|Octo]] | VLA Models | Octo is an open generalist robot policy trained on large-scale robot trajectories and designed for broad manipulation research. |
| [[2026_Li_EmbodiedAISafetySurvey|EmbodiedAISafetySurvey]] | Embodied AI Safety | This survey provides a broad taxonomy of embodied AI risks, attacks, and defenses across perception, cognition, planning, action, interaction, and agent systems. |
| [[2023_Ji_SafetyGymnasium|SafetyGymnasium]] | Benchmarks Evaluation | Safety-Gymnasium standardizes SafeRL tasks, constraints, and algorithms for evaluating reward-constraint trade-offs. |
| [[2022_Brohan_RT1|RT1]] | VLA Models | RT-1 scales language-conditioned real-robot behavior cloning with a transformer policy over tokenized actions. |
| [[2023_Bousmalis_RoboCat|RoboCat]] | VLA Models | RoboCat studies self-improving generalist manipulation across tasks and embodiments. |
| [[2024_Mao_VLASurvey|VLASurvey]] | VLA Models | This survey maps VLA architectures, datasets, training methods, and embodied applications. |
| [[2025_Wang_VLAFool|VLAFool]] | VLA Safety | VLA-Fool studies multimodal perturbations across text, vision, and grounding that cause unsafe or incorrect VLA behavior. |
| [[2026_Wang_VLAReasoningFaithfulness|VLAReasoningFaithfulness]] | VLA Safety | This paper probes whether VLA driving-model reasoning faithfully reflects entities and actions relevant to safety. |
| [[2025_Son_PhysicalSafetyLLMs|PhysicalSafetyLLMs]] | Embodied AI Safety | This paper diagnoses physical safety failures in LLM decision making for embodied contexts. |
| [[2023_Zhao_GUARD|GUARD]] | Benchmarks Evaluation | GUARD provides a generalized benchmark for comparing SafeRL algorithms under diverse constraints and tasks. |
| [[2023_Liu_LIBERO|LIBERO]] | Benchmarks Evaluation | LIBERO provides language-conditioned manipulation task suites for evaluating lifelong robot learning and VLA policies. |
| [[2019_James_RLBench|RLBench]] | Benchmarks Evaluation | RLBench offers a large suite of vision-guided manipulation tasks with generated demonstrations. |
| [[2020_Zhu_robosuite|robosuite]] | Benchmarks Evaluation | robosuite is a modular MuJoCo-based simulation framework widely used for robot learning and manipulation benchmarks. |
| [[2023_Gu_ManiSkill2|ManiSkill2]] | Benchmarks Evaluation | ManiSkill2 provides scalable simulated manipulation tasks with rich object variation, demonstrations, and controller interfaces. |
| [[2019_Ray_SafetyGym|SafetyGym]] | Benchmarks Evaluation | Safety Gym helped standardize constrained RL evaluation for safe exploration. |
| [[2019_Wainwright_SafeLife|SafeLife]] | Benchmarks Evaluation | SafeLife benchmarks side effects and impact regularization in complex gridworld environments. |
