# Residual Connection

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)  
**Original paper:** He et al., "Deep Residual Learning for Image Recognition", CVPR 2016

## Summary

Residual (skip) connections wrap every sub-layer in the [[transformer]], adding the sub-layer's input directly to its output before [[layer-normalization]]. This enables training deep stacks without gradient degradation.

## Explanation

**Pattern applied in the [[transformer]]:**

```
output = LayerNorm(x + Sublayer(x))
```

The input x is added back to the transformed output Sublayer(x) before normalization. This is applied to every sub-layer: [[multi-head-attention]] and [[feed-forward-network]] in the encoder, and all three sub-layers in the decoder.

**Why residual connections work:** They provide a "highway" for gradients to flow backwards through many layers without passing through potentially saturated non-linearities, addressing the vanishing gradient problem in deep networks.

**Constraint they impose:** All sub-layers in the model must produce outputs of the same dimension (d_model = 512 for the base model; 1024 for the big model) so that the addition x + Sublayer(x) is dimensionally consistent. This is why the embedding layers also produce d_model-dimensional outputs.

**Pre-LN vs Post-LN:** The Transformer uses Post-LN: `LayerNorm(x + Sublayer(x))`. [[gpt-3]] and subsequent large models use Pre-LN: `x + Sublayer(LayerNorm(x))`, applying [[layer-normalization]] before the sublayer rather than after the residual sum. Pre-LN produces more stable gradients at very large scale. See [[layer-normalization]] for full discussion.

## Related Concepts

- [[layer-normalization]]
- [[transformer]]
- [[encoder-decoder]]
- [[feed-forward-network]]
- [[multi-head-attention]]
- [[gpt-3]]
