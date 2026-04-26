# Feed-Forward Network

A position-wise fully connected network applied identically and independently to each token in a Transformer layer.

## Summary

Each layer of a Transformer encoder or decoder contains a two-layer feed-forward network (FFN) applied to each position separately after the attention sub-layer. It consists of two linear transformations with a ReLU activation in between. Although the transformation is the same across positions, different parameters are used from layer to layer. The FFN provides a per-token non-linear transformation that complements the global mixing done by multi-head attention.

## Explanation

### Formula

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

Where:
- $W_1 \in \mathbb{R}^{d_{\text{model}} \times d_{ff}}$ expands to the inner dimension
- $W_2 \in \mathbb{R}^{d_{ff} \times d_{\text{model}}}$ projects back

In the original Transformer: $d_{\text{model}} = 512$, $d_{ff} = 2048$ (4× expansion). The big model uses $d_{ff} = 4096$ with $d_{\text{model}} = 1024$.

### Role in the Transformer

Multi-head attention aggregates information **across** positions (global, mixing). The FFN then transforms each position's representation **independently** (local, per-token). Together they form the complete Transformer block:

```
Input → [Multi-Head Attention → Add & Norm] → [FFN → Add & Norm] → Output
```

The FFN can be interpreted as two convolutions with kernel size 1, applying the same dense transformation to every position.

### Modern Variants

- **SwiGLU / GeGLU**: Replace ReLU with gated activations (used in LLaMA, PaLM)
- **Mixture of Experts (MoE)**: Replace the FFN with a sparse set of expert FFNs, routing each token to a subset — reduces compute per forward pass while scaling capacity
- The expansion ratio (typically 4×) is a key hyperparameter; larger ratios increase model capacity

## Related Concepts

- [[transformer]] — FFN is one of two sub-layers in every Transformer block
- [[residual-connection]] — Wraps the FFN to aid gradient flow
- [[layer-normalization]] — Applied after the residual addition following the FFN
- [[multi-head-attention]] — The other sub-layer; FFN and attention work together in each block

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.3

---

**Status**: Complete
**Last Updated**: 2026-04-25
