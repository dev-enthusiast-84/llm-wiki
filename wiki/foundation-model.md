# Foundation Model

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

A foundation model is any model trained on broad data — generally using self-supervision at scale — that can be adapted to a wide range of downstream tasks. The term was coined to capture both the critical and unfinished character of these models. Examples: [[bert]], GPT-3, CLIP, DALL-E.

## Explanation

**Defining characteristics:**
- Trained on broad, diverse data (often the open web or large corpora)
- Self-supervised: no human-labeled data required for pre-training
- Adapted (not used directly) for downstream tasks via [[adaptation]]
- Exhibits [[emergence]]: capabilities arise implicitly from scale, not explicit design
- Drives [[homogenization]]: most downstream NLP/vision systems now derive from a handful of foundation models

**Why "foundation"?**
The name was deliberately chosen over alternatives ("pretrained model", "self-supervised model", "large language model") to convey:
1. These models serve as a *common basis* from which many task-specific models are built
2. The word "foundation" connotes the need for architectural stability, safety, and security
3. Their current character is *incomplete* — they are intermediary assets requiring [[adaptation]]

**Three ingredients that made foundation models possible:**
1. Hardware improvements (GPU throughput/memory ×10 in four years)
2. The [[transformer]] architecture enabling unprecedented parallelism
3. Availability of vast unlabeled training data for [[self-supervised-learning]]

**The foundation model ecosystem (5 stages):**
1. Data creation → 2. Data curation → 3. Training → 4. Adaptation → 5. Deployment

**The leverage-and-liability duality:**
- *Leverage:* improvements to the foundation model immediately benefit all downstream adapted models
- *Liability:* defects, biases, and failure modes in the foundation are inherited by all adapted derivatives

**Current examples (as of 2021):**
- Language: [[bert]], [[gpt-3]], RoBERTa, T5, BART
- Vision-language: CLIP, DALL-E
- Code: Codex (based on GPT-3)

## Contradictions with Prior Papers

- **vs. Vaswani et al. (2017):** The Transformer paper trains models from scratch for each task. Foundation models invert this: train once at massive scale, adapt cheaply many times. The Transformer paper's eval methodology (WMT translation benchmark) is a direct task-specific training paradigm that foundation models have largely superseded.
- **vs. Devlin et al. (2019):** BERT is characterized as one of the first foundation models and as "the beginning of the era of foundation models". However, the BERT paper frames the model purely as a pre-train/fine-tune improvement for NLP — it does not present or anticipate the broader paradigm shift across modalities, the [[homogenization]] risk, or the societal implications that Bommasani et al. document extensively.

## Related Concepts

- [[emergence]]
- [[homogenization]]
- [[self-supervised-learning]]
- [[adaptation]]
- [[in-context-learning]]
- [[scaling-laws]]
- [[transformer]]
- [[bert]]
- [[gpt-3]]
- [[pre-training-fine-tuning]]
