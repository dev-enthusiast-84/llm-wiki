# Positional Encoding

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

Positional encoding injects information about token order into the [[transformer]], which has no inherent notion of sequence position because [[self-attention]] treats all positions symmetrically.

## Explanation

Since the [[transformer]] contains no recurrence and no convolution, it cannot distinguish token order without explicit positional signals. Positional encodings are added to input embeddings at the bottom of both the encoder and decoder stacks.

**Sinusoidal positional encoding (used in the paper):**

```
PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
```

- `pos`: position in sequence
- `i`: dimension index
- Each dimension corresponds to a sinusoid with a different frequency
- Wavelengths form a geometric progression from 2π to 10000·2π

**Why sinusoidal?** For any fixed offset k, PE(pos+k) can be expressed as a linear function of PE(pos) — making it easy for the model to attend by relative positions. It also extrapolates naturally to sequence lengths longer than seen during training.

**Alternative: learned positional embeddings** were also tested (row E in Table 3) and produced nearly identical results. The sinusoidal version was chosen for its extrapolation property.

Both encodings have the same dimensionality (d_model = 512) as the token embeddings, so they can be summed directly.

## Contradictions / Tensions Across Papers

- **Sinusoidal vs learned:** The [[transformer]] paper tests both sinusoidal and learned positional embeddings and finds them nearly identical (Table 3, row E). It recommends sinusoidal for its extrapolation property to longer sequences. [[bert]] uses **learned positional embeddings exclusively**, with a maximum sequence length of 512. During pre-training, BERT trains on sequences of length 128 for 90% of steps, then 512 for the remaining 10%, specifically to learn the position embeddings at longer lengths. This contradicts the Transformer paper's suggestion that sinusoidal encodings are preferable for length generalization — BERT treats length generalization as a non-issue given its fixed 512-token cap.

## Related Concepts

- [[transformer]]
- [[self-attention]]
- [[encoder-decoder]]
- [[bert]]
- [[cls-sep-tokens]]
