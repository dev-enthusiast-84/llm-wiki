# Byte-Pair Encoding

A subword tokenization algorithm that iteratively merges the most frequent adjacent character pairs to build a vocabulary.

## Summary

Byte-Pair Encoding (BPE), originally a data compression algorithm adapted for NLP by Sennrich et al. (2016), builds a subword vocabulary by starting with individual characters and repeatedly merging the most frequently co-occurring adjacent pair. The resulting vocabulary balances coverage of common words (represented as single tokens) with the ability to decompose rare words into known subword pieces. BPE is used in GPT-3 and the original Transformer, while BERT uses the related [[wordpiece]] algorithm.

## Explanation

### Algorithm

1. Initialize vocabulary with all individual characters (and a special end-of-word symbol)
2. Count all adjacent symbol pairs in the training corpus
3. Merge the most frequent pair into a single new symbol
4. Repeat until the desired vocabulary size is reached

Example merges on "low", "lower", "newest", "widest":
```
Initial: l o w</w>, l o w e r</w>, n e w e s t</w>, w i d e s t</w>
Merge (e, s): l o w</w>, l o w e r</w>, n e w es t</w>, w i d es t</w>
Merge (es, t): l o w</w>, l o w e r</w>, n e w est</w>, w i d est</w>
...
```

### Differences from WordPiece

| Property | BPE | WordPiece |
|----------|-----|-----------|
| Merge criterion | Frequency | Likelihood improvement |
| Used in | GPT-3, original Transformer | BERT |
| End-of-word marker | `</w>` suffix | `##` prefix for continuations |

Both achieve similar goals; practical performance is similar.

### GPT-3's BPE

GPT-3 uses a byte-level BPE with a 50,257-token vocabulary (50,000 merges + 256 byte tokens + 1 special token). Operating at the byte level (rather than character level) guarantees that no sequence is out-of-vocabulary — any string of bytes can be tokenized.

### Role in the Transformer (2017)

The original Transformer trained on WMT English-German used BPE with ~37,000 tokens (shared source-target vocabulary), and English-French used a 32,000 word-piece vocabulary. Shared vocabularies allow the model to directly compare source and target subwords, which helps for closely related languages.

## Related Concepts

- [[wordpiece]] — Similar subword algorithm used in BERT; merges by likelihood instead of frequency
- [[transformer]] — Used BPE for its machine translation experiments
- [[gpt-3]] — Uses byte-level BPE with 50K vocabulary

## Sources

- Vaswani et al. — "Attention Is All You Need" (2017) — Section 5.1
- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Section 2.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
