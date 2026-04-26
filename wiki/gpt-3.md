# GPT-3

A 175-billion parameter autoregressive language model by OpenAI that demonstrated strong few-shot learning across diverse NLP tasks.

## Summary

GPT-3 (Brown et al., 2020) is the third generation of OpenAI's Generative Pre-trained Transformer. Trained on ~300 billion tokens of text data, it showed for the first time that a single pre-trained model — without any gradient updates or fine-tuning — can perform competitively with task-specific fine-tuned models across a wide range of NLP tasks, simply by conditioning on a few examples in the context window (few-shot prompting). This demonstrated that model scale and broad pre-training can substitute for task-specific supervision.

## Explanation

### Architecture

GPT-3 uses a decoder-only Transformer with modifications from GPT-2: alternating dense and locally banded sparse attention patterns. It was trained in 8 sizes ranging from 125M to 175B parameters:

| Model | Params | Layers | d_model | Heads |
|-------|--------|--------|---------|-------|
| GPT-3 Small | 125M | 12 | 768 | 12 |
| GPT-3 XL | 1.3B | 24 | 2048 | 24 |
| GPT-3 175B | 175B | 96 | 12288 | 96 |

Context window: 2048 tokens. All trained for 300B tokens.

### Training Data

| Dataset | Tokens | Weight |
|---------|--------|--------|
| Common Crawl (filtered) | 410B | 60% |
| WebText2 | 19B | 22% |
| Books1 + Books2 | 67B | 16% |
| Wikipedia | 3B | 3% |

Higher-quality datasets (Books, Wikipedia) are sampled more frequently than their size would suggest.

### Few-Shot Learning Protocol

GPT-3 is evaluated in three settings with no gradient updates:
- **Zero-shot**: Only a natural language description of the task
- **One-shot**: Description + 1 example (context, completion) pair
- **Few-shot**: Description + K examples (K typically 10–100, limited by context window)

For multiple-choice tasks, GPT-3 picks the completion with highest conditional log-probability. For open-ended tasks, it generates by sampling or beam search.

### Key Results

- **LAMBADA**: 86.4% accuracy few-shot (vs 68.0% SOTA at time)
- **TriviaQA**: 71.2% few-shot, matching fine-tuned SOTA in closed-book setting
- **Translation**: Few-shot outperforms prior unsupervised NMT by 5+ BLEU on Fr→En
- **SuperGLUE**: 71.8 few-shot, approaching fine-tuned BERT-Large (69.0) without any fine-tuning
- **News article generation**: humans distinguish GPT-3 articles from human articles only ~52% of the time

### Scaling Laws

GPT-3 provided key evidence for scaling laws: performance (measured by validation loss) follows a power-law $L = 2.57 \cdot C^{-0.048}$ as a function of compute $C$. Both zero-shot and few-shot performance improve smoothly and consistently with model size across all tasks studied.

### Limitations

- Still falls behind fine-tuned SOTA on many tasks (NLI, reading comprehension)
- Does not learn from in-context examples (no gradient updates); can't acquire new knowledge
- Data contamination risk from large training set overlapping test benchmarks
- Societal risks: bias, disinformation, misuse via text generation

## Related Concepts

- [[autoregressive-language-model]] — GPT-3's architecture and training objective
- [[in-context-learning]] — GPT-3's primary evaluation paradigm
- [[scaling-laws]] — GPT-3 demonstrated smooth power-law scaling
- [[pre-training-fine-tuning]] — GPT-3 relies on pre-training alone, not fine-tuning
- [[transformer]] — The underlying architecture
- [[byte-pair-encoding]] — GPT-3 uses byte-level BPE with 50K vocabulary
- [[foundation-model]] — GPT-3 exemplifies the foundation model paradigm
- [[rlhf]] — InstructGPT applied RLHF on top of GPT-3 for alignment
- [[data-contamination]] — A concern identified and analyzed in the GPT-3 paper

## Sources

- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Sections 1–3
- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1

---

**Status**: Complete
**Last Updated**: 2026-04-25
