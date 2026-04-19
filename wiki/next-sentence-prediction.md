# Next Sentence Prediction (NSP)

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2019

## Summary

Next Sentence Prediction (NSP) is the second pre-training objective in [[bert]], training the model to predict whether two sentences are consecutive in a document. It was designed to capture inter-sentence understanding not encoded by token-level [[masked-language-model]] training. **Note:** NSP's benefit is contested — RoBERTa (Liu et al., 2019) removed NSP and matched or exceeded BERT's performance, suggesting the gains shown in the BERT paper may be confounded with other training differences (see Contradictions section).

## Explanation

**Task construction:**  
For each pre-training example, two text segments A and B are sampled:
- 50% of the time: B is the actual next sentence following A in the corpus (label: `IsNext`)
- 50% of the time: B is a random sentence from the corpus (label: `NotNext`)

The prediction is made using the `[CLS]` token representation. The final model achieves 97–98% accuracy on NSP.

**Motivation:**  
Many NLP tasks require understanding relationships *between* sentences — question answering (QA), natural language inference (NLI), paraphrase detection. Standard language modeling objectives do not capture this. NSP provides a direct training signal for cross-sentence coherence.

**Ablation findings (Table 5):**  
Removing NSP significantly hurts:
- QNLI: 88.4 → 84.9
- SQuAD F1: 88.5 → 87.9
- MNLI-m: 84.4 → 83.9

The degradation is most pronounced on tasks that explicitly require cross-sentence reasoning.

**Limitation acknowledged:**  
The `[CLS]` vector is not a meaningful sentence representation *without fine-tuning*, since it was trained specifically for the NSP binary prediction task.

**Later research (not in this paper):**  
Subsequent work (RoBERTa, 2019) found that NSP may actually hurt performance and removed it — suggesting the benefit shown here may be partly confounded with BERT's larger batch size and more training data vs the baseline. This is an open question in the literature.

## Related Concepts

- [[bert]]
- [[masked-language-model]]
- [[pre-training-fine-tuning]]
- [[cls-sep-tokens]]
- [[glue]]
