# Transformer

A neural network architecture based entirely on attention mechanisms, dispensing with recurrence and convolutions.

## Summary

The Transformer, introduced by Vaswani et al. (2017), replaced recurrent and convolutional architectures for sequence transduction with a design built purely on self-attention and feed-forward layers. It enables massive parallelization during training and achieves state-of-the-art results on machine translation, while generalizing to a wide range of NLP tasks. Its architecture became the foundation for virtually all modern large language models.

## Explanation

### Architecture Overview

The Transformer follows an encoder-decoder structure. Both the encoder and decoder are composed of stacked identical layers (N=6 in the original paper):

- **Encoder**: Each layer has two sub-layers — a multi-head self-attention mechanism and a position-wise feed-forward network.
- **Decoder**: Each layer adds a third sub-layer — multi-head attention over the encoder output (cross-attention).

Residual connections and layer normalization are applied around each sub-layer:
$$\text{Output} = \text{LayerNorm}(x + \text{Sublayer}(x))$$

All sub-layers and embedding layers produce outputs of dimension $d_{\text{model}} = 512$.

### Key Hyperparameters (Base Model)

| Parameter | Value |
|-----------|-------|
| Layers (N) | 6 |
| Model dim ($d_{\text{model}}$) | 512 |
| Feed-forward dim ($d_{ff}$) | 2048 |
| Attention heads (h) | 8 |
| Key/value dim ($d_k = d_v$) | 64 |

### Why Attention Over Recurrence?

Self-attention connects all positions with a constant number of sequential operations (O(1)), versus O(n) for recurrent layers. This allows learning long-range dependencies more easily and enables full parallelization over sequence positions.

### Training

Trained on WMT 2014 English-German (~4.5M sentence pairs, byte-pair encoding, 37K tokens) and English-French (36M sentences, 32K word-piece vocabulary). Achieved 28.4 BLEU on EN-DE and 41.8 on EN-FR, outperforming all prior models at a fraction of the training cost.

## Related Concepts

- [[self-attention]] — Core mechanism; each sub-layer in the encoder uses self-attention
- [[multi-head-attention]] — Extension that runs multiple attention operations in parallel
- [[scaled-dot-product-attention]] — The specific attention function used
- [[positional-encoding]] — Required because attention is position-agnostic
- [[encoder-decoder]] — The overall architectural pattern the Transformer follows
- [[feed-forward-network]] — The second sub-layer in each Transformer block
- [[residual-connection]] — Used around each sub-layer to ease gradient flow; also addresses vanishing gradients
- [[layer-normalization]] — Applied after each residual addition
- [[bert]] — Encoder-only Transformer pre-trained with MLM
- [[gpt-3]] — Decoder-only Transformer scaled to 175B parameters
- [[byte-pair-encoding]] — Tokenization scheme used in Transformer training
- [[bleu]] — Evaluation metric used to benchmark the Transformer on WMT 2014 translation tasks
- [[recurrent-neural-network]] — Predecessor architecture replaced by the Transformer; suffers from sequential bottleneck
- [[vanishing-gradient]] — Key weakness of RNNs that the Transformer avoids via direct attention connections

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Sections 3, 5, 6
- Wikipedia — "Transformer (deep learning)" — History and architecture overview

---

**Status**: Complete
**Last Updated**: 2026-04-25
