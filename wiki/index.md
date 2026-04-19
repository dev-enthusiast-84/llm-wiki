# Wiki Index

Total source pages compiled: **370** (Attention.pdf: 15pp · BERT.pdf: 16pp · FMs.pdf: 214pp · GPT-3.pdf: 75pp · RHLF.pdf: ~50pp)

---

## Foundation Model Paradigm

- [foundation-model](foundation-model.md) — Any model trained on broad data via self-supervision that can be adapted to diverse downstream tasks (Bommasani et al., 2021)
- [emergence](emergence.md) — Capabilities implicitly induced by scale, not explicitly designed; source of both excitement and safety risk
- [homogenization](homogenization.md) — Consolidation of AI methodologies and models; strong leverage but single point of failure
- [scaling-laws](scaling-laws.md) — Power-law relationships between model/data/compute and capability; quantitative but doesn't capture emergent phase transitions
- [self-supervised-learning](self-supervised-learning.md) — Training from unlabeled data by predicting withheld or corrupted parts of the input; umbrella for MLM, autoregressive LM, contrastive learning

## Adaptation

- [adaptation](adaptation.md) — Broad spectrum from full fine-tuning to gradient-free prompting; lightweight methods can match full fine-tuning with 1000× fewer parameters
- [rlhf](rlhf.md) — Three-step alignment fine-tuning (SFT → reward model → PPO); aligns LMs to human preferences; 1.3B InstructGPT beats 175B GPT-3
- [pre-training-fine-tuning](pre-training-fine-tuning.md) — Two-stage paradigm: pre-train on unlabeled text, fine-tune all weights on downstream tasks (BERT-era canonical approach)
- [in-context-learning](in-context-learning.md) — Adapting a model via natural language prompt with no parameter updates; emergent capability in GPT-3
- [reward-model](reward-model.md) — Neural network predicting human preference from comparison rankings; scalar output used as RL reward in RLHF pipeline

## Core Architectures

- [transformer](transformer.md) — Sequence transduction model using only self-attention; eliminates recurrence; foundation of virtually all modern foundation models
- [bert](bert.md) — Bidirectional Transformer encoder pre-trained with MLM+NSP; beginning of the foundation model era (Devlin et al., 2019)
- [gpt-3](gpt-3.md) — 175B autoregressive Transformer LM; first robust demonstration of zero/one/few-shot in-context learning (Brown et al., 2020)
- [instructgpt](instructgpt.md) — RLHF fine-tuned GPT-3; 1.3B version preferred over 175B GPT-3 in human eval; reduces hallucination 41% → 21% (Ouyang et al., 2022)
- [encoder-decoder](encoder-decoder.md) — Stacked encoder/decoder with cross-attention; the Transformer's macro structure for seq2seq tasks

## Attention Mechanisms

- [self-attention](self-attention.md) — Attention over all positions within a single sequence; O(n²) complexity; O(1) sequential ops vs O(n) for RNNs
- [scaled-dot-product-attention](scaled-dot-product-attention.md) — Core attention function: softmax(QKᵀ/√d_k)·V with scaling to prevent vanishing gradients
- [multi-head-attention](multi-head-attention.md) — Parallel attention over h learned projections, enabling joint attention to multiple representational subspaces

## Pre-training Objectives

- [masked-language-model](masked-language-model.md) — MLM: predict randomly masked tokens from bidirectional context; enables deep bidirectionality; ELECTRA is 4× more efficient
- [autoregressive-language-model](autoregressive-language-model.md) — Left-to-right next-token prediction; every token supervised per pass; GPT lineage; enables few-shot in-context learning at scale
- [next-sentence-prediction](next-sentence-prediction.md) — NSP: binary task predicting whether sentence B follows A; later questioned by RoBERTa

## Building Blocks

- [feed-forward-network](feed-forward-network.md) — Position-wise FFN with two linear layers; ReLU in Transformer, GELU in BERT
- [residual-connection](residual-connection.md) — Skip connections wrapping every sub-layer; prerequisite for training deep stacks
- [layer-normalization](layer-normalization.md) — Applied after every sub-layer with residual; stabilizes deep network training
- [positional-encoding](positional-encoding.md) — Sinusoidal in Transformer (recommended), learned in BERT (fixed 512-token cap)

## Tokenization

- [byte-pair-encoding](byte-pair-encoding.md) — Subword tokenization via frequency-based pair merges; used in the Transformer (Sennrich et al.)
- [wordpiece](wordpiece.md) — Subword tokenization via likelihood-based merges; used in BERT (Wu et al.); similar purpose, different criterion

## BERT-specific Concepts

- [cls-sep-tokens](cls-sep-tokens.md) — [CLS] aggregate representation for classification; [SEP] sentence boundary delimiter

## Robustness and Safety

- [distribution-shift](distribution-shift.md) — Train/test mismatch; foundation models improve robustness but don't solve spurious correlations or temporal drift
- [data-contamination](data-contamination.md) — Benchmark test examples present in web-crawled training data; studied systematically in GPT-3; minimal effect on most benchmarks
- [hallucination](hallucination.md) — Generating false or unsupported information; 41% rate in GPT-3, 21% in InstructGPT; root cause is next-token prediction objective
- [ai-safety-alignment](ai-safety-alignment.md) — Value alignment, corrigibility, emergent goal-directed behavior; RLHF as practical alignment technique (HHH framework)

## Evaluation

- [glue](glue.md) — Multi-task NLU benchmark; BERT_LARGE 80.5; deemed inadequate for foundation model evaluation by Bommasani et al.
- [bleu](bleu.md) — N-gram precision metric for machine translation; Transformer 28.4 EN→DE, 41.8 EN→FR
