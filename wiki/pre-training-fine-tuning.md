# Pre-training and Fine-tuning

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2019

## Summary

The pre-train/fine-tune paradigm first trains a large model on unlabeled text with self-supervised objectives, then adapts the entire model to downstream tasks with labeled data. [[bert]] is the canonical example of this approach applied to NLP with a bidirectional [[transformer]] encoder.

## Explanation

**Two-stage framework:**

**Stage 1 — Pre-training:**  
The model is trained on massive unlabeled corpora using task-agnostic objectives ([[masked-language-model]] + [[next-sentence-prediction]]). This is expensive but done once; the resulting weights encode broad linguistic knowledge.

**Stage 2 — Fine-tuning:**  
The pre-trained weights initialize a task-specific model. A minimal output layer is added (e.g., a single linear layer). All parameters are fine-tuned end-to-end on labeled task data.

Fine-tuning is cheap: all BERT results are replicable in ≤1 hour on a single Cloud TPU. Typical hyperparameters: batch size 16–32, learning rate 2e-5 to 5e-5, 2–4 epochs.

**Contrast with feature-based approach (ELMo):**  
ELMo extracts frozen contextual embeddings from a pre-trained model and uses them as features in a task-specific architecture. Fine-tuning (BERT's approach) updates all parameters jointly, which is empirically stronger — but feature-based extraction is useful when (a) the task requires architectures not expressible as a Transformer encoder, or (b) pre-computation of representations saves repeated inference cost.

Ablation (Table 7 — NER): Feature-based BERT (concatenating last 4 layers) reaches 96.1 dev F1, only 0.3 behind fine-tuning (96.4). Both beat prior SOTA.

**Task adaptation patterns:**

| Task type       | Input to BERT            | Prediction head              |
|-----------------|--------------------------|------------------------------|
| Classification  | [CLS] + single sentence  | Linear layer over [CLS]      |
| Sentence pairs  | [CLS] + A + [SEP] + B    | Linear layer over [CLS]      |
| Token labeling  | [CLS] + sequence         | Linear layer over each token |
| QA span         | [CLS] + Q + [SEP] + P    | Start + end vector dot products |

**Unified architecture advantage:**  
Because BERT uses [[self-attention]] to process concatenated pairs, it handles cross-sentence reasoning natively — no task-specific cross-attention module needed (unlike prior work such as BiDAF for QA).

## Contradictions / Tensions Across Papers

**From Bommasani et al. (2021):**
- **Full fine-tuning is not necessary:** Bommasani et al. demonstrate that lightweight adaptation methods updating ~1000× fewer parameters (adapters, prefix tuning, prompt tuning, LoRA) can achieve performance comparable to full fine-tuning, especially as model size increases. The BERT paper presents full fine-tuning as *the* adaptation approach; the FMs paper shows this is just one end of a broad spectrum.
- **Adaptation scope is broader than task specialization:** BERT's fine-tuning paradigm addresses only task specialization. Bommasani et al. define adaptation to also include temporal adaptation (world knowledge updates), domain adaptation, privacy constraints (machine unlearning), and bias correction — none of which are addressed by BERT's fine-tuning framework.
- **In-context learning bypasses fine-tuning entirely:** For sufficiently large models, [[in-context-learning]] achieves useful task performance with zero labeled examples and no gradient updates. This was not demonstrated in BERT-scale models but emerges in GPT-3 (175B), suggesting the fine-tuning paradigm may be unnecessary beyond a certain scale threshold.

See [[adaptation]] for a full taxonomy of adaptation methods.

**From Ouyang et al. (2022) — RLHF as a third paradigm:**  
[[rlhf]] ([[instructgpt]]) introduces a third form of post-pre-training fine-tuning: optimization against *human preference comparisons* via reinforcement learning, rather than cross-entropy on task-specific labeled data. This is a qualitatively different learning signal — it encodes what humans judge as helpful, honest, and harmless across a broad instruction distribution, not correctness on a specific NLU task. A 1.3B RLHF-tuned model is preferred over 175B GPT-3 in human evaluations, demonstrating that the *nature* of the fine-tuning signal can matter more than model scale.

## Contradictions with "Attention Is All You Need"

The Transformer paper does not use pre-training — it trains from scratch for each task (machine translation, constituency parsing). The pre-train/fine-tune paradigm is absent from that paper and represents a fundamentally different approach to transfer learning introduced and validated by BERT.

## Related Concepts

- [[bert]]
- [[masked-language-model]]
- [[next-sentence-prediction]]
- [[transformer]]
- [[self-attention]]
- [[glue]]
- [[cls-sep-tokens]]
- [[adaptation]]
- [[in-context-learning]]
- [[rlhf]]
- [[foundation-model]]
