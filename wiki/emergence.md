# Emergence

The phenomenon where model capabilities are implicitly induced by training at scale rather than explicitly programmed.

## Summary

Emergence in AI means that a system exhibits behaviors and capabilities that were not directly trained for and could not be predicted simply by examining its training procedure. In foundation models, emergence refers to abilities like in-context learning, chain-of-thought reasoning, and arithmetic that appear surprisingly at sufficient model scale. Bommasani et al. (2022) identify emergence as a defining property of foundation models — it is both the source of their power (unexpected useful capabilities) and their risk (unexpected harmful behaviors).

## Explanation

### What Makes It "Emergence"?

A capability is emergent if:
1. It was not directly supervised during training
2. It arises from the interaction of scale and broad data rather than specific design choices
3. It may appear suddenly (non-linearly) as a function of model scale

Example: GPT-3 was trained purely to predict the next token. In-context learning — the ability to perform translation, arithmetic, or question answering from a few examples without any gradient updates — was never explicitly trained for. It emerged as a side effect of learning from a sufficiently large and diverse corpus.

### Examples of Emergent Capabilities

| Capability | Emerges at approximately |
|-----------|--------------------------|
| In-context learning | ~100M–1B parameters |
| Chain-of-thought reasoning | ~100B parameters |
| Instruction following (basic) | ~100B parameters |
| Multi-step arithmetic | ~175B parameters |

These capabilities show phase-transition-like behavior: nearly absent at smaller scales, then suddenly effective at larger scales. This non-linearity makes them difficult to predict and raises questions about what capabilities might emerge in future (larger) models.

### Emergence and Homogenization Interaction

Bommasani et al. note that emergence and homogenization interact in an "unsettling" way:
- Emergent capabilities spread to all downstream applications via homogenization (beneficial)
- Unexpected emergent failure modes also propagate to all downstream applications (risky)
- The opacity of emergence means we cannot characterize what capabilities a model has until they are discovered

This creates a precautionary challenge: how do we safely deploy models whose full capability profiles are unknown?

### Relationship to Scaling Laws

Emergent capabilities don't always follow smooth scaling laws. While validation loss improves as a smooth power law with compute, specific capabilities can jump discontinuously. This means:
- Log loss is a poor proxy for whether a capability exists
- Evaluating foundation models requires probing many diverse tasks, not just loss

## Related Concepts

- [[foundation-model]] — Emergence is one of two defining properties
- [[homogenization]] — The other defining property; interacts with emergence
- [[scaling-laws]] — Provides smooth metrics; emergent capabilities may not follow them smoothly
- [[in-context-learning]] — The canonical example of an emergent capability in LLMs
- [[gpt-3]] — The model that made emergence widely recognized in NLP

## Sources

- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
