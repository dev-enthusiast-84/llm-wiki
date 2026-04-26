# RLHF

Reinforcement Learning from Human Feedback — a three-stage training pipeline that aligns language models with human preferences.

## Summary

RLHF (Reinforcement Learning from Human Feedback) is the primary practical technique for aligning large language models with human values and intentions. It works by first supervised-fine-tuning a base model on demonstrations, then training a reward model from human preference comparisons, and finally optimizing the LM against the reward model using PPO with a KL divergence penalty. InstructGPT (Ouyang et al., 2022) demonstrated that a 1.3B RLHF-trained model was preferred over a 175B GPT-3 baseline by human raters.

## Explanation

### The Three Stages

**Stage 1: Supervised Fine-Tuning (SFT)**
- Collect high-quality demonstration data: human labelers write ideal responses to prompts
- Fine-tune the base language model on this data using standard cross-entropy loss
- Result: an SFT model that can follow instructions but is not yet preference-optimized

**Stage 2: Reward Model (RM) Training**
- Collect comparison data: the SFT model generates multiple responses to the same prompt; human raters rank them by quality
- Train a separate reward model (initialized from the SFT model) to predict which response a human would prefer
- The RM outputs a scalar quality score r(prompt, response)
- Details: typically the final transformer layer is replaced by a scalar head; trained with a ranking loss (Bradley-Terry model)

**Stage 3: PPO Fine-Tuning**
- Use the RM as a reward signal to fine-tune the SFT model via Proximal Policy Optimization (PPO)
- Key constraint: KL divergence penalty between the RLHF model and the SFT model:
  - `r_final = r_RM(prompt, response) - β · KL(π_RLHF || π_SFT)`
  - The KL penalty (β ≈ 0.02 in InstructGPT) prevents the model from drifting too far from the SFT model and gaming the reward model
- The policy (language model) is updated to maximize expected reward

### Why the KL Penalty Matters

Without the KL constraint, the LM would optimize for the reward model in degenerate ways — producing responses that score highly but are incoherent or harmful. This is called "reward hacking." The KL penalty keeps the output distribution close to the reference SFT model, maintaining fluency and factual grounding.

### DPO: A Simpler Alternative

Direct Preference Optimization (Rafailov et al., 2023) reformulates RLHF as a supervised learning problem — no separate reward model or RL loop required. Instead, preferences are used to directly update the LM parameters via a log-likelihood ratio objective. DPO achieves comparable alignment with simpler training.

### Alignment Properties

| Property | Pre-RLHF | Post-RLHF |
|----------|-----------|-----------|
| Instruction following | Poor | Strong |
| Helpfulness | Variable | Improved |
| Harmlessness | Variable | Improved |
| Verbosity bias | Less | More (rater preference artifact) |

## Related Concepts

- [[reward-model]] — The RM trained on human preference rankings; used as RLHF reward signal
- [[instructgpt]] — The InstructGPT model that demonstrated RLHF's effectiveness at scale
- [[ai-safety-alignment]] — RLHF is a primary practical alignment technique
- [[hallucination]] — RLHF can reduce but not eliminate hallucination
- [[gpt-3]] — Base model on which InstructGPT's RLHF was applied

## Sources

- Ouyang et al. — "Training language models to follow instructions with human feedback" (2022) — via rlhf-overview.docx

---

**Status**: Complete
**Last Updated**: 2026-04-25
