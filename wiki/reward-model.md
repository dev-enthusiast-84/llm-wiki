# Reward Model

**Source:** "Training language models to follow instructions with human feedback" — Ouyang et al., OpenAI, 2022 (NeurIPS)

## Summary

A reward model (RM) is a neural network trained to predict which of two model outputs a human labeler would prefer, given a prompt. In the [[rlhf]] pipeline, the RM's scalar output serves as the optimization target for reinforcement learning. The RM operationalizes human preferences as a differentiable reward signal, enabling gradient-based alignment of language models.

## Explanation

**Architecture:**  
The RM starts from the SFT model with the final unembedding layer removed. It takes a prompt and a completion as input and outputs a scalar reward score r(x, y). Ouyang et al. use a 6B parameter RM (not 175B) because:
- 175B RM training was empirically unstable
- A 6B RM is more suitable as the value function during RL training
- Saves significant compute

**Training data:**  
Labelers are shown K=4–9 model completions for the same prompt and asked to rank them. This produces K-choose-2 pairwise comparisons per prompt. Rather than shuffling all pairs into a dataset (which causes overfitting), all pairs from a single prompt are batched together in a single training step.

**Loss function:**

```
loss(θ) = -1/C(K,2) · E_(x,y_w,y_l)~D [log σ(r_θ(x, y_w) - r_θ(x, y_l))]
```

where y_w is the preferred completion, y_l is the rejected completion, and σ is the logistic sigmoid. The difference in reward scores represents the log-odds that one response will be preferred over the other.

**Normalization:**  
Since the RM loss is invariant to reward shifts, the RM is normalized with a bias so that labeler demonstrations achieve a mean score of 0 before RL training.

**Generalization:**  
5-fold cross-validation across labeler groups shows:
- RM accuracy on held-out labelers: 69.6 ± 0.9%
- RM accuracy on training labelers: 72.4 ± 0.4%

The small drop confirms the RM generalizes to preferences of labelers who did not produce training data — a prerequisite for the RLHF pipeline to work beyond just memorizing training labeler preferences.

**Role in the RLHF pipeline:**  
The RM is used as the reward function in PPO training. Its scalar output is combined with a KL penalty (to prevent the policy from drifting too far from the SFT baseline):

```
reward = r_θ(x, y) - β · log(π_RL(y|x) / π_SFT(y|x))
```

This prevents the RL policy from producing outputs that receive high RM scores but are incoherent or otherwise degenerate (reward hacking).

**Limitations:**  
- The RM encodes the preferences of a specific labeler group (~40 English-speaking contractors), not universal human values
- RM training instability at 175B scale is an active research challenge
- The RM may be gamed by the RL policy if the policy finds high-scoring outputs that humans would actually find poor (reward hacking)
- Inter-annotator agreement is ~73%, meaning the RM must reconcile genuine labeler disagreements by learning the average preference

## Contradictions / Tensions Across Papers

- **vs. Bommasani et al. (2021):** Bommasani et al. argue alignment is an open and unsolved challenge. The reward model provides a practical mechanism to encode and optimize toward human preferences — though the authors of the InstructGPT paper explicitly acknowledge this encodes specific group preferences, not a universal notion of alignment.
- **vs. standard fine-tuning (Devlin et al., 2019):** BERT fine-tuning uses task-specific ground-truth labels. Reward modeling replaces labels with relative human preference comparisons, which are easier to obtain and more naturally capture human judgment on open-ended tasks where there is no single correct answer.

## Related Concepts

- [[rlhf]]
- [[instructgpt]]
- [[ai-safety-alignment]]
- [[adaptation]]
- [[gpt-3]]
- [[hallucination]]
