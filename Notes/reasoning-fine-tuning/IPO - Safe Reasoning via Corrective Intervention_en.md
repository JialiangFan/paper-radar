# Towards Safe Reasoning in Large Reasoning Models via Corrective Intervention

## Topic
Safe Reasoning Alignment via Intervention

## Background
Large Reasoning Models (LRMs) such as DeepSeek-R1 have achieved impressive breakthroughs in complex reasoning tasks, but their chain-of-thought (CoT) reasoning often contains harmful content even when final responses appear safe. Existing safety alignment methods primarily target output-level safety and overlook the safety of intermediate reasoning, which poses significant risks as unsafe reasoning can be exploited by malicious users and makes models more susceptible to jailbreak attacks.

## Limitations & Research Problem
- **Limitation:** Existing SFT-based alignment methods (SafeChain, RealSafe, STAR) trained on curated safe CoT data fail to fully eliminate unsafe intermediate reasoning content
- **Limitation:** Even when final responses are safe, reasoning traces may leak harmful information (e.g., detailed criminal methods), posing particular risks for open-source models
- **Limitation:** RL-based approaches like GRPO are inefficient for safe reasoning due to low rollout diversity — approximately 50% of harmful prompts yield few or no safe reasoning trajectories, resulting in weak training signals
- **Problem:** How to achieve process-level safety alignment for LRM reasoning without sacrificing reasoning capabilities

## Contributions
- Identified three critical insights: (1) safe reasoning is consolidated by a few critical **safety triggers**; (2) **compliance cues** strongly correlate with unsafe reasoning (Pearson R=0.853); (3) corrective interventions replacing compliance cues with safety triggers reliably steer reasoning toward safety
- Proposed **Intervened Preference Optimization (IPO)**, extending DPO to reasoning safety by constructing preference pairs through interventions at safety-critical steps
- Demonstrated effectiveness across three LRMs (DS-8B, DS-7B, Qwen3-8B) on multiple adversarial safety benchmarks, achieving over 30% relative reduction in overall harmfulness while preserving or enhancing reasoning capabilities
- Showed superior training efficiency over GRPO (~40 minutes vs 2+ hours), requiring at most 14 generations per prompt

## Methodology
- **Core Framework**: IPO extends DPO by intervening at safety-critical positions in reasoning trajectories, constructing preference pairs for preference learning
- **Safety Trigger Identification**: Defined Continuation Safety Ratio (CSR) to measure the probability of safe continuation at each token; identified turning points where CSR sharply rises to near 100% as safety triggers (present in >90% of safe trajectories)
- **Compliance Cue Detection**: Used GPT-4o to automatically detect the first compliance cue (a reasoning step expressing willingness to comply with malicious requests) in unsafe trajectories, strongly correlated with CSR drop points
- **Intervention Process**: Replaced the first compliance cue in unsafe trajectories with a sampled safety trigger from a curated pool of 6 representative triggers; the model continues generation from the intervention point to produce corrected safe trajectories
- **Preference Pair Construction**: Original unsafe trajectory serves as rejected; intervened safe trajectory serves as chosen; both share the same prefix but diverge at the intervention point
- **Training Strategy**: Two-stage training — (1) partial DPO with auxiliary SFT loss on intervened preference data; (2) mixed benign prompt data to mitigate over-refusal
- **Experimental Setup**: Constructed data from STAR-1 with 1,000 harmful + 915 benign prompts; evaluated on JailbreakBench, StrongReject, WildJailbreak (safety) and AIME2024, MATH-500, GPQA-Diamond, HumanEval (reasoning capabilities)
