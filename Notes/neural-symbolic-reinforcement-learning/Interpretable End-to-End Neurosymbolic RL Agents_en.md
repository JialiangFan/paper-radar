# Interpretable End-to-End Neurosymbolic RL Agents

> Grandien, Delfosse & Kersting (2024) — arXiv:2410.14371 — TU Darmstadt

## Topic
Object-Centric Interpretable RL

## Background
Deep RL agents are prone to shortcut learning, resulting in poor generalization to even slightly different environments, while their black-box nature makes it difficult to inspect and debug decision-making. The SCoBots (Successive Concept Bottleneck Agents) framework addresses this by decomposing policies into interpretable intermediate steps via concept bottlenecks. However, SCoBots had previously only been evaluated with ground truth object detection, and its components had not been integrated end-to-end with unsupervised training.

## Limitations and Research Questions
- **Limitation:** The existing SCoBots framework relies on ground truth object detection provided by OCAtari. Individual components suitable for the pipeline have been proposed in prior work but never combined, preventing fully autonomous deployment.
- **Problem:** How to construct a fully end-to-end neurosymbolic RL agent using unsupervisedly trained components that maintains interpretability while achieving competitive performance?

## Contributions
- First end-to-end implementation of a SCoBot with all components trained unsupervisedly, eliminating the dependency on ground truth object detection.
- Integration of SPACE+MOC (object representation learning), k-means classification, object tracking, relation extraction, and ECLAIRE (rule extraction for policy distillation) into a complete pipeline.
- Separate evaluation of each component on multiple Atari games (Pong, Boxing, Skiing), demonstrating the framework's potential for interpretable and performant RL.
- Demonstration that modular architecture permits incremental component upgrades, while also revealing error accumulation as a key challenge.

## Methodology
- **Overall Architecture (SCoBots pipeline):** Decomposes the policy into three stages with intermediate interpretable concept bottlenecks (ICBs): Object Extractor → Relation Extractor → Action Selector.
- **Object Extractor:**
  - SPACE (VAE-based) architecture trained with the MOC (Motion and Object Continuity) scheme for unsupervised extraction of object bounding boxes and encodings from raw images.
  - K-means clustering for unsupervised object classification based on latent encodings.
  - Simple centroid-based tracking algorithm to infer object identity across consecutive frames, enabling temporal properties (position history, speed).
- **Relation Extractor:** Applies deterministic relational functions (e.g., Euclidean distance, speed) to extracted object properties, producing a scalar relational concept vector as input to the action selector.
- **Action Selector:**
  - A neural policy is first trained via PPO on the relational concept vector.
  - ECLAIRE rule extraction then distills the neural policy into an IF-THEN rule set policy, yielding full interpretability.
- **Experimental Setup:** Evaluated on OCAtari environments (Pong, Boxing, Skiing). Object extractor tested across all three games; action selector tested on Pong and Boxing. Configurations compared include ground truth vs. SPACE+MOC input, neural vs. rule set policies, and pruned vs. unpruned relational concept sets.

## Key Results
- Object extraction: High F-scores for Boxing and Pong; Skiing performed poorly due to classifier confusion (trees misclassified as player).
- Action selector: On Pong, SPACE+MOC input with rule set policy achieved an average reward of 14.4 (ground truth neural: ~17–19); on Boxing, up to 51.8.
- Rule set policies approached neural policy performance under certain configurations, demonstrating that interpretability and performance can coexist.
- Modular design enables independent component upgrades, but error accumulation across stages is the primary bottleneck.

## Limitations
- Relies on strong assumptions: training images must cover all object variations, and optical flow motion data must be available.
- Only location and class properties are extracted; advanced properties such as orientation are not captured.
- ECLAIRE-generated rule sets contain many rules with complex premises, limiting practical interpretability.

## Future Directions
- Replace the object extractor with unified detection-and-tracking models (e.g., YOLO) or explore alternatives such as SlotAttention and CutLER.
- Tune ECLAIRE hyperparameters for simpler rule sets; investigate alternative policy distillation methods.
- Extend evaluation to a wider variety of games and three-dimensional environments to test framework generality.
