# Adaptation

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

Adaptation is the process of conditioning a [[foundation-model]] to perform a specific downstream task. It encompasses a broad spectrum from full parameter fine-tuning to gradient-free prompting. Bommasani et al. define adaptation more expansively than the BERT-era fine-tuning paradigm — including temporal, domain, privacy, and bias-correction adaptations beyond task specialization.

## Explanation

**Two fundamental modes:**
1. **Input priming (in-context):** Model parameters are frozen; the task is specified through a natural language prompt or demonstrations concatenated to the input. No gradient updates needed. → [[in-context-learning]]
2. **Parameter updating:** Some or all model parameters are modified on labeled task data via gradient descent.

**Spectrum of parameter-updating methods (by compute cost):**

| Method                    | Parameters updated         | Typical param count   |
|---------------------------|----------------------------|-----------------------|
| Full fine-tuning          | All (θ)                    | 100M–340M (BERT scale)|
| Adapter modules           | New MLP layers inserted between frozen layers | ~1% of θ |
| Prefix / prompt tuning    | Continuous vectors prepended to each layer | ~0.1% of θ |
| Bias tuning               | Bias terms only            | ~0.1% of θ |
| Low-rank residuals (LoRA) | Low-rank matrices added to weight matrices | variable |
| Linear probing            | Final classification layer only | K × H params |

**Key finding (Bommasani et al.):**  
Lightweight adaptation updating ~1000× fewer parameters than full fine-tuning sometimes achieves **comparable performance**. As model size increases, the gap between soft prompts and full fine-tuning vanishes (Lester et al., 2021). This challenges the BERT paper's implicit assumption that full parameter fine-tuning is necessary.

**Three critical axes for choosing an adaptation method:**
1. Compute budget (training time, memory)
2. Task-specific labeled data availability
3. Gradient access (can you backpropagate through the model? API-only? Black-box?)

**Expanded scope of adaptation beyond task specialization:**
- **Temporal adaptation:** World knowledge changes over time; retrieval-augmented models (REALM, RAG, RETRO) update knowledge without full retraining by querying an external index
- **Domain specialization:** Balance general vs. specialized pre-training; sometimes domain-specific pre-training outperforms diverse pre-training (Cole et al. 2021, Chalkidis et al. 2020)
- **Constraint application:** Machine unlearning (GDPR right-to-be-forgotten), privacy preservation, bias mitigation
- **Local model editing:** Correcting specific input-output mappings without affecting global behavior

**Continual learning challenge:**  
Catastrophic forgetting remains unsolved: repeated adaptation to non-stationary data streams degrades earlier knowledge. Memory mechanisms and localized updates show promise but do not fully resolve the issue.

**RLHF as a distinct adaptation mode (Ouyang et al., 2022):**  
[[rlhf]] introduces a third fundamental adaptation paradigm, distinct from gradient descent on task labels (fine-tuning) and gradient-free prompting (ICL):
- Supervision signal: *human preference comparisons* (not task labels, not demonstrations alone)
- Process: SFT → reward model training → PPO optimization against reward model
- Key property: encodes broad behavioral alignment across many tasks simultaneously, not task-specific performance
- Key cost: aligns to the preferences of whoever provides the comparisons — not a universal alignment signal

## Contradictions with Prior Papers

- **vs. Devlin et al. (2019):** The BERT paper presents full fine-tuning as the standard adaptation approach and demonstrates it across 11 tasks. Bommasani et al. show this is the expensive end of a spectrum — lightweight methods using 1000× fewer parameters can achieve comparable results, especially at BERT_LARGE scale and beyond. BERT's claim that fine-tuning is "relatively inexpensive" is scale-dependent: it is expensive enough that it motivated the entire lightweight adaptation research agenda.
- **vs. Devlin et al. (2019) — from Brown et al. (2020):** GPT-3 explicitly argues that fine-tuning risks *poor out-of-distribution generalization*: "fine-tuned models can overfit to narrow task distributions, potentially failing on examples that differ slightly from training" [HLW+20, MPL19]. This is a stronger critique than Bommasani et al.'s efficiency argument — not just that fine-tuning is expensive, but that it may be epistemically harmful for robust generalization.
- **vs. Vaswani et al. (2017):** The Transformer paper treats adaptation as task-specific training from scratch (no pre-trained weights). The concept of adapting a pre-trained model is absent. In the foundation model paradigm, adaptation is the *primary* mode of deploying a model — training from scratch is essentially never done for downstream NLP tasks.

## Related Concepts

- [[in-context-learning]]
- [[rlhf]]
- [[pre-training-fine-tuning]]
- [[foundation-model]]
- [[self-supervised-learning]]
- [[bert]]
- [[scaling-laws]]
