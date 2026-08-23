# Let's Verify Step by Step

## Topic
Process Supervision for Reward Models

## Background
Large language models have demonstrated strong multi-step reasoning capabilities via chain-of-thought, yet even state-of-the-art models regularly produce logical errors and hallucinations. Reward models can be trained to discriminate between correct and incorrect solutions and then used for rejection sampling or reinforcement learning. Two paradigms exist for supervising reward models: outcome supervision (feedback on the final answer only) and process supervision (feedback on each intermediate reasoning step), but their relative merits had not been rigorously compared at scale.

## Limitations and Research Questions
- **Limitation:** Outcome supervision only uses final-answer correctness, making credit assignment difficult for the reward model; furthermore, false positives (incorrect reasoning that reaches the correct answer) corrupt the training signal.
- **Problem:** Does process supervision yield more reliable reward models than outcome supervision for mathematical reasoning? How can step-level human feedback be collected efficiently at scale?

## Contributions
- Demonstrated that process-supervised reward models (PRMs) significantly outperform outcome-supervised reward models (ORMs) on the MATH dataset (78.2% vs 72.4% at best-of-1860)
- Showed that a large-scale PRM can reliably serve as a surrogate for human labelers, enabling synthetic process supervision for smaller models at modest cost
- Introduced an active learning strategy (prioritizing convincing wrong-answer solutions) that improves process supervision data efficiency by approximately 2.6x
- Released PRM800K, a dataset of approximately 800,000 step-level human feedback labels across 75K solutions to 12K MATH problems

## Methodology
- **Evaluation framework:** A fixed generator produces candidate solutions; an independently trained reward model performs best-of-N selection; performance is measured by the fraction of problems solved
- **Base model:** All large-scale models are fine-tuned from GPT-4, with an additional pretraining stage on MathMix (~1.5B math-relevant tokens)
- **ORM training:** Uniformly sampled solutions are labeled correct/incorrect by automatic final-answer checking; the ORM's prediction at the final token serves as the solution score
- **PRM training:** Human data-labelers assign positive/negative/neutral labels to each step; the PRM predicts step-level correctness probabilities; the solution score is defined as the product of all step-level correctness probabilities
- **Active learning:** A small-scale PRM_selector identifies the most convincing wrong-answer solutions (high PRM score but incorrect final answer) for priority labeling; the PRM is iteratively retrained on the expanding dataset
- **Small-scale synthetic ablations:** PRM_large is used as a labeling oracle to provide both process and outcome supervision for smaller models, enabling controlled comparisons that confirm process supervision outperforms outcome supervision at all data scales
- **OOD generalization:** Evaluated on 224 held-out STEM questions (AP Physics, AP Calculus, AP Chemistry, AMC10/12), confirming the PRM advantage generalizes beyond MATH (aggregate best-of-100: PRM 72.9% vs ORM 63.8%)

> **Title:** Let's Verify Step by Step
> **Authors:** Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, Karl Cobbe
> **Venue:** arXiv:2305.20050
> **Year:** 2023
> **Affiliations:** OpenAI