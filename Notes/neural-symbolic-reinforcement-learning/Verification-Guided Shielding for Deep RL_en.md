# Verification-Guided Shielding for Deep RL

## Topic
Efficient Safety Shielding

## Background
Deep reinforcement learning (DRL) has demonstrated strong performance in complex decision-making tasks, yet trained policies cannot guarantee absolute safety across all inputs, limiting deployment in safety-critical domains. Two principal formal approaches exist: verification (offline assessment of policy safety, unable to provide corrective actions) and shielding (online override of unsafe actions, but incurring substantial runtime overhead by activating at every time step). Corsi, Amir et al. propose verification-guided shielding, a method that integrates both techniques to preserve formal safety guarantees while significantly reducing the computational cost of shielding.

## Limitations and Research Problem
- **Limitation:** Standard shielding requires invoking the shield at every time step to validate and potentially correct actions, even though the agent's original decisions are safe in the vast majority of cases (shield interventions occur in fewer than 9% of steps). This results in 31x--40x runtime overhead, rendering it impractical for real-time systems. Conversely, formal verification can detect unsafe policies offline but offers no remediation mechanism upon finding violations.
- **Problem:** How can one activate the shield only when necessary---i.e., when the agent operates in a potentially unsafe input region---while retaining formal safety guarantees and drastically reducing runtime overhead?

## Contributions
- Introduces the verification-guided shielding framework, the first to systematically combine formal verification and shielding: verification partitions the input space into safe and unsafe regions; the shield is activated only in unsafe regions
- Designs a five-stage pipeline: domain splitting (epsilon-ProVe), formal verification (Marabou), clustering (agglomerative clustering to compress unsafe regions), symbolic representation (propositional logic / SMT encoding), and shield synthesis with selective execution
- Demonstrates on Particle World and Mapless Navigation benchmarks that runtime overhead is reduced by 20%--71% relative to full shielding, while maintaining identical formal safety guarantees
- Provides an in-depth analysis of scalability and completeness, clarifying the complementary roles of probabilistic guarantees (epsilon-ProVe approximation stage) and sound guarantees (Marabou exact verification stage)

## Methodology
- **(1) Domain Splitting:** The epsilon-ProVe algorithm partitions the continuous input domain by constructing a search tree; each node represents a sub-region whose safety is estimated via sampling. Regions are iteratively split until the confidence threshold is met, yielding an underapproximation of safe regions and an overapproximation of unsafe regions.
- **(2) Formal Verification of Safe Regions:** Regions approximated as safe by epsilon-ProVe are subjected to exact verification using Marabou, a sound and complete DNN verifier. Any region for which a counterexample is found (SAT) is reclassified as unsafe, ensuring that the final safe-region partition is formally sound.
- **(3) Clustering:** To address the large cardinality of unsafe regions (~60,000 in Particle World), agglomerative clustering merges adjacent unsafe regions into a compact overapproximation. This does not compromise soundness---at most, the shield is activated slightly more often than strictly necessary.
- **(4) Symbolic Representation:** Unsafe regions are encoded using propositional logic or first-order logic modulo theories (SMT). The Z3 solver's simplify primitive further reduces formula complexity, enabling efficient online membership queries to determine whether the current state falls within an unsafe region.
- **(5) Shield Synthesis and Execution:** A shield is synthesized from an LTL specification (supporting LTL modulo theories for continuous domains). At runtime, each time step requires only evaluating a symbolic formula to check region membership: if the input lies in an unsafe region the shield is activated to correct the action; otherwise the original policy output is executed directly.
- **Evaluation:** The offline stage runs on a 160-CPU cluster, with formal verification as the most time-consuming step (~2 hours per policy). Online experiments show shield active time drops from 100% to 1.3%--61.7%, overhead decreases from 31x--40x to 1.5x--21.5x, and the overall time gain ranges from 20.5% to 71.1%.
