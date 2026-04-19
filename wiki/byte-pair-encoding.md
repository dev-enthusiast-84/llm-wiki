# Byte-Pair Encoding (BPE)

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)  
**Original paper:** Sennrich et al., "Neural Machine Translation of Rare Words with Subword Units", arXiv:1508.07909, 2015

## Summary

Byte-Pair Encoding (BPE) is a subword tokenization algorithm used in the [[transformer]] to handle rare and out-of-vocabulary words by representing text as sequences of variable-length subword units.

## Explanation

BPE starts from a character vocabulary and iteratively merges the most frequent adjacent symbol pairs until reaching a target vocabulary size. This balances vocabulary coverage with sequence length:
- Common words become single tokens
- Rare words are split into known subword pieces
- No true OOV problem (worst case: character-level fallback)

**Usage in the Transformer paper:**

| Task  | Dataset       | Vocab size | Shared vocab? |
|-------|--------------|------------|---------------|
| EN→DE | WMT 2014     | ~37,000    | Yes (source+target) |
| EN→FR | WMT 2014     | 32,000 (word-piece) | Yes |

The EN→DE task uses BPE with a shared source-target vocabulary. The EN→FR task uses a similar approach called word-piece encoding (Wu et al., 2016) which optimizes the language model likelihood of the training data rather than merge frequency.

**Why shared vocabulary?** Sharing embeddings across source, target, and the pre-softmax projection matrix (as done in the Transformer) is possible only when source and target use the same vocabulary. The paper multiplies embedding weights by √d_model for stability.

## Related Concepts

- [[transformer]]
- [[bleu]]
- [[encoder-decoder]]
- [[gpt-3]]
- [[wordpiece]]
