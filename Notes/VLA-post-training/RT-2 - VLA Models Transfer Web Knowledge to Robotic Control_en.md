# RT-2 - VLA Models Transfer Web Knowledge to Robotic Control

- **Title:** RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
- **Authors:** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, et al.
- **Venue:** arXiv preprint (arXiv:2307.15818)
- **Year:** 2023
- **Affiliations:** Google DeepMind


## Topic
VLA Web-Knowledge Robotic Control Transfer

## Background
Large-scale vision-language models (VLMs) pretrained on Internet data exhibit powerful visual understanding, semantic reasoning, and open-vocabulary recognition. However, transferring these capabilities to low-level robotic control remains an open challenge. Prior robotic policies such as RT-1 use dedicated transformer architectures trained solely on robot demonstration data and thus fail to leverage the rich semantic knowledge embedded in web-scale pretraining. Meanwhile, existing methods that incorporate LLMs/VLMs into robotics typically address only high-level planning, leaving the low-level controller unable to benefit from Internet-scale knowledge.

## Limitations & Research Problem
- **Limitation:** Existing robotic policies (e.g., RT-1) are trained on limited robot demonstration data, lacking generalization to novel objects, unseen backgrounds, and new environments. Prior VLM-for-robotics approaches use VLMs only as high-level planners or perception modules, so the low-level controller does not directly inherit web-scale semantic knowledge.
- **Problem:** Can a large pretrained VLM be integrated directly into end-to-end low-level robotic control, enabling a single model to output robot actions while retaining the semantic reasoning and generalization capabilities acquired from Internet-scale data?

## Contributions
- Proposes the Vision-Language-Action (VLA) model paradigm: robot actions are represented as text tokens sharing the same output space as natural language, enabling direct co-fine-tuning of pretrained VLMs into end-to-end robotic policies.
- Instantiates two RT-2 variants: RT-2-PaLI-X (5B/55B) and RT-2-PaLM-E (12B), achieving VLA without introducing any action-only model components.
- Through approximately 6,000 real-robot evaluation trials, demonstrates that RT-2 matches RT-1 on seen tasks while improving generalization to unseen objects/backgrounds/environments by roughly 2x, and exhibits emergent capabilities (symbol understanding, reasoning, human recognition).
- Shows that co-fine-tuning (jointly using web data and robot data) outperforms fine-tuning on robot data alone, and that larger models yield better generalization.
- Demonstrates that chain-of-thought reasoning can be integrated into VLA, allowing RT-2 to generate a natural-language plan before outputting action tokens, thereby handling more complex semantic instructions.

## Methodology
- **Action Tokenization:** Robot actions (6-DoF end-effector displacement + gripper extension + termination command) are discretized into 256 bins. Each action dimension is mapped to an integer token, and the full action is represented as a string of 8 tokens sharing the vocabulary with natural language tokens.
- **Co-Fine-Tuning:** The model is jointly fine-tuned on the original VLM pretraining data (WebLI and other web-scale vision-language data) and robot demonstration data. Training uses a VQA format ("Q: what action should the robot take to [instruction]? A: [action tokens]"), with robot data weighted at approximately 50%-66% of each training batch.
- **Output Constraint:** At inference time, when the model is prompted with a robot-action task, the decoding vocabulary is constrained to sample only valid action tokens, ensuring outputs are directly executable on a real robot.
- **Real-Time Inference:** The largest model (55B) is deployed on a multi-TPU cloud service and queried over the network to achieve 1-3 Hz closed-loop control; the 5B variant achieves approximately 5 Hz.
- **Chain-of-Thought Extension:** A "Plan" field is added to the fine-tuning data, where the model first outputs the action intent in natural language and then produces action tokens, enabling multi-stage semantic reasoning (e.g., determining that a rock serves as an improvised hammer).
- **Backbone Architecture:** RT-2-PaLI-X is built on a ViT-22B encoder coupled with a 32B encoder-decoder backbone; RT-2-PaLM-E is built on a ViT encoder with a 12B PaLM decoder-only LLM, fusing visual and language tokens through a projection layer.
