# Masked Language Model

A self-supervised pre-training objective where random tokens are masked and the model learns to predict them from context.

## Summary

Masked Language Modeling (MLM) is the primary pre-training objective used in BERT. Rather than predicting the next token (as in autoregressive language models), MLM randomly masks a fraction of input tokens and trains the model to reconstruct them using both left and right context. This enables fully bidirectional representations — every token's representation is influenced by all surrounding tokens — which is crucial for understanding tasks.

## Explanation

### Procedure

In BERT's implementation, 15% of all WordPiece tokens are selected for prediction. Of those selected tokens:
- **80%** are replaced with the special `[MASK]` token
- **10%** are replaced with a random vocabulary token
- **10%** are left unchanged

The model must predict the original token at all selected positions. The three-way split prevents the model from simply learning "if I see [MASK], output whatever" — the 10% random and 10% unchanged cases force the model to maintain a contextual representation of all tokens at all times.

### Why Not Just Mask?

Replacing all selected tokens with `[MASK]` creates a train-test mismatch: `[MASK]` never appears during fine-tuning. The mixed strategy (80/10/10) mitigates this by exposing the model to actual tokens in roughly 20% of the selected positions.

### Whole Word Masking

An improvement (released May 2019) always masks all tokens belonging to the same word at once. For example, if `##son` of `Johanson` is selected, all of `Johan ##son` is masked. This prevents the model from trivially reconstructing masked pieces from visible word fragments.

### Contrast with Autoregressive LM

| Property | MLM (BERT) | Autoregressive (GPT) |
|----------|-----------|---------------------|
| Context used | Bidirectional (full) | Unidirectional (left only) |
| Token dependence | All tokens simultaneously | Left-to-right only |
| Best for | Understanding, classification | Generation |
| Training signal | Subset of tokens (15%) | All tokens |

## Related Concepts

- [[bert]] — MLM is BERT's primary pre-training objective
- [[next-sentence-prediction]] — BERT's second pre-training objective
- [[self-supervised-learning]] — MLM is a form of self-supervised learning
- [[autoregressive-language-model]] — The contrasting generation paradigm
- [[wordpiece]] — Tokenization used before masking is applied

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers" (2018) — bert-overview.txt

---

**Status**: Complete
**Last Updated**: 2026-04-25
