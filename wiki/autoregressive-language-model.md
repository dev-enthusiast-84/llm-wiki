# Autoregressive Language Model

A language model that generates text by predicting one token at a time, left-to-right, conditioned on all previously generated tokens.

## Summary

Autoregressive language models (AR-LMs) define a probability distribution over sequences by factoring the joint probability as a product of conditional distributions: $p(x) = \prod_t p(x_t | x_{<t})$. At each step, the model predicts the next token given all previous tokens. This approach powers GPT-3, LLaMA, and most current large language models. It is the natural paradigm for text generation, though it provides only left-to-right (causal) context, in contrast to bidirectional models like BERT.

## Explanation

### Probability Factorization

$$p(x_1, \ldots, x_n) = \prod_{t=1}^{n} p(x_t \mid x_1, \ldots, x_{t-1})$$

Each factor is a categorical distribution over the vocabulary. The model is trained to minimize the negative log-likelihood (cross-entropy) over all tokens:

$$\mathcal{L} = -\sum_t \log p(x_t \mid x_{<t})$$

### Architecture: Decoder-Only Transformer

Modern AR-LMs use decoder-only Transformers with causal (masked) self-attention:
- Position $i$ can only attend to positions $\leq i$
- This is implemented by masking future positions to $-\infty$ before softmax
- All positions are processed in parallel during training; generation is sequential (one token at a time)

### Training Signal

Every token in the training sequence is a label: the model predicts token $t$ from tokens $1, \ldots, t-1$. This means 100% of tokens contribute training signal (vs. BERT's 15% masked tokens). With trillions of training tokens, this provides an enormous amount of supervision.

### Generation

At inference, tokens are generated autoregressively:
1. Start with a prompt
2. Predict next-token distribution
3. Sample (or argmax/beam search) a token
4. Append to context, repeat

Different decoding strategies (temperature sampling, top-k, top-p/nucleus, beam search) trade off diversity and coherence.

### Contrast with Masked Language Models

| Property | Autoregressive (GPT) | Masked (BERT) |
|----------|---------------------|---------------|
| Context direction | Left-to-right only | Bidirectional |
| Pre-training signal | All tokens | ~15% masked tokens |
| Best for | Generation | Understanding/classification |
| Can generate text? | Yes | No (not natively) |

## Related Concepts

- [[gpt-3]] — The largest and most studied autoregressive language model at time of publication
- [[transformer]] — Uses a decoder-only Transformer with causal masking
- [[masked-language-model]] — The contrasting approach used by BERT
- [[in-context-learning]] — Emerges from large-scale autoregressive pre-training
- [[scaling-laws]] — Loss follows a power law as function of model size and compute
- [[foundation-model]] — Most modern foundation models for generation are autoregressive

## Sources

- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Section 2.1
- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022)

---

**Status**: Complete
**Last Updated**: 2026-04-25
