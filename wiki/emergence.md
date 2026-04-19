# Emergence

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

Emergence describes capabilities that arise implicitly from scale and training dynamics rather than being explicitly designed or anticipated. It is one of two defining properties of [[foundation-model]]s (alongside [[homogenization]]). Emergent capabilities are the source of both scientific excitement and anxiety about unanticipated consequences.

## Explanation

**Definition:**  
A system exhibits emergence when its behavior is *implicitly induced* rather than *explicitly constructed*. In the context of foundation models, this means a model acquires capabilities that were neither specifically trained for nor anticipated to arise.

**Historical progression of emergence in AI:**

| Era           | What emerges                                      |
|---------------|--------------------------------------------------|
| Machine learning | How to perform a task (induced from examples)  |
| Deep learning | High-level features used for prediction          |
| Foundation models | Advanced functionalities (e.g., in-context learning, arithmetic, code generation) |

**Canonical example — GPT-3:**  
[[gpt-3]] (175B parameters) demonstrates [[in-context-learning]] — the ability to adapt to a new task given only a natural language prompt and a few examples. This capability was not present in GPT-2 (1.5B parameters), appeared only as "barest glimpses" in intermediate sizes, and was neither trained for nor anticipated by the model's designers.

**Other documented emergent capabilities:**
- Arithmetic (GPT-3 improves dramatically when commas are added to numbers in the input format)
- Translation between language pairs not seen during training
- Code generation and debugging
- Multi-step logical reasoning

**Why emergence creates risk:**  
Emergent capabilities interact with [[homogenization]] in a potentially unsettling way:
- Because capabilities arise implicitly, existing models are hard to fully characterize
- Unknown failure modes may be inherited by all adapted models
- Evaluation benchmarks cannot anticipate capabilities that have not yet been observed
- Forecasting emergent behaviors at deployment time remains an open research problem

**Emergent capabilities and scale:**  
[[scaling-laws]] predict quantitative improvement (accuracy) reliably, but emergent *qualitative* capabilities (e.g., in-context learning) appear discontinuously and require sufficient scale to even observe. This limits the usefulness of academic-scale experiments for studying emergent behavior.

## Contradictions with Prior Papers

- **vs. Vaswani et al. (2017):** The Transformer paper makes no mention of emergent properties; its framing is purely task-driven performance on translation benchmarks. Bommasani et al. argue that emergent capabilities are among the most important and least understood aspects of Transformer-based models at scale.
- **vs. Devlin et al. (2019):** BERT was specifically designed for each pre-training objective (MLM, NSP) with clearly anticipated downstream tasks (NLU benchmarks). The concept that scale might produce *unanticipated* capabilities is absent from the BERT paper. Bommasani et al. cite BERT as the beginning of the foundation model era precisely because such emergent generality began appearing at BERT's scale.

## Related Concepts

- [[foundation-model]]
- [[homogenization]]
- [[in-context-learning]]
- [[scaling-laws]]
- [[ai-safety-alignment]]
- [[self-supervised-learning]]
