# Scaled Dot-Product Attention

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

Scaled Dot-Product Attention is the specific attention function used in the [[transformer]]. It computes attention weights via scaled dot products between queries and keys, then applies them to values.

## Explanation

**Formula:**

```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

- Q: matrix of queries (dimension d_k)
- K: matrix of keys (dimension d_k)
- V: matrix of values (dimension d_v)
- √d_k: scaling factor

**Why the scaling?** For large d_k, dot products grow large in magnitude, pushing softmax into regions with extremely small gradients. Dividing by √d_k counteracts this. Formally, if q and k have independent components with mean 0 and variance 1, then q·k has variance d_k — scaling normalizes this back to unit variance.

**Comparison with additive attention (Bahdanau et al.):**
- Additive attention uses a feed-forward network with a single hidden layer to compute compatibility
- Both have similar theoretical complexity, but dot-product attention is faster and more space-efficient due to optimized matrix multiplication
- At small d_k, both perform similarly; additive attention outperforms unscaled dot-product at large d_k

**Masking:** In the decoder, illegal future positions are masked by setting their pre-softmax values to −∞, which zeroes out those attention weights after softmax.

## Related Concepts

- [[multi-head-attention]]
- [[self-attention]]
- [[transformer]]
