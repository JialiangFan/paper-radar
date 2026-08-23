# Semi-supervised Concept Bottleneck Models

## Research Problem
How to train concept bottleneck models with minimal concept annotations by jointly addressing semi-supervised concept labeling and concept-saliency spatial alignment.

> Hu, L., Huang, T., Xie, H., Gong, X., Ren, C., Hu, Z., Yu, L., Ma, P., & Wang, D. (2024). Semi-supervised Concept Bottleneck Models. arXiv:2406.18992v3.

## Topic

Semi-supervised Interpretable Concept Learning

## Background

Concept Bottleneck Models (CBMs) have emerged as a prominent approach in explainable AI by introducing a human-interpretable concept bottleneck layer into deep learning classifiers. During inference, CBMs first predict concept labels from inputs and then use these predicted concepts to determine the final classification, yielding a self-explanatory decision process. However, training CBMs requires dense, expert-provided concept annotations that are expensive and labor-intensive to obtain. Unsupervised alternatives such as Label-free CBM circumvent annotation requirements by leveraging large language models (e.g., GPT-3) to generate concept sets, but these methods suffer from reliability concerns, lack rigorous concept evaluation metrics, and rest on the impractical assumption that no concept labels are available whatsoever.

## Limitations & Research Problem

- **Limitation 1:** Standard CBMs require complete expert concept annotations for all training samples, imposing prohibitive labeling costs that hinder scalable deployment in real-world applications.
- **Limitation 2:** Existing CBM methods exhibit systematic misalignment between concept saliency maps and input saliency maps -- predicted concepts frequently correspond to irrelevant image regions rather than semantically meaningful features, undermining the faithfulness of explanations.
- **Limitation 3:** Unsupervised CBM approaches rely on LLM-generated concepts with limited reliability and cannot exploit the small amounts of labeled concept data that are often available in practice.
- **Problem:** How can one train a CBM under a semi-supervised setting with only a small fraction of concept labels, while simultaneously achieving high concept prediction accuracy and faithful concept-input feature alignment?

## Contributions

- Proposes SSCBM (Semi-supervised Concept Bottleneck Model), the first unified framework to jointly address the semi-supervised concept annotation problem and the concept-saliency alignment problem within CBMs.
- Introduces a KNN-based pseudo-labeling strategy that assigns high-quality pseudo concept labels (c_img) to unlabeled data by computing cosine similarity with labeled samples and taking a weighted average of their concept vectors.
- Designs an Image-Textual Semantics Alignment module that generates concept heatmaps from the similarity between concept embeddings and spatial image feature maps, derives alignment-based pseudo concept labels (c_align) via thresholding, and optimizes an alignment loss between the two types of pseudo labels to resolve concept-saliency misalignment.
- Demonstrates through comprehensive experiments on four benchmark datasets (CUB, AwA2, WBCatt, 7-point) that with only 10% labeled data, SSCBM achieves concept and task accuracy on average only 2.44% and 3.93% lower, respectively, than the best fully supervised baseline.

## Methodology

- **Overall Architecture:** Built upon the Concept Embedding Model (CEM), the framework comprises a backbone feature extractor (e.g., ResNet50), an embedding generator, a concept bottleneck layer with sigmoid activation, and a downstream label predictor.
- **Labeled Data Pipeline:** Input images are processed through the backbone to obtain latent representations h, which are passed to the embedding generator to produce concept embeddings. These embeddings are projected through fully connected and sigmoid layers to yield predicted binary concept vectors. A binary cross-entropy concept loss (L_c) is computed against ground-truth concept labels, and a task loss (L_task) is computed via cross-entropy between predicted and true class labels.
- **Pseudo Labeling for Unlabeled Data (c_img):** A visual encoder extracts image features for each unlabeled sample. Cosine distances to all labeled samples are computed, and the k nearest neighbors are selected. Their concept label vectors are combined via normalized inverse-distance weighting to produce pseudo concept labels c_img.
- **Concept Heatmap Generation and Alignment Labels (c_align):** The visual encoder's spatial feature map V of dimensions H x W x m is used to compute a cosine-similarity heatmap H_i for each concept embedding c_i^m, capturing spatially localized concept-image relevance. Average pooling over each heatmap yields a concept score vector s, which is binarized via a learned threshold to produce alignment pseudo labels c_align.
- **Alignment Loss:** An alignment loss L_align = BCE(c_img, c_align) is computed between the two types of pseudo concept labels. This loss encourages the concept encoder to learn from KNN-derived concept information while simultaneously grounding concepts in spatially relevant image features.
- **Overall Objective:** The total loss is L = L_task + lambda_1 * L_c + lambda_2 * L_align, where lambda_1 and lambda_2 are hyperparameters balancing classification performance and interpretability.
- **Evaluation Protocol:** The framework is evaluated on concept accuracy, task accuracy, concept saliency map visualization (verifying spatial alignment), and test-time intervention experiments (correcting 10%-100% of concept predictions at inference to assess interpretability faithfulness).
