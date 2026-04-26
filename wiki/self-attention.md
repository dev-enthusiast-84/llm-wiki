# Self-Attention

An attention mechanism where a sequence attends to itself — each position can directly access information from every other position.

## Summary

Self-attention (also called intra-attention) allows every token in a sequence to compute a weighted combination of all other tokens, capturing dependencies regardless of distance. It is the core mechanism behind Transformers and replaces the sequential processing of RNNs, enabling parallelization. Each position produces three vectors — Query, Key, Value — and the output is a weighted sum of Values where weights come from Query-Key similarity.

## Explanation

### Intuition

In a sentence like "The animal didn't cross the street because **it** was too tired," self-attention lets the model resolve that "it" refers to "animal" by directly attending to it across the sequence — something RNNs could only achieve by propagating state through many steps.

### Mechanism

Each input token $x_i$ is projected into three vectors:
- **Query** $Q = xW^Q$: what this token is "looking for"
- **Key** $K = xW^K$: what this token "advertises"
- **Value** $V = xW^V$: the actual content to be aggregated

Attention scores between all pairs are computed, scaled, softmaxed, and used to weight the Values:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### Computational Properties

| Property | Self-Attention | Recurrent |
|----------|---------------|-----------|
| Complexity per layer | O(n²·d) | O(n·d²) |
| Sequential operations | O(1) | O(n) |
| Max path length | O(1) | O(n) |

Self-attention scales quadratically with sequence length but connects all positions in constant sequential steps, making long-range dependency learning tractable.

### Applications in the Transformer

The Transformer uses self-attention in three distinct ways:
1. **Encoder self-attention**: Each encoder position attends to all encoder positions
2. **Decoder self-attention (masked)**: Positions attend only to earlier positions (causal masking, setting future positions to −∞)
3. **Cross-attention**: Decoder queries attend to encoder keys/values

## Related Concepts

- [[scaled-dot-product-attention]] — The specific computation inside self-attention
- [[multi-head-attention]] — Runs multiple self-attention operations in parallel
- [[transformer]] — Architecture that uses self-attention as its core building block
- [[positional-encoding]] — Required because self-attention is permutation-invariant
- [[encoder-decoder]] — How self-attention fits into the full model structure

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Sections 3.2, 4
- Wikipedia — "Transformer (deep learning)" — Attention mechanism section

---

**Status**: Complete
**Last Updated**: 2026-04-25
