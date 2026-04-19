# [CLS] and [SEP] Tokens

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2019

## Summary

`[CLS]` and `[SEP]` are special tokens in [[bert]]'s input format. `[CLS]` acts as an aggregate sequence representation for classification tasks; `[SEP]` delimits sentence boundaries in multi-sentence inputs.

## Explanation

**[CLS] — Classification token:**  
Every BERT input sequence begins with `[CLS]`. After processing through all [[transformer]] layers, the final hidden state corresponding to `[CLS]` (denoted C ∈ ℝ^H) serves as the aggregate sequence representation fed into task-specific output layers for classification.

Important caveat: C is **not a meaningful sentence representation without fine-tuning** — it was trained for the binary [[next-sentence-prediction]] task during pre-training and only becomes a useful general-purpose representation after fine-tuning on a downstream task.

**[SEP] — Separator token:**  
`[SEP]` separates sentence A from sentence B when two sentences are packed into a single input. Combined with segment embeddings (learned A/B embeddings added to each token), it allows BERT to distinguish which sentence a token belongs to.

**Segment embeddings:**  
Each token receives an additional learned embedding indicating whether it is in segment A or segment B. This is summed with the token embedding and [[positional-encoding]] to form the full input representation.

**Input representation formula:**

```
Input_i = TokenEmbedding_i + SegmentEmbedding_i + PositionEmbedding_i
```

**Contrast with the Transformer:**  
The original [[transformer]] does not use special classification or separator tokens — its encoder-decoder architecture does not need them. `[CLS]` and `[SEP]` are BERT-specific design choices required because BERT is encoder-only and must handle multi-sentence inputs in a single forward pass.

## Related Concepts

- [[bert]]
- [[next-sentence-prediction]]
- [[pre-training-fine-tuning]]
- [[positional-encoding]]
- [[transformer]]
