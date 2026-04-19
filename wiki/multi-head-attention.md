# Multi-Head Attention

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

Multi-Head Attention runs [[scaled-dot-product-attention]] in parallel across h learned linear projections of the queries, keys, and values, then concatenates and re-projects the results. This lets the model attend to information from different representation subspaces simultaneously.

## Explanation

**Formula:**

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W_O

where head_i = Attention(Q·W_Q_i, K·W_K_i, V·W_V_i)
```

**Parameter dimensions (base model):**
- h = 8 heads
- d_k = d_v = d_model / h = 512 / 8 = 64
- W_Q_i, W_K_i ∈ ℝ^(d_model × d_k)
- W_V_i ∈ ℝ^(d_model × d_v)
- W_O ∈ ℝ^(h·d_v × d_model)

Because each head operates at reduced dimension (64 instead of 512), total computational cost is similar to single-head attention at full dimensionality.

**Why multiple heads?** A single attention head averages over subspaces, inhibiting the model from jointly attending to different positional and representational patterns. Multiple heads specialize: empirically, different heads learn to resolve anaphora, track long-distance dependencies, and capture syntactic structure.

**Ablation findings (Table 3 in paper):**
- Single-head attention (h=1) loses 0.9 BLEU vs best setting
- Too many heads (h=32) also degrades quality
- Optimal was h=8 for the base model

## Related Concepts

- [[scaled-dot-product-attention]]
- [[self-attention]]
- [[transformer]]
- [[encoder-decoder]]
