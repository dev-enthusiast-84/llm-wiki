# Scaled Dot-Product Attention

The specific attention function used in Transformers: dot-product similarity scaled by the square root of key dimension.

## Summary

Scaled Dot-Product Attention computes attention weights by taking dot products of queries against all keys, dividing by $\sqrt{d_k}$ to counteract magnitude growth, applying softmax to get a probability distribution, and using those weights to aggregate the values. It is the core computation inside both self-attention and cross-attention in the Transformer. The scaling factor is the key innovation over vanilla dot-product attention, stabilizing gradients for large $d_k$.

## Explanation

### Formula

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Where:
- $Q \in \mathbb{R}^{n \times d_k}$ — matrix of query vectors
- $K \in \mathbb{R}^{m \times d_k}$ — matrix of key vectors
- $V \in \mathbb{R}^{m \times d_v}$ — matrix of value vectors
- $d_k$ — dimension of keys (also queries)

### Why the Scaling?

For large $d_k$, dot products grow large in magnitude, pushing the softmax into regions with extremely small gradients. Dividing by $\sqrt{d_k}$ counteracts this: if $q$ and $k$ are independent random variables with mean 0 and variance 1, their dot product has variance $d_k$, so dividing by $\sqrt{d_k}$ restores unit variance.

### Masked Variant

In the decoder, a mask is applied before softmax to prevent positions from attending to future positions:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T + M}{\sqrt{d_k}}\right)V$$
where $M_{ij} = -\infty$ for $j > i$ (future positions) and $0$ otherwise.

### Comparison with Additive Attention

The two most common attention functions:
- **Additive (Bahdanau)**: uses a feed-forward network with one hidden layer
- **Dot-Product (this)**: faster and more space-efficient; identical in theoretical complexity

For small $d_k$ both are similar; for large $d_k$, dot-product without scaling performs worse, but with scaling it outperforms additive attention.

## Related Concepts

- [[self-attention]] — Uses this computation; queries, keys, values come from the same sequence
- [[multi-head-attention]] — Applies this function h times in parallel with different projections
- [[transformer]] — The architecture that introduced and popularized this formulation

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.2.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
