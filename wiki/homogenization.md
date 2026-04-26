# Homogenization

The consolidation of AI system development around a small number of foundation models, creating shared capabilities but also shared failure modes.

## Summary

Homogenization (Bommasani et al., 2022) describes how the rise of foundation models has led to a convergence in NLP: most state-of-the-art systems now derive from a small number of pre-trained models (BERT, GPT, etc.). This creates powerful leverage — improvements to foundation models instantly benefit many downstream systems — but also a critical liability: the biases, errors, and failure modes of foundation models are inherited by all models adapted from them, creating systemic single points of failure.

## Explanation

### Historical Trajectory of Homogenization

Bommasani et al. trace homogenization through AI's history:
- **Machine learning** homogenized *learning algorithms* (e.g., logistic regression, SVMs)
- **Deep learning** homogenized *architectures* (e.g., CNNs for vision, RNNs for text)
- **Foundation models** homogenize the *models themselves* (e.g., BERT, GPT-3)

Each step represents increasing leverage — and increasing risk concentration.

### Benefits of Homogenization

- **Efficient knowledge transfer**: improvements to BERT immediately improve all BERT-based systems across NLP benchmarks and applications (Google Search, Bing, etc.)
- **Reduced redundancy**: organizations don't need to train models from scratch for each task
- **Research leverage**: studying one foundation model generates insights applicable to many downstream uses

### Risks of Homogenization

- **Inherited biases**: if a foundation model encodes gender bias or racial stereotypes, these propagate to all downstream systems — amplified by deployment at scale
- **Single point of failure**: a security vulnerability or adversarial attack on a foundation model compromises all systems built on it
- **Epistemic uniformity**: when all systems derive from the same models, they have correlated failures; diversity of approaches is lost
- **Power concentration**: few organizations (Google, OpenAI, Meta, Anthropic) develop the foundation models that everyone else depends on

### Relationship to Emergence

Homogenization amplifies both the benefits and risks of [[emergence]]:
- Emergent capabilities spread instantly across all downstream applications (beneficial)
- Emergent failure modes also spread instantly (dangerous)
- The uncertainty of emergence, combined with homogenization's leverage, means we may be deploying systems with unknown capabilities at enormous scale

## Related Concepts

- [[foundation-model]] — Homogenization is one of two defining properties
- [[emergence]] — The other defining property; its effects are amplified by homogenization
- [[ai-safety-alignment]] — Homogenization makes alignment especially critical (one model → many harms)
- [[distribution-shift]] — Shared training data means shared distribution assumptions across all downstream models
- [[hallucination]] — If a foundation model consistently hallucinates on certain topics, all derived models may too

## Sources

- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
