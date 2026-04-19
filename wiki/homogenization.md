# Homogenization

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

Homogenization is the consolidation of methodologies and, increasingly, the actual models used across AI research and applications. It is one of two defining properties of [[foundation-model]]s (alongside [[emergence]]). Homogenization provides strong leverage — any improvement to the foundation model benefits all downstream applications simultaneously — but also creates systemic single points of failure.

## Explanation

**Historical progression of homogenization in AI:**

| Era             | What is homogenized                                |
|-----------------|----------------------------------------------------|
| Machine learning | Learning algorithms (e.g., logistic regression)  |
| Deep learning   | Model architectures (e.g., CNNs)                 |
| Foundation models | The model itself (e.g., BERT, GPT-3)           |

**Homogenization of models:**  
As of 2021, almost all state-of-the-art NLP models are adapted from a small number of foundation models (BERT, RoBERTa, T5, BART). The same [[transformer]]-based sequence modeling approach is applied across text, images, speech, tabular data, protein sequences, molecules, and reinforcement learning — suggesting convergence toward a unified paradigm across research communities.

**The leverage-liability duality:**
- *Leverage:* improvements to a foundation model propagate immediately to all downstream adapted models
- *Liability:* defects of the foundation model (biases, failure modes, security vulnerabilities) are blindly inherited by all adapted derivatives

**Interaction with [[emergence]]:**  
Homogenization is particularly risky when combined with emergence: since emergent capabilities and failures are not fully predictable, aggressively homogenizing around a model whose behavior is not fully characterized is a high-stakes bet.

**Concentration effects:**  
Foundation model training is accessible only to large organizations (Google, Microsoft, Meta, OpenAI, Anthropic). This creates:
- A barrier-to-entry that is rising, not falling
- A concentration of power over the models that underlie most AI systems
- Limited academic ability to study or improve foundation models at their actual scale of operation

**Homogenization across research communities:**  
Transformer-based approaches are now applied to: text (BERT, GPT), images (ViT), speech (wav2vec), tabular data, protein sequences (ESM), molecules, and reinforcement learning (Decision Transformer). Multimodal models (CLIP, DALL-E) further blur the boundaries.

## Contradictions with Prior Papers

- **vs. Devlin et al. (2019):** The BERT paper presents fine-tuning as uniformly beneficial ("reduce the need for many heavily-engineered task-specific architectures"). Bommasani et al. argue this homogenization effect is simultaneously a strength *and* a liability — biases and failures in BERT propagate to all BERT-derived systems, a concern the BERT paper does not address.
- **vs. Vaswani et al. (2017):** The Transformer paper does not discuss the societal implications of architectural homogenization. Bommasani et al. argue the [[transformer]]'s dominance is itself a form of homogenization that centralizes both the capabilities and the risks of AI systems.

## Related Concepts

- [[foundation-model]]
- [[emergence]]
- [[scaling-laws]]
- [[adaptation]]
- [[bert]]
- [[transformer]]
