# ProbStar Temporal Logic for Verifying Complex Behaviors of Learning-enabled Systems

## Topic
Probabilistic Temporal Logic Verification

## Background
Learning-enabled Systems (LES) are increasingly used in safety-critical domains, requiring verification of correct behavior under environmental uncertainties and adversarial attacks. Existing formal verification methods focus primarily on safety and robustness of open-loop and closed-loop LES, but a crucial gap remains in verifying spatio-temporal behaviors and temporal properties. This paper introduces ProbStar Temporal Logic (ProbStarTL), a novel temporal logic defined over ProbStar reachable sets that enables quantitative verification of temporal properties by computing satisfaction probabilities.

## Limitations & Research Problem
- **Limitation:** Existing LES verification methods focus on qualitative safety and robustness verification and cannot quantitatively verify complex temporal properties (e.g., "always" and "eventually" behaviors). The neurosymbolic approach uses STL syntax but computes robustness values rather than satisfaction probabilities, making it unsuitable for applications involving probabilistic uncertainties.
- **Problem:** How to design a temporal logic formalism that can quantitatively verify complex temporal behaviors of closed-loop LES based on ProbStar reachable sets, precisely computing the satisfaction probability of temporal specifications while guaranteeing soundness and completeness?

## Contributions
- Propose ProbStarTL temporal logic with clear syntax and dual semantics (qualitative + quantitative), supporting temporal operators always (□) and eventually (◇), with a procedure for computing satisfaction probability
- Design a Depth-first Search (DFS) ProbStar reachability algorithm for constructing exact and approximate ProbStar traces (reachable set traces) of closed-loop LES
- Propose a new quantitative verification algorithm that transforms ProbStarTL specifications into Computable Disjunctive Normal Form (CDNF), computes exact and approximate upper/lower bounds of satisfaction probability, and introduces conservativeness and constitution metrics
- Implement the verification framework using StarV and demonstrate effectiveness on Le-ACC (learning-based adaptive cruise control) and AEBS (advanced emergency braking system) case studies

## Methodology
- **ProbStarTL Definition:** Based on DT-STL (Discrete-Time Signal Temporal Logic) syntax, ProbStarTL is defined over bounded-time ProbStar signal (ProbStar trace) sequences; a recursive constraint function C(R, t, φ) symbolically captures the set of trajectories satisfying temporal specifications
- **DNF Transformation:** ProbStarTL constraint formulas are converted to Disjunctive Normal Form (DNF), where each conjunctive literal is a ProbStar intersected with a half-space; the probability of the DNF is computed using the inclusion-exclusion principle or approximated via a max lower bound
- **DFS Reachability Algorithm:** Since the ReLU network controller may split one ProbStar into multiple sets at each time step, a DFS strategy generates all ProbStar traces; a filtering probability p_f parameter filters out low-probability traces to improve scalability
- **Quantitative Verification Algorithm:** For each ProbStar trace, the temporal specification's CDNF is instantiated and the upper bound (ρ_max) and lower bound (ρ_min) of satisfaction probability are computed; two metrics are introduced — conservativeness (tightness of the probability estimation range) and constitution (proportion of ignored traces and CDNFs contributing to the estimation)
- **Experimental Validation:** Verified 4 complex temporal properties on the Le-ACC system (covering safe distance, speed following) and temporal safety properties of emergency braking on the AEBS system; significantly faster than the neurosymbolic approach with consistent results
