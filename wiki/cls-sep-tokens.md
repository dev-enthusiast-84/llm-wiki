# CLS and SEP Tokens

Special tokens used in BERT's input format to mark the start of a sequence ([CLS]) and to separate or end segments ([SEP]).

## Summary

BERT introduces two special tokens as part of its input representation scheme. `[CLS]` (Classification) is prepended to every input sequence; its final hidden state serves as a pooled aggregate representation used for classification tasks. `[SEP]` (Separator) is appended after each sentence segment, marking boundaries in sentence-pair inputs and signaling end-of-sequence. These tokens are not linguistic in nature — they are structural artifacts of BERT's input format that the model learns to use during pre-training.

## Explanation

### Input Format

Single sentence:
```
[CLS] the man went to the store [SEP]
```

Sentence pair (for NSP, QA, NLI):
```
[CLS] question text [SEP] passage or hypothesis text [SEP]
```

BERT also uses a **segment embedding** (A or B) added to each token to distinguish the two sentences, on top of the token and positional embeddings.

### [CLS] Token

- Always at position 0
- Receives attention from all other tokens throughout all 12/24 encoder layers
- Its final representation is used as the aggregate sequence representation for classification tasks
- Trained to encode sequence-level semantics during NSP pre-training
- For token-level tasks (NER, SQuAD span extraction), [CLS] is typically ignored

### [SEP] Token

- Marks the end of each sentence segment
- In single-sentence inputs: appended at the end
- In sentence-pair inputs: inserted between the two sentences and at the very end
- Helps the model identify sentence boundaries when processing pairs

### Tokenization Order

The BERT tokenizer applies three steps:
1. Text normalization (whitespace, lowercase for uncased models)
2. Punctuation splitting
3. WordPiece tokenization
4. Special token insertion: `[CLS]` at start, `[SEP]` between/at end

### Maximum Sequence Length

BERT supports sequences up to 512 tokens (including special tokens). Longer sequences must be truncated or handled with sliding windows (as in SQuAD).

## Related Concepts

- [[bert]] — [CLS] and [SEP] are core to BERT's input format
- [[wordpiece]] — The tokenization used alongside these special tokens
- [[next-sentence-prediction]] — [CLS] is used for NSP prediction; [SEP] delineates sentence boundaries
- [[masked-language-model]] — [CLS] and [SEP] positions are never masked

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers" (2018) — bert-overview.txt

---

**Status**: Complete
**Last Updated**: 2026-04-25
