# Reinforcement Learning from Human Feedback (RLHF)

**Source:** "Training language models to follow instructions with human feedback" — Ouyang et al., OpenAI, 2022 (NeurIPS)  
**Background technique:** Christiano et al., 2017 (originally applied to robotics and Atari games)

## Summary

RLHF is a three-step fine-tuning technique that aligns a pre-trained language model to user intent by using human preference comparisons as a reward signal. Applied to [[gpt-3]] by Ouyang et al. (2022), it produces [[instructgpt]] — a model that 40 human labelers prefer to the original GPT-3 85% of the time despite being identical in architecture. RLHF demonstrates that alignment is a tractable fine-tuning problem, not a fundamental barrier.

## Explanation

**The three-step pipeline:**

**Step 1 — Supervised Fine-Tuning (SFT):**  
Human labelers write demonstrations of desired model behavior for a diverse set of prompts. The pre-trained model is fine-tuned on these demonstrations using standard cross-entropy supervised learning.
- Dataset: ~13,000 prompts (mix of labeler-written and real API prompts)
- Labelers: ~40 contractors from Upwork/Scale AI, screened for sensitivity and agreement with researchers
- Fine-tuning: 16 epochs, cosine LR decay, residual dropout 0.2

**Step 2 — Reward Model (RM) Training:**  
Labelers rank K=4–9 model outputs for the same prompt, producing K-choose-2 comparison pairs. A [[reward-model]] is trained to predict which output human labelers prefer. Using comparison rankings (rather than absolute scores) is more reliable since humans judge relative quality more consistently than absolute quality.
- Dataset: ~33,000 prompts
- RM size: 6B parameters (smaller than 175B for training stability; see [[reward-model]])
- Loss: log-sigmoid on reward difference between preferred and rejected completion

**Step 3 — Reinforcement Learning via PPO:**  
The SFT model is fine-tuned using PPO (Proximal Policy Optimization; Schulman et al., 2017), with the reward model's scalar output as the reward signal. Two critical regularization mechanisms:

1. **KL penalty:** A per-token KL divergence penalty from the SFT model is added to the reward at each step, penalizing the RL policy for drifting too far from the SFT baseline. This prevents reward hacking — gaming the RM by generating superficially appealing but low-quality outputs.

2. **PPO-ptx (pretraining mix):** The PPO objective is augmented with pretraining log-likelihood gradients:

```
objective(φ) = E[r_θ(x,y) − β·log(π_RL(y|x) / π_SFT(y|x))] + γ·E[log π_RL(x)]
```

where β controls the KL penalty and γ controls the pretraining mix weight. PPO-ptx mitigates the **alignment tax** (performance regressions on public NLP benchmarks) without compromising labeler preference scores.

**Data collection:**  
- SFT dataset: 13k prompts (labeler-written + real API)
- RM dataset: 33k prompts (labeler rankings of K=4–9 outputs each)
- PPO dataset: 31k prompts (API prompts only, used as environment inputs)
- Prompt distribution (RM): 45.6% generation, 12.4% open QA, 11.2% brainstorming, 8.4% chat, 6.6% rewrite, 4.2% summarization — predominantly open-ended, not classification/QA

**Evaluation — Helpful, Honest, Harmless (HHH):**  
The paper uses the HHH framework (Askell et al., 2021) as an alignment target:
- **Helpful:** follows instructions, infers intent from prompts
- **Honest:** avoids fabricating information; measured via TruthfulQA and [[hallucination]] rate
- **Harmless:** avoids toxic, biased, and harmful outputs

**The alignment tax:**  
By default, RLHF fine-tuning causes performance regressions on some public NLP benchmarks (SQuAD, DROP, HellaSwag, WMT FR→EN). This trade-off — improved alignment at the cost of benchmark performance — is called the alignment tax. PPO-ptx largely eliminates this regression. The alignment cost (4.9 petaflop/s-days for SFT, 60 for PPO-ptx) is a small fraction of pretraining cost (3,640 petaflop/s-days for GPT-3).

**Who are we aligning to?**  
The paper explicitly acknowledges that RLHF aligns to a *specific* group's preferences:
- ~40 contractors (primarily English-speaking, US/Southeast Asia)
- OpenAI researchers who wrote labeling instructions
- OpenAI API customers whose prompts were collected
- This is not representative of all users or global values — a fundamental limitation

## Contradictions / Tensions Across Papers

- **vs. Brown et al. (2020) — scale as primary lever:** GPT-3 demonstrates that scaling alone produces capable models via in-context learning. RLHF shows that a 1.3B InstructGPT is preferred over 175B GPT-3 (100× larger) — alignment fine-tuning is more impactful than a 100× parameter increase for user-facing instruction following.
- **vs. Brown et al. (2020) — fine-tuning OOD risk:** GPT-3 argues fine-tuning risks poor out-of-distribution generalization. RLHF fine-tuning (InstructGPT) actually *improves* generalization to non-English instructions and code Q&A — tasks not explicitly supervised during RLHF fine-tuning.
- **vs. Devlin et al. (2019) — supervised fine-tuning:** BERT-style fine-tuning uses task-specific labeled datasets. RLHF replaces task-specific labels with human preference comparisons, which are cheaper to collect and produce more human-aligned behavior across a broad task distribution.
- **vs. Bommasani et al. (2021) — alignment as open problem:** Bommasani et al. present alignment as an unsolved challenge. RLHF provides an empirically validated, production-deployed solution — iterative, imperfect, but demonstrably effective and low-cost relative to pretraining.

## Related Concepts

- [[instructgpt]]
- [[reward-model]]
- [[gpt-3]]
- [[adaptation]]
- [[ai-safety-alignment]]
- [[hallucination]]
- [[in-context-learning]]
- [[pre-training-fine-tuning]]
- [[foundation-model]]
