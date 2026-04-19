# Scaling Laws

**Source:** "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021  
**Original paper:** Kaplan et al., "Scaling Laws for Neural Language Models", arXiv:2001.08361, 2020

## Summary

Scaling laws describe the empirical observation that [[foundation-model]] capabilities improve predictably and reliably as model size, dataset size, and compute increase — following smooth power-law relationships. This regularity makes training large models strategically predictable, but does not capture [[emergence|emergent]] capabilities that appear discontinuously at scale.

## Explanation

**The core observation (Kaplan et al., 2020):**  
For language models, test loss scales as a power law with:
- Model size (number of parameters)
- Dataset size (number of tokens)
- Compute budget (FLOPs)

Each dimension contributes independently, and there is an optimal allocation of compute between model size and data given a fixed budget.

**Implication for research strategy:**  
The surprisingly smooth regularity predicted by scaling laws means that smaller models, within academic compute budgets, can be used to predict the behavior of larger models — at least for quantitative improvements (e.g., accuracy on a benchmark). This makes scaling law experiments a practical tool for model selection without training at full scale.

**Limitation — emergent capabilities:**  
Scaling laws capture *quantitative* improvements (loss goes down, accuracy goes up). They do not capture *qualitative* phase transitions — [[emergence|emergent]] capabilities like [[in-context-learning]] that appear discontinuously only above a threshold model size. For these, small-scale experiments cannot predict when or whether a capability will appear.

**Hardware-model growth mismatch:**  
GPU throughput and memory have increased approximately 10× over four years, while model/compute growth has been 10× annually. Foundation model training therefore increasingly exceeds what can fit on a single device, requiring distributed training systems.

**GPT-3 as direct application (Brown et al., 2020):**  
GPT-3 trained 8 model sizes from 125M to 175B parameters, all on 300 billion tokens. The performance curve across these sizes shows roughly smooth power-law improvement on language modeling loss — the Related Work section notes "relatively smooth increases in many (though not all) downstream tasks across 3 orders of magnitude of scaling." Some tasks show discontinuous improvement (see [[emergence]]).

**Compute requirements (as of 2021):**  
GPT-3 training required several thousand petaFLOP/s-days (vs. tens of petaFLOP/s-days for GPT-2 at 1.5B), far exceeding single-GPU capacity and motivating systems-level co-design (pipeline parallelism, tensor parallelism, data parallelism).

**Role in the foundation model paradigm:**  
Scaling laws provide the theoretical justification for investing in ever-larger foundation models: predictable capability gains with scale make the compute investment legible and plannable. They are a core reason why [[homogenization]] around a few large models has occurred — the returns to scale are reliable.

## Contradictions with Prior Papers

- **vs. Vaswani et al. (2017):** The Transformer paper explores a specific size range (base: 65M params, big: 213M encoder+decoder) and treats model scaling as a hyperparameter choice rather than a systematic research direction. Kaplan et al.'s scaling laws were published three years later and show that the Transformer paper explored only a small region of a much larger and predictable design space.
- **vs. Devlin et al. (2019):** BERT reports results for BASE (110M) and LARGE (340M) and notes "larger models lead to strict accuracy improvement" (Table 6). This observation is consistent with scaling laws but anecdotal. The systematic study of scaling relationships and their power-law nature postdates BERT.
- **vs. Ouyang et al. (2022) — alignment vs. scale:** Scaling laws predict that capability improves with parameter count. Ouyang et al. show that 1.3B [[instructgpt]] is preferred over 175B [[gpt-3]] in human evaluations — RLHF alignment fine-tuning can be more impactful than a 100× parameter increase for user-facing task performance. This is not a refutation of scaling laws (test-set loss still improves with scale) but demonstrates that human preference is not simply a function of scale.

## Related Concepts

- [[foundation-model]]
- [[emergence]]
- [[in-context-learning]]
- [[homogenization]]
- [[transformer]]
- [[gpt-3]]
- [[self-supervised-learning]]
