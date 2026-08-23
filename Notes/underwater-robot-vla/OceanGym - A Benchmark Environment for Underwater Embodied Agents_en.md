# OceanGym: A Benchmark Environment for Underwater Embodied Agents

## Topic
Comprehensive simulation benchmark for evaluating multimodal LLM-driven underwater embodied agents across perception and decision-making tasks.

## Background
Underwater environments present extreme challenges for embodied AI agents, including severely limited visibility, dynamic ocean currents, and the need to interpret non-standard sensor modalities like sonar. Despite significant progress in embodied AI on land, there has been no comprehensive benchmark specifically designed for ocean underwater agents. OceanGym fills this gap by providing a high-fidelity simulation platform built on Unreal Engine 5.3 and HoloOcean, spanning approximately 800m x 800m with dynamically adjustable depth (50m shallow / 500m deep water), enabling systematic evaluation of multimodal LLMs as underwater autonomous vehicle controllers.

## Limitations & Research Problem
- **Limitation:** Existing embodied AI benchmarks focus almost exclusively on terrestrial or indoor environments, leaving underwater agent capabilities largely untested. Current MLLMs have not been evaluated under the unique perceptual challenges of underwater settings (low visibility, sonar interpretation, dynamic currents).
- **Problem:** How capable are state-of-the-art multimodal LLMs at underwater perception, navigation, and decision-making compared to human experts, and what are their fundamental failure modes in these extreme conditions?

## Contributions
1. First comprehensive benchmark environment specifically designed for underwater embodied agents, featuring 8 task domains spanning perception and decision-making across varying visibility conditions
2. A unified agent framework modeling underwater navigation as a POMDP with multimodal perception (RGB + sonar), sliding-window memory architecture, and MLLM-parameterized discrete action policies
3. Systematic evaluation revealing that state-of-the-art MLLMs (GPT-4o-mini, Gemini, Qwen2.5-VL-7B) exhibit 43-85 percentage point gaps compared to human experts, with decision success rates dropping to 14.8% in low-visibility deep water
4. Critical finding that MLLMs show "limited and inconsistent improvements" when incorporating sonar data, unlike human experts who consistently benefit from multimodal sensor fusion
5. Analysis of failure modes including perception-driven navigation errors, memory degradation over extended missions, and early performance plateaus indicating insufficient intrinsic exploration capabilities

## Methodology
- **Simulation Environment**: Built on Unreal Engine 5.3 with HoloOcean physics simulation; ~800m x 800m marine environment with realistic underwater assets (oil pipelines, shipwrecks, aircraft debris, electrical equipment, wind turbines); two depth levels (50m shallow with high illumination, 500m deep with severely limited visibility); six-directional synchronized RGB and sonar sensors (front, back, left, right, up, down)
- **Agent Framework (POMDP-based)**: Navigation modeled as Partially Observable Markov Decision Process with contextual memory; multimodal perception module processes synchronized RGB images and sonar data from six directional sensors; sliding-window memory architecture manages dynamic conditions and partial observability; MLLM-parameterized policy outputs discrete directional movements and rotational controls
- **Task Domains (8 total)**: Perception tasks include multi-view perception (identifying objects from six-directional RGB) and context-based perception (understanding temporal changes via chronological sequences). Decision-making tasks cover 8 real-world scenarios: sunken ship discovery, aircraft wreckage search, mining robot localization, oil drum detection, electrical equipment inspection, pipeline monitoring, wind turbine assessment, and docking maneuvers
- **Evaluated Models**: GPT-4o-mini, Google Gemini, Alibaba Qwen2.5-VL-7B, and other MLLMs; human expert baselines for all tasks
- **Experimental Setup**: All tasks evaluated under both shallow (50m) and deep (500m) water conditions; perception accuracy and decision success rate as primary metrics; additional analysis of sonar integration effectiveness, memory transfer (within-task vs. cross-task), temporal performance trajectories, and failure mode categorization
- **Key Results**: Perception -- Qwen2.5-VL-7B achieves 57.12% (shallow) / 28.48% (deep) vs. human near-100%; Decision -- GPT-4o-mini achieves 18.4% (shallow) / 14.8% (deep) vs. human 100% (shallow) / 69.6% (deep); sonar fusion helps humans consistently but provides limited/inconsistent benefit to MLLMs; cross-task memory transfer outperforms within-task transfer, especially in deep water; dominant failure modes are perception errors leading to navigational mistakes and memory degradation causing circular navigation patterns
