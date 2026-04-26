# GLUE

The General Language Understanding Evaluation benchmark — a collection of NLP tasks used to measure a model's general language understanding.

## Summary

GLUE (Wang et al., 2018) is a multi-task benchmark comprising 9 diverse NLP tasks (sentiment analysis, textual entailment, coreference resolution, etc.) designed to evaluate a model's general language understanding. BERT achieved state-of-the-art results on all GLUE tasks upon release, demonstrating the power of pre-training + fine-tuning as a paradigm. SuperGLUE, a harder follow-up benchmark, was released after human performance was exceeded on GLUE.

## Explanation

### Composition

| Task | Type | Description |
|------|------|-------------|
| CoLA | Acceptability | Is the sentence grammatically acceptable? |
| SST-2 | Sentiment | Is movie review positive or negative? |
| MRPC | Paraphrase | Are two sentences paraphrases? |
| STS-B | Similarity | Rate semantic similarity of two sentences (1–5) |
| QQP | Paraphrase | Are two Quora questions equivalent? |
| MNLI | Entailment | Does premise entail/contradict/neutralize hypothesis? |
| QNLI | Entailment | Does sentence contain the answer to the question? |
| RTE | Entailment | 2-class textual entailment |
| WNLI | Coreference | Winograd schema coreference challenge |

A single aggregate GLUE score is computed as the average across tasks.

### BERT on GLUE

BERT's GLUE performance (Wang et al., 2018; Devlin et al., 2018):
- BERT-Large achieved 80.5 GLUE score, outperforming prior SOTA (OpenAI GPT) by 7 points
- BERT achieved human-level performance on most individual tasks
- Fine-tuning required only a classification head on the [CLS] token — no task-specific architecture

This validated the pre-training/fine-tuning paradigm as a general approach to NLP.

### SuperGLUE and Beyond

After BERT exceeded human performance on most GLUE tasks, SuperGLUE (Wang et al., 2019) was released with harder tasks including:
- Multi-sentence reasoning
- Coreference resolution
- Question answering with evidence selection

Benchmark leaderboards have continued to saturate as models grow, leading to more dynamic evaluation frameworks.

### Data Contamination Risk

Because GLUE is publicly available and widely cited, its examples appear throughout the internet. Large models trained on web-scraped data (GPT-3, foundation models) may have GLUE examples in their training data, making GLUE scores difficult to interpret as clean generalization measures (see [[data-contamination]]).

## Related Concepts

- [[bert]] — BERT achieved state-of-the-art on all 9 GLUE tasks
- [[pre-training-fine-tuning]] — GLUE benchmarks the fine-tuning stage of the paradigm
- [[cls-sep-tokens]] — BERT uses the [CLS] token representation for GLUE classification tasks
- [[data-contamination]] — GLUE examples may appear in large model training data
- [[foundation-model]] — Foundation models are often evaluated on GLUE/SuperGLUE

## Sources

- Devlin et al. — "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (2018) — via bert-overview.txt

---

**Status**: Complete
**Last Updated**: 2026-04-25
