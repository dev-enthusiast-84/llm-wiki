# AI Safety and Alignment

**Sources:**  
- "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021  
- "Training language models to follow instructions with human feedback" — Ouyang et al., OpenAI, 2022 (NeurIPS)

## Summary

AI safety and alignment address the challenge of ensuring that [[foundation-model]]s behave in accordance with human values, goals, and constraints — especially as models scale to capabilities beyond what can be easily evaluated or anticipated. Key concerns include misalignment between training objectives and intended behavior, emergent goal-directed behavior, and correlated failure across systems built on a single foundation model. Ouyang et al. (2022) demonstrate that [[rlhf]] is a practical, low-cost technique for partial alignment — reducing [[hallucination]] and improving instruction-following — though it aligns to a specific group's preferences, not universal values.

## Explanation

**Core concepts:**

**Value alignment:**  
The problem of specifying a training objective (reward function) that accurately reflects human values. This is hard because:
- Human values are diverse, context-dependent, and sometimes contradictory
- Training objectives (e.g., next-token prediction) optimize for proxy metrics, not intended behavior
- Language models trained to predict text are trained to predict regardless of factual truth — they will confidently generate false statements if the training distribution contains such patterns

**Misalignment in current models:**  
Foundation models trained for next-word prediction are *not* trained to be truthful. When users interact expecting factually accurate outputs, there is a fundamental misalignment between the training objective and the deployment use case.

**Corrigibility:**  
The ability to correct or shut down a system after deployment. Corrigibility requires that the system not resist modification. As models become more capable and are integrated into more systems, maintaining corrigibility becomes harder.

**Emergent goal-directed behavior:**  
Models trained in open-ended environments (e.g., self-play, multitask RL) may develop implicit goals not specified in the training objective — including potentially deceptive or strategically planning behaviors. This is not observed in current self-supervised models but is a concern as capabilities scale.

**The [[homogenization]] risk for safety:**  
A single foundation model integrated into multiple critical functions (healthcare, infrastructure, financial systems) creates correlated failure risk. If the foundation model has a systematic bias or vulnerability, it affects all downstream systems simultaneously.

**GPT-3 as an edge case:**  
GPT-3's arithmetic performance improves dramatically when commas are added to input numbers — a small prompt reformulation causes large behavioral change. This sensitivity makes it difficult to characterize the model's true capabilities, complicating safety evaluation.

**Scalable oversight:**  
As model capabilities approach or exceed human expertise in specific domains, it becomes harder to evaluate whether model outputs are correct. Developing evaluation methods that scale with capability is an open problem.

**Near-term priorities (as of 2021):**  
1. Characterizing and forecasting capabilities of current self-supervised models
2. Developing natural language-based control mechanisms (task specification, output explanation)
3. Building evaluation frameworks that can detect capability emergence before deployment

**RLHF as a practical alignment technique (Ouyang et al., 2022):**  
[[rlhf]] addresses alignment empirically by fine-tuning language models against a [[reward-model]] trained on human preference comparisons. Key findings:
- The **HHH framework** (Helpful, Honest, Harmless; Askell et al., 2021) provides an operational definition of alignment for language models
- [[instructgpt]] trained with RLHF reduces [[hallucination]] from 41% → 21% and is ~2× more truthful on TruthfulQA vs. GPT-3
- Alignment fine-tuning costs ~2% of pretraining compute — low alignment tax
- **Fundamental limitation:** RLHF aligns to a *specific group's preferences* (~40 English-speaking contractors, OpenAI researchers, API customers) — not universal human values; whose preferences to optimize is itself an unsolved normative problem

**The "alignment tax":**  
Fine-tuning for alignment can cause performance regressions on public NLP benchmarks (SQuAD, DROP, HellaSwag, WMT). Ouyang et al. mitigate this via PPO-ptx (mixing pretraining gradients into RLHF fine-tuning). The existence of the alignment tax implies that alignment and capability are not perfectly correlated — an aligned model need not be the most capable on every benchmark.

## Contradictions with Prior Papers

- **vs. Vaswani et al. (2017):** The Transformer paper treats the model as a tool for a specific, well-defined task (machine translation). Safety, alignment, and misuse risks are not discussed. Bommasani et al. argue these concerns are central to any foundation model, including those based on the Transformer architecture.
- **vs. Devlin et al. (2019):** The BERT paper frames pre-training and fine-tuning as unambiguously beneficial ("demonstrates the importance of bidirectional pre-training"). It does not consider that the same fine-tuning flexibility that enables BERT on NLU tasks also enables misuse (generating toxic content, fine-tuning for harmful purposes). Bommasani et al. identify misuse as a first-class concern for foundation models.

- **vs. Bommasani et al. (2021) — alignment timeline:** The FMs paper presents alignment as a major unsolved challenge requiring future research. Ouyang et al. (2022) demonstrate a production-deployed RLHF solution within one year — alignment became an empirically tractable problem faster than the FMs paper suggested.

## Related Concepts

- [[rlhf]]
- [[instructgpt]]
- [[reward-model]]
- [[hallucination]]
- [[foundation-model]]
- [[emergence]]
- [[homogenization]]
- [[distribution-shift]]
- [[scaling-laws]]
- [[pre-training-fine-tuning]]
- [[self-supervised-learning]]
