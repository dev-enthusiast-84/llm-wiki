# Layer Normalization

A normalization technique that standardizes activations across the feature dimension for each training example independently.

## Summary

Layer Normalization (Ba et al., 2016) normalizes the inputs across the feature dimension (rather than across the batch) for each individual token position. In the Transformer, it is applied after every residual addition, stabilizing activations throughout the deep stack. Unlike Batch Normalization, it has no dependence on batch size, making it well-suited for variable-length sequences and small-batch training scenarios common in NLP.

## Explanation

### Formula

Given an input vector $x \in \mathbb{R}^{d}$:

$$\text{LayerNorm}(x) = \frac{x - \mu}{\sigma + \epsilon} \odot \gamma + \beta$$

Where:
- $\mu = \frac{1}{d}\sum_{i=1}^d x_i$ — mean of the features
- $\sigma = \sqrt{\frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2}$ — standard deviation
- $\gamma, \beta \in \mathbb{R}^d$ — learned scale and shift parameters
- $\epsilon$ — small constant for numerical stability

### Placement in the Transformer

Used in the **Post-LN** convention (original Transformer):
```
Output = LayerNorm(x + Sublayer(x))
```

In the **Pre-LN** convention (most modern models):
```
Output = x + Sublayer(LayerNorm(x))
```

Pre-LN is generally more stable during training, especially with large learning rates, and has become the standard in GPT-2 onward.

### Contrast with Batch Normalization

| Property | Layer Norm | Batch Norm |
|----------|-----------|-----------|
| Normalized over | Feature dim (per example) | Batch dim (per feature) |
| Depends on batch size | No | Yes |
| Works with seq of varying length | Yes | Awkward |
| Typical use | NLP, Transformers | Vision, CNNs |

## Related Concepts

- [[transformer]] — Applies layer norm after every residual addition
- [[residual-connection]] — Always paired with layer normalization
- [[feed-forward-network]] — One sub-layer after which layer norm is applied
- [[multi-head-attention]] — The other sub-layer after which layer norm is applied

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.1
- Ba et al. — "Layer Normalization" (2016)

---

**Status**: Complete
**Last Updated**: 2026-04-25
