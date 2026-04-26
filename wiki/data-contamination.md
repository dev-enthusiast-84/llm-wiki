# Data Contamination

The overlap between a model's training data and benchmark test sets, which can inflate reported performance metrics.

## Summary

Data contamination occurs when test or development examples from evaluation benchmarks appear in a model's training corpus. Since models trained on internet-scale data (e.g., Common Crawl) may have ingested benchmark content from web sources, contaminated models can appear to "memorize" test answers rather than generalize. GPT-3 identified this as a systematic concern and introduced contamination analysis; it remains an open challenge in foundation model evaluation.

## Explanation

### Mechanism

Modern foundation models train on hundreds of billions of tokens scraped from the internet. Evaluation benchmarks (SQuAD, SuperGLUE, LAMBADA, etc.) are publicly available and their examples appear on the web — in blog posts, academic papers, leaderboard discussions, and GitHub repositories. If a test example appeared in the training data, the model may have memorized the answer rather than learning to solve the underlying task.

### GPT-3's Contamination Analysis

GPT-3 (Brown et al., 2020) performed 13-gram overlap analysis between training data and benchmarks:
- Several benchmarks showed significant contamination (e.g., Winogrande, QuAD)
- Results on contaminated benchmarks were marked with asterisks
- The paper excluded some datasets entirely or analyzed contamination impact separately
- Conclusion: contamination had minimal measurable impact on most tasks, but caused some results to be likely inflated

### Contamination vs. Memorization

- **Data contamination**: test examples appear verbatim or near-verbatim in training data
- **Memorization**: model stores specific training examples rather than learning generalizable patterns
- These are related but distinct: memorization can occur even without intentional test-set exposure

### Mitigation Strategies

1. **Deduplication**: remove near-duplicates from training data during preprocessing
2. **Post-hoc analysis**: n-gram overlap detection between training data and benchmarks
3. **Held-out benchmarks**: use benchmarks created after the training data cutoff
4. **Canary insertion**: embed secret strings in training data to detect memorization

### Broader Implications

As foundation models train on ever-larger fractions of the internet, contamination becomes harder to avoid and harder to measure. Bommasani et al. (2022) identify benchmark contamination as a significant evaluation challenge that requires reform of evaluation practices — moving toward benchmarks that cannot be easily contaminated (dynamic benchmarks, held-out test sets from private sources).

## Related Concepts

- [[gpt-3]] — First large-scale analysis of contamination at 175B scale
- [[foundation-model]] — Training on internet-scale data makes contamination systematic
- [[scaling-laws]] — Scaling increases contamination risk as training sets grow
- [[glue]] — A benchmark that may be contaminated in large model training

## Sources

- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Section 4
- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 4.4

---

**Status**: Complete
**Last Updated**: 2026-04-25
