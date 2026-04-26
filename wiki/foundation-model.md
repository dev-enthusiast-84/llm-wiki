# Foundation Model

A model trained on broad data at scale (typically using self-supervision) that can be adapted to a wide range of downstream tasks.

## Summary

Foundation models (Bommasani et al., 2022) are any models trained on massive, diverse datasets using self-supervised learning and subsequently adapted to numerous downstream applications. Examples include BERT, GPT-3, CLIP, DALL-E, and LLaMA. The term was coined at Stanford to capture the paradigm shift: a single model serves as the "foundation" for many task-specific applications rather than building each from scratch. They are characterized by two defining properties — **emergence** and **homogenization** — and carry both extraordinary potential and significant societal risks.

## Explanation

### Definition

A foundation model satisfies two criteria:
1. **Broad training**: trained on large, diverse data using self-supervision (often web-scale corpora, images, or code)
2. **Adaptable**: can be fine-tuned, prompted, or otherwise adapted to a wide variety of downstream tasks

The word "foundation" emphasizes that these models are incomplete on their own — they require adaptation and are the base from which task-specific models are built.

### Why "Foundation Model" (Not "Pretrained Model")?

Existing terms like "pretrained model" or "self-supervised model" capture the technical mechanism but miss the sociological significance:
- A foundation model is adapted to tasks by many different users for many different purposes
- Its properties (capabilities, biases, failures) are inherited by all downstream applications
- This creates systemic leverage: improvements propagate widely, but so do flaws

### The Foundation Model Ecosystem

Bommasani et al. describe a pipeline from **data creation → data curation → training → adaptation → deployment**. Foundation models sit at the training stage, but their impact radiates through all stages:
- Data creators influence what capabilities emerge
- Downstream deployers inherit the model's biases and limitations
- End users are the ultimate recipients of both benefits and harms

### Emergence and Homogenization

The two defining properties of foundation models:
- **[[emergence]]**: capabilities are implicitly induced from training, not explicitly programmed. GPT-3's in-context learning was never directly trained for — it emerged from broad pre-training at scale.
- **[[homogenization]]**: most NLP systems now derive from a small number of foundation models (BERT, GPT, etc.). This concentrates power and risk: all systems inherit the same biases and failure modes.

### Risks and Opportunities

Key concerns (from Bommasani et al. 2022):
- **Inequity and fairness**: biases in training data propagate to all adapted models
- **Misuse**: powerful generation capabilities can be exploited for disinformation
- **Environmental impact**: training costs are enormous (GPT-3 required ~3.14×10²³ FLOPs ≈ hundreds of thousands of GPU-hours; the "3.5 days × 8 GPUs" figure refers to the original Transformer (2017), not GPT-3)
- **Security**: single point of failure — attacks on foundation models compromise all downstream systems
- **Distribution shift**: models may behave unexpectedly on data different from training distribution

## Related Concepts

- [[emergence]] — A defining property; capabilities arise from scale, not explicit design
- [[homogenization]] — A defining property; one model underpins many applications
- [[self-supervised-learning]] — The training paradigm enabling foundation models
- [[pre-training-fine-tuning]] — The adaptation mechanism
- [[scaling-laws]] — Foundation models work because performance scales predictably
- [[bert]] — Encoder-based foundation model for NLP understanding
- [[gpt-3]] — Decoder-based foundation model for generation
- [[in-context-learning]] — A key emergent capability of large foundation models
- [[ai-safety-alignment]] — Critical concern given foundation models' societal reach
- [[hallucination]] — A key failure mode of generative foundation models
- [[distribution-shift]] — A robustness challenge for deployed foundation models
- [[small-language-model]] — Task-specialized alternative to foundation models; contrasts the "one model fits all" paradigm

## Sources

- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Sections 1–1.4

---

**Status**: Complete
**Last Updated**: 2026-04-25
