# Recurrent Neural Network

A neural network with loops that allows information to persist across sequential inputs.

## Summary

A Recurrent Neural Network (RNN) is designed for sequential data — time series, natural language, speech — where order matters and context from earlier steps must inform later ones. Unlike feed-forward networks, RNNs maintain a hidden state that is updated at each time step, creating an implicit memory. This made them the dominant architecture for NLP before the Transformer.

## Explanation

### How RNNs Work

At each time step $t$, an RNN receives an input $x_t$ and a hidden state $h_{t-1}$ from the previous step, producing a new hidden state:

$$h_t = f(W_h \cdot h_{t-1} + W_x \cdot x_t + b)$$

The same weights ($W_h$, $W_x$, $b$) are shared across all time steps — this is what makes them recurrent. The hidden state acts as a compressed memory of everything seen so far.

### Unrolling

An RNN can be conceptually "unrolled" through time: each time step becomes a layer in a deep feed-forward network, with the same weights applied at every layer. This framing is important for understanding backpropagation through time (BPTT), the training algorithm.

### Shared Weights

Because the same weight matrices are applied at every time step, RNNs have far fewer parameters than equivalent feed-forward networks applied to sequences. However, shared weights also mean that gradients flow through many multiplications during backpropagation.

### Problems with Vanilla RNNs

| Problem | Description |
|---------|-------------|
| Vanishing gradients | Gradients shrink exponentially as they propagate back through many time steps |
| Exploding gradients | Gradients grow exponentially, causing unstable weight updates |

Both problems make it difficult for basic RNNs to learn long-term dependencies — patterns where the relevant context occurred many steps earlier.

### RNN vs. Transformer

| | RNN | Transformer |
|---|---|---|
| Sequential operations | O(n) — must process token-by-token | O(1) — all positions in parallel |
| Long-range dependencies | Difficult (vanishing gradients) | Direct via self-attention |
| Training speed | Slow (sequential) | Fast (parallel) |

The Transformer replaced RNNs as the dominant NLP architecture precisely because self-attention addresses both the parallelism and long-range dependency problems inherent to recurrence.

## Related Concepts

- [[lstm]] — Extension of RNN that solves the vanishing gradient problem via gated memory cells
- [[vanishing-gradient]] — Core failure mode of vanilla RNNs on long sequences
- [[transformer]] — Replaced RNNs for NLP by using attention instead of recurrence
- [[self-attention]] — The mechanism that makes Transformers position-parallel and long-range capable
- [[autoregressive-language-model]] — Language models that process tokens sequentially; historically implemented with RNNs

## Sources

- "RNN and LSTM Simply Explained" (presentation) — raw/RNN and LSTM Basics.pptx

---

**Status**: New (from sync)
**Last Updated**: 2026-04-25
