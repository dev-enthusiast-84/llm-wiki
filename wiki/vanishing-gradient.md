# Vanishing Gradient

A training failure mode where gradients shrink exponentially during backpropagation, preventing deep or long networks from learning.

## Summary

The vanishing gradient problem occurs when gradients become extremely small as they are propagated back through many layers or time steps. With tiny gradients, early layers (or early time steps in RNNs) receive almost no update signal, making it impossible to learn long-range dependencies. It was the primary reason vanilla RNNs failed on long sequences and motivated the development of LSTMs.

## Explanation

### Why Gradients Vanish

During backpropagation, gradients are computed via the chain rule — a product of partial derivatives across every layer or time step. If each factor in this product is less than 1, the product shrinks exponentially:

$$\frac{\partial L}{\partial h_0} = \frac{\partial L}{\partial h_T} \cdot \prod_{t=1}^{T} \frac{\partial h_t}{\partial h_{t-1}}$$

For an RNN with weight matrix $W$ and activation $\tanh$:

$$\frac{\partial h_t}{\partial h_{t-1}} = W^T \cdot \text{diag}(\tanh'(h_{t-1}))$$

The eigenvalues of this Jacobian determine gradient magnitude. If the spectral radius is less than 1, gradients vanish as $T$ grows.

### Effect on Learning

| Sequence length | Gradient magnitude | Learning |
|---|---|---|
| Short (≤10 steps) | Normal | Works fine |
| Medium (10–50 steps) | Diminished | Slow, unstable |
| Long (50+ steps) | Near zero | Early context effectively forgotten |

The network can still learn short-term patterns but cannot capture dependencies spanning many time steps.

### Exploding Gradients

The symmetric failure mode — exploding gradients — occurs when the spectral radius exceeds 1, causing gradients to grow exponentially. This leads to wildly unstable weight updates (NaN losses). The common fix is **gradient clipping**: cap gradient norms at a threshold before applying updates.

Vanishing gradients are harder to detect and fix because the network appears to train (loss decreases) but simply ignores distant context.

### Solutions

| Solution | How it helps |
|----------|--------------|
| [[lstm]] | Additive cell state update keeps gradient path short |
| GRU (Gated Recurrent Unit) | Simplified LSTM-like gating |
| [[residual-connection]] | Skip connections bypass layers, shortening gradient path |
| [[transformer]] / [[self-attention]] | Eliminates recurrence; attention provides direct gradient path from output to any input position |

The Transformer architecture sidesteps vanishing gradients entirely by replacing recurrence with self-attention, where every output position attends directly to every input position — no sequential gradient chain.

## Related Concepts

- [[recurrent-neural-network]] — Primary architecture affected by this problem
- [[lstm]] — Gated architecture designed specifically to solve it
- [[residual-connection]] — Architectural fix used in Transformers and deep CNNs
- [[transformer]] — Avoids the problem by eliminating recurrence
- [[self-attention]] — Direct position-to-position connections eliminate the sequential chain

## Sources

- "RNN and LSTM Simply Explained" (presentation) — raw/RNN and LSTM Basics.pptx

---

**Status**: New (from sync)
**Last Updated**: 2026-04-25
