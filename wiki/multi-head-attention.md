# Multi-Head Attention

Running multiple attention operations in parallel with different learned projections, then concatenating and projecting the results.

## Summary

Multi-Head Attention extends Scaled Dot-Product Attention by performing h independent attention operations ("heads") on linearly projected versions of the queries, keys, and values. Each head can attend to different representation subspaces at different positions, which a single attention head cannot do when averaging. The outputs are concatenated and projected back, producing the same total dimensionality. This is used throughout the Transformer in encoder self-attention, decoder self-attention, and cross-attention.

## Explanation

### Formula

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O$$

where each head is:
$$\text{head}_i = \text{Attention}(Q W_i^Q,\; K W_i^K,\; V W_i^V)$$

Projection matrices:
- $W_i^Q \in \mathbb{R}^{d_{\text{model}} \times d_k}$
- $W_i^K \in \mathbb{R}^{d_{\text{model}} \times d_k}$
- $W_i^V \in \mathbb{R}^{d_{\text{model}} \times d_v}$
- $W^O \in \mathbb{R}^{h d_v \times d_{\text{model}}}$

### Hyperparameters (Original Paper)

In the base Transformer: h = 8 heads, $d_k = d_v = d_{\text{model}}/h = 512/8 = 64$. The reduced dimension per head keeps total compute comparable to single-head attention at full dimensionality.

### Why Multiple Heads?

A single attention function averages over all positions when weighting values, which can dilute attention patterns. Multiple heads can jointly attend to information from different representation subspaces — for example, one head may track syntactic dependencies while another tracks semantic similarity. Empirical attention visualizations confirm that different heads learn different structural roles.

### Computational Cost

Each head operates on $d_k = d_{\text{model}}/h$ dimensions, so total cost is similar to one full-dimensional attention operation. The Concat + $W^O$ projection is the only overhead.

## Related Concepts

- [[scaled-dot-product-attention]] — The attention function run inside each head
- [[self-attention]] — Multi-head attention applied where Q, K, V all come from the same source
- [[transformer]] — Uses multi-head attention in three distinct places per decoder layer
- [[bert]] — Uses 12 heads (Base) or 16 heads (Large) in its encoder

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.2.2

---

**Status**: Complete
**Last Updated**: 2026-04-25
