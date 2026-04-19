# BERT

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., Google AI Language, 2019 (NAACL)

## Summary

BERT (Bidirectional Encoder Representations from Transformers) is a language representation model that pre-trains a deep bidirectional [[transformer]] encoder on unlabeled text, then fine-tunes the entire model for downstream NLP tasks. At publication (2019), it achieved state-of-the-art results on 11 NLP tasks with minimal task-specific architecture changes; these scores have since been surpassed.

## Explanation

BERT applies the [[pre-training-fine-tuning]] paradigm to NLP at scale. The core insight is that existing pre-training methods (OpenAI GPT, ELMo) are fundamentally limited by **unidirectionality** — each token can only see context to its left (or independently to its left and right). BERT enables truly deep bidirectional representations by using the [[masked-language-model]] objective.

**Model architecture:**  
BERT is the encoder half of the [[transformer]] — there is no decoder. It uses bidirectional [[self-attention]] throughout, meaning every token attends to all other tokens in both directions at every layer.

| Model       | Layers (L) | Hidden (H) | Heads (A) | Parameters |
|-------------|-----------|-----------|----------|-----------|
| BERT_BASE   | 12        | 768       | 12       | 110M      |
| BERT_LARGE  | 24        | 1024      | 16       | 340M      |

Note: feed-forward inner dimension is always 4×H (3072 for BASE, 4096 for LARGE).

**Input representation:**  
Every input token's embedding is the sum of three components:
1. Token embedding (30,000-token [[wordpiece]] vocabulary)
2. Segment embedding (sentence A vs sentence B)
3. Position embedding (learned, not sinusoidal)

Special tokens: [[cls-sep-tokens]]

**Pre-training objectives:**
1. [[masked-language-model]] (MLM) — enables bidirectionality
2. [[next-sentence-prediction]] (NSP) — captures sentence relationships

**Pre-training data:** BooksCorpus (800M words) + English Wikipedia (2,500M words). Document-level corpus is critical for learning long contiguous sequences.

**Pre-training compute:** BERT_BASE: 4 Cloud TPUs × 4 days. BERT_LARGE: 16 Cloud TPUs × 4 days.

**Results (at publication, 2019; since surpassed):**
- GLUE: 80.5 (BERT_LARGE), +7.7 points over prior SOTA
- SQuAD v1.1 Test F1: 93.2
- SQuAD v2.0 Test F1: 83.1 (+5.1 over prior SOTA)
- SWAG: 86.3%, outperforming ESIM+ELMo by 27.1%

**Fine-tuning:** Inexpensive — all results replicable in ≤1 hour on a single Cloud TPU. Task-specific architecture change is minimal: add a single output layer on top of the [CLS] token (classification tasks) or token representations (token-level tasks).

## Contradictions / Tensions with Bommasani et al. (2021)

- **BERT as "beginning of the era":** Bommasani et al. characterize BERT's introduction as the sociological inflection point marking the beginning of the foundation model era — the first time a single NLP model became a *substrate* for the entire field. This is a stronger claim than the BERT paper makes about itself.
- **Full fine-tuning challenged:** The BERT paper presents full parameter fine-tuning as the standard and efficient approach. Bommasani et al. demonstrate that lightweight adaptation (adapters, prompt tuning, prefix tuning) can match full fine-tuning performance using 1000× fewer parameters, especially at larger model scales. See [[adaptation]].
- **Anglocentric bias:** BERT is trained on English Wikipedia + BooksCorpus. Bommasani et al. (citing Zhou et al. 2021) note this produces an Anglocentric bias — BERT-based models perform significantly worse on non-English, low-resource languages and cross-cultural tasks. The BERT paper does not evaluate multilinguality or linguistic diversity.
- **MLM efficiency:** ELECTRA achieves 4× the training efficiency of BERT's MLM objective on the same data. See [[masked-language-model]].
- **NSP utility questioned:** Subsequent work (RoBERTa, 2019 — cited in Bommasani et al.) finds that NSP may hurt rather than help downstream performance, suggesting BERT's ablation results showing NSP benefit may be confounded with other training differences (batch size, data).
- **GLUE inadequacy:** BERT was evaluated primarily on GLUE. Bommasani et al. argue task-specific benchmarks like GLUE are inadequate for characterizing foundation models, which require intrinsic evaluation, meta-benchmarks, and evaluation of emergent capabilities not captured by static benchmark suites.

## Contradictions with "Attention Is All You Need"

- **Activation function:** [[transformer]] paper uses ReLU in [[feed-forward-network]]; BERT uses GELU (Hendrycks & Gimpel, 2016), following OpenAI GPT.
- **Positional encoding:** [[transformer]] paper recommends sinusoidal encodings and shows learned embeddings are equivalent; BERT uses learned positional embeddings exclusively, training them on sequences ≤512 tokens.
- **Self-attention directionality:** [[transformer]] decoder uses causal (left-to-right) [[self-attention]]; BERT's ablations show bidirectional attention is strictly superior for understanding tasks, contradicting the implicit assumption that causal attention is sufficient for representation learning.
- **Model scale:** The "big" [[transformer]] has ~213M params (encoder+decoder). BERT_BASE alone has 110M params (encoder only). BERT_LARGE has 340M — larger than any Transformer variant discussed in Vaswani et al.

## Related Concepts

- [[masked-language-model]]
- [[next-sentence-prediction]]
- [[pre-training-fine-tuning]]
- [[self-attention]]
- [[transformer]]
- [[wordpiece]]
- [[cls-sep-tokens]]
- [[glue]]
- [[feed-forward-network]]
- [[positional-encoding]]
- [[foundation-model]]
- [[adaptation]]
- [[self-supervised-learning]]
- [[homogenization]]
