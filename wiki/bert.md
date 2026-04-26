# BERT

Bidirectional Encoder Representations from Transformers — a pre-trained language model using a bidirectional Transformer encoder.

## Summary

BERT (Devlin et al., 2018) fundamentally changed NLP by showing that a single deeply bidirectional Transformer encoder, pre-trained on large text corpora using Masked Language Modeling and Next Sentence Prediction, could be fine-tuned with minimal task-specific modifications to achieve state-of-the-art results across a wide range of tasks. Unlike prior unidirectional models (GPT), BERT processes context from both left and right simultaneously at every layer.

## Explanation

### Architecture

BERT-Base: 12 layers, 768 hidden dim, 12 attention heads, 110M parameters
BERT-Large: 24 layers, 1024 hidden dim, 16 attention heads, 340M parameters

Uses [[wordpiece]] tokenization with a 30,000-token vocabulary. Special tokens: `[CLS]` at the start of every sequence (used for classification), `[SEP]` between sentence pairs and at the end.

### Pre-training Tasks

**1. Masked Language Model (MLM)**: 15% of tokens are randomly selected. Of those:
- 80% are replaced with `[MASK]`
- 10% are replaced with a random token
- 10% are kept unchanged

The model predicts the original tokens at masked positions. This enables **deeply bidirectional** context — the representation of each token depends on all other tokens, since masking prevents "seeing itself."

**2. Next Sentence Prediction (NSP)**: Given two sentences A and B, predict whether B is the actual next sentence following A (50%) or a random sentence (50%). This was intended to improve understanding of sentence relationships, though later work (RoBERTa) found NSP to be less important than originally thought.

### Fine-tuning

BERT is fine-tuned end-to-end for downstream tasks by adding a simple output layer:
- **Classification** (e.g., sentiment): use `[CLS]` token representation
- **Token labeling** (e.g., NER): use per-token representations
- **Span extraction** (e.g., SQuAD): add start/end position classifiers over tokens

Fine-tuning is fast: most results reproducible in 1 hour on a Cloud TPU.

### Results

At time of publication (2018), set new state-of-the-art on 11 NLP benchmarks:
- SQuAD v1.1: 93.2% F1 (ensemble)
- MultiNLI: 86.7%
- GLUE benchmark: significant improvements across all tasks

### Smaller BERT Models

Turc et al. (2020) released 24 compact BERT models (BERT-Tiny through BERT-Base) for resource-constrained environments, best used with knowledge distillation.

## Related Concepts

- [[transformer]] — BERT uses a Transformer encoder stack
- [[masked-language-model]] — Primary pre-training objective
- [[next-sentence-prediction]] — Secondary pre-training objective
- [[cls-sep-tokens]] — Special tokens in BERT's input format
- [[wordpiece]] — Tokenization scheme used
- [[pre-training-fine-tuning]] — BERT's two-stage training paradigm
- [[glue]] — Benchmark on which BERT achieved SOTA at release

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (2018/2019) — bert-overview.txt
- Turc et al. — "Well-Read Students Learn Better" (2019/2020)

---

**Status**: Complete
**Last Updated**: 2026-04-25
