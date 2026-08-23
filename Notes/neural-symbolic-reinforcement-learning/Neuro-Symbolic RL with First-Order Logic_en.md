# Neuro-Symbolic RL with First-Order Logic

## Topic
First-Order Logic RL

## Background
Deep reinforcement learning has achieved success in text-based games, computer games, and robot control, yet these methods typically require many training trials to converge and store policies in black-box neural networks without interpretability. The Logical Neural Network (LNN) is a recent neuro-symbolic framework that simultaneously provides the learning capability of neural networks and the reasoning capability of symbolic logic within a differentiable architecture. This paper applies LNN to RL for text-based interaction games, using first-order logic representations extracted from natural language observations to achieve interpretable and fast-converging policy learning.

## Limitations and Research Questions
- **Limitation:** Conventional deep RL methods (e.g., LSTM-DQN++) store policies in opaque neural networks, making learned rules neither understandable nor verifiable by human operators. Convergence is slow and generalization to unseen game configurations is limited.
- **Problem:** How can first-order logic and neuro-symbolic methods be leveraged to learn RL policies for text-based games that are both interpretable and significantly faster to converge?

## Contributions
- Designed and implemented a novel neuro-symbolic RL method (FOL-LNN) that integrates Logical Neural Networks into policy training for text-based games
- Proposed an algorithm to extract first-order logical facts from natural language text observations using a semantic parser, agent history, and ConceptNet as external knowledge
- Demonstrated through experiments on the TextWorld CoinCollector benchmark that FOL-LNN converges significantly faster than state-of-the-art methods (LSTM-DQN++, NLM-DQN, NN-DQN, LNN-NN-DQN) and is the only method capable of extracting human-readable logical rules

## Methodology
- **Problem formulation:** Text-based games are modeled as POMDPs where the agent receives partial information via text observations. Actions consist of a verb-noun pair (e.g., "go east", "take coin").
- **FOL Converter:** Natural language observations are first parsed into propositional logic via a semantic parser. Word categories are then retrieved from ConceptNet (e.g., "east" classified as direction-type), and propositional logic is lifted to first-order logic predicates (e.g., Find(x), Visited(x)) with universal quantification over category members.
- **LNN Training:** An AND-OR structured Logical Neural Network is constructed with all FOL facts at the first layer, multiple AND gates at the second layer, and a single OR gate at the output. Training follows a DQN-style mechanism with a replay buffer, reward-based loss, and gradient updates on LNN weights.
- **Rule extraction:** After training, a threshold alpha is applied to discretize continuous node values into True/False, enabling extraction of interpretable logical rules from high-weight connections (e.g., "if a direction is found and not yet visited, go to that direction").
- **Evaluation:** Tested on TextWorld CoinCollector across easy, medium, and hard difficulty levels. FOL-LNN achieved the fastest convergence and highest reward across all settings, and successfully extracted human-understandable action rules for both "take" and "go" actions.
