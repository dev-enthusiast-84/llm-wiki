# In-Context Learning

**Sources:**  
- "Language Models are Few-Shot Learners" — Brown et al., OpenAI, 2020 (NeurIPS) — primary paper  
- "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021

## Summary

In-context learning (ICL) is a form of [[adaptation]] in which a [[foundation-model]] is steered toward a downstream task by providing a natural language prompt — with or without task examples — *without any parameter updates*. It is a key [[emergence|emergent]] capability of large language models, formally defined and first rigorously demonstrated in [[gpt-3]].

## Explanation

**How it works:**  
The model parameters remain frozen. The task specification, optional demonstrations, and the actual query are all concatenated into the input context window. The model generates the output by completing the sequence, leveraging patterns learned during pre-training.

**Formal taxonomy (Brown et al., 2020):**
- *Zero-shot (K=0):* task description only in natural language, no examples
- *One-shot (K=1):* one demonstration example prepended
- *Few-shot (K=10–100):* multiple demonstrations, limited by context window length (2048 tokens in GPT-3)

Demonstrations are formatted as input–output pairs directly in the context. The value of K is constrained by context window size, not by any algorithmic limit.

**Meta-learning framing:**  
Brown et al. frame GPT-3's ICL as a form of meta-learning. During pre-training, the model implicitly learns many tasks embedded in natural language text. At inference time ("outer loop"), it uses the demonstrated task format to identify and execute the intended task — analogous to RL² and MAML in meta-learning literature. Whether ICL represents true "learning from scratch" at inference time or pattern-matching to training distribution remains an open question.

**Why it is significant:**  
Prior [[adaptation]] approaches (fine-tuning, lightweight tuning) all require labeled data and gradient computation. In-context learning requires neither — it collapses task specification into natural language, making AI accessible without any ML expertise. GPT-3 performs passably on many tasks in zero/few-shot settings despite never being trained explicitly for them.

**GPT-3 results:**  
- TriviaQA: 71.2% few-shot (SOTA closed-book at publication)
- CoQA: 85.0 F1 few-shot (within 3 F1 of fine-tuned BERT)
- Weaker on ANLI (near chance), WIC — tasks requiring bidirectional comparison of two spans

**Scale dependence:**  
ICL is an [[emergence|emergent]] capability that only appears reliably at sufficient model scale. GPT-2 (1.5B parameters) showed only "barest glimpses"; GPT-3 (175B parameters) demonstrated it robustly across dozens of tasks. This makes studying ICL in academic-budget models difficult.

**Theoretical perspective (Xie et al., 2021):**  
Under infinite pre-training data, in-context learning can be understood as implicit Bayesian inference — the model infers a latent concept from the provided examples and uses it to predict the query. This requires the pre-training distribution to have coherent latent structure (e.g., documents that are topically consistent).

**Fragility:**  
ICL is highly sensitive to prompt formulation:
- Small rewordings of the task description cause large accuracy changes
- The order of few-shot examples matters
- A well-tuned prompt is estimated to be worth roughly 100 labeled training examples
- The space of possible prompts is intractable to search exhaustively

**Prompt tuning (soft prompts):**  
A related approach replaces discrete natural language tokens with continuous learned vectors (soft prompts) prepended to the input. Performance gap between soft prompts and full fine-tuning shrinks as model size increases (Lester et al., 2021).

## Contradictions with Prior Papers

- **vs. Devlin et al. (2019):** BERT requires fine-tuning (gradient updates on labeled data) for every downstream task. In-context learning entirely bypasses this, suggesting the gradient-update fine-tuning paradigm presented as universal in the BERT paper is not the only viable adaptation approach — and may be unnecessary for sufficiently large models.
- **vs. Vaswani et al. (2017):** The Transformer paper does not contemplate task adaptation via the input alone; it is purely a sequence transduction architecture fine-tuned for specific tasks. In-context learning represents a qualitatively different operating mode that was not anticipated.

## Related Concepts

- [[gpt-3]]
- [[adaptation]]
- [[foundation-model]]
- [[emergence]]
- [[scaling-laws]]
- [[pre-training-fine-tuning]]
- [[self-supervised-learning]]
- [[autoregressive-language-model]]
