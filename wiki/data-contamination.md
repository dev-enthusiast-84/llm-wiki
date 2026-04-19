# Data Contamination

**Source:** "Language Models are Few-Shot Learners" — Brown et al., OpenAI, 2020 (NeurIPS)

## Summary

Data contamination is the presence of benchmark test set examples (or near-duplicates) in a model's training data. It is an inherent risk when training on large web-crawled corpora, since benchmark data is often publicly available online and may be indexed by Common Crawl. GPT-3 studied this systematically and found contamination to be present but to have minimal effect on most reported benchmarks.

## Explanation

**Why it occurs:**  
Web-crawled datasets like Common Crawl are drawn from broad swaths of the internet. Many NLP benchmarks (SuperGLUE, WinoGrande, QuAC, etc.) publish their data publicly. If benchmark examples appear in web documents that were crawled before the training data cutoff, the model may have seen test examples during pre-training.

**Why it matters:**  
Reported benchmark performance would be inflated — the model may recall or partially recall specific test instances rather than demonstrating genuine generalization. This makes cross-paper comparisons unreliable if contamination levels differ between models.

**GPT-3's methodology:**  
The authors detected contamination by searching for overlapping 13-gram sequences between each benchmark's test set and the training data. Benchmarks were classified into:
- **Clean:** no or minimal overlap detected
- **Contaminated:** meaningful overlap detected

**Findings:**  
- Contamination was found in a subset of benchmarks
- Performance on contaminated vs. clean benchmarks was compared
- In most cases, contamination had negligible effect on reported scores
- A few benchmarks showed modest contamination-driven inflation; the authors reported both contaminated and clean numbers

**Structural challenge:**  
At the scale of GPT-3's training data (300 billion tokens from web sources), perfectly isolating training from evaluation data is not practically feasible. This is an inherent limitation of web-scale pretraining — distinct from the controlled data splits used in smaller-scale supervised learning.

**Broader implication:**  
Data contamination is a general concern for any large-scale [[autoregressive-language-model]] or [[foundation-model]] trained on web data. It motivates:
- Temporal holdout datasets (benchmarks published after model training cutoff)
- Adversarial or procedurally generated evaluation sets
- Contamination auditing as standard practice in model evaluation

## Related Concepts

- [[gpt-3]]
- [[autoregressive-language-model]]
- [[foundation-model]]
- [[distribution-shift]]
