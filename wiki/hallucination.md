# Hallucination

The tendency of language models to generate plausible-sounding but factually incorrect or fabricated content.

## Summary

Hallucination refers to outputs where a language model produces content that is fluent and confident but factually wrong, unsupported by context, or entirely fabricated. It is one of the most critical reliability failures of generative foundation models and has significant implications for deployment in high-stakes domains (healthcare, law, factual QA). Hallucination arises because LLMs are trained to maximize token-level likelihood, not factual accuracy — they learn to generate plausible continuations, not verified truths.

## Explanation

### Types of Hallucination

**Intrinsic hallucination**: contradicts information provided in the input context (e.g., a model summarizes a document and invents facts not present).

**Extrinsic hallucination**: generates content that cannot be verified or is contradicted by external knowledge (e.g., inventing citations, fabricating statistics, attributing quotes incorrectly).

### Why Models Hallucinate

1. **Training objective mismatch**: Models maximize log-likelihood on training text, not factual accuracy. A model learns that "Albert Einstein said: 'The definition of insanity is...'" is a fluent pattern because it appears frequently in web text — even if the attribution is incorrect.

2. **Knowledge cutoff**: Models have no access to information beyond their training data. Questions about recent events may trigger confident but incorrect responses.

3. **Ambiguous or underspecified prompts**: When the model lacks sufficient information to answer correctly, it still produces a high-probability completion rather than expressing uncertainty.

4. **Exposure bias**: Autoregressive models condition on their own previous outputs. Errors in early tokens compound.

### Connection to Evaluation

Bommasani et al. (2022) highlight that hallucination makes foundation model evaluation difficult: standard benchmarks often have closed-form correct answers, but real-world deployment involves open-ended generation where hallucination detection is much harder.

### Mitigation Strategies

- **Retrieval-Augmented Generation (RAG)**: ground model outputs in retrieved documents
- **RLHF**: fine-tuning with human feedback penalizing incorrect responses
- **Chain-of-thought prompting**: encouraging step-by-step reasoning can improve factual accuracy
- **Calibrated confidence**: training models to express uncertainty rather than confabulate

## Related Concepts

- [[foundation-model]] — Hallucination is a key failure mode of generative foundation models
- [[rlhf]] — A training technique that can reduce (but not eliminate) hallucination
- [[instructgpt]] — RLHF-trained model specifically targeting helpfulness and honesty
- [[ai-safety-alignment]] — Hallucination is an alignment failure (model output ≠ correct/intended output)
- [[in-context-learning]] — RAG and few-shot prompting are partial mitigations

## Stale Claims

This page relies solely on Bommasani et al. (2022). Hallucination research has moved rapidly post-2022 (TruthfulQA benchmark, factuality probing, RAG systems, calibration training). When newer sources are added to `/raw`, update the mitigation strategies and add a post-2022 citation.

## Sources

- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Sections 4.4, 5.2

---

**Status**: Complete
**Last Updated**: 2026-04-25
