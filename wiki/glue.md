# GLUE Benchmark

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2019  
**Original paper:** Wang et al., "GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding", EMNLP 2018

## Summary

GLUE (General Language Understanding Evaluation) is a benchmark of diverse NLU tasks used to evaluate [[bert]] and compare it against prior systems. BERT_LARGE achieved 80.5 on GLUE at publication (2019), a 7.7-point absolute improvement over the prior state of the art. Bommasani et al. (2021) argue that task-specific benchmarks like GLUE are inadequate for evaluating foundation models; scores on GLUE have been far surpassed by subsequent models.

## Explanation

**Tasks included:**

| Task   | Type                        | Training size | BERT_LARGE |
|--------|----------------------------|---------------|-----------|
| MNLI   | Entailment (3-class)        | 392k          | 86.7/85.9 |
| QQP    | Paraphrase detection        | 363k          | 72.1      |
| QNLI   | Question NLI                | 108k          | 92.7      |
| SST-2  | Sentiment (binary)          | 67k           | 94.9      |
| CoLA   | Linguistic acceptability    | 8.5k          | 60.5      |
| STS-B  | Semantic similarity         | 5.7k          | 86.5      |
| MRPC   | Paraphrase (news)           | 3.5k          | 89.3      |
| RTE    | Entailment (binary)         | 2.5k          | 70.1      |
| WNLI   | Winograd NLI                | 634           | excluded* |

*WNLI is excluded due to known dataset construction issues where every submitted system performs below the majority-class baseline.

**Fine-tuning setup for GLUE:**  
- Batch size: 32
- Fine-tune for 3 epochs
- Learning rate selected from {5e-5, 4e-5, 3e-5, 2e-5} on dev set
- For BERT_LARGE on small datasets: multiple random restarts, select best dev model

**Key finding (as of 2019):**  
BERT_LARGE outperforms OpenAI GPT (72.8) by 7.7 points despite near-identical architecture — the difference is bidirectionality ([[masked-language-model]]) and [[next-sentence-prediction]] pre-training. Both scores have since been surpassed by many models.

**Benchmark adequacy:**  
Bommasani et al. (2021) argue GLUE is insufficient for evaluating foundation models: it tests only in-distribution task performance, cannot capture emergent capabilities, and does not measure robustness, fairness, or efficiency. Meta-benchmarks (BIG-Bench, FLEX) and intrinsic evaluation are proposed as more suitable frameworks.

## Related Concepts

- [[bert]]
- [[pre-training-fine-tuning]]
- [[masked-language-model]]
- [[next-sentence-prediction]]
