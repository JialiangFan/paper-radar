# Concept Bottleneck Models

## Research Problem
How to make deep learning predictions interpretable and intervenable by routing all decisions through a human-understandable concept layer without sacrificing accuracy.

> Koh, P.W., Nguyen, T., Tang, Y.S., Mussmann, S., Pierson, E., Kim, B., & Liang, P. (2020). Concept Bottleneck Models. *Proceedings of the 37th International Conference on Machine Learning (ICML)*, PMLR 119.

## Topic
Interpretable Concept-Based Prediction Models

## Background
Modern deep learning models are typically trained end-to-end, mapping directly from raw inputs (e.g., pixels) to target outputs (e.g., disease severity scores), without exposing interpretable intermediate reasoning. In high-stakes domains such as medical imaging (e.g., knee osteoarthritis grading from X-rays) and fine-grained visual recognition (e.g., bird species identification), domain experts require the ability to understand, inspect, and intervene on a model's reasoning process. Earlier concept-based models attempted to introduce human-understandable intermediate representations but were significantly overtaken in predictive accuracy by end-to-end neural networks, fostering a perceived tradeoff between accuracy and interpretability in terms of concepts.

## Limitations & Research Problem
- **Limitation 1:** End-to-end black-box models do not support interpretation or intervention in terms of human-specified concepts. Existing post-hoc methods (e.g., linear probes, concept activation vectors) can only approximately recover concepts from learned representations and cannot enable precise, targeted intervention on individual concepts at test time.
- **Limitation 2:** Earlier concept bottleneck approaches suffered from substantially lower predictive accuracy compared to standard end-to-end models. Furthermore, there had been no systematic comparison of training schemes or exploration of the previously-unexplored capacity for test-time concept intervention.
- **Problem:** Can a model achieve competitive task accuracy with end-to-end models while routing all predictions through a human-interpretable concept bottleneck, thereby enabling both interpretability and test-time intervention? How do different training strategies affect the triad of task accuracy, concept accuracy, and intervention effectiveness?

## Contributions
- Proposes a systematic framework for Concept Bottleneck Models (CBMs) with architecture $x \xrightarrow{g} c \xrightarrow{f} y$, where $g$ maps inputs to human-specified concepts $c$ and $f$ maps concepts to the final target $y$, with all information flowing through an explicit concept bottleneck layer.
- Systematically compares three training strategies -- **Independent** ($g$ and $f$ trained separately), **Sequential** ($g$ trained first, then $f$ trained on predicted concepts), and **Joint** (concept and task losses optimized simultaneously with tradeoff hyperparameter $\lambda$) -- demonstrating that CBMs achieve competitive or superior task accuracy to standard end-to-end models on both OAI (knee osteoarthritis X-ray grading; $n=36{,}369$) and CUB (bird species identification; $n=11{,}788$), while maintaining high concept accuracy.
- Provides the first systematic study of test-time intervention: domain experts can directly edit predicted concept values $\hat{c}$ at inference time, propagating corrections to the final prediction $\hat{y}$. This substantially improves task accuracy (e.g., on OAI, correcting just 2 out of 10 concepts reduces RMSE from >0.4 to approximately 0.3, approaching individual radiologist performance).
- Demonstrates that CBMs are more robust to spurious correlations and covariate shifts: on a CUB+Places background shift experiment, bottleneck models achieve substantially lower task error than standard models (approximately 0.48 vs. 0.63).
- Provides theoretical analysis in a well-specified linear regression setting, deriving an upper bound on the asymptotic excess error ratio of independent bottleneck models relative to standard models: $\frac{k/d \cdot \sigma_Y^2 + \sigma_C^2}{\sigma_Y^2 + \sigma_C^2}$, showing bottleneck models are particularly effective when the number of concepts $k$ is much smaller than the input dimension $d$ and concept noise $\sigma_C^2$ is small relative to target noise $\sigma_Y^2$.

## Methodology
- **Model Architecture:** Any end-to-end neural network is converted into a CBM by resizing an intermediate layer to match the number of concepts $k$ and adding a loss to align that layer component-wise with human-specified concepts. For OAI: pretrained ResNet-18 ($x \to c$) followed by a 3-layer MLP ($c \to y$). For CUB: fine-tuned Inception-v3 ($x \to c$) followed by a single linear layer ($c \to y$).
- **Three Training Schemes:**
  - *Independent:* $\hat{g}$ and $\hat{f}$ are each optimized on their respective losses independently; $\hat{f}$ is trained using true concepts $c$ but at test time receives predicted concepts $\hat{c}$.
  - *Sequential:* $\hat{g}$ is trained first, then $\hat{f}$ is trained using the concept predictions $\hat{g}(x)$ as input, eliminating the train-test distribution mismatch of the independent scheme.
  - *Joint:* Both components are trained end-to-end by minimizing $\sum_i [L_Y(f(g(x^{(i)})); y^{(i)}) + \lambda \sum_j L_{C_j}(g_j(x^{(i)}); c_j^{(i)})]$, where $\lambda$ controls the tradeoff between task and concept losses. Setting $\lambda \to 0$ recovers the standard model; $\lambda \to \infty$ approximates the sequential bottleneck.
- **Test-Time Intervention:** At inference, predicted concept values $\hat{c}_j$ are replaced with expert-provided true values $c_j$, and the correction is propagated to update $\hat{y}$. For regression tasks (OAI), direct replacement is used. For classification tasks (CUB), concept logits $\hat{\ell}_j$ are set to the 5th or 95th percentile of the training distribution (for $c_j=0$ or $c_j=1$ respectively) to approximate the true concept value through the sigmoid.
- **Robustness Evaluation:** A CUB+Places dataset variant is constructed where each bird species is spuriously correlated with a specific background category (from the Places dataset) during training, but this mapping is shuffled at test time, evaluating robustness to background-based spurious correlations.
- **Theoretical Analysis:** Under a linear Gaussian setting, the authors derive the asymptotic ratio of excess mean-squared error for the independent bottleneck model vs. the standard model, showing the bottleneck model's advantage grows as $k/d$ decreases and $\sigma_Y^2 / \sigma_C^2$ increases.
