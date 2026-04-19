# Wiki Log Format

Track wiki changes over time for reference and audit purposes. Create `wiki/log.md` when wiki reaches 30+ pages.

## Log Structure

```markdown
# Wiki Compilation Log

This log tracks which sources are compiled and what changes were made.

## Summary

- **Total pages**: [N]
- **Last updated**: [DATE]
- **Last source**: [SOURCE]

## Compilation History

| Date | Source | New Entities | Updated Entities | Notes |
|------|--------|---|---|---|
| 2026-04-20 | "Attention is All You Need" (Vaswani et al., 2017) | self-attention, scaled-dot-product-attention, multi-head-attention | transformer | Core transformer concepts |
| 2026-04-20 | "BERT: Pre-training" (Devlin et al., 2019) | masked-language-model, next-sentence-prediction, bert | pre-training-fine-tuning, encoder-decoder | Contradiction noted: bidirectional vs unidirectional |
| | | | | |

## Legend

- **New Entities**: Concepts that didn't have pages before this sync
- **Updated Entities**: Existing pages modified due to new source information
- **Notes**: Contradictions discovered, important clarifications, or special updates
```

## Log Entry Guidelines

### Date Format
- Use: `YYYY-MM-DD` (e.g., `2026-04-20`)

### Source Format
- Format: `"[FULL TITLE]" ([AUTHOR/AUTHORS], [YEAR])`
- Examples:
  - `"Attention is All You Need" (Vaswani et al., 2017)`
  - `"BERT: Pre-training of Deep Bidirectional Transformers" (Devlin et al., 2019)`
  - `"Language Models are Few-Shot Learners" (Brown et al., 2020)`

### New Entities (comma-separated)
- List all pages created: `concept1, concept2, concept3`
- Or leave blank if only updating existing pages

### Updated Entities (comma-separated)
- List all pages modified: `concept1, concept2`
- Or leave blank if only adding new pages

### Notes Column
- **Contradictions**: "Contradiction noted: Paper defines X differently than Y"
- **Major discovery**: "Introduces new paradigm for understanding X"
- **Stale info updated**: "Previous understanding superseded by new findings"
- **Complex relationship**: "Clarified relationship between X and Y"
- Leave blank if no notable issues

## Example Log Entry

```markdown
| 2026-04-22 | "The Scaling Laws for Language Models" (Hoffmann et al., 2022) | scaling-laws | transformer, pre-training-fine-tuning | Documents how performance scales with model/data size |
```

## Querying the Log

Use the log to:
- **Find source of concept**: Search concept name in "New Entities" column
- **Track contradictions**: Search notes for "Contradiction"
- **Find related papers**: Look for papers citing same concepts
- **Update frequency**: Check dates to see when wiki was last updated

## Maintenance

- Add entry every time you sync a new source
- Review notes monthly to identify (and resolve) contradictions
- Update "Last updated" and "Total pages" in summary regularly
