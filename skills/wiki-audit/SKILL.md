---
name: wiki-audit
description: 'Audit wiki for quality issues. Use when wiki reaches ~20+ pages: find orphan pages, missing linked concepts, contradictions, stale claims from old sources. Identify and fix inconsistencies.'
argument-hint: 'Optional: specific areas to audit'
---

# Wiki Audit

Comprehensive quality check of the wiki structure and content. Run this maintenance task when wiki reaches ~20 pages.

## When to Use

- **Periodic maintenance**: Every ~20-30 new pages (roughly monthly for active projects)
- **After major updates**: After syncing large batches of new sources
- **Before releases**: Before publishing or sharing wiki
- **Content review**: Ensure consistency and accuracy across entries

## Procedure

### 1. Identify Orphan Pages

Pages that no other page links to:
- Scan all files in `wiki/` for `[[references]]`
- Find pages with zero inbound links
- Check if orphan is truly standalone or should be linked

### 2. Find Missing Pages

Concepts referenced but without their own page:
- Search for `[[concept]]` patterns across all pages
- Extract all referenced concepts
- Compare against existing filenames
- Create list of missing pages to add

### 3. Detect Contradictions

Claims that conflict across pages:
- Compare definitions of the same concept across multiple pages
- Look for conflicting explanations or different approaches
- Check Sources sections for conflicting papers
- Review any explicit "Contradictions" sections

### 4. Flag Stale Claims

Outdated information that may be superseded:
- Cross-reference claims with dates in `/raw` folder
- Identify papers that update or contradict earlier sources
- Check if Source citations are from older papers
- Note if multiple versions of a concept exist (old vs. new understanding)

### 5. Suggest and Apply Fixes

For each issue found:
- **Orphans**: Add backlinks from related pages or remove if truly irrelevant
- **Missing pages**: Create new files or update references to clarify
- **Contradictions**: Add "Contradictions" section noting differences and citing sources
- **Stale claims**: Update with newer information, add note about evolution of understanding

See [Audit Checklist](./references/audit-checklist.md) for detailed verification steps.

## Example Issues & Fixes

| Issue | Detection | Fix |
|-------|-----------|-----|
| Orphan: `transformer-variants.md` | No other page links to it | Add reference in `[[transformer]]` page's related concepts |
| Missing: `attention-mechanism` | Appears in 5 pages as `[[attention-mechanism]]` but no page exists | Create `attention-mechanism.md` and update sources |
| Contradiction | `bert.md` says "unidirectional" but `bidirectional-encoder.md` says "bidirectional" | Add Contradictions section clarifying they refer to same concept |
| Stale | `gpt-3.md` cites 2020 paper but `/raw` has 2023 GPT-4 paper | Update with newer source, note progression |

## Output

Generate a report including:
- Count of orphan pages
- List of missing pages to create
- Table of contradictions with locations
- List of potentially stale claims
- Recommended fixes (applied where confident, pending approval where not)

See [Audit Report Template](./assets/audit-report.md).

## Tips

- **Link liberally**: Orphans often indicate connections that should be made explicit
- **Contradictions aren't bad**: Different sources may define same concepts differently; document this nuance
- **Source tracking**: Pages with multiple sources are less likely to be stale
- **Iterative**: You may need to create missing pages before all links resolve
