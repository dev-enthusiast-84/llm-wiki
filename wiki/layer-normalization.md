# Layer Normalization

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)  
**Original paper:** Ba et al., "Layer Normalization", arXiv:1607.06450, 2016

## Summary

Layer normalization is applied after every sub-layer in the [[transformer]], combined with a [[residual-connection]], to stabilize training of deep networks.

## Explanation

Every sub-layer in the [[transformer]] encoder and decoder is wrapped as:

```
output = LayerNorm(x + Sublayer(x))
```

This pattern (residual + norm) is applied uniformly to all sub-layers: [[multi-head-attention]] and [[feed-forward-network]] in the encoder, and all three sub-layers in the decoder.

Layer normalization normalizes activations across the feature dimension (rather than the batch dimension as in batch normalization), making it well-suited for variable-length sequences and small batch sizes common in sequence modeling.

**Why it matters for the Transformer:**  
Deep stacks (N=6 layers, each with multiple sub-layers) can suffer from unstable gradients. LayerNorm helps gradients flow through the network during training, and is a prerequisite for the residual connection pattern to work effectively at this depth.

**Note:** The paper does not discuss layer normalization in detail — it cites Ba et al. (2016) and applies it as a standard component without ablation. Its importance was validated in subsequent work on Transformer variants (Pre-LN vs Post-LN).

## Contradictions / Tensions Across Papers

- **vs. Brown et al. (2020) — Pre-LN vs Post-LN:** The original Transformer uses Post-LN: `LayerNorm(x + Sublayer(x))` — normalization applied *after* the residual sum. [[gpt-3]] uses Pre-LN: `x + Sublayer(LayerNorm(x))` — normalization applied *before* each sublayer. At very large scale, Post-LN requires careful learning rate warm-up to avoid early training instability; Pre-LN avoids this and has become the standard in large models. The Transformer paper predates the scale at which this difference matters and does not evaluate it.

## Related Concepts

- [[residual-connection]]
- [[transformer]]
- [[encoder-decoder]]
- [[feed-forward-network]]
- [[multi-head-attention]]
- [[gpt-3]]
