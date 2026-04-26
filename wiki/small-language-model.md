# Small Language Model

A language model with ≤10B parameters, designed to run efficiently on consumer-grade hardware with low latency — suited for agentic AI pipelines.

## Summary

Small Language Models (SLMs) are language models typically under 10B parameters that fit on consumer devices (laptop GPUs, mobile hardware) and operate with millisecond latency. Belcak et al. (NVIDIA, 2025) argue that SLMs — not large frontier models — are the future of agentic AI: agents require fast, frequent, parallelizable inference calls, and the overhead of LLMs makes them impractical as agent orchestrators for most real-world deployments.

## Explanation

### Definition

No universal definition exists, but common thresholds:
- **SLM**: ≤10B parameters; fits on consumer GPUs (8–24 GB VRAM); latency <100ms per token on appropriate hardware
- **LLM**: >10B parameters; typically requires datacenter infrastructure; higher latency and cost

Examples of SLMs: Phi-3 (3.8B), Gemma 2 (2B/9B), Llama 3.2 (1B/3B), Mistral 7B.

### Why SLMs for Agentic AI

Belcak et al. (2025) identify four agentic AI requirements that favor SLMs over LLMs:

| Requirement | LLM | SLM |
|-------------|-----|-----|
| Low latency (fast tool calls) | ❌ high latency | ✅ millisecond range |
| Cost efficiency (many calls) | ❌ expensive per-call | ✅ low cost |
| On-device / private deployment | ❌ cloud-dependent | ✅ runs locally |
| Parallelizable agents | ❌ GPU bottleneck | ✅ many concurrent |

In agentic pipelines, a single user task may require dozens to hundreds of LM inference calls (tool selection, argument generation, result parsing, error recovery). LLM latency compounds across these steps; SLMs allow near-real-time agentic execution.

### LLM-to-SLM Conversion Algorithm

Belcak et al. propose a systematic process for converting a capable LLM into a task-specialized SLM:

1. **Task scoping**: define the agent's task set precisely; identify inputs, outputs, and required tool calls
2. **Data generation**: use the LLM to generate synthetic training data for the scoped tasks
3. **Distillation or fine-tuning**: train a small model on the generated data (knowledge distillation from the LLM, or SFT on the synthetic corpus)
4. **Specialization**: the resulting SLM is not general-purpose — it excels at the target task with high reliability
5. **Evaluation**: verify SLM performance matches LLM baseline on the task distribution

This is analogous to the [[pre-training-fine-tuning]] paradigm applied in reverse: start from a capable general model, produce specialized training data, train a small specialist.

### Trade-offs

SLMs are not appropriate for all applications:
- **General-purpose chat**: LLMs still outperform SLMs on open-ended reasoning and rare tasks
- **Research/ideation**: complex multi-step reasoning benefits from LLM depth
- **Data generation for SLM training**: still requires an LLM

Belcak et al.'s argument is specifically about *agentic deployment* — where the same narrow task is executed repeatedly at scale.

### Connection to Foundation Models

The SLM paradigm contrasts with the [[foundation-model]] approach (one large model, many tasks). SLMs represent a return to task-specialized models — but bootstrapped via LLMs rather than trained from scratch, and deployed as coordinated fleets rather than single monolithic systems.

## Related Concepts

- [[foundation-model]] — SLMs contrast with the "one model fits all" foundation model paradigm
- [[pre-training-fine-tuning]] — SLM creation leverages fine-tuning (and distillation) from a large base
- [[in-context-learning]] — LLMs use ICL for task adaptation; SLMs use fine-tuning for specialization
- [[scaling-laws]] — Scaling laws favor larger models; SLMs trade peak capability for deployability
- [[emergence]] — Emergent capabilities may require scale that SLMs cannot reach

## Sources

- Belcak et al. — "Small Language Models are the Future of Agentic AI" (NVIDIA, 2025) — raw/SLL.pdf

---

**Status**: Complete
**Last Updated**: 2026-04-25
