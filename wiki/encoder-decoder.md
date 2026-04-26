# Encoder-Decoder

An architectural pattern where an encoder maps inputs to a latent representation and a decoder generates outputs from that representation.

## Summary

The encoder-decoder (seq2seq) architecture processes an input sequence into a continuous representation and then generates an output sequence from it. Originally used with RNNs for machine translation, the Transformer adopted this pattern with self-attention replacing recurrence. The encoder produces rich contextualized representations, and the decoder attends to them via cross-attention while auto-regressively generating output tokens. BERT uses only the encoder; GPT uses only the decoder; models like T5 and the original Transformer use the full encoder-decoder structure.

## Explanation

### Encoder

The encoder maps an input sequence $(x_1, \ldots, x_n)$ to a sequence of continuous representations $\mathbf{z} = (z_1, \ldots, z_n)$. In the Transformer, this is done by stacking N=6 identical layers, each containing:
1. Multi-head self-attention (all positions attend to all positions)
2. Position-wise feed-forward network
3. Residual connection + layer normalization around each

The output is a rich, context-aware representation of every input token.

### Decoder

The decoder generates output tokens $(y_1, \ldots, y_m)$ one at a time, auto-regressively. Each of its N layers contains:
1. **Masked self-attention**: attends only to previously generated output tokens (causal masking)
2. **Cross-attention**: attends to the encoder's output $\mathbf{z}$
3. **Feed-forward network**
4. Residual + layer norm around each

The masking ensures the model is auto-regressive: prediction of $y_t$ depends only on $(y_1, \ldots, y_{t-1})$ and $\mathbf{z}$.

### Variants by Architecture Type

| Architecture | Encoder | Decoder | Examples |
|---|---|---|---|
| Encoder-only | ✓ | ✗ | BERT, RoBERTa |
| Decoder-only | ✗ | ✓ | GPT-3, LLaMA |
| Encoder-decoder | ✓ | ✓ | T5, original Transformer, BART |

Encoder-only models excel at classification and representation tasks. Decoder-only models excel at generation. Encoder-decoder models are natural for tasks with distinct input and output sequences (translation, summarization).

## Related Concepts

- [[transformer]] — Uses encoder-decoder as its overall architecture
- [[self-attention]] — Used within both encoder and decoder
- [[multi-head-attention]] — The cross-attention layer is multi-head attention from decoder to encoder
- [[bert]] — Encoder-only variant; bidirectional attention throughout
- [[gpt-3]] — Decoder-only variant; causal attention throughout
- [[bleu]] — Primary evaluation metric for machine translation (the canonical encoder-decoder task)

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 3.1
- Wikipedia — "Transformer (deep learning)"

---

**Status**: Complete
**Last Updated**: 2026-04-25
