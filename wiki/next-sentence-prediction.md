# Next Sentence Prediction

A binary pre-training task where a model predicts whether two sentences appear consecutively in the original text.

## Summary

Next Sentence Prediction (NSP) is the second pre-training objective used in BERT, designed to help the model understand inter-sentence relationships useful for tasks like question answering and natural language inference. Given sentence pairs (A, B), the model predicts "IsNextSentence" or "NotNextSentence." Half the examples use genuine consecutive sentences; half use randomly sampled sentences. Later work found NSP to be largely unnecessary and RoBERTa removed it without performance degradation.

## Explanation

### Training Format

```
Sentence A: the man went to the store .
Sentence B: he bought a gallon of milk .
Label: IsNextSentence

Sentence A: the man went to the store .
Sentence B: penguins are flightless .
Label: NotNextSentence
```

The `[CLS]` token's final representation is used to predict the label. During pre-training, 50% of pairs use the true next sentence and 50% use a random sentence from the corpus.

### Intended Purpose

NSP was introduced to capture cross-sentence semantics that MLM alone cannot provide, since MLM operates on individual segments. BERT's authors believed NSP would improve downstream tasks like:
- Natural Language Inference (is sentence B entailed by A?)
- Question Answering (is passage A relevant to question B?)

### Controversy: Is NSP Necessary?

Later research significantly questioned the value of NSP:
- **RoBERTa** (Liu et al., 2019) showed that removing NSP and training with full-sentence inputs improved downstream performance
- NSP may be too easy (random sentences are trivially distinguishable by topic)
- Better cross-sentence tasks like Sentence Order Prediction (SOP, used in ALBERT) proved more effective

## Related Concepts

- [[bert]] — NSP is BERT's second pre-training objective, alongside MLM
- [[masked-language-model]] — BERT's primary pre-training objective
- [[cls-sep-tokens]] — The `[CLS]` and `[SEP]` tokens structure sentence pairs for NSP
- [[pre-training-fine-tuning]] — NSP is part of BERT's pre-training stage

## Contradictions

Different sources evaluate NSP differently:
- **BERT paper** (Devlin et al., 2019): NSP improves QA and NLI tasks by 3-5 points
- **RoBERTa** (Liu et al., 2019): removing NSP improves most benchmarks; suggests NSP hurts rather than helps by restricting to shorter sequences

Context: NSP as originally implemented (document-level next sentence) was likely too easy. More carefully designed sentence-relationship tasks (SOP, inter-sentence coherence) may provide the intended benefit.

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers" (2018) — bert-overview.txt

---

**Status**: Complete
**Last Updated**: 2026-04-25
