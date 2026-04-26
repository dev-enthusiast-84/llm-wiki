# Reward Model

A neural network trained on human preference rankings that outputs a scalar quality score for a given (prompt, response) pair.

## Summary

The reward model (RM) is an intermediate model in the RLHF pipeline. It is trained to predict which of two model outputs a human would prefer, then used as a differentiable proxy for human judgment during reinforcement learning. The RM turns expensive human feedback into a dense reward signal the PPO optimizer can use at scale. Because the RM is an imperfect approximation of human preferences, reward hacking — where the LM exploits RM weaknesses — is a central challenge.

## Explanation

### Architecture

- Initialized from the supervised fine-tuning (SFT) model checkpoint
- The language model head (vocab projection) is replaced with a linear layer projecting to a scalar
- Takes the full (prompt + response) as input; outputs a single real number representing quality

### Training Objective

Given pairs of responses `y_w` (preferred) and `y_l` (rejected) to the same prompt `x`, the RM is trained to maximize:

```
log σ(r(x, y_w) − r(x, y_l))
```

This is the Bradley-Terry pairwise ranking loss: the RM is trained to assign higher scores to preferred responses. The RM does not need absolute ratings — relative preferences are sufficient.

### Data Collection

1. Sample a prompt from the dataset
2. Generate k responses from the SFT model (k typically 4–9 in InstructGPT)
3. Human labelers rank the k responses
4. Extract all C(k,2) pairwise comparisons as training signal

### Reward Hacking

When the LM is trained against the RM via PPO, it may discover responses that exploit RM weaknesses:
- Very long responses that pattern-match to "thorough" even if content is poor
- Flattery or sycophantic language that raters happen to prefer
- Surface-level coherence masking factual errors

The KL divergence penalty in RLHF (see [[rlhf]]) partially mitigates this by penalizing large deviations from the SFT model.

### RM Limitations

- RM captures labeler preferences, which may not reflect true human values
- Rater disagreement introduces noise; inter-annotator agreement is typically moderate
- RM generalizes imperfectly to prompts outside the training distribution
- Reward overoptimization: as PPO trains longer, LM performance against RM increases but true human preference peaks and then declines

## Related Concepts

- [[rlhf]] — The reward model is stage 2 of the 3-stage RLHF pipeline
- [[instructgpt]] — InstructGPT used an RM trained on GPT-3 outputs ranked by human labelers
- [[ai-safety-alignment]] — RM imperfections are a key alignment challenge (misspecified objectives)
- [[hallucination]] — RM may inadvertently reward confident-sounding but false outputs

## Sources

- Ouyang et al. — "Training language models to follow instructions with human feedback" (2022) — via rlhf-overview.docx

---

**Status**: Complete
**Last Updated**: 2026-04-25
