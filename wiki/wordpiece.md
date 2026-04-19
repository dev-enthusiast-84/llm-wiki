# WordPiece Tokenization

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2019  
**Original paper:** Wu et al., "Google's Neural Machine Translation System", arXiv:1609.08144, 2016

## Summary

WordPiece is the subword tokenization algorithm used by [[bert]], closely related to but distinct from [[byte-pair-encoding]] (BPE) used by the original [[transformer]]. Both decompose rare words into known subword units, but they differ in how merges are chosen.

## Explanation

**WordPiece algorithm:**  
Like BPE, WordPiece starts from characters and iteratively merges symbol pairs. The key difference: BPE merges the *most frequent* pair, while WordPiece merges the pair that *maximizes the likelihood of the training data* under the language model — i.e., it picks the merge that best explains the corpus.

**BERT's vocabulary:**  
30,000 WordPiece tokens. Subword units that are continuations (not word-initial) are prefixed with `##` (e.g., `play##ing`).

**Usage in BERT:**  
The same 30,000-token vocabulary is used for both pre-training and fine-tuning, with no separate source/target vocabularies (BERT is encoder-only, unlike the [[transformer]] which has a shared source-target vocab for translation).

## Contradictions with "Attention Is All You Need"

| Property           | Transformer (BPE)                      | BERT (WordPiece)                        |
|--------------------|---------------------------------------|-----------------------------------------|
| Merge criterion    | Frequency of pair                     | Language model likelihood               |
| Vocabulary size    | ~37k (EN-DE), 32k (EN-FR)             | 30,000                                  |
| Shared vocab       | Yes (source + target)                 | N/A (encoder only)                      |
| Continuation mark  | None specified                        | `##` prefix                             |

Both serve the same purpose — handling rare/OOV words without pure character-level fallback — but BERT's choice of WordPiece over BPE is a design decision driven by following Google's NMT system rather than any demonstrated superiority in this context.

## Related Concepts

- [[bert]]
- [[byte-pair-encoding]]
- [[masked-language-model]]
- [[transformer]]
