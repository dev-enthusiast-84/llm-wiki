# LLM Wiki Index

A structured knowledge base of concepts in large language models, agentic AI, and related systems.

---

## Core Architecture

- [[transformer]] — Full encoder-decoder architecture from Vaswani et al. (2017)
- [[self-attention]] — Q/K/V mechanism; relates all token positions in O(n²·d)
- [[scaled-dot-product-attention]] — Attention(Q,K,V) = softmax(QK^T/√d_k)V
- [[multi-head-attention]] — h parallel attention heads concatenated and projected
- [[positional-encoding]] — Sinusoidal or learned position signals injected into embeddings
- [[encoder-decoder]] — Encoder-only, decoder-only, and full encoder-decoder architectures
- [[feed-forward-network]] — Position-wise FFN with 4× hidden expansion in each Transformer block
- [[residual-connection]] — Skip connections with layer normalization: LayerNorm(x + Sublayer(x))
- [[layer-normalization]] — Per-example feature normalization with learned scale and shift

---

## BERT and Tokenization

- [[bert]] — Bidirectional encoder pre-trained with MLM + NSP; BERT-Base (110M), BERT-Large (340M)
- [[masked-language-model]] — Predict randomly masked tokens; 80/10/10 masking strategy
- [[next-sentence-prediction]] — Binary IsNext/NotNext task; shown to be unhelpful by RoBERTa
- [[cls-sep-tokens]] — [CLS] for classification output; [SEP] as segment boundary marker
- [[wordpiece]] — Subword tokenization by likelihood-maximizing merges; 30K vocabulary
- [[byte-pair-encoding]] — Subword tokenization by frequency-maximizing merges; used in GPT-3

---

## Learning Paradigms

- [[pre-training-fine-tuning]] — Two-stage transfer learning: broad pre-training, then task-specific fine-tuning
- [[self-supervised-learning]] — Labels derived from data structure; enables training on unlabeled corpora
- [[autoregressive-language-model]] — p(x) = ∏ p(x_t | x_{<t}); causal masking; 100% training signal
- [[in-context-learning]] — Zero/one/few-shot task adaptation via prompting, no gradient updates

---

## GPT-3 and Scaling

- [[gpt-3]] — 175B parameter decoder-only Transformer; 300B training tokens; 8 model sizes
- [[scaling-laws]] — L ≈ L₀ · C^(−0.048); power-law relationship with compute, parameters, data

---

## Foundation Models

- [[foundation-model]] — Trained on broad data at scale via SSL; adapted to many downstream tasks
- [[emergence]] — Capabilities implicitly induced by scale, not explicitly programmed
- [[homogenization]] — Consolidation around few models; leverage with shared failure modes

---

## Alignment and Safety

- [[rlhf]] — 3-stage pipeline: SFT → Reward Model → PPO with KL penalty
- [[reward-model]] — Trained on human preference rankings; outputs scalar quality score
- [[instructgpt]] — RLHF-trained GPT-3; 1.3B InstructGPT preferred over 175B GPT-3
- [[ai-safety-alignment]] — Ensuring model behaviors match human values and intentions
- [[hallucination]] — Fluent but factually incorrect or fabricated model outputs
- [[distribution-shift]] — Mismatch between training and deployment data distributions

---

## Evaluation and Benchmarks

- [[glue]] — 9-task NLP benchmark; BERT achieved SOTA on all tasks
- [[bleu]] — N-gram overlap metric for machine translation; Transformer: 28.4 EN-DE, 41.8 EN-FR
- [[data-contamination]] — Benchmark test examples appearing in training data, inflating scores

---

## Pre-Transformer Architectures

- [[recurrent-neural-network]] — Sequential network with hidden state; predecessor to the Transformer for NLP
- [[lstm]] — Gated RNN variant with cell state; solves the vanishing gradient problem
- [[vanishing-gradient]] — Gradient shrinkage over long sequences; core failure mode of vanilla RNNs

---

## Agentic AI

- [[small-language-model]] — ≤10B parameters; fast inference; suited for agentic pipelines

---

*Last updated: 2026-04-25 — 37 entities across 9 categories*
