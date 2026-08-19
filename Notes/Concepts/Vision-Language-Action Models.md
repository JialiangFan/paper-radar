# Vision-Language-Action Models

Policies that map visual observations, language instructions, and robot state into executable actions or plans.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Zhang_SafeVLA|SafeVLA]] | VLA Safety | SafeVLA treats safety alignment for VLA policies as a constrained learning problem rather than relying on inherited LLM/VLM harmlessness. |
| [[2025_Ying_AGENTSAFE|AGENTSAFE]] | Embodied AI Safety | AGENTSAFE benchmarks whether embodied VLM agents comply with or refuse hazardous instructions across perception, planning, and execution. |
| [[2023_Brohan_RT2|RT2]] | VLA Models | RT-2 popularized the VLA formulation by co-training web-scale vision-language models and robotic action prediction through action tokenization. |
| [[2024_Kim_OpenVLA|OpenVLA]] | VLA Models | OpenVLA provides an accessible 7B VLA pretrained on diverse robot demonstrations, making it a practical base policy for safety-layer research. |
| [[2026_Li_VLASafetySurvey|VLASafetySurvey]] | VLA Safety | This survey organizes VLA safety across attack timing and defense timing, explicitly identifying unified runtime safety architectures as an open problem. |
| [[2024_Agia_Sentinel|Sentinel]] | Runtime Monitoring Assurance | Sentinel separates fast action-consistency failures from slower task-progress failures for runtime monitoring of generative robot policies. |
| [[2023_Driess_PaLME|PaLME]] | VLA Models | PaLM-E injects embodied visual and state observations into a large language model for multimodal embodied reasoning. |
| [[2024_Black_Pi0|Pi0]] | VLA Models | π0 uses flow matching and a pretrained VLM backbone for high-frequency continuous robot control across diverse embodiments. |
| [[2023_ONeill_OpenXEmbodiment|OpenXEmbodiment]] | VLA Models | Open X-Embodiment standardizes a large multi-robot manipulation dataset and trains RT-X models for cross-embodiment transfer. |
| [[2024_Duan_AHA|AHA]] | Runtime Monitoring Assurance | AHA fine-tunes a VLM to detect and explain manipulation failures, turning failure recognition into a reusable monitor signal. |
| [[2024_Ghosh_Octo|Octo]] | VLA Models | Octo is an open generalist robot policy trained on large-scale robot trajectories and designed for broad manipulation research. |
| [[2022_Brohan_RT1|RT1]] | VLA Models | RT-1 scales language-conditioned real-robot behavior cloning with a transformer policy over tokenized actions. |
| [[2022_Ahn_SayCan|SayCan]] | VLA Models | SayCan combines language-model planning scores with learned affordance scores so plans are both semantically plausible and executable. |
| [[2023_Huang_GroundedDecoding|GroundedDecoding]] | Language Specified Constraints | Grounded Decoding constrains LLM-generated action sequences using grounded environment models during decoding. |
| [[2022_Liang_CodeAsPolicies|CodeAsPolicies]] | Language Specified Constraints | Code as Policies shows that LLM-generated programs can compose perception and control APIs for embodied tasks. |
| [[2023_Yuan_ConBaT|ConBaT]] | CBF Reachability | ConBaT brings CBF-inspired safety into transformer policy learning. |
| [[2024_Liu_RDT1B|RDT1B]] | VLA Models | RDT-1B scales diffusion-transformer robot policies to bimanual manipulation with a physically interpretable unified action space. |
| [[2024_Cheang_GR2|GR2]] | VLA Models | GR-2 pretrains on web-scale video and fine-tunes for video generation and action prediction in robot manipulation. |
| [[2024_Zheng_TraceVLA|TraceVLA]] | VLA Models | TraceVLA encodes state-action history as visual traces to improve spatial-temporal awareness in VLA policies. |
| [[2023_Bousmalis_RoboCat|RoboCat]] | VLA Models | RoboCat studies self-improving generalist manipulation across tasks and embodiments. |
| [[2025_Shukor_SmolVLA|SmolVLA]] | VLA Models | SmolVLA explores smaller, efficient VLA models trained on community robotics data. |
| [[2024_Mao_VLASurvey|VLASurvey]] | VLA Models | This survey maps VLA architectures, datasets, training methods, and embodied applications. |
| [[2025_Peng_FailSafeVLA|FailSafeVLA]] | VLA Safety | FailSafe targets failure detection and recovery for VLA manipulation policies rather than only offline evaluation. |
| [[2023_Liu_LIBERO|LIBERO]] | Benchmarks Evaluation | LIBERO provides language-conditioned manipulation task suites for evaluating lifelong robot learning and VLA policies. |
| [[2019_James_RLBench|RLBench]] | Benchmarks Evaluation | RLBench offers a large suite of vision-guided manipulation tasks with generated demonstrations. |
| [[2023_Gu_ManiSkill2|ManiSkill2]] | Benchmarks Evaluation | ManiSkill2 provides scalable simulated manipulation tasks with rich object variation, demonstrations, and controller interfaces. |
