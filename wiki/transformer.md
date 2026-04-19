# Transformer

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

The Transformer is a sequence transduction model that replaces recurrent and convolutional layers entirely with [[self-attention]] mechanisms. It was the first model to achieve state-of-the-art translation quality using only attention (at publication, 2017), enabling far greater parallelization than RNN-based approaches.

## Explanation

The Transformer follows an [[encoder-decoder]] structure. Both the encoder and decoder are stacks of N=6 identical layers. Each encoder layer has two sub-layers: a [[multi-head-attention]] mechanism and a [[feed-forward-network]]. Each decoder layer has three sub-layers: masked [[multi-head-attention]], encoder-decoder [[multi-head-attention]], and a [[feed-forward-network]].

Every sub-layer is wrapped with a [[residual-connection]] followed by [[layer-normalization]]:

```
output = LayerNorm(x + Sublayer(x))
```

All sub-layers and embeddings produce outputs of dimension d_model = 512.

**Key design choices:**
- No recurrence → O(1) sequential operations (vs O(n) for RNNs)
- [[positional-encoding]] injects sequence order information
- [[scaled-dot-product-attention]] with scaling by 1/√d_k prevents vanishing gradients in softmax

**Results (WMT 2014):**
- EN→DE: 28.4 BLEU (SOTA at time of publication, 2017; +2 over previous best ensemble)
- EN→FR: 41.8 BLEU (SOTA at time of publication, 2017; at 1/4 the training cost of prior best)
- Trained on 8 P100 GPUs in 3.5 days (big model)

## Contradictions / Tensions Across Papers

See [[bert]] for BERT-specific architectural divergences. Additional tensions from Bommasani et al. (2021):

- **Quadratic complexity:** The paper treats self-attention's O(n²) cost per layer as an acceptable trade-off for O(1) path length. Bommasani et al. identify this as a fundamental bottleneck for long-sequence modeling, motivating linear-complexity alternatives: Longformer, BigBird, Sparse Transformer (exploit attention sparsity), Perceiver and GANformer (bipartite/bottleneck attention achieving linear complexity). None of these were anticipated by the original paper.
- **Scale:** The Transformer paper's largest model is ~213M parameters (encoder + decoder). [[gpt-3]], built on the same architecture, has 175B parameters — nearly 1000× larger — and exhibits [[emergence|emergent]] capabilities not present at the scale the paper studied.
- **Layer normalization placement:** The original Transformer applies LayerNorm *after* the residual addition: `LayerNorm(x + Sublayer(x))` (post-normalization). GPT-3 applies LayerNorm *before* the sublayer: `x + Sublayer(LayerNorm(x))` (pre-normalization). Pre-normalization improves training stability at very large scale and has become standard in subsequent models.
- **Attention pattern:** GPT-3 uses *alternating dense and locally-banded sparse* attention layers (Sparse Transformer style), not full self-attention over all positions. This reduces cost for long sequences while preserving expressive capacity.
- **Task generality:** The paper evaluates on translation and constituency parsing. Bommasani et al. confirm the Transformer architecture underlies virtually all state-of-the-art foundation models across text, images, speech, proteins, and reinforcement learning — a generality far beyond what the original paper envisioned.
- **Training paradigm:** The Transformer paper trains models from scratch for each task. The foundation model paradigm (Bommasani et al.) inverts this: train once at massive scale on unlabeled data using [[self-supervised-learning]], then [[adaptation|adapt]] cheaply.

BERT-specific contradictions:
- [[bert]] uses the Transformer **encoder only** (no decoder).
- [[bert]] replaces ReLU with GELU in the [[feed-forward-network]].
- [[bert]] uses learned [[positional-encoding]] instead of sinusoidal.
- At scale, BERT_LARGE (340M params, encoder only) is larger than the Transformer's biggest model (213M params, encoder + decoder combined).

## Related Concepts

- [[self-attention]]
- [[multi-head-attention]]
- [[scaled-dot-product-attention]]
- [[positional-encoding]]
- [[encoder-decoder]]
- [[layer-normalization]]
- [[feed-forward-network]]
- [[residual-connection]]
- [[bleu]]
- [[byte-pair-encoding]]
- [[bert]]
- [[foundation-model]]
- [[self-supervised-learning]]
- [[scaling-laws]]
