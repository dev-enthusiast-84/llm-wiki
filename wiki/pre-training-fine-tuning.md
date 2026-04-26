# Pre-training and Fine-tuning

A two-stage transfer learning paradigm where a model is first trained broadly on unlabeled data, then adapted to specific tasks with labeled data.

## Summary

The pre-training/fine-tuning paradigm has become the dominant approach in modern NLP and foundation model research. In the pre-training phase, a large model trains on massive unlabeled corpora using self-supervised objectives (e.g., MLM, next-token prediction), learning general linguistic and world knowledge. In fine-tuning, this pre-trained model is adapted to a specific downstream task with a small labeled dataset, often with minimal architectural changes. This dramatically reduces the amount of task-specific data needed and achieves far better performance than training from scratch.

## Explanation

### Why Pre-training Works

Pre-trained models have already learned:
- Syntax and morphology (from word prediction)
- Semantic relationships (from context modeling)
- World knowledge (from training on broad corpora)
- General representations useful across many tasks

Fine-tuning then steers these representations toward the specific task distribution, requiring far fewer labeled examples than training from scratch.

### Fine-tuning Approaches for BERT

BERT fine-tunes end-to-end (all layers updated):

| Task Type | BERT Approach |
|-----------|--------------|
| Single-sentence classification | [CLS] → dense → softmax |
| Sentence-pair classification (NLI) | [CLS] → dense → softmax |
| Token labeling (NER) | Per-token → dense → softmax |
| Span extraction (SQuAD) | Start/end position classifiers |

Most fine-tuning runs for 2–4 epochs with learning rates of 2e-5 to 5e-5, completing in minutes to hours even on a single GPU.

### GPT-style: Pre-training as the Paradigm

GPT-3 pushed this further: rather than fine-tuning (which still requires labeled data), it showed that a sufficiently large pre-trained model can perform tasks via [[in-context-learning]] with no gradient updates at all. This suggested that pre-training, at sufficient scale, encodes enough task knowledge to enable zero- and few-shot performance.

### Historical Context

The foundation model era began around 2018 when BERT demonstrated that a single pre-trained model (rather than task-specific architectures) could achieve SOTA across many benchmarks. Bommasani et al. (2022) describe this as a sociological inflection point: after BERT, self-supervised pre-training + fine-tuning became the substrate of NLP rather than a subfield.

### Parameter-Efficient Fine-tuning (PEFT)

Full fine-tuning updates all model weights. For large models, this becomes expensive. PEFT methods update only a small subset of parameters:
- **LoRA** (Low-Rank Adaptation): adds low-rank decomposition matrices to key weight matrices
- **QLoRA**: LoRA with quantized base model weights
- **Adapters**: small bottleneck modules inserted between layers
- These enable fine-tuning large models with a fraction of the GPU memory and compute

## Related Concepts

- [[bert]] — Introduced the pre-training/fine-tuning paradigm at scale for NLP
- [[self-supervised-learning]] — The mechanism used in pre-training
- [[masked-language-model]] — BERT's pre-training objective
- [[in-context-learning]] — Alternative to fine-tuning for large models
- [[foundation-model]] — Pre-training/fine-tuning is what makes foundation models possible
- [[gpt-3]] — Showed that pre-training alone (without fine-tuning) can work via in-context learning
- [[rlhf]] — A post-pre-training alignment step that uses further fine-tuning

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers" (2018) — bert-overview.txt
- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Section 2
- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
