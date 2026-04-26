# LSTM

A gated recurrent architecture that solves the vanishing gradient problem by separating short-term and long-term memory.

## Summary

Long Short-Term Memory (LSTM), introduced by Hochreiter & Schmidhuber (1997), is a special kind of RNN designed to learn long-term dependencies. Where vanilla RNNs fail on long sequences due to vanishing gradients, LSTMs avoid this by maintaining a cell state — a dedicated long-term memory — that is modified additively through learned gates rather than multiplicatively at every step.

## Explanation

### Core Idea

The key insight of LSTMs is to replace the single hidden state of a vanilla RNN with two distinct streams:

- **Cell state** ($c_t$): long-term memory; information flows along it with only minor, controlled changes
- **Hidden state** ($h_t$): short-term output; used for predictions and passed to the next time step

By adding controlled changes to the cell state (rather than multiplying by the same weight matrix repeatedly), gradients can flow back through many time steps without vanishing or exploding.

### The Three Gates

Each LSTM cell controls information flow through three learned gates, each producing values between 0 and 1:

| Gate | Function |
|------|----------|
| **Forget gate** | Decides what fraction of the previous cell state to discard |
| **Input gate** | Decides what new information to write into the cell state |
| **Output gate** | Decides what portion of the cell state to expose as the hidden state |

Formally:
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$
$$c_t = f_t \odot c_{t-1} + i_t \odot \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$
$$h_t = o_t \odot \tanh(c_t)$$

### Why This Solves Vanishing Gradients

The cell state update ($c_t$) is additive — new information is added to memory rather than multiplying the entire state by a weight matrix. When backpropagating, gradients flow back through additions rather than repeated matrix multiplications, which avoids the exponential decay that plagues vanilla RNNs.

### LSTMs vs. Transformers

LSTMs were the state-of-the-art for NLP through the mid-2010s (seq2seq, neural machine translation). The Transformer replaced them by eliminating recurrence entirely — all positions are processed in parallel via self-attention, enabling much faster training and better long-range modeling.

## Related Concepts

- [[recurrent-neural-network]] — Base architecture that LSTM extends and improves
- [[vanishing-gradient]] — The problem LSTMs were specifically designed to solve
- [[transformer]] — Successor architecture that eliminated recurrence entirely
- [[self-attention]] — The mechanism Transformers use instead of gated memory

## Sources

- "RNN and LSTM Simply Explained" (presentation) — raw/RNN and LSTM Basics.pptx

---

**Status**: New (from sync)
**Last Updated**: 2026-04-25
