# Self-Attention

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

Self-attention (also called intra-attention) is an attention mechanism that relates different positions within a single sequence to compute a representation of that sequence. It is the core building block of the [[transformer]].

## Explanation

In a self-attention layer, queries, keys, and values all come from the same source — the output of the previous layer. Each position can attend to every other position in the same sequence, capturing global dependencies in O(1) sequential operations.

**Comparison with other layer types (sequence length n, dimension d):**

| Layer Type         | Complexity/Layer | Sequential Ops | Max Path Length |
|--------------------|-----------------|----------------|-----------------|
| Self-Attention     | O(n² · d)       | O(1)           | O(1)            |
| Recurrent (RNN)    | O(n · d²)       | O(n)           | O(n)            |
| Convolutional      | O(k · n · d²)   | O(1)           | O(log_k(n))     |

Self-attention is faster than recurrence when sequence length n < representation dimension d, which is typical in NLP (word-piece / BPE representations).

**Three uses in the [[transformer]]:**
1. **Encoder self-attention** — every position attends to all positions in the previous encoder layer
2. **Decoder masked self-attention** — each position attends only to positions ≤ its own (masked to preserve auto-regressive property)
3. **Encoder-decoder attention** — decoder queries attend to all encoder output positions

A notable side benefit: self-attention can yield more interpretable models — individual heads exhibit behavior related to syntactic and semantic sentence structure (e.g., anaphora resolution, long-distance verb dependencies).

## Contradictions / Tensions Across Papers

**From Bommasani et al. (2021):**
- **Quadratic complexity is a real bottleneck:** This paper's Table 1 notes self-attention is O(n²·d) per layer, which the authors frame as acceptable given NLP sequence lengths. Bommasani et al. identify this as a fundamental constraint for long-sequence tasks (documents, high-resolution images, genomics). Two distinct families of solutions have emerged:
  - **Sparse/linear-complexity attention** — reduce the O(n²) cost within the attention operation itself:
    - *Longformer / BigBird / Sparse Transformer* — attend only to a sparse subset of positions (local window + global tokens)
    - *Perceiver / GANformer* — route input through a small bottleneck or bipartite structure to achieve O(n) complexity
  - **Retrieval-augmented models** (REALM, RAG, RETRO) — a structurally different approach: offload long-range knowledge storage to an *external index* queried at inference time, reducing the context that the Transformer must attend over. These do not modify the attention operation itself but sidestep the need for very long context windows.

- **Directionality:** The [[transformer]] decoder uses causal (left-to-right) self-attention by design, treating unidirectionality as a prerequisite for auto-regressive generation. [[bert]]'s ablations (Table 5) demonstrate that for *understanding* tasks, bidirectional self-attention learned via [[masked-language-model]] outperforms left-to-right self-attention across every benchmark tested. The two papers are not strictly contradictory — one optimizes for generation, the other for understanding — but they represent different design philosophies about what "correct" self-attention looks like.

## Related Concepts

- [[multi-head-attention]]
- [[scaled-dot-product-attention]]
- [[transformer]]
- [[encoder-decoder]]
- [[positional-encoding]]
- [[bert]]
- [[masked-language-model]]
- [[foundation-model]]
