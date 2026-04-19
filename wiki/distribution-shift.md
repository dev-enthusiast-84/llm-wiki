# Distribution Shift

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

Distribution shift occurs when the distribution of data at test time (or deployment) differs from the distribution at training time. It is a fundamental limitation of standard machine learning. [[foundation-model]]s trained on broad, diverse data improve robustness to many distribution shifts — but are not a panacea.

## Explanation

**Formal setup:**
- p_pre: pre-training distribution (broad, diverse)
- p^T_ID: in-distribution test data for downstream task
- p^T_OOD: out-of-distribution test data (shifted)

**Why foundation models improve robustness:**  
Pre-training on diverse data brings p_pre closer to many possible test distributions simultaneously. Intuitively, a model that has seen many domains during pre-training is less likely to be "surprised" by a shifted test distribution. Formally, domain adaptation theory (Ben-David et al., 2010) bounds the OOD error by a divergence term between pre-training and test distributions.

**Empirical evidence (CLIP, from Bommasani et al.):**
- CLIP achieves 76% accuracy on ImageNet
- +6% improvement on ImageNetV2 (re-sampled test set) relative to a standard ResNet50
- +35% improvement on ImageNet Sketch (distribution-shifted test set)

**Multilingual BERT:** Improves performance on unseen language pairs through diverse multilingual pre-training.

**Persistent challenges:**

1. **Spurious correlations:** Models learn shortcuts (background color, demographic correlates, annotator artifacts) that hold in the training distribution but fail OOD. Larger models and more pre-training data do not solve this (Taori et al. 2020, Santurkar et al. 2020).

2. **Temporal shifts:** World knowledge changes over time. Language models cannot incorporate post-training knowledge without retraining or retrieval augmentation.

3. **Domain mismatch:** CLIP zero-shot transfer fails on satellite imagery; ImageNet pre-training does not help medical images. The pre-training distribution must be sufficiently close to the target domain.

4. **Extrapolation:** Foundation models do not reliably extrapolate beyond patterns seen during pre-training. They interpolate within the training distribution but struggle at its boundaries.

**Promising directions:**
- **Retrieval augmentation:** Separate knowledge storage (external index) from DNN parameters; enables updating knowledge without retraining
- **Data augmentation strategies:** Contrastive learning augmentations confer task-specific robustness (Xiao et al. 2021)
- **Adaptation method choice:** Lightweight tuning (adapter, prefix, prompt) sometimes provides better OOD generalization than full fine-tuning by limiting the model's complexity

## Contradictions with Prior Papers

- **vs. Devlin et al. (2019):** The BERT paper does not discuss distribution shift or robustness — it evaluates on held-out splits of the same benchmark distributions. Bommasani et al. show that OOD robustness is a distinct and important property not captured by standard in-distribution benchmarks like GLUE, and that larger BERT models alone do not guarantee robustness.
- **vs. Vaswani et al. (2017):** The Transformer paper evaluates on WMT newstest sets, which are in-distribution relative to training data. Out-of-distribution generalization is not evaluated or discussed.

## Related Concepts

- [[foundation-model]]
- [[adaptation]]
- [[self-supervised-learning]]
- [[bert]]
- [[scaling-laws]]
- [[ai-safety-alignment]]
