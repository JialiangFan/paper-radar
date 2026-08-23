# DREAM: Domain-aware Reasoning for Efficient Autonomous Underwater Monitoring

## Topic
VLM-guided autonomy framework for underwater robot exploration and habitat monitoring using domain-aware reasoning.

## Background
Ocean warming and acidification are increasing mass mortality risks for temperature-sensitive shellfish such as oysters, motivating the development of long-term autonomous monitoring systems. Human-conducted underwater monitoring is costly and hazardous, making robotic solutions a safer and more efficient alternative. However, enabling underwater robots to make real-time, environment-aware decisions without human intervention requires equipping them with intelligent perception and planning capabilities -- a challenge that Vision Language Models (VLMs) can address.

## Limitations & Research Problem
- **Limitation:** Existing underwater monitoring approaches either rely heavily on human intervention or lack the environmental awareness needed for efficient autonomous exploration. Vanilla VLM-based planners, when directly applied to underwater domains, achieve low coverage (60.23% on shipwreck tasks) and require excessive steps.
- **Problem:** How to leverage VLMs for real-time, domain-aware autonomous decision-making in underwater robots, enabling efficient exploration and habitat monitoring without prior knowledge of target locations.

## Contributions
- A three-layer autonomy architecture (perception, cognitive-aware planning, control) that integrates VLMs as the decision-making core for underwater robots
- Reasoning-augmented prompts that inject underwater domain knowledge into VLM planning, significantly improving exploration efficiency and coverage
- Demonstration of efficient target discovery and exploration without prior location information across two challenging real-world tasks (oyster monitoring and shipwreck exploration)
- Quantitative improvements: 31.5% less time on oyster monitoring, 100% coverage on shipwreck exploration (vs. 60.23% baseline), 27.5% fewer steps, and zero collisions

## Methodology
- **Three-Layer Architecture**: The system is organized into a perception layer (processing visual input from underwater cameras), a cognitive-aware planning layer (VLM-based reasoning and decision-making), and a control layer (translating high-level plans into robot motion commands). This separation of concerns allows each layer to be optimized independently.
- **VLM-Guided Planning**: A Vision Language Model serves as the robot's "brain," receiving real-time visual observations and generating exploration decisions. The VLM reasons about what it sees in the underwater environment to determine the next exploration action.
- **Reasoning-Augmented Prompts**: Domain-specific prompts are crafted to guide the VLM's reasoning process, embedding underwater exploration heuristics and domain knowledge (e.g., habitat patterns, search strategies) into the prompt context. This domain awareness is the key differentiator from vanilla VLM application.
- **Experimental Setup**: Evaluated on two tasks -- (1) oyster monitoring, where the robot must efficiently locate and survey oyster populations on the seabed, and (2) shipwreck exploration, where the robot must achieve full coverage mapping of a wreck while avoiding collisions. Baselines include prior monitoring methods and a vanilla VLM planner without domain-aware prompting.
