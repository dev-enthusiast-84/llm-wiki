# Distribution Shift

A mismatch between the data distribution a model was trained on and the distribution it encounters during deployment.

## Summary

Distribution shift occurs when the statistical properties of real-world deployment data differ from the training distribution. For language models, this includes domain shifts (a model trained on web text deployed for medical QA), temporal shifts (model knowledge cutoff vs. current events), and demographic shifts (different linguistic styles, dialects, or languages). Foundation models mitigate some distribution shift challenges through broad pre-training, but Bommasani et al. (2022) note this is not a panacea — foundation models trained on broad but still biased data can fail systematically on underrepresented populations.

## Explanation

### Types of Distribution Shift

**Covariate shift**: The distribution of inputs P(X) changes, but the conditional distribution P(Y|X) remains the same. Example: a model trained on formal text deployed on social media text.

**Label shift**: P(Y) changes, but P(X|Y) stays constant. Less common in language modeling.

**Concept drift**: The relationship P(Y|X) itself changes over time. Example: the meaning of "AI" has evolved significantly; a model trained on older text may have outdated associations.

**Domain shift**: Input comes from an entirely different domain. Example: a general language model applied to legal or biomedical text.

### Why Foundation Models Are Partially Robust

Pre-training on diverse data (web text, books, code, Wikipedia) exposes models to many distributions. Bommasani et al. (2022) note that broad pre-training generally improves robustness to distribution shifts compared to narrowly trained models:
- A BERT model pre-trained on Wikipedia+Books is more robust when fine-tuned on medical text than a model pre-trained only on medical text (due to general linguistic understanding)
- Foundation models act as strong priors that regularize downstream fine-tuning

### Why Foundation Models Are Not Fully Robust

Despite broad training:
- **Spurious correlations**: foundation models may learn shortcuts (e.g., associating certain demographics with certain roles) that fail out-of-distribution
- **Underrepresented groups**: if some populations are rare in training data, the model may fail on their inputs
- **Temporal shift**: knowledge is frozen at training time; the model cannot update for new events
- **Domain-specific knowledge**: general pre-training may not capture specialized distributions (medical imaging, legal documents) sufficiently

### Connection to Alignment

Distribution shift is relevant to AI safety: a model that behaves well in testing may fail harmfully in deployment if deployment conditions differ from test conditions. This is a form of specification failure — the model learned to optimize the training objective in the training distribution, but that optimization doesn't generalize.

## Related Concepts

- [[foundation-model]] — Broad pre-training provides some but not full robustness to distribution shift
- [[ai-safety-alignment]] — Distribution shift is a deployment safety challenge
- [[hallucination]] — Can be triggered by out-of-distribution prompts where the model lacks grounding
- [[pre-training-fine-tuning]] — Fine-tuning can partially adapt a model to a target distribution

## Sources

- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 4.8

---

**Status**: Complete
**Last Updated**: 2026-04-25
