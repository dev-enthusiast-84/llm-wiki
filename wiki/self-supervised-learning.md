# Self-Supervised Learning

A learning paradigm where training labels are automatically derived from the input data itself, requiring no human annotation.

## Summary

Self-supervised learning (SSL) generates supervision signals from the structure of the data — for example, by masking part of the input and predicting the missing part, or by predicting the next token given previous tokens. This enables training on virtually unlimited amounts of unlabeled data (web text, books, code), which is the key ingredient that makes large language models possible. It contrasts with supervised learning (human-labeled data) and is distinct from unsupervised learning (typically clustering or density estimation with no prediction task).

## Explanation

### Core Idea

Rather than requiring expensive human annotations, self-supervised learning defines pretext tasks where labels can be automatically extracted:

| Task | Input | Label |
|------|-------|-------|
| Masked Language Model | "The [MASK] sat on the mat" | "cat" |
| Next-token prediction | "The cat sat on the" | "mat" |
| Next sentence prediction | Sentence A, Sentence B | IsNext / NotNext |

These tasks force the model to learn deep representations of language structure and semantics as a byproduct of solving the prediction problem.

### Why SSL Enables Scale

The practical consequence of self-supervision is that training data is effectively unlimited:
- Wikipedia, Common Crawl, Books, GitHub — all usable without any labeling effort
- GPT-3 trained on ~300B tokens (Common Crawl, WebText2, Books, Wikipedia)
- This is orders of magnitude more than any labeled NLP dataset

Bommasani et al. (2022) note that self-supervised learning is one of two key enablers of foundation models (the other being scale); it shifts the source of supervision from human labels to data structure itself.

### Relationship to Unsupervised Learning

SSL is sometimes called "unsupervised" in older literature (e.g., BERT is described as "unsupervised pre-training"), but the term is technically imprecise:
- SSL **does** have a prediction target — it's just automatically constructed
- Unsupervised learning (clustering, PCA) has no prediction target
- "Self-supervised" is now the preferred precise term

### Vision and Other Modalities

SSL extends beyond NLP:
- **Images**: predict masked image patches (MAE, BEiT), contrastive self-prediction (DINO, SimCLR)
- **Audio**: predict masked spectrogram patches (wav2vec)
- Foundation models are increasingly multimodal, using SSL objectives across modalities simultaneously

## Related Concepts

- [[masked-language-model]] — A self-supervised objective used to pre-train BERT
- [[autoregressive-language-model]] — Another self-supervised objective (predict next token)
- [[pre-training-fine-tuning]] — SSL is used in the pre-training stage
- [[foundation-model]] — Built on self-supervised pre-training at scale
- [[bert]] — Pre-trained using MLM and NSP (both self-supervised)
- [[gpt-3]] — Pre-trained using autoregressive next-token prediction (self-supervised)

## Sources

- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1.1
- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers" (2018) — bert-overview.txt

---

**Status**: Complete
**Last Updated**: 2026-04-25
