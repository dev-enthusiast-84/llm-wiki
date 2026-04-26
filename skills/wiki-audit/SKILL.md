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

### 1. Build Link Graph

List every `.md` file in `wiki/` except `index.md` and `log.md`. For each page collect:
- All `[[bracket]]` outbound links
- All source citations (paper title + year) from `## Sources`

This produces the entity list and link map needed by the parallel agents.

### 2. Spawn Parallel Audit Agents

Call the Agent tool four times in a **single response** — all four run simultaneously.

**Agent 1 — Orphan Check** (`subagent_type: "Explore"`): Read all wiki entity pages. Identify pages with zero inbound `[[bracket]]` references from other pages. For each orphan, suggest the 1–2 most related pages that should add a backlink.

**Agent 2 — Missing Pages** (`subagent_type: "Explore"`): Read all wiki entity pages. Collect every `[[concept]]` bracket reference. Compare referenced concepts against existing `.md` filenames. List every missing concept, grouped by how many pages reference it (most-referenced first).

**Agent 3 — Contradictions** (`subagent_type: "Explore"`): Read all wiki entity pages. For concepts appearing in multiple pages, compare definitions and core claims. Identify conflicting statements or incompatible claims. Return: which pages conflict, what the conflicting claims are, which sources support each.

**Agent 4 — Stale Claims** (`subagent_type: "Explore"`): Read all wiki entity pages and `wiki/log.md`. For each page, check the publication years of cited sources. Cross-reference against newer sources in `wiki/log.md`. Flag pages whose core claims rely solely on older sources when newer papers already exist.

### 3. Apply Fixes

Wait for all four agents to complete, then:
- **Apply confidently**: add backlinks for orphans, create stub pages for top-priority missing concepts, update `wiki/index.md`
- **Flag for review**: contradictions and stale claims requiring subject-matter judgment

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
