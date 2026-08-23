# Quiet-STaR - Language Models Can Teach Themselves to Think

## Topic
Internal Rationale Generation for Reasoning

## Background
Language models struggle with reasoning tasks despite evidence that intermediate reasoning steps (e.g., chain-of-thought prompting) substantially improve performance. The prior Self-Taught Reasoner (STaR) method bootstrapped reasoning by sampling rationales on curated question-answering datasets and training on those leading to correct answers, but this approach is limited in scale and generalizability. Quiet-STaR generalizes STaR to arbitrary text by training models to generate internal rationales at every token position to predict future text, enabling the learning of general reasoning from diverse unstructured corpora.

## Limitations and Research Questions
- **Limitation:** STaR relies on curated QA datasets for reasoning training, covering only a narrow subset of reasoning tasks and failing to generalize to implicit reasoning in general text.
- **Problem:** How can language models autonomously learn general-purpose reasoning from large-scale unstructured text, rather than being confined to task-specific or dataset-specific settings?

## Contributions
- Generalizes STaR to arbitrary text data, constituting the first work to train LMs to reason generally from unstructured text rather than curated reasoning tasks.
- Proposes a tokenwise parallel sampling algorithm that generates rationales from all token positions simultaneously, resolving the computational efficiency bottleneck.
- Introduces learnable meta-tokens (`<|startofthought|>` and `<|endofthought|>`) to demarcate rationale boundaries.
- Designs a mixing head (shallow MLP) that learns to interpolate between post-rationale and base predictions, mitigating distribution shift during early training.
- Introduces a non-myopic loss that incorporates multiple future tokens with teacher-forcing to improve rationale quality.
- Achieves zero-shot improvements without any fine-tuning: GSM8K accuracy from 5.9% to 10.9%, CommonsenseQA from 36.3% to 47.2%.

## Methodology
- **Think (parallel rationale generation):** For each token in the input sequence, rationales of length $t$ are generated in parallel using a custom attention mask that enables efficient batched inference without separate forward passes per token.
- **Talk (mixing predictions):** A mixing head (shallow MLP) produces a learned weight to interpolate the post-rationale next-token logits with the original base logits, initially biasing toward base predictions for training stability.
- **Learn (optimizing rationale generation):** REINFORCE is used to optimize rationale parameters. The reward for each rationale is defined as the difference between its mixed prediction log-likelihood and the average across all sampled rationales for that token. Gradients update LM parameters, meta-token embeddings, and the mixing head jointly.
- **Non-myopic scoring:** The loss function spans $n_{true}$ ground-truth tokens following each thought, combined with teacher-forcing to address gradient absence caused by the parallel sampling strategy.
- **Meta-token initialization:** Start and end thought token embeddings are initialized to the em dash ("---") embedding, with a hyperparameter weight applied to their gradients to accelerate optimization.
- **Experimental setup:** Built on Mistral 7B, trained on OpenWebMath and C4 corpora using 8 x 80GB H100 GPUs.

> **Title:** Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking
> **Authors:** Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, Noah D. Goodman
> **Venue:** arXiv:2403.09629
> **Year:** 2024
> **Affiliations:** Stanford University, Notbad AI Inc