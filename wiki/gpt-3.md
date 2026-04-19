# GPT-3

**Source:** "Language Models are Few-Shot Learners" — Brown et al., OpenAI, 2020 (NeurIPS)

## Summary

GPT-3 is a 175-billion-parameter [[autoregressive-language-model]] trained on 300 billion tokens of web text. It demonstrates that scale alone, without any fine-tuning or task-specific architecture changes, enables strong performance across a wide range of NLP tasks through [[in-context-learning]]. It is a canonical example of a [[foundation-model]] and the primary empirical demonstration of [[emergence|emergent]] capabilities.

## Explanation

**Architecture:**  
GPT-3 uses the same architecture as GPT-2 with two modifications:
- **Alternating dense and locally-banded sparse attention** (Sparse Transformer style) in the attention layers — differs from the full attention in the original [[transformer]]
- **Pre-normalization:** [[layer-normalization]] is applied *before* each sub-layer input (before attention / FFN), not after the residual addition as in the original [[transformer]] (`output = x + Sublayer(LayerNorm(x))`). This improves training stability at large scale.
- Feed-forward inner dimension is always 4 × d_model, consistent with the [[transformer]] and [[bert]]
- Uses GELU activation (same as [[bert]]), not ReLU
- Tokenization: reversible [[byte-pair-encoding]]
- Context window: 2048 tokens

**Model sizes (Table 2.1):**

| Model          | Parameters | Layers | d_model | Heads |
|----------------|-----------|--------|---------|-------|
| GPT-3 Small    | 125M      | 12     | 768     | 12    |
| GPT-3 Medium   | 350M      | 24     | 1024    | 16    |
| GPT-3 Large    | 760M      | 24     | 1536    | 16    |
| GPT-3 XL       | 1.3B      | 24     | 2048    | 24    |
| GPT-3 2.7B     | 2.7B      | 32     | 2560    | 32    |
| GPT-3 6.7B     | 6.7B      | 32     | 4096    | 32    |
| GPT-3 13B      | 13B       | 40     | 5140    | 40    |
| **GPT-3 175B** | **175B**  | 96     | 12288   | 96    |

All 8 sizes trained for 300 billion tokens.

**Training data:**

| Dataset       | Weight | Notes |
|---------------|--------|-------|
| Common Crawl (filtered) | 60% | Heavily filtered by quality heuristics + deduplication |
| WebText2      | 22%    | Reddit-upvoted links, GPT-2 data + more |
| Books1        | 8%     | Fiction/non-fiction books |
| Books2        | 8%     | Additional books corpus |
| Wikipedia     | 3%     | English Wikipedia |

**Evaluation paradigm — no fine-tuning:**  
Unlike BERT, GPT-3 performs all evaluations in zero-shot, one-shot, or few-shot settings:
- **Zero-shot (K=0):** task description in natural language, no examples
- **One-shot (K=1):** one demonstration example
- **Few-shot (K=10–100):** up to context window capacity

Demonstrations are formatted as input–output pairs concatenated directly into the context. No gradient updates are performed at evaluation time.

**Key results:**

| Task       | Setting  | Score          | Notes |
|------------|----------|----------------|-------|
| TriviaQA   | Few-shot | 71.2%          | SOTA closed-book at publication |
| CoQA       | Few-shot | 85.0 F1        | Within 3 F1 of fine-tuned BERT |
| WebQS      | Few-shot | 41.5%          | Strong open-domain QA |
| Winogrande | Few-shot | 77.7%          | Near fine-tuned SOTA |
| SuperGLUE  | Few-shot | 71.8           | Below fine-tuned BERT |

**Weaknesses:**  
- NLI tasks requiring bidirectional comparison: ANLI (near chance), WIC
- Some reading comprehension: RACE, QuAC
- Common-sense physics: difficulty with questions like "If I put cheese in the fridge, will it melt?"
- Long document coherence: semantic repetition, occasional self-contradiction over long passages

**Limitations acknowledged by the authors:**
1. No bidirectional architecture — tasks requiring comparison of two spans are harder
2. Token-level pre-training objective (every token equal weight) — lacks notion of what is important to predict
3. Not grounded in perceptual or physical experience
4. Poor pre-training sample efficiency (sees vastly more text than a human lifetime)
5. Expensive inference at 175B scale; distillation proposed as future direction
6. Biases inherited from training data:
   - **Gender:** 83% of 388 occupations tested are more likely followed by a male identifier
   - **Race:** "Black" had consistently lowest sentiment across 5 of 7 model sizes; "Asian" highest
   - **Religion:** Islam more frequently co-occurs with "violent", "terrorism" than other religions
7. Training energy: several thousand petaFLOP/s-days (vs. tens for GPT-2 1.5B)

**Data contamination:**  
Web-crawled training data may contain benchmark test sets. The authors studied this systematically using n-gram overlap detection. Finding: contamination exists but has minimal effect on most benchmarks. See [[data-contamination]].

## Contradictions / Tensions Across Papers

- **vs. Devlin et al. (2019) — bidirectionality:** BERT's ablations (Table 5) show bidirectionality is essential for understanding tasks. GPT-3 achieves strong NLU results *without* bidirectionality, through scale alone. GPT-3 explicitly acknowledges bidirectionality would likely help on comparison/NLI tasks — the two approaches are complementary, not mutually exclusive, but GPT-3 demonstrates bidirectionality is not *necessary* for competitive performance.
- **vs. Devlin et al. (2019) — fine-tuning:** BERT presents full-parameter fine-tuning as the standard, efficient, and unambiguously beneficial adaptation approach. GPT-3 explicitly argues that fine-tuning can cause *poor out-of-distribution generalization* and risks overfitting to narrow task distributions [HLW+20, MPL19]. GPT-3 proposes in-context learning as a principled alternative that avoids updating weights entirely.
- **vs. Vaswani et al. (2017) — layer normalization placement:** The original Transformer applies LayerNorm *after* the residual addition: `LayerNorm(x + Sublayer(x))`. GPT-3 applies LayerNorm *before* the sublayer input: `x + Sublayer(LayerNorm(x))` (pre-normalization). Pre-normalization is empirically stabler at very large scale.
- **vs. Vaswani et al. (2017) — attention pattern:** The original Transformer uses full self-attention (every position attends to every other). GPT-3 uses *alternating dense and locally-banded sparse* attention layers, reducing cost for long sequences.

## Related Concepts

- [[autoregressive-language-model]]
- [[in-context-learning]]
- [[instructgpt]]
- [[rlhf]]
- [[foundation-model]]
- [[emergence]]
- [[scaling-laws]]
- [[self-supervised-learning]]
- [[adaptation]]
- [[transformer]]
- [[byte-pair-encoding]]
- [[data-contamination]]
- [[ai-safety-alignment]]
- [[distribution-shift]]
