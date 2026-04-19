# Self-Supervised Learning (SSL)

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

Self-supervised learning (SSL) is a family of training methods in which supervision signals are derived automatically from unlabeled data — no human annotation required. SSL is the dominant pre-training paradigm for [[foundation-model]]s. The [[masked-language-model]] objective used by [[bert]] and the autoregressive language modeling objective used by GPT are both instances of SSL.

## Explanation

**Core idea:**  
The pre-training task is constructed by withholding or corrupting part of the input and training the model to predict or reconstruct it. The structure of the data itself provides the supervision signal.

**Key SSL objectives:**

| Objective                   | Method                  | Examples               |
|-----------------------------|-------------------------|------------------------|
| Masked prediction           | Mask tokens/patches, predict them | [[masked-language-model]] (BERT), MAE (images) |
| Autoregressive generation   | Predict next token      | GPT, GPT-2, GPT-3     |
| Span corruption/denoising   | Corrupt spans, reconstruct full sequence | T5 (span corruption), BART |
| Contrastive learning        | Pull similar examples together, push dissimilar apart | CLIP (text-image), SimCLR (vision) |
| Discriminative (replaced token) | Distinguish real from corrupted tokens | ELECTRA                |

**Efficiency comparison (from Bommasani et al.):**
- ELECTRA vs BERT: 4× more efficient (discriminative vs generative SSL on same data)
- Contrastive vs generative for CLIP: 12× more efficient

**Why SSL is central to foundation models:**  
SSL enables pre-training on essentially unlimited unlabeled data (the web, books, images, etc.), bypassing the bottleneck of human annotation. It forces the model to acquire broadly useful representations in order to solve the prediction task.

**Domain-general SSL (an open goal):**  
Current SSL objectives tend to be modality-specific (MLM for text, SimCLR for images). Bommasani et al. argue that a domain-general SSL objective applicable to any data type without modification is an important open research direction.

**Design trade-offs:**
- *Generative vs discriminative:* Autoregressive models (generative) enable prefix-based conditioning; masked/denoising models (discriminative in spirit) enable bidirectional context
- *Abstraction level:* Raw-byte modeling is intractable due to sequence length; tokenization (BPE, WordPiece, patch embeddings) provides efficiency but may lose information
- *Multimodal alignment:* Late-fusion (separate encoders, aligned via contrastive loss, e.g. CLIP) vs early-fusion (joint encoder, e.g. ViLBERT)

## Contradictions with Prior Papers

- **vs. Devlin et al. (2019):** BERT presents MLM as its central innovation, but Bommasani et al. contextualize it as one instance of a broader SSL family. They note ELECTRA (Clark et al., ICLR 2020 — a 2020 follow-up to BERT) achieves 4× the efficiency of BERT on the same pre-training data — implying that BERT's specific MLM objective is not optimal, just historically first.
- **vs. Vaswani et al. (2017):** The Transformer paper uses fully supervised training (labeled parallel corpora for translation). SSL as the dominant paradigm for pre-training Transformers is entirely absent from the paper, representing a fundamental shift in how the architecture is actually used in practice.
- **vs. Ouyang et al. (2022) — RLHF is not SSL:** [[rlhf]] introduces a *human-supervised* fine-tuning stage (human preference comparisons → [[reward-model]] → PPO). This is explicitly not self-supervised: it requires human annotation. RLHF is a post-pre-training alignment technique, applied on top of an SSL-pretrained model. The SSL framework (unsupervised pre-training on unlabeled data) describes pre-training only; RLHF demonstrates that the most impactful improvements to deployed model behavior require human feedback — something SSL alone cannot provide.

## Related Concepts

- [[masked-language-model]]
- [[autoregressive-language-model]]
- [[foundation-model]]
- [[pre-training-fine-tuning]]
- [[bert]]
- [[scaling-laws]]
- [[in-context-learning]]
- [[rlhf]]
