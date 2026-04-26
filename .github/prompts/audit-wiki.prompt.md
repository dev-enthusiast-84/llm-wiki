---
mode: agent
description: Audit entire wiki for quality issues. Check for orphan pages, missing linked concepts, contradictions, and stale claims. Run when wiki reaches ~20 pages.
---

Audit the entire `wiki/` folder using parallel agents.

## Step 1: Build Link Graph

List every `.md` file in `wiki/` except `index.md` and `log.md`. Collect all `[[bracket]]` outbound links and source citations per page.

## Step 2: Spawn Parallel Audit Agents

Call the Agent tool four times in a **single response** — all four run simultaneously.

**Agent 1 — Orphan Check** (`subagent_type: "Explore"`): Read all wiki entity pages. Find pages with zero inbound `[[bracket]]` references. For each orphan, suggest the 1–2 most related pages that should link to it.

**Agent 2 — Missing Pages** (`subagent_type: "Explore"`): Read all wiki entity pages. Collect every `[[concept]]` reference. Compare against existing filenames. List missing concepts sorted by how many pages reference them (most-referenced first).

**Agent 3 — Contradictions** (`subagent_type: "Explore"`): Read all wiki entity pages. For concepts in multiple pages, identify conflicting definitions or incompatible claims. Return: which pages conflict, the conflicting claims, and which sources support each.

**Agent 4 — Stale Claims** (`subagent_type: "Explore"`): Read all wiki entity pages and `wiki/log.md`. Flag pages whose core claims rely solely on older sources when newer papers already exist in the wiki.

## Step 3: Apply Fixes

Wait for all four agents, then apply confident fixes (backlinks, stub pages, index updates) and flag uncertain issues (contradictions, stale claims) for manual review.

Use the [Audit Checklist](../../skills/wiki-audit/references/audit-checklist.md) and [Report Template](../../skills/wiki-audit/assets/audit-report.md).

## Output

After all steps, emit this results block:

```
✅ Audit Wiki — complete  YYYY-MM-DD

🔍 Findings:
   Orphan pages:        N  (list filenames, or "none")
   Missing pages:       N  (list concept names, or "none")
   Contradictions:      N  (list affected pages, or "none")
   Stale claims:        N  (list affected pages, or "none")

🔧 Auto-fixed: N issues
📌 Needs manual review: N issues (list each with page + issue description)

📋 wiki/index.md  — updated (stubs added) / no changes
📋 wiki/log.md    — unchanged (audit does not add log rows)

➡️  Next step: resolve manual-review items, then commit with
    git add wiki/ && git commit -m "Wiki audit: fix orphans, contradictions, stale claims"
```
