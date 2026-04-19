# Entity Template

Copy this template when creating a new wiki entity page. Save as `wiki/concept-name.md`.

```markdown
# Concept Name

One-line definition or tagline.

## Summary

2-3 sentence high-level overview of what this concept is and why it matters in the context of LLMs/AI.

## Explanation

Detailed breakdown of the concept:
- How it works
- Why it's important
- Key components or aspects
- Mathematical notation (if applicable)

Use subsections for complex topics:

### Section 1

Details...

### Section 2

Details...

## Related Concepts

- [[concept1]] - How it relates
- [[concept2]] - How it relates
- [[concept3]] - How it relates

## Sources

- [Author Name] - "Paper Title" (Year) - Section/Page
- [Author Name] - "Paper Title" (Year)

## Contradictions

(Optional section - include only if you found conflicting definitions in the literature)

Description of the contradiction:
- Definition A per [Paper X]
- Definition B per [Paper Y]
- Context: When each definition applies or which is more commonly accepted

---

**Status**: Draft / Complete
**Last Updated**: YYYY-MM-DD
```

## Tips for Filling Out

**Concept Name**: Exactly as it appears in links (must match kebab-case filename)

**Summary**: Assume reader has no background. Explain in plain language.

**Explanation**: This is where you go deep. Include:
- Formal definitions
- Mathematical formulations (use `$KaTeX$` syntax)
- Examples
- Use cases in LLMs

**Related Concepts**: Always add this section. Use `[[brackets]]` for each link. Helps readers navigate.

**Sources**: Always cite. This provides traceability and helps readers dive deeper.

**Contradictions**: If you noticed different papers define something differently, document it. This is valuable for researchers.

## Example (Filled)

```markdown
# Self-Attention

A neural network mechanism that computes attention weights between all pairs of tokens in a sequence.

## Summary

Self-attention allows each token in a sequence to attend to every other token (and itself), computing a weighted combination based on learned similarity scores. It's the core mechanism that makes Transformers work and enables models to capture long-range dependencies without recurrence.

## Explanation

In self-attention, each token is transformed into three vectors: Query (Q), Key (K), and Value (V). Attention scores are computed as the dot product of queries and keys, scaled and normalized with softmax, then used to weight the values.

### Mathematical Formulation

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Where $d_k$ is the dimension of the key vectors.

## Related Concepts

- [[scaled-dot-product-attention]] - The specific implementation used in Transformers
- [[multi-head-attention]] - Extension using multiple attention heads
- [[transformer]] - Architecture that uses self-attention as its core
- [[positional-encoding]] - How position information is added since self-attention is position-agnostic

## Sources

- Vaswani et al. - "Attention is All You Need" (2017) - Section 3.2
- Clark et al. - "What does BERT look at?" (2019)

---

**Status**: Complete
**Last Updated**: 2026-04-19
```
