# Masked Language Model (MLM)

**Source:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" — Devlin et al., 2019

## Summary

Masked Language Model (MLM) is the primary pre-training objective for [[bert]]. It randomly masks a fraction of input tokens and trains the model to predict them from context on both sides, enabling deep bidirectional [[self-attention]].

## Explanation

**Why MLM is necessary:**  
Standard left-to-right language models cannot be used to train a bidirectional model because bidirectional conditioning would let each word "see itself" in a multi-layered context, allowing the model to trivially predict the target. MLM breaks this circularity by masking the target tokens first.

**Procedure:**  
15% of [[wordpiece]] tokens are randomly selected for prediction. Of those selected tokens:
- 80% are replaced with a `[MASK]` token
- 10% are replaced with a random token from the vocabulary
- 10% are left unchanged

**Why the 80/10/10 split?**  
The `[MASK]` token never appears at fine-tuning time, creating a pre-training/fine-tuning mismatch. The 10% random replacement and 10% unchanged cases force the model to maintain a meaningful contextual representation for *every* token (not just masked ones), since it cannot know which tokens will be asked to predict. Random replacement accounts for only 1.5% of all tokens total, causing minimal harm to language understanding.

**Training signal:** Only 15% of tokens are predicted per batch (vs 100% for left-to-right LM). This means MLM requires more pre-training steps to converge, though it outperforms LTR in absolute accuracy almost immediately.

**Ablation (Table 8 in paper):**  
Using only `[MASK]` (100% masking) is problematic for feature-based approaches (NER). The mixed strategy is most robust across tasks.

**Relationship to Cloze task:** MLM is directly inspired by the Cloze task from psycholinguistics (Taylor, 1953), where subjects fill in blanks in a passage.

## Contradictions / Tensions Across Papers

**From Bommasani et al. (2021):**
- **MLM is not optimally efficient:** Bommasani et al. note that ELECTRA — a 2020 follow-up model (Clark et al., ICLR 2020; published ~1.5 years after BERT) that trains a discriminator to distinguish real tokens from replaced tokens — achieves **4× the training efficiency** of BERT's MLM on the same data. MLM predicts only 15% of tokens per batch; ELECTRA generates a supervision signal for every token. This directly challenges the BERT paper's framing of MLM as the natural, superior approach to bidirectional pre-training.
- **MLM as one instance of SSL:** Bommasani et al. position MLM within a broader taxonomy of [[self-supervised-learning]] objectives (autoregressive, span corruption, contrastive, discriminative). The BERT paper does not frame MLM this way; it treats it as a novel task-specific contribution rather than an instance of a general paradigm.

## Contradictions with "Attention Is All You Need"

The Transformer paper's decoder uses causal masking (preventing leftward information flow) as a design choice for generation. BERT's MLM pre-training shows this is suboptimal for *understanding* tasks: bidirectional context learned through MLM outperforms left-to-right models across every NLU benchmark tested.

## Related Concepts

- [[bert]]
- [[next-sentence-prediction]]
- [[pre-training-fine-tuning]]
- [[self-attention]]
- [[wordpiece]]
- [[self-supervised-learning]]
- [[foundation-model]]
