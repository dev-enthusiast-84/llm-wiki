# InstructGPT

A GPT-3 variant fine-tuned with RLHF to follow natural language instructions, preferred by human raters over GPT-3 despite having far fewer parameters.

## Summary

InstructGPT (Ouyang et al., 2022) demonstrated that applying RLHF to GPT-3 produces models that are substantially more helpful, less harmful, and more honest than the base model — and that a 1.3B InstructGPT model is preferred by human evaluators over a 175B GPT-3 model. This established alignment interventions as complementary to (not in conflict with) scaling: small aligned models can outperform large unaligned ones on user-facing tasks.

## Explanation

### Motivation

GPT-3, despite impressive few-shot performance, produces outputs that can be unhelpful, harmful, or misaligned with user intent. It will:
- Generate harmful content when prompted (jailbreaks)
- Produce verbose non-answers on ambiguous prompts
- Follow the surface form of a prompt rather than the user's intent

InstructGPT aimed to make models that do what users actually want, not just what the training data distribution dictates.

### Training Pipeline

InstructGPT applied the full 3-stage RLHF pipeline to GPT-3:

1. **SFT**: Human labelers wrote high-quality responses to ~13K prompts; GPT-3 was fine-tuned on these demonstrations
2. **RM**: Human labelers ranked 4–9 SFT responses per prompt; a reward model (1.3B params) was trained on ~33K comparison pairs
3. **PPO**: The SFT model was fine-tuned against the RM using PPO with a KL penalty (β ≈ 0.02)

InstructGPT released three model sizes: 1.3B, 6B, and 175B parameters.

### Key Results

| Comparison | Human Preference |
|-----------|-----------------|
| InstructGPT 1.3B vs GPT-3 175B | InstructGPT preferred 85% of the time |
| InstructGPT 175B vs GPT-3 175B | InstructGPT preferred 85% of the time |
| InstructGPT 175B vs FLAN/T0 (prompted) | InstructGPT preferred |

- InstructGPT produced fewer hallucinations on TruthfulQA
- Generated far fewer toxic outputs when prompted with harmful instructions
- "Alignment tax" was minimal: InstructGPT 175B matched or exceeded GPT-3 on most NLP benchmarks

### Design Decisions

- **Prompt distribution**: sampled from real OpenAI API usage, not synthetic benchmarks — this gives a realistic training distribution
- **Labeler training**: extensive guidelines and training for human labelers to ensure consistent quality judgments
- **Public SFT data**: ~13K demonstrations with explicit "helpful, harmless, honest" framing

### Limitations and Critiques

- Captures labeler preferences, not universal human values — labeler demographics introduce bias
- RLHF does not eliminate hallucination, only reduces it
- Still exhibits sycophancy — agreeing with users even when wrong
- Alignment may degrade on tasks not well-represented in the RLHF training distribution

## Related Concepts

- [[rlhf]] — The training methodology used to create InstructGPT
- [[reward-model]] — The RM is trained on human preference rankings of InstructGPT outputs
- [[gpt-3]] — The base model InstructGPT fine-tunes
- [[hallucination]] — InstructGPT reduces but does not eliminate hallucination
- [[ai-safety-alignment]] — InstructGPT is the flagship practical demonstration of LLM alignment

## Sources

- Ouyang et al. — "Training language models to follow instructions with human feedback" (2022) — via rlhf-overview.docx

---

**Status**: Complete
**Last Updated**: 2026-04-25
