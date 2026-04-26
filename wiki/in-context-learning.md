# In-Context Learning

The ability of a language model to perform new tasks from a few examples provided in the prompt, without any parameter updates.

## Summary

In-context learning (ICL) allows a pre-trained language model to adapt to a new task by conditioning on a natural language description and/or a small number of input-output examples provided in the context window. No gradients are computed and no weights are updated — the model performs the task based purely on pattern recognition in the forward pass. GPT-3 demonstrated that this ability emerges strongly with scale: larger models are significantly better at using in-context examples. ICL is a form of meta-learning implicit in the pre-training objective.

## Explanation

### The Three Settings

As formalized in Brown et al. (2020):

| Setting | What the model sees |
|---------|---------------------|
| **Zero-shot** | Task description only (no examples) |
| **One-shot** | Task description + 1 (input, output) example |
| **Few-shot** | Task description + K examples (typically K=10–100) |

All settings require only forward passes — no fine-tuning. GPT-3's context window of 2048 tokens limits K in practice.

### Mechanism

During pre-training on massive text corpora, the model is exposed to many sequences that implicitly contain tasks embedded in context (e.g., dictionaries, Q&A pairs, translations). The model learns to recognize and continue these patterns. At inference time, providing examples in context activates the same pattern-matching ability.

Bommasani et al. (2022) describe this as an **emergent property**: GPT-2 (1.5B) shows modest ICL ability; GPT-3 (175B) shows dramatic improvement, suggesting ICL requires sufficient scale to fully emerge.

### Key Findings (GPT-3)

- Few-shot performance consistently improves with model size across all tasks
- The gap between zero-shot and few-shot performance grows with model capacity — larger models are more efficient "meta-learners"
- On some tasks (TriviaQA), GPT-3 few-shot matches fine-tuned SOTA without gradient updates
- On others (NLI, reading comprehension), ICL still falls significantly behind fine-tuning

### Distinction from Fine-tuning

| Property | In-Context Learning | Fine-tuning |
|----------|--------------------|-----------:|
| Gradient updates | None | Yes |
| Task-specific data needed | K examples (in context) | Thousands of labeled examples |
| Persists after inference | No | Yes (weights updated) |
| Generalizes to new examples | Via prompt only | Via updated weights |

### Implications for Scale

ICL is one of the strongest arguments for training very large models. A single GPT-3-scale model can be rapidly deployed to diverse tasks simply by writing prompts, without the engineering overhead of fine-tuning for each task. This matches the [[foundation-model]] paradigm of one model → many downstream tasks.

## Related Concepts

- [[gpt-3]] — Demonstrated ICL at scale as the primary evaluation framework
- [[foundation-model]] — ICL is a key emergent capability of foundation models
- [[emergence]] — ICL is a prime example of an emergent capability in LLMs
- [[pre-training-fine-tuning]] — ICL is an alternative to fine-tuning that requires no gradient updates
- [[scaling-laws]] — ICL performance scales predictably with model size
- [[autoregressive-language-model]] — The architecture that enables ICL via next-token prediction

## Sources

- Brown et al. — "Language Models are Few-Shot Learners" (2020) — Sections 1, 2
- Bommasani et al. — "On the Opportunities and Risks of Foundation Models" (2022) — Section 1.1

---

**Status**: Complete
**Last Updated**: 2026-04-25
