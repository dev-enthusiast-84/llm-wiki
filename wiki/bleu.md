# BLEU Score

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

BLEU (Bilingual Evaluation Understudy) is the standard automatic metric for evaluating machine translation quality, used in the [[transformer]] paper to benchmark results on WMT 2014 English-German and English-French tasks.

## Explanation

BLEU measures the overlap between a model's output and one or more reference translations, based on n-gram precision with a brevity penalty. Higher is better; human-level translation is roughly 50+ on standard benchmarks.

**Transformer results reported:**

| Model              | EN→DE | EN→FR |
|--------------------|-------|-------|
| Transformer (base) | 27.3  | 38.1  |
| Transformer (big)  | 28.4  | 41.8  |
| Previous SOTA      | 26.36 | 41.29 |

The big model established SOTA on EN→DE at time of publication (2017) by +2.0 BLEU over the previous best ensemble. These scores have since been surpassed by later models.

**Training details affecting BLEU:**
- [[byte-pair-encoding]] tokenization (shared source-target vocabulary)
- Beam search with beam size=4, length penalty α=0.6
- Checkpoint averaging (last 5 checkpoints for base, last 20 for big)
- Label smoothing (ε=0.1) — hurts perplexity but improves BLEU

**Note:** BLEU scores depend heavily on tokenization, vocabulary, and decoding hyperparameters. Scores in this paper use [[byte-pair-encoding]] and are not directly comparable to per-word perplexity metrics.

## Related Concepts

- [[transformer]]
- [[byte-pair-encoding]]
