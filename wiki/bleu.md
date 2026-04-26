# BLEU

Bilingual Evaluation Understudy — an automatic metric for evaluating machine translation quality by measuring n-gram overlap between generated and reference translations.

## Summary

BLEU (Papineni et al., 2002) is the standard automatic metric for machine translation, measuring the precision of n-grams (1–4) in a generated translation against one or more reference translations, with a brevity penalty to discourage overly short outputs. The Transformer (Vaswani et al., 2017) achieved BLEU scores of 28.4 on WMT 2014 English-to-German and 41.8 on English-to-French, surpassing prior state-of-the-art while requiring significantly less training time.

## Explanation

### Formula

BLEU is computed as:

```
BLEU = BP · exp(∑ wₙ · log pₙ)
```

Where:
- `pₙ` = modified n-gram precision for n-grams of length n (clipped by reference count)
- `wₙ` = uniform weight 1/N (typically N=4)
- `BP` = brevity penalty: exp(1 − r/c) if c < r, else 1 (penalizes short translations)
- `r` = reference length, `c` = candidate length

### Modified n-gram Precision

To prevent gaming by repeating common words, BLEU uses clipped counts: each n-gram's count in the candidate is clipped to its maximum count in any reference translation.

### Transformer Results on WMT 2014

| Translation Pair | Transformer (big) | Previous SOTA | Notes |
|-----------------|-------------------|---------------|-------|
| EN→DE | **28.4** | 26.4 (ensemble) | +2.0 BLEU |
| EN→FR | **41.8** | 41.1 (ensemble) | New SOTA |

The Transformer big model trained for 3.5 days on 8 P100 GPUs. Prior SOTA required 6× more training compute (Sliced RNNs, ConvSeq2Seq).

### Limitations

BLEU has well-known limitations:
- **Adequacy vs. fluency**: a BLEU-high translation can be grammatically correct but miss the meaning; a human-preferred translation may score lower
- **Reference dependency**: quality depends heavily on the number and quality of reference translations
- **No semantic understanding**: BLEU treats all word substitutions as equally wrong, even near-synonyms
- **Language dependency**: works better for morphologically simple languages; poor for agglutinative languages

Despite these limitations, BLEU remains the de facto standard because it is fast, reproducible, and correlates reasonably well with human judgment at the system level.

### Modern Alternatives

| Metric | Mechanism |
|--------|-----------|
| chrF | Character n-gram F-score; better for morphologically rich languages |
| BERTScore | Contextual embedding similarity using BERT |
| COMET | Neural MT quality estimation model |
| BLEURT | Fine-tuned BERT for translation quality |

## Related Concepts

- [[transformer]] — The Transformer paper used BLEU as its primary evaluation metric
- [[encoder-decoder]] — Machine translation is typically an encoder-decoder task
- [[pre-training-fine-tuning]] — Fine-tuning for MT tasks is measured by BLEU

## Sources

- Papineni et al. — "BLEU: a Method for Automatic Evaluation of Machine Translation" (2002) — original metric definition
- Vaswani et al. — "Attention Is All You Need" (2017) — Table 2, Section 6

---

**Status**: Complete
**Last Updated**: 2026-04-25
