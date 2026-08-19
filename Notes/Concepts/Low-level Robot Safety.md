# Low-level Robot Safety

Hardware and controller constraints such as joint limits, velocity limits, torque limits, force limits, collision bounds, and braking.

## Relevance To Safe VLA

For the preferred project direction, this concept should be treated as part of a runtime assurance stack rather than an isolated model property.

## Linked Papers

| Paper | Category | Relevance |
|---|---|---|
| [[2025_Hu_VLSA_AEGIS|VLSA_AEGIS]] | VLA Safety | AEGIS wraps VLA actions in a plug-and-play control-barrier-function safety constraint layer to reduce collisions without retraining the base policy. |
| [[2017_Ames_CBF_QP|CBF_QP]] | CBF Reachability | This is the core CBF-QP formulation for enforcing forward invariance of safe sets while staying close to a nominal controller. |
| [[2024_Black_Pi0|Pi0]] | VLA Models | π0 uses flow matching and a pretrained VLM backbone for high-frequency continuous robot control across diverse embodiments. |
| [[2023_Ji_SafetyGymnasium|SafetyGymnasium]] | Benchmarks Evaluation | Safety-Gymnasium standardizes SafeRL tasks, constraints, and algorithms for evaluating reward-constraint trade-offs. |
| [[2018_Dalal_SafeExploration|SafeExploration]] | Action Shielding Safety Filters | Dalal et al. introduce a safety layer that projects continuous actions to satisfy linearized constraints during exploration. |
| [[2022_Lederer_ElasticJointCBF|ElasticJointCBF]] | CBF Reachability | The paper shows how CBF safety can be robustified for elastic-joint robots with uncertain dynamics. |
| [[2025_Yang_CBFRL|CBFRL]] | CBF Reachability | CBF-RL uses CBF filtering during training so policies internalize safety and may deploy without an online filter. |
| [[2024_Liu_RDT1B|RDT1B]] | VLA Models | RDT-1B scales diffusion-transformer robot policies to bimanual manipulation with a physically interpretable unified action space. |
| [[2025_Shukor_SmolVLA|SmolVLA]] | VLA Models | SmolVLA explores smaller, efficient VLA models trained on community robotics data. |
| [[2020_Zhu_robosuite|robosuite]] | Benchmarks Evaluation | robosuite is a modular MuJoCo-based simulation framework widely used for robot learning and manipulation benchmarks. |
