# InstructGPT

**Source:** "Training language models to follow instructions with human feedback" — Ouyang et al., OpenAI, 2022 (NeurIPS)

## Summary

InstructGPT is a family of language models produced by applying [[rlhf]] fine-tuning to [[gpt-3]]. Despite being up to 100× smaller than GPT-3 in parameter count, human evaluators prefer InstructGPT outputs 85% of the time over GPT-3. It is the direct predecessor to ChatGPT and represents the first large-scale demonstration that behavioral alignment via human feedback is practical, low-cost, and generalizable.

## Explanation

**Architecture:**  
Identical to [[gpt-3]] — same Transformer architecture, same tokenization, same context window. The only difference is the training procedure. Three sizes were trained: 1.3B, 6B, and 175B parameters.

**Training procedure:** See [[rlhf]] for full detail. Summary:
1. **SFT:** Fine-tune GPT-3 on labeler-written demonstrations (~13k prompts)
2. **RM training:** Train a 6B [[reward-model]] to predict human preferences from ranked comparison data (~33k prompts, K=4–9 responses per prompt)
3. **PPO-ptx:** Fine-tune the SFT model against the RM using PPO, with a KL penalty to prevent reward hacking, and a pretraining gradient mix to prevent alignment tax

**Key results:**

| Comparison | Result |
|-----------|--------|
| 175B InstructGPT vs. 175B GPT-3 | InstructGPT preferred 85 ± 3% of the time |
| 175B InstructGPT vs. few-shot 175B GPT-3 | InstructGPT preferred 71 ± 4% of the time |
| **1.3B InstructGPT vs. 175B GPT-3** | **1.3B preferred** (100× fewer params) |
| TruthfulQA (truthfulness) | InstructGPT ~2× more truthful than GPT-3 |
| Hallucination rate (closed-domain tasks) | 21% (InstructGPT) vs. 41% (GPT-3) |
| Toxicity (with respectful prompt) | ~25% fewer toxic outputs than GPT-3 |
| Bias (Winogender, CrowS-Pairs) | No improvement over GPT-3 |

**Behaviors improved over GPT-3:**
- Follows explicit constraints in instructions
- Attempts the correct instruction more reliably
- Produces less fabricated information ([[hallucination]]) on closed-domain tasks
- Responds appropriately in the context of a customer assistant
- Generalizes to non-English instructions and code Q&A (despite minimal supervised coverage in training)

**Remaining limitations:**
- Assumes false premises in instructions without questioning them
- Over-hedges on simple factual questions (erring too far toward epistemic humility)
- Degrades on multi-constraint instructions (e.g. "list 10 1930s French films")
- When explicitly prompted to be harmful, produces *more* toxic output than GPT-3 (complies with harmful instructions)
- Bias not reduced (Winogender, CrowS-Pairs show no improvement)
- Labeler preferences reflect a specific demographic (English-speaking US/SE Asia contractors), not universal human values

**Alignment tax:**  
Before applying PPO-ptx, RLHF fine-tuning caused performance regressions on SQuAD, DROP, HellaSwag, and WMT FR→EN translation. The PPO-ptx variant largely mitigates these regressions by mixing pretraining log-likelihood gradients into the PPO update. See [[rlhf]].

**Cost of alignment:**  
Training the 175B InstructGPT required 4.9 petaflop/s-days (SFT) + 60 petaflop/s-days (PPO-ptx), compared to 3,640 petaflop/s-days for pre-training GPT-3. Alignment fine-tuning costs <2% of pretraining compute.

## Contradictions / Tensions Across Papers

- **vs. Brown et al. (2020) — scale:** GPT-3's central thesis is that scale enables few-shot generalization. InstructGPT shows that 1.3B parameters, properly aligned, outperforms 175B parameters for instruction following — suggesting alignment is a more efficient lever than scale for user-facing tasks.
- **vs. Brown et al. (2020) — fine-tuning risk:** GPT-3 argues fine-tuning risks poor OOD generalization. RLHF fine-tuning on InstructGPT *improves* OOD generalization (non-English languages, code) despite never being explicitly supervised on these domains.
- **vs. Devlin et al. (2019) — task-specific fine-tuning:** BERT fine-tunes on task-specific labeled data. InstructGPT uses human preference comparisons across a broad instruction distribution — a qualitatively different and more general fine-tuning paradigm.
- **vs. Bommasani et al. (2021) — alignment timeline:** The FMs paper presents alignment as a major open challenge requiring future research. InstructGPT demonstrates a production-deployed alignment solution within one year of publication, showing the timeline is much shorter than anticipated.

## Related Concepts

- [[rlhf]]
- [[gpt-3]]
- [[reward-model]]
- [[adaptation]]
- [[hallucination]]
- [[ai-safety-alignment]]
- [[in-context-learning]]
- [[pre-training-fine-tuning]]
