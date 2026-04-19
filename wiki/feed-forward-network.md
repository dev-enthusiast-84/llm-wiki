# Position-wise Feed-Forward Network

**Source:** "Attention Is All You Need" — Vaswani et al., 2017 (NIPS)

## Summary

Each layer in the [[transformer]] encoder and decoder contains a position-wise feed-forward network (FFN) applied identically and independently to each position, providing non-linear transformation capacity beyond what [[multi-head-attention]] provides.

## Explanation

**Formula:**

```
FFN(x) = max(0, x·W₁ + b₁)·W₂ + b₂
```

- Two linear transformations with a ReLU activation in between
- Applied to each position separately and identically (hence "position-wise")
- Equivalent to two convolutions with kernel size 1

**Dimensions (base model):**
- Input/output: d_model = 512
- Inner layer: d_ff = 2048

**Dimensions (big model):**
- Input/output: d_model = 1024
- Inner layer: d_ff = 4096

While the same transformation is applied to each position, different layers use different weight matrices W₁, W₂ — there is no weight sharing across layers.

**Role in the Transformer:** The FFN provides the bulk of the model's representational capacity (parameter count-wise). The [[multi-head-attention]] mechanism routes information between positions; the FFN transforms each position's representation independently. Together they cover both long-range interaction and local non-linear feature extraction.

## Contradictions / Tensions Across Papers

- **Activation function:** The [[transformer]] paper uses **ReLU** (`max(0, x)`) as the activation between the two linear layers. [[bert]] uses **GELU** (Gaussian Error Linear Unit, Hendrycks & Gimpel 2016), following OpenAI GPT. GELU is a smooth approximation to ReLU that weights inputs by their magnitude under a Gaussian CDF. BERT does not ablate this choice, so it is unclear how much of BERT's performance gain is attributable to GELU vs bidirectionality. [[gpt-3]] also uses GELU and maintains the 4×d_model inner dimension ratio across all 8 model sizes — establishing GELU + 4×d_model as the de facto standard in the GPT lineage.

## Related Concepts

- [[transformer]]
- [[encoder-decoder]]
- [[multi-head-attention]]
- [[residual-connection]]
- [[layer-normalization]]
- [[bert]]
