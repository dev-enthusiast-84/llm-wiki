# Residual Connection

A shortcut connection that adds a layer's input directly to its output, enabling gradient flow through deep networks.

## Summary

Residual (skip) connections, introduced by He et al. (2016) for image recognition, are used throughout the Transformer to stabilize training of deep networks. Each sub-layer in the Transformer (attention or FFN) has its output added to its input before layer normalization: $\text{LayerNorm}(x + \text{Sublayer}(x))$. This allows gradients to flow directly through the network without passing through the sub-layer, making it much easier to train deep stacks.

## Explanation

### Formula

For each sub-layer:
$$\text{Output} = \text{LayerNorm}(x + \text{Sublayer}(x))$$

Where $\text{Sublayer}(x)$ is either the multi-head attention function or the feed-forward network.

### Why Residuals?

Without skip connections, gradients in deep networks either vanish (become too small to update early layers) or explode (grow uncontrollably). Adding the identity shortcut ensures that even if $\text{Sublayer}(x)$ produces a small contribution, the gradient can still flow through the addition directly. This allows training of much deeper networks.

In practice, residual connections allow the model to "learn what to change" rather than "learn the full transformation from scratch" — the sub-layer only needs to learn a residual update $\Delta x$ on top of the identity.

### Pre-LN vs. Post-LN

The original Transformer (2017) uses **Post-LN**: normalization is applied after the residual addition. Modern architectures (e.g., GPT-2, LLaMA) typically use **Pre-LN**: normalization is applied to the sub-layer input before it is processed, which generally leads to more stable training and removes the need for careful learning rate warmup.

### Requirement: Matching Dimensions

For residual connections to work, the sub-layer input and output must have the same dimension. This is why all Transformer sub-layers produce outputs of dimension $d_{\text{model}}$, including the embedding layers.

## Related Concepts

- [[transformer]] — Uses residual connections around every sub-layer
- [[layer-normalization]] — Applied in conjunction with every residual connection
- [[feed-forward-network]] — One of the two sub-layers wrapped with residuals
- [[multi-head-attention]] — The other sub-layer wrapped with residuals

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
