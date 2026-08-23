# Neurosymbolic RL and Planning: A Survey

## Topic
Neurosymbolic RL Survey

## Background
Neurosymbolic AI, regarded as the third wave of AI, integrates neural networks (connectionist AI) with symbolic reasoning to harness the learning capacity of the former and the interpretability of the latter. Deep Reinforcement Learning (DRL) has achieved remarkable successes (e.g., AlphaGo, AlphaStar) but suffers from poor data efficiency, lack of interpretability, and difficulty in formal verification. Neurosymbolic RL merges symbolic reasoning with DRL to address these shortcomings, enabling agents that can both learn from raw data and reason over structured, human-readable representations.

## Limitations & Research Problem
- **Limitation 1:** DRL is extremely data-inefficient (e.g., Rainbow DQN requires ~83 hours of gameplay to match performance humans achieve in minutes) and, outside narrow scenarios, domain-specific algorithms often outperform general DRL.
- **Limitation 2:** DRL models are black boxes lacking interpretability and explainability, making formal verification difficult and posing serious risks in safety-critical applications such as autonomous driving, robotics, and medical diagnosis.
- **Limitation 3:** Symbolic AI provides reasoning and explainability but cannot handle large-scale unstructured data or generalize from incomplete information.
- **Problem:** No comprehensive survey exists that specifically covers the intersection of Neurosymbolic AI and RL; prior surveys address either Neurosymbolic AI or RL in isolation.

## Contributions
- Provides the first comprehensive literature survey dedicated to the Neurosymbolic RL field, bridging the gap between existing Neurosymbolic AI surveys and RL surveys.
- Proposes a taxonomy of three model categories based on the role of neural and symbolic components in RL: **Learning for Reasoning**, **Reasoning for Learning**, and **Learning-Reasoning**.
- Systematically analyzes RL components (state space, action space, policy module, RL algorithm) and neural/symbolic components across all surveyed works.
- Identifies research opportunities in robotics, gaming, question answering, safe RL, and RL parameter optimization, along with key challenges in automated symbolic knowledge generation, verification/validation, algorithm design, and neural-symbolic balancing.

## Methodology
- **Taxonomy framework:** Adopts and extends the three-class Neurosymbolic taxonomy from D. Yu et al., applied specifically to RL:
  - **Learning for Reasoning RL model:** The neural component acts as an auxiliary that abstracts unstructured data into symbolic form; the symbolic component handles reasoning and action generation. The connection is serial/unidirectional (neural to symbolic). Applications include: transforming unstructured data into symbolic representations (DSRL, SRL+CS, NSRL, Deep Symbolic Policy), Knowledge Graph reasoning (DeepPath, MINERVA), verification (VIPER, REVEL), and gaming (AlphaGo Zero).
  - **Reasoning for Learning RL model:** The symbolic system acts as a helper, providing structured knowledge to guide the neural network. The connection is parallel/unidirectional (symbolic to neural). Applications include: reward shaping (MCTS-A, MATS-A, Buchi automaton methods), programmatic policy design (PROPEL, IP-PRL, PIRL), task segmentation (DeepSynth), and knowledge-initialized models (PROLONETS).
  - **Learning-Reasoning RL model:** Neural and symbolic components interact bidirectionally, with each serving as input to the other. This combines the benefits of both preceding models for balanced interpretability and reasoning. Applications include task segmentation (SDRL).
- **Analysis dimensions:** Each surveyed work is compared across five dimensions: neural component type (CNN, DNN, RNN, Transformer, etc.), symbolic component type (First Order Logic, Decision Tree, Knowledge Graph, Programmatic Policy, etc.), RL algorithm, state/action space, and policy module (Tables III-V).
- **Opportunities and challenges:** Identifies five application opportunities (Robotics and Control, Gaming, Intelligent Question Answering, Safe RL, Optimizing RL Parameters) and four core challenges (automated generation of symbolic knowledge, verification and validation, Neurosymbolic RL algorithm design, balancing reasoning and learning between neural and symbolic components).
