# Compilation Log

---

## 2026-04-19 (Session 6)

**RHLF.pdf added (~50pp); total ~370 pages**

- Source files: `raw/Attention.pdf` (15pp), `raw/BERT.pdf` (16pp), `raw/FMs.pdf` (214pp), `raw/gpt3.pdf` (75pp), `raw/RHLF.pdf` (~50pp)
- RHLF paper: "Training language models to follow instructions with human feedback" — Ouyang et al., OpenAI, 2022 (NeurIPS); InstructGPT
- Extraction method: pdfminer.six

**New entity pages created (4):**
- `rlhf.md` — Three-step RLHF pipeline (SFT → reward model → PPO); KL penalty; PPO-ptx to mitigate alignment tax; HHH framework; alignment cost relative to pretraining
- `instructgpt.md` — GPT-3 fine-tuned with RLHF; 1.3B preferred over 175B GPT-3; hallucination 41%→21%; remaining limitations (false premises, over-hedging, bias unchanged)
- `reward-model.md` — Predicts human preferences from K=4–9 ranked comparisons; 6B size; log-sigmoid loss; 69.6% held-out accuracy; role in KL-penalized PPO
- `hallucination.md` — Generating false/unsupported information; 41% GPT-3 vs 21% InstructGPT; TruthfulQA; root cause in next-token prediction objective; reduced but not solved by RLHF

**Existing pages updated (5):**
- `ai-safety-alignment.md` — Added RLHF as practical alignment technique; HHH framework; alignment tax concept; explicit caveat that RLHF aligns to specific group preferences; updated source attribution; added new related concepts
- `adaptation.md` — Added RLHF as distinct third adaptation mode (human preference comparisons); added [[rlhf]] to Related Concepts
- `gpt-3.md` — Added [[instructgpt]] and [[rlhf]] to Related Concepts
- `scaling-laws.md` — Added contradiction: 1.3B InstructGPT preferred over 175B GPT-3 — alignment more impactful than 100× scale for instruction following
- `index.md` — Updated total pages; added instructgpt, rlhf, reward-model, hallucination entries

**New cross-paper contradictions documented:**

| # | Contradiction | Pages |
|---|---------------|-------|
| 19 | Scale vs. alignment: Scaling laws predict capability improves with params; 1.3B InstructGPT preferred over 175B GPT-3 — alignment fine-tuning more impactful than 100× scale increase for user-facing tasks | `rlhf.md`, `instructgpt.md`, `scaling-laws.md` |
| 20 | Fine-tuning OOD risk: GPT-3 argues fine-tuning risks poor OOD generalization; RLHF fine-tuning (InstructGPT) improves generalization to non-English/code instructions not explicitly supervised | `instructgpt.md`, `rlhf.md`, `adaptation.md`, `gpt-3.md` |
| 21 | Alignment timeline: Bommasani et al. present alignment as a major unsolved challenge (2021); Ouyang et al. demonstrate a production-deployed RLHF solution within one year | `rlhf.md`, `instructgpt.md`, `ai-safety-alignment.md` |
| 22 | Hallucination as anticipated vs. measured problem: BERT/Transformer/GPT-3 papers do not measure hallucination; Ouyang et al. provide first systematic rate (41% GPT-3, 21% InstructGPT) and a working mitigation | `hallucination.md`, `gpt-3.md`, `ai-safety-alignment.md` |
| 23 | Supervision source: BERT fine-tuning uses task-specific ground-truth labels; RLHF replaces labels with human preference comparisons — more general but encodes specific group preferences | `rlhf.md`, `reward-model.md`, `pre-training-fine-tuning.md` |

---

## 2026-04-19 (Session 5)

**GPT-3.pdf added (75pp); total 320 pages**

- Source files: `raw/Attention.pdf` (15pp), `raw/BERT.pdf` (16pp), `raw/FMs.pdf` (214pp), `raw/gpt3.pdf` (75pp)
- GPT-3 paper: "Language Models are Few-Shot Learners" — Brown et al., OpenAI, 2020 (NeurIPS)
- Extraction method: pdfminer.six

**New entity pages created (3):**
- `gpt-3.md` — 175B autoregressive Transformer LM; 8 model sizes; zero/one/few-shot ICL; architecture modifications (pre-normalization, sparse attention); results; limitations; bias analysis
- `autoregressive-language-model.md` — Left-to-right next-token prediction; full token supervision; contrast with MLM; role in GPT lineage; unidirectionality limitation
- `data-contamination.md` — Train/test overlap in web-crawled data; GPT-3 systematic study; n-gram detection methodology; finding: minimal effect on most benchmarks

**Existing pages updated (8):**
- `in-context-learning.md` — Upgraded to GPT-3 as primary source; added formal K definition (K=0/1/10–100); 2048-token context window; meta-learning framing (RL² analogy); GPT-3 benchmark results; added link to [[gpt-3]], [[autoregressive-language-model]]
- `scaling-laws.md` — Added GPT-3 direct application: 8 model sizes (125M–175B), 300B training tokens, smooth power-law trend confirmed across 3 orders of magnitude
- `adaptation.md` — Added GPT-3's fine-tuning OOD critique: fine-tuning risks poor out-of-distribution generalization [HLW+20, MPL19] — stronger than efficiency argument
- `transformer.md` — Added GPT-3 architectural modifications: pre-normalization (LayerNorm before sublayer) and alternating dense/sparse attention
- `feed-forward-network.md` — Added GPT-3 GELU + 4×d_model note; establishing de facto standard across GPT lineage
- `emergence.md` — Updated GPT-3 example to use [[gpt-3]] link
- `foundation-model.md` — Added [[gpt-3]] to examples and Related Concepts
- `index.md` — Updated total pages (245 → 320); added gpt-3, autoregressive-language-model, data-contamination entries

**New cross-paper contradictions documented:**

| # | Contradiction | Pages |
|---|---------------|-------|
| 15 | Bidirectionality necessity: BERT ablations show bidirectionality essential for understanding; GPT-3 achieves competitive NLU without it via scale alone | `gpt-3.md`, `bert.md`, `autoregressive-language-model.md` |
| 16 | Fine-tuning risk: BERT presents fine-tuning as standard and beneficial; GPT-3 argues fine-tuning causes poor OOD generalization, proposing in-context learning as principled alternative | `gpt-3.md`, `adaptation.md`, `bert.md` |
| 17 | Layer normalization placement: Transformer uses post-normalization (LayerNorm after residual); GPT-3 uses pre-normalization (LayerNorm before sublayer) — stabler at very large scale | `gpt-3.md`, `transformer.md` |
| 18 | Attention pattern: Transformer uses full self-attention; GPT-3 uses alternating dense + locally-banded sparse attention | `gpt-3.md`, `transformer.md`, `self-attention.md` |

---

## 2026-04-19 (Session 4 — Audit)

**Full wiki audit: link graph, contradictions, stale claims**

**No orphan pages found** (all 27 content pages have ≥1 inbound link).  
**No missing pages** (all `[[...]]` targets resolve, after fixes below).

**Fixes applied (7 issues):**

| # | Type | File(s) | Fix |
|---|------|---------|-----|
| A1 | Broken link | `emergence.md` | `[[Scaling-laws]]` → `[[scaling-laws]]` (case bug) |
| A2 | Factual error | `masked-language-model.md`, `self-supervised-learning.md` | ELECTRA described as "contemporaneous" with BERT; corrected to "2020 follow-up / Clark et al., ICLR 2020" (BERT: NAACL 2019; ELECTRA: ICLR 2020 — 1.5-year gap) |
| A3 | Stale claim | `transformer.md` | "new SOTA" BLEU results undated → "(SOTA at time of publication, 2017)" |
| A4 | Stale claim | `bleu.md` | "establishes new SOTA" undated → "(established SOTA at time of publication, 2017); since surpassed" |
| A5 | Stale claim | `bert.md`, `glue.md` | Undated SOTA claims → "(at publication, 2019; since surpassed)"; GLUE entry expanded with benchmark adequacy note (Bommasani et al. critique) |
| A6 | Stale/misleading | `next-sentence-prediction.md` | Summary presented NSP benefit as settled fact; added prominent caveat noting RoBERTa's contradicting finding |
| A7 | Structural error | `self-attention.md` | RAG/REALM/RETRO grouped with linear-complexity attention variants (Longformer, Perceiver) — these solve different problems; split into two labelled families: *sparse/linear-complexity attention* vs *retrieval-augmented models* |

---

## 2026-04-19 (Session 3)

**FMs.pdf added (214pp); total 245 pages**

- Source files: `raw/Attention.pdf` (15pp), `raw/BERT.pdf` (16pp), `raw/FMs.pdf` (214pp)
- FMs paper: "On the Opportunities and Risks of Foundation Models" — Bommasani et al., Stanford CRFM, 2021 (arXiv:2108.07258)
- Extraction method: pdfminer.six

**New entity pages created (9):**
- `foundation-model.md` — Core concept: trained on broad data, adapted to downstream tasks; ecosystem stages; leverage-liability duality
- `emergence.md` — Capabilities implicitly induced by scale (in-context learning, arithmetic); historical progression across ML eras
- `homogenization.md` — Consolidation of models/methodologies; leverage vs single-point-of-failure risk
- `scaling-laws.md` — Power-law capability scaling (Kaplan et al. 2020); limitation for emergent phase transitions
- `self-supervised-learning.md` — SSL taxonomy (autoregressive, MLM, contrastive, discriminative); efficiency comparisons
- `adaptation.md` — Full adaptation spectrum (fine-tuning → lightweight → in-context); temporal, domain, privacy adaptations
- `in-context-learning.md` — Gradient-free task adaptation via prompt; emergent in GPT-3; sensitivity/fragility analysis
- `distribution-shift.md` — p_pre / p_ID / p_OOD framework; CLIP robustness numbers; persistent challenges
- `ai-safety-alignment.md` — Value alignment, misalignment in current models, corrigibility, homogenization-correlated failure

**Existing pages updated (6):**
- `transformer.md` — Added quadratic complexity bottleneck, linear alternatives (Longformer, Perceiver), scale implications, paradigm shift
- `pre-training-fine-tuning.md` — Added lightweight adaptation challenge to full fine-tuning; ICL bypasses fine-tuning entirely; broader adaptation scope
- `masked-language-model.md` — Added ELECTRA 4× efficiency comparison; MLM as one SSL instance
- `self-attention.md` — Added O(n²) bottleneck discussion; named linear alternatives (Longformer, BigBird, Perceiver, RAG)
- `bert.md` — Added Bommasani et al. contradictions: Anglocentric bias, NSP controversy, GLUE inadequacy, lightweight adaptation challenge
- `index.md` — Rebuilt to include all 27 entity pages organized by category

**New cross-paper contradictions documented:**

| # | Contradiction | Pages |
|---|---------------|-------|
| 7 | Full fine-tuning necessity: BERT treats it as standard; FMs shows 1000× lighter methods match at scale | `adaptation.md`, `bert.md`, `pre-training-fine-tuning.md` |
| 8 | MLM efficiency: BERT presents MLM as the approach; ELECTRA achieves 4× efficiency on same data | `masked-language-model.md`, `self-supervised-learning.md` |
| 9 | Self-attention quadratic complexity: Transformer paper treats O(n²) as acceptable; FMs identifies it as a fundamental bottleneck requiring new architectures | `self-attention.md`, `transformer.md` |
| 10 | BERT Anglocentric bias: BERT paper implies broad generalization; FMs notes training on English-only data produces demonstrably poor multilingual performance | `bert.md`, `distribution-shift.md` |
| 11 | NSP utility: BERT shows NSP beneficial (ablation Table 5); FMs cites RoBERTa showing NSP may hurt; benefit may be confounded | `next-sentence-prediction.md`, `bert.md` |
| 12 | GLUE as evaluation: BERT uses GLUE as the primary benchmark; FMs argues task-specific benchmarks like GLUE are inadequate for foundation models needing intrinsic evaluation | `glue.md`, `bert.md` |
| 13 | Training paradigm: Transformer trains from scratch per task; FMs confirms foundation model paradigm has completely superseded this | `transformer.md`, `foundation-model.md` |
| 14 | Emergent capabilities: Neither Transformer nor BERT papers discuss emergent properties; FMs argues emergence is a defining feature of Transformer-based models at scale | `emergence.md`, `scaling-laws.md` |

---

## 2026-04-19 (Session 2)

**BERT.pdf added (16pp); index.md + log.md created (≥30pp threshold met)**

- Source files: `raw/Attention.pdf` (15pp), `raw/BERT.pdf` (16pp) — **31 pages total**

**Entity pages created:** `bert.md`, `masked-language-model.md`, `next-sentence-prediction.md`, `pre-training-fine-tuning.md`, `wordpiece.md`, `cls-sep-tokens.md`, `glue.md`

**Existing pages updated:** `self-attention.md`, `feed-forward-network.md`, `positional-encoding.md`, `transformer.md`

**Cross-paper contradictions documented (1–6):**
1. Activation: ReLU (Transformer) vs GELU (BERT) — `feed-forward-network.md`
2. Positional encoding: sinusoidal recommended (Transformer) vs learned with 512-cap (BERT) — `positional-encoding.md`
3. Attention directionality: causal decoder (Transformer) vs bidirectional (BERT) — `self-attention.md`
4. Model scale: Transformer big ~213M; BERT_LARGE 340M encoder-only — `bert.md`
5. Tokenization: BPE (Transformer) vs WordPiece (BERT) — `wordpiece.md`
6. Training paradigm: scratch (Transformer) vs pre-train/fine-tune (BERT) — `pre-training-fine-tuning.md`

---

## 2026-04-19 (Session 1)

**Attention.pdf only (15pp); no index/log created (<30pp threshold)**

**Entity pages created:** `transformer.md`, `self-attention.md`, `scaled-dot-product-attention.md`, `multi-head-attention.md`, `positional-encoding.md`, `encoder-decoder.md`, `layer-normalization.md`, `feed-forward-network.md`, `residual-connection.md`, `bleu.md`, `byte-pair-encoding.md`
