# Hallucination

**Source:** "Training language models to follow instructions with human feedback" — Ouyang et al., OpenAI, 2022 (NeurIPS); also implicitly present in Brown et al. (2020) and Bommasani et al. (2021)

## Summary

Hallucination is the generation of text that is factually incorrect or contains information not present in the input, produced with apparent confidence. It is a direct consequence of the next-token prediction objective: language models are trained to produce plausible continuations of text, not to assert only what is true. Ouyang et al. measure [[gpt-3]]'s hallucination rate at 41% on closed-domain tasks, and show that [[rlhf]] fine-tuning ([[instructgpt]]) reduces this to 21%.

## Explanation

**Two categories:**

1. **Closed-domain hallucination:** The model generates information that is not present in the input context, on tasks that require using only the provided input (summarization, closed-domain QA). Measured as a binary rate per response.

2. **Open-domain hallucination:** The model states factually false claims about the world. Measured via TruthfulQA (Lin et al., 2021) — a benchmark of 817 questions designed to elicit confident false answers from language models.

**Root cause:**  
The next-token prediction objective rewards a model for producing statistically likely text. If the training corpus contains false statements (internet text routinely does), the model can assign high probability to false continuations. The model has no mechanism to distinguish "what I believe is true" from "what I can predict." This is a fundamental misalignment between the training objective and truthful generation.

**Empirical measurements (Ouyang et al., 2022):**

| Metric | GPT-3 (175B) | InstructGPT (175B) |
|--------|-------------|-------------------|
| Closed-domain hallucination rate | 41% | 21% |
| TruthfulQA truthfulness | baseline | ~2× higher |
| TruthfulQA (with "I have no comment" option) | less likely to abstain | more likely to abstain than fabricate |

InstructGPT is able to say "I have no comment" when uncertain, rather than confidently fabricating an answer — a behavior elicited by RLHF fine-tuning without explicit task-specific training for abstention.

**Why RLHF reduces hallucination:**  
Human labelers penalize responses that appear to fabricate information. The [[reward-model]] learns to assign lower scores to hallucinated outputs, and [[rlhf]] fine-tuning optimizes against this. This is a form of indirect supervision: the training objective does not explicitly distinguish true from false, but human preferences do.

**Limitations of hallucination reduction:**  
- InstructGPT still hallucinates — 21% is a significant improvement over 41%, but not zero
- [[instructgpt]] will follow user instructions even to be misleading; when explicitly prompted to generate biased or false content, it does so more reliably than GPT-3
- TruthfulQA captures only questions that were adversarially selected to elicit falsehoods; real-world hallucination may differ
- The root cause (misalignment between LM objective and truthfulness) is not resolved; RLHF treats a symptom

**Connection to alignment:**  
Hallucination is one of three core misalignment failure modes identified in the HHH framework (Askell et al., 2021): models should be **honest** (not fabricate or mislead). Hallucination is the primary manifestation of dishonesty in current LMs, and measuring and reducing it is a central alignment goal.

## Contradictions / Tensions Across Papers

- **vs. Vaswani et al. (2017) and Devlin et al. (2019):** Neither the Transformer nor BERT papers discuss hallucination. Both assume models are evaluated on tasks with ground-truth labels, where hallucination cannot occur. Ouyang et al. identify hallucination as a first-class problem when LMs are deployed on open-ended generative tasks.
- **vs. Brown et al. (2020):** GPT-3 acknowledges that larger models may produce more confident incorrect text, but does not measure hallucination rates directly. Ouyang et al. provide the first systematic measurement (41% rate) on closed-domain tasks.
- **vs. Bommasani et al. (2021):** The FMs paper identifies hallucination as a risk from misaligned training objectives, but frames it as a future challenge. InstructGPT demonstrates that RLHF substantially reduces it in practice (41% → 21%), a much faster resolution than implied.

## Related Concepts

- [[rlhf]]
- [[instructgpt]]
- [[reward-model]]
- [[ai-safety-alignment]]
- [[gpt-3]]
- [[autoregressive-language-model]]
- [[distribution-shift]]
