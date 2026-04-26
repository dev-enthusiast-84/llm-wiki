---
description: Audit entire wiki for quality issues. Check for orphan pages, missing linked concepts, contradictions, and stale claims. Run when wiki reaches ~20 pages.
---

## Usage

**Invoke:** type `/audit-wiki` in the Claude Code CLI  
**When to run:** every ~20–30 new pages, after a large sync batch, or before publishing/sharing  
**Prerequisites:** `wiki/` must contain entity pages (`/compile-papers` has been run at least once)  
**Arguments:** optionally pass a category or page name to scope the audit  
**Example:** `/audit-wiki contradictions` — only run the contradictions check  

---

## Step 1: Build Link Graph

List every `.md` file in `wiki/` except `index.md` and `log.md`. For each page collect:
- All `[[bracket]]` outbound links
- All source citations (paper title + year) from the `## Sources` section

This produces the complete entity list and link graph needed by the parallel agents below.

## Step 2: Spawn Parallel Audit Agents

Call the Agent tool four times in a **single response** — all four run simultaneously.

**Agent 1 — Orphan Check**
`subagent_type: "Explore"` — prompt: "Read all `.md` files in `wiki/` (exclude `index.md` and `log.md`). For each page scan every `[[bracket]]` reference made by other pages. Identify pages that appear in zero inbound references — these are orphans. For each orphan suggest the 1–2 most related pages that should add a backlink to it. Return a list of orphan filenames and suggested backlink sources."

**Agent 2 — Missing Pages**
`subagent_type: "Explore"` — prompt: "Read all `.md` files in `wiki/` (exclude `index.md` and `log.md`). Collect every `[[concept]]` bracket reference found across all pages. Compare each referenced concept against the list of existing `.md` filenames in `wiki/`. Identify every concept that is referenced but has no corresponding file. Group results by how many pages reference each missing concept (most-referenced first). Return the list."

**Agent 3 — Contradictions**
`subagent_type: "Explore"` — prompt: "Read all `.md` files in `wiki/` (exclude `index.md` and `log.md`). For concepts that appear in multiple pages compare their definitions and core claims. Identify conflicting statements: different definitions of the same term, incompatible claims, or disagreements between cited sources. For each contradiction return: which pages conflict, what the conflicting claims are, and which sources support each."

**Agent 4 — Stale Claims**
`subagent_type: "Explore"` — prompt: "Read all `.md` files in `wiki/` (exclude `index.md` and `log.md`) and `wiki/log.md`. For each entity page check the publication years of sources listed in its `## Sources` section. Cross-reference against newer sources recorded in `wiki/log.md`. Flag pages whose core claims rely solely on older sources when newer papers already exist in the wiki. Return a prioritised list of pages that need updating."

## Step 3: Apply Fixes

Wait for all four agents to complete, then:
- **Apply confidently**: add backlinks for orphans, create stub pages for the top-priority missing concepts, update `wiki/index.md`
- **Flag for review**: contradictions and stale claims where subject-matter judgment is required

Use the [Audit Checklist](../skills/wiki-audit/references/audit-checklist.md) and [Report Template](../skills/wiki-audit/assets/audit-report.md) for guidance.

---

## Verification Steps

After the skill completes, confirm success by checking:

1. **Orphans resolved**: open each formerly-orphan page and confirm at least one other page now links to it
2. **Missing pages addressed**: `ls wiki/*.md` — stub pages should now exist for high-priority missing concepts
3. **Contradictions documented**: open affected pages and confirm a `## Contradictions` section exists with both viewpoints cited
4. **Index consistent**: `wiki/index.md` should list every entity page including any new stubs
5. **No new broken links**: confirm any new stubs have at least a `## Summary` and `## Sources` section

---

## Results Summary

Once all steps are complete, output this exact block:

```
✅ Audit Wiki — complete  YYYY-MM-DD

🔍 Findings:
   Orphan pages:        N  (list filenames, or "none")
   Missing pages:       N  (list concept names, or "none")
   Contradictions:      N  (list affected pages, or "none")
   Stale claims:        N  (list affected pages, or "none")

🔧 Auto-fixed: N issues
   ✓ Added backlink X → Y
   ✓ Created stub wiki/missing-concept.md
   ...

📌 Needs manual review: N issues
   ! wiki/concept.md — contradiction between "Source A" and "Source B" on definition of Z
   ! wiki/old-claim.md — relies solely on 2018 paper; check against newer sources in /raw
   ...

📋 wiki/index.md  — updated (stubs added) / no changes
📋 wiki/log.md    — unchanged (audit does not add log rows)

🔍 Verification: open each flagged page and confirm the Contradictions section is populated.
➡️  Next step: resolve manual-review items, then commit with
    git add wiki/ && git commit -m "Wiki audit: fix orphans, contradictions, stale claims"
```

$ARGUMENTS
