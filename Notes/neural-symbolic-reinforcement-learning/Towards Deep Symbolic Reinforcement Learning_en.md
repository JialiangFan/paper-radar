# Towards Deep Symbolic Reinforcement Learning

> Garnelo, Arulkumaran & Shanahan, 2016 (Imperial College London) | arXiv:1609.05518

## Topic
Deep Symbolic RL Foundation

## Background
Deep reinforcement learning (DRL) has achieved impressive results on tasks such as Atari games and Go, yet it inherits fundamental shortcomings from deep learning, including data inefficiency, lack of abstract reasoning, and opacity. Classical symbolic AI offers compositional representations and high-level reasoning but has long been hindered by the symbol grounding problem, where symbols are hand-crafted rather than learned from data. This paper proposes a hybrid neural-symbolic architecture that combines the perceptual strengths of neural networks with the reasoning advantages of symbolic systems.

## Limitations & Research Questions
- **Limitation 1:** Contemporary DRL systems require very large datasets, resulting in slow and data-inefficient learning.
- **Limitation 2:** DRL agents lack the capacity for abstract reasoning, making transfer learning, analogical reasoning, and causal reasoning difficult or impossible.
- **Limitation 3:** DRL models are opaque; it is typically infeasible to extract human-comprehensible justifications for their decisions, limiting applicability in safety-critical domains.
- **Limitation 4:** Classical symbolic AI suffers from the symbol grounding problem, preventing autonomous learning from raw perceptual data.
- **Problem:** How to design an architecture that leverages neural networks for unsupervised symbol grounding from raw perception while enabling data-efficient, transferable, and interpretable reinforcement learning through symbolic reasoning?

## Contributions
- Proposes a hybrid neural-symbolic RL architecture consisting of a neural back end (unsupervised mapping from raw sensory input to compositionally structured symbolic representations) and a symbolic front end (action selection via symbolic reasoning).
- Articulates four core architectural principles: **conceptual abstraction**, **compositional structure**, **common sense priors**, and **causal reasoning**.
- Implements a proof-of-concept system and evaluates it on four variants of a simple grid-based game.
- Demonstrates that the system dramatically outperforms DQN on the most challenging (stochastic) game variant and exhibits transfer learning capabilities.

## Methodology
- **Overall architecture:** An end-to-end pipeline comprising a neural back end and a symbolic front end, with three processing stages: low-level symbol generation, representation building, and reinforcement learning.
- **Low-level symbol generation:** A convolutional autoencoder is trained unsupervised on 5000 randomly generated images. Salient regions in the middle-layer activations are used for object detection; objects are assigned symbolic types by comparing their activation spectra against known type averages.
- **Representation building:**
  - **Object tracking:** Cross-frame object persistence is established via a weighted combination of three measures: spatial proximity ($L_{dist} = \frac{1}{1+d}$), type transition probability ($L_{trans}$, from a learned transition matrix), and neighbourhood similarity ($L_{neigh} = \frac{1}{1+\Delta N}$). The overall likelihood is $L = w_1 L_{dist} + w_2 L_{trans} + w_3 L_{neigh}$.
  - **Symbolic interaction extraction:** Absolute positions are converted to relative positions between nearby object pairs, yielding a spatio-temporal representation encoding inter-object interactions (type changes and relative displacements across frames).
- **Reinforcement learning:** A separate tabular Q-function is trained for each pair of interacting object types. Action selection aggregates all currently relevant Q-values: $a_{t+1} = \arg\max_a \sum_Q Q(s_{t+1}, a)$. An $\epsilon$-greedy exploration strategy ($\epsilon = 0.1$) is used during training.
- **Common sense priors:** The representational ontology encodes assumptions such as object persistence over time and the expectation that visually similar objects behave similarly, reducing the learning burden.

## Experiments
- **Benchmark:** Four variants of a simple game: (1) single object type on a grid, (2) two object types on a grid, (3) single object type with random placement, (4) two object types with random placement.
- **Key results:** On the most difficult variant (two types, random placement), DQN failed to exceed chance performance within 1000 epochs. The proposed system learned an effective policy within approximately 200 epochs, achieving ~70% correct collection of positive-reward objects.
- **Transfer learning:** An agent trained on the grid variant and tested on the random variant exhibited a learning curve comparable to one trained directly on the random variant, demonstrating the transferability of the learned symbolic representation.
- **Interpretability:** Because the symbolic front end operates via explicit Q-functions, each corresponding to a specific object-type interaction, the decision-making process can be traced and understood by humans.

## Limitations
- Validated only on minimalistic game environments; the neural back end is shallow and the symbolic front end performs limited reasoning.
- Object tracking weights ($w_1, w_2, w_3$) are set manually rather than learned.
- The locality assumption does not guarantee convergence to a globally optimal policy.
- The system remains a preliminary proof-of-concept, far from general-purpose applicability.

## Future Directions
- Incorporate inductive logic programming for more powerful generalization over the Q-function.
- Integrate formal analogical reasoning techniques (e.g., structure mapping engine).
- Add a planning component to exploit learned causal structure for off-line exploration.
- Employ more advanced unsupervised learning methods (e.g., disentangled representation learning) to handle richer visual environments.
