# Scaling Laws

Empirical relationships describing how language model performance improves as a power law with model size, dataset size, and compute.

## Summary

Scaling laws (Kaplan et al., 2020; Hoffmann et al., 2022) are empirical observations showing that language model validation loss follows smooth, predictable power-law relationships with the number of model parameters (N), amount of training data (D), and total compute (C). These laws allow practitioners to forecast performance of larger models and make principled decisions about how to allocate a compute budget. GPT-3's results confirmed that scaling laws continue for at least two additional orders of magnitude beyond prior work.

## Explanation

### The Basic Power Law

For a fixed compute budget, loss scales approximately as:

$$L \approx L_0 \cdot C^{-\alpha}$$

Where $C$ is compute in FLOP/s-days and $\alpha \approx 0.048$ (GPT-3 empirical). Figure 3.1 of the GPT-3 paper shows this relationship holding smoothly across 7 orders of magnitude of compute.

Separately, loss scales with model size and data:
$$L(N) \propto N^{-\alpha_N}, \quad L(D) \propto D^{-\alpha_D}$$

### Key Implication: How to Allocate Compute

Given a fixed compute budget $C = 6ND$ (approximate FLOPs for training), there is an optimal balance between N and D:
- **Kaplan et al. (2020)**: scale N more aggressively than D (led to GPT-3's 175B model trained on 300B tokens)
- **Hoffmann et al. (Chinchilla, 2022)**: for truly optimal compute-efficiency, scale N and D roughly equally (~20 tokens per parameter)

This revised understanding (Chinchilla scaling laws) suggests GPT-3 is significantly undertrained relative to its parameter count.

### What Scaling Laws Predict vs. Don't

**Predict well:**
- Validation cross-entropy loss as a function of N, D, C
- Downstream task performance on most benchmarks (especially when performance is a smooth function of loss)

**Don't predict well:**
- [[emergence|Emergent capabilities]]: specific skills that appear discontinuously with scale (arithmetic, chain-of-thought reasoning)
- Qualitative capability jumps (e.g., in-context learning ability)
- Out-of-distribution generalization

### Implications for Foundation Models

Scaling laws provide the theoretical justification for investing in very large models:
- Predictable returns on compute investment
- Larger models are more sample-efficient (more performance per training token)
- The scaling curve has not shown signs of flattening within the parameter ranges studied

Bommasani et al. (2022) note that scaling makes foundation models possible: the returns are sufficient to justify the enormous training costs, and the smooth scaling allows planned resource allocation.

## Related Concepts

- [[gpt-3]] — Confirmed scaling laws for 2+ additional orders of magnitude
- [[foundation-model]] — Scaling laws justify training large foundation models
- [[emergence]] — Contrasts with scaling laws: some capabilities jump discontinuously
- [[autoregressive-language-model]] — Loss metrics used to measure scaling laws assume this architecture
- [[pre-training-fine-tuning]] — Scaling laws primarily describe the pre-training phase
- [[small-language-model]] — Represents a deliberate departure from scale-maximizing; trades peak capability for deployability

## Contradictions

The two foundational scaling law papers disagree on how to allocate a fixed compute budget:

- **Kaplan et al. (2020)**: scale model size (N) more aggressively than data (D); led to GPT-3's 175B parameters trained on ~300B tokens
- **Hoffmann et al. / Chinchilla (2022)**: for optimal compute efficiency, scale N and D roughly equally (~20 tokens per parameter); GPT-3 is significantly undertrained relative to its parameter count

Context: both papers agree on the power-law relationship between loss and compute. The disagreement is about the optimal N/D ratio within that budget. The Chinchilla result has largely superseded Kaplan et al.'s recommendation in post-2022 model training practice.

## Sources

- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Sections 1, 3.1
- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1.3
- Hoffmann et al. — "Training Compute-Optimal Large Language Models" (Chinchilla, 2022)

---

**Status**: Complete
**Last Updated**: 2026-04-25
