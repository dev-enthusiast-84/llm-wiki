# Entity Template (for Sync)

Copy this template when creating a new entity page during wiki sync. Save as `wiki/concept-name.md`.

```markdown
# Concept Name

One-line definition or tagline.

## Summary

2-3 sentence high-level overview of what this concept is and why it matters.

## Explanation

Detailed breakdown of the concept:
- How it works
- Why it's important
- Key components or aspects
- Mathematical notation (if applicable)

Use subsections for complex topics:

### Section 1: Aspect or Components

Details...

### Section 2: Application or Context

Details...

## Related Concepts

- [[concept1]] - How it relates to this concept
- [[concept2]] - Connection or distinction
- [[concept3]] - Position in the broader architecture

## Sources

- [Author(s)] - "[Paper Title]" ([Year]) - Section/Page number or specific finding

## Contradictions

(Optional: include only if different sources define this differently)

Description of the contradiction:
- Definition/approach A per [Paper X]
- Definition/approach B per [Paper Y]
- Context: When each applies or which is more commonly accepted

---

**Status**: New (from sync) / Updated  
**Last Updated**: YYYY-MM-DD  
**Source**: [SOURCE]
```

## Quick Fill Guide

**Concept Name**: Match the filename exactly (kebab-case)

**Summary**: Assume minimal background knowledge. One sentence definition, then why it matters.

**Explanation**: Go deeper here. Include:
- How it's used
- Why the research community cares about it
- Examples from papers
- Mathematical formulation if relevant

**Related Concepts**: Think of the concept as a node in a graph. What nodes connect to it?
- Use `[[brackets]]` for links
- Explain the relationship (e.g., "Component of X", "Alternative to Y", "Builds on Z")

**Sources**: Always cite the specific paper. If you're syncing from a new source, add it here.

**Status**: Mark as "New (from sync)" if creating during sync, or "Updated" if revising existing page.

## Example (Filled)

```markdown
# Masked Language Model

A pre-training task where random tokens are masked and the model learns to predict them from context.

## Summary

Masked language modeling (MLM) is a self-supervised learning objective used during transformer pre-training. A percentage of input tokens are replaced with [MASK], and the model learns to predict the original tokens using context from surrounding tokens. This forces the model to develop bidirectional representations.

## Explanation

In MLM, typically 15% of tokens are randomly selected. Of those:
- 80% are replaced with [MASK]
- 10% are replaced with random tokens
- 10% are kept unchanged

The model's only task is to predict the original token. This is fundamentally different from causal language modeling (next-token prediction), which only looks left. MLM allows the model to condition on both left and right context.

### Why It Works

Bidirectional context is more informative than unidirectional context for understanding meaning. By forcing the model to use both directions, representations capture richer semantic information.

### Implementation in BERT

BERT uses MLM as its primary pre-training objective alongside [[next-sentence-prediction]].

## Related Concepts

- [[transformer]] - Architecture that performs MLM
- [[pre-training-fine-tuning]] - MLM is the pre-training phase
- [[bert]] - Model that popularized this approach
- [[next-sentence-prediction]] - Alternative pre-training objective used with MLM
- [[self-supervised-learning]] - MLM is a form of this
- [[autoregressive-language-model]] - Contrast: uses causal masking instead

## Sources

- Devlin et al. - "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (2019) - Section 3.1

## Contradictions

Bidirectional pre-training vs. unidirectional pre-training:
- MLM (bidirectional): Used in BERT, RoBERTa - can see left and right context
- Causal LM (unidirectional): Used in GPT family - only sees left context
- Context: MLM is better for understanding tasks; causal LM is required for generation

---

**Status**: New (from sync - BERT paper)  
**Last Updated**: 2026-04-20  
**Source**: BERT paper (Devlin et al., 2019)
```

## Syncing Tips

- ✓ Skim existing wiki pages before writing
- ✓ Link liberally - you can add stubs and fill them later
- ✓ Include examples from the source paper
- ✓ Note publication date (helps identify stale vs. current understanding)
- ✓ Mark new pages with "New (from sync)" so they're easy to find
