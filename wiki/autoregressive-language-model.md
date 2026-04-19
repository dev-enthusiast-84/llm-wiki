# Autoregressive Language Model

**Source:** "Language Models are Few-Shot Learners" — Brown et al., OpenAI, 2020 (NeurIPS)  
**Background:** Standard LM formulation predates this paper; GPT-3 is the primary example at scale.

## Summary

An autoregressive language model (ALM) assigns probability to a token sequence by factoring it left-to-right: P(x₁, ..., xₙ) = ∏ P(xₜ | x₁, ..., xₜ₋₁). Each token is predicted from all *preceding* tokens only, making the representation causal and unidirectional. GPT-3 (175B) is the largest and most capable autoregressive LM at publication.

## Explanation

**Objective:**  
Training maximizes the log-likelihood of each token in the corpus given its left context:

```
L = Σₜ log P(xₜ | x₁, ..., xₜ₋₁; θ)
```

Every token in the training sequence contributes a prediction signal, making training highly efficient per-pass compared to [[masked-language-model]], which only predicts ~15% of tokens.

**Implementation in the Transformer:**  
Autoregressive LMs use the *decoder* half of the [[transformer]] with causal (masked) [[self-attention]] — each position can only attend leftward. This is the same masked self-attention used in the [[transformer]] decoder for auto-regressive generation.

**Contrast with masked language modeling:**

| Property                  | Autoregressive LM (GPT-3)       | Masked LM ([[bert]])             |
|---------------------------|----------------------------------|----------------------------------|
| Directionality            | Left-to-right (causal)           | Bidirectional                    |
| % tokens predicted/pass   | 100%                             | ~15%                             |
| Can see future tokens?    | No                               | Yes (except masked positions)    |
| Primary use               | Generation, few-shot inference   | Classification, understanding    |
| Fine-tuning needed?       | No (ICL), though possible        | Yes (standard BERT paradigm)     |

**Why scale matters:**  
The GPT-3 paper shows that autoregressive LMs acquire [[in-context-learning]] as an [[emergence|emergent]] capability at scale. GPT-2 (1.5B) showed only weak few-shot performance; GPT-3 (175B) demonstrates robust zero/one/few-shot adaptation across diverse tasks. This is consistent with [[scaling-laws]]: capability improves smoothly as parameters and compute increase, but qualitative emergence (ICL) appears discontinuously.

**Limitation — unidirectionality:**  
Because each token only sees its left context, autoregressive models cannot directly compare two spans or look back. GPT-3's authors explicitly acknowledge this as a structural weakness for tasks requiring bidirectional comparison (NLI, WIC, RACE). Bidirectional models like [[bert]] handle these tasks better when fine-tuned. GPT-3 partially compensates with scale, but remains weaker on comparison-heavy benchmarks.

## Contradictions / Tensions Across Papers

- **vs. Devlin et al. (2019):** The BERT paper argues that purely autoregressive (left-to-right) language model pre-training is "fundamentally limited" for understanding tasks because it prevents bidirectional context. GPT-3 demonstrates that at 175B scale, autoregressive pre-training alone enables competitive NLU performance in few-shot settings, weakening (without fully refuting) BERT's claim.
- **vs. Bommasani et al. (2021):** The FMs paper lists both autoregressive models (GPT-3) and masked/discriminative models (BERT, ELECTRA) as instances of [[self-supervised-learning]], treating the unidirectional vs. bidirectional distinction as an architectural choice within a larger SSL taxonomy rather than a fundamental divide.

## Related Concepts

- [[gpt-3]]
- [[self-supervised-learning]]
- [[masked-language-model]]
- [[transformer]]
- [[self-attention]]
- [[in-context-learning]]
- [[scaling-laws]]
- [[byte-pair-encoding]]
- [[data-contamination]]
