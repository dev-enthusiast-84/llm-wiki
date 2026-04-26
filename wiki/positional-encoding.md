# Positional Encoding

Information added to token embeddings to give the Transformer awareness of token order, since attention itself is permutation-invariant.

## Summary

Self-attention has no inherent notion of sequence order — it treats inputs as a set, not a sequence. Positional encodings inject position information by adding a fixed or learned vector to each token embedding before the first layer. The original Transformer uses sinusoidal functions of different frequencies so that the model can learn to attend by relative positions, and so that encodings can extrapolate to sequence lengths unseen during training.

## Explanation

### Sinusoidal Positional Encoding

The original formulation uses sine and cosine functions:

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$
$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

Where $pos$ is the position in the sequence and $i$ is the dimension index. Each dimension corresponds to a sinusoid with wavelengths forming a geometric progression from $2\pi$ to $10000 \cdot 2\pi$.

### Why Sinusoidal?

The sinusoidal encoding has a useful property: for any fixed offset $k$, $PE_{pos+k}$ can be expressed as a linear function of $PE_{pos}$. This allows the model to easily learn to attend by relative offset. It also allows extrapolation beyond the training sequence length.

### Learned vs. Fixed

Vaswani et al. (2017) also experimented with learned positional embeddings (as used in BERT) and found nearly identical results. The sinusoidal version was chosen because it can extrapolate to longer sequences without retraining.

The encodings are added (not concatenated) to token embeddings, so they must match $d_{\text{model}}$. The same encoding is added at both the encoder and decoder input layers.

### Modern Variants

- **Learned absolute** (BERT, GPT): trainable embedding per position
- **Rotary (RoPE)**: encodes relative positions via rotation in complex space
- **ALiBi**: adds a position bias directly to attention scores
- **Relative position encoding**: encodes distance between token pairs rather than absolute positions

## Related Concepts

- [[self-attention]] — Position-agnostic without this injection
- [[transformer]] — Adds positional encoding to inputs before the encoder and decoder stacks
- [[bert]] — Uses learned positional embeddings instead of sinusoidal

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.5

---

**Status**: Complete
**Last Updated**: 2026-04-25
