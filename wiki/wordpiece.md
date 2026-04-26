# WordPiece

A subword tokenization algorithm that splits words into the most frequent subword units present in the vocabulary.

## Summary

WordPiece is the tokenization algorithm used in BERT. It builds a vocabulary of subword units by iteratively merging the pair of symbols that maximizes the likelihood of the training data. At inference time, words are greedily split into the longest subword segments found in the vocabulary. Subwords that are continuations of a word are prefixed with `##`. WordPiece allows the model to handle unseen or rare words by decomposing them into known subwords, balancing vocabulary size with coverage.

## Explanation

### Motivation

Pure word-level tokenization has two problems:
1. **Out-of-vocabulary (OOV)**: rare or unseen words get mapped to `[UNK]`, losing all information
2. **Vocabulary size**: covering all words requires enormous vocabularies

Character-level tokenization avoids OOV but creates very long sequences and loses morphological structure. WordPiece (and BPE) find a middle ground: common words are whole tokens; rare words are split into known subword pieces.

### Algorithm

1. Start with a character-level vocabulary
2. Iteratively merge the pair of symbols (characters or subwords) that maximizes the language model likelihood on training data
3. Stop when the target vocabulary size is reached

This differs from [[byte-pair-encoding]] (which maximizes merge frequency rather than likelihood).

### Output Format

BERT uses a 30,000-token WordPiece vocabulary. Word-initial subwords appear as-is; word-internal continuation subwords are prefixed with `##`:

```
Input:  john johanson's house
Output: john  johan  ##son  '  s  house
```

### Cased vs. Uncased Models

- **Uncased**: text is lowercased and accent markers stripped before WordPiece; simpler, usually better for most tasks
- **Cased**: preserves case and accents; needed for case-sensitive tasks like Named Entity Recognition

### Implications for Training Labels

For token-level tasks (e.g., NER), the input word boundaries and the WordPiece boundaries don't align 1:1. BERT uses the representation of the first subword of each word for classification, discarding representations of `##` continuation pieces.

## Related Concepts

- [[bert]] — Uses WordPiece with a 30K vocabulary
- [[byte-pair-encoding]] — A similar algorithm; BPE merges by frequency, WordPiece by likelihood
- [[cls-sep-tokens]] — Added after WordPiece tokenization
- [[transformer]] — Original Transformer (2017) used WordPiece for the EN-FR 32K shared vocabulary

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers" (2018) — bert-overview.txt

---

**Status**: Complete
**Last Updated**: 2026-04-25
