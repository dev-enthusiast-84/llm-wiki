# Encoder-Decoder Architecture

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

The encoder-decoder (seq2seq) architecture maps an input sequence to a continuous representation, then auto-regressively generates an output sequence. The [[transformer]] is the first encoder-decoder model built entirely on [[self-attention]] rather than recurrence.

## Explanation

**Encoder:**
- Stack of N=6 identical layers
- Each layer: [[multi-head-attention]] sub-layer + [[feed-forward-network]] sub-layer
- Each sub-layer wrapped in [[residual-connection]] + [[layer-normalization]]
- Maps input (x_1, ..., x_n) → continuous representations z = (z_1, ..., z_n)

**Decoder:**
- Stack of N=6 identical layers
- Each layer: three sub-layers
  1. Masked [[multi-head-attention]] (prevents attending to future positions)
  2. Cross-attention over encoder output (queries from decoder, keys/values from encoder)
  3. [[feed-forward-network]]
- Each sub-layer wrapped in [[residual-connection]] + [[layer-normalization]]
- Auto-regressive: consumes previously generated symbols as additional input

**Cross-attention (encoder-decoder attention):** Allows every decoder position to attend to all encoder positions, mimicking the attention mechanism in earlier seq2seq models (e.g., Bahdanau et al., 2014). This is where the "translation" information flows from source to target.

**Prior work this replaces:**
- RNN/LSTM encoder-decoder (Sutskever et al., 2014; Cho et al., 2014)
- ConvS2S (Gehring et al., 2017) — convolutional, O(log n) path length
- ByteNet (Kalchbrenner et al., 2017) — convolutional, O(log n) path length

The [[transformer]] reduces cross-position path length to O(1), enabling better long-range dependency learning.

## Related Concepts

- [[transformer]]
- [[self-attention]]
- [[multi-head-attention]]
- [[layer-normalization]]
- [[residual-connection]]
- [[feed-forward-network]]
- [[positional-encoding]]
