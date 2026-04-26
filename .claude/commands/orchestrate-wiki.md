---
description: Run the full wiki pipeline in one command — detect wiki state, compile or sync all sources with parallel agents, audit quality with parallel agents, then sync docs.
---

## Usage

**Invoke:** type `/orchestrate-wiki` in Claude Code CLI  
**When to run:** after adding papers to `/raw`, or as a periodic full refresh  
**Prerequisites:** Python 3 installed; run from repo root  
**Arguments:** none required  
**Tip:** This runs the full pipeline end-to-end. For targeted updates use `/compile-papers`, `/sync-wiki`, or `/audit-wiki` individually.

---

## Phase 1: Detect Wiki State

```bash
ls wiki/*.md 2>/dev/null | grep -v -e index.md -e log.md | wc -l
```

- **0 entity pages** → proceed to Phase 2a (compile)
- **1+ entity pages** → proceed to Phase 2b (sync)

Announce the detected state.

---

## Phase 2a: Compile (empty wiki)

1. Confirm wiki is empty (no entity pages other than `index.md` / `log.md`)
2. List all supported files in `raw/` (`.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`)
3. Spawn one `Explore` sub-agent per source file in a **single response** (all in parallel). Each agent reads its file using the appropriate method and returns: concept names, definitions, related concepts, and conflicting definitions. See `/compile-papers` for per-format read methods.
4. Wait for all agents to complete. Merge concept lists; flag cross-source contradictions.
5. Create entity pages in `wiki/`, update `wiki/index.md` and `wiki/log.md`

---

## Phase 2b: Sync (existing wiki)

1. List all files in `raw/` with supported extensions
2. Read `wiki/log.md` — find files not yet in the Source column
3. If no new files: report "Wiki is up to date" and skip to Phase 3
4. If new files exist: spawn one `Explore` sub-agent per new file in a **single response** (all in parallel). Each agent reads its file and returns: concepts introduced, existing wiki pages to update, proposed changes. See `/sync-wiki` for per-format read methods.
5. Wait for all agents. Update existing entity pages, create new ones, update `wiki/index.md` and `wiki/log.md`

---

## Phase 3: Audit Quality

1. List all entity pages in `wiki/` and collect their `[[bracket]]` links and source citations
2. Spawn four `Explore` sub-agents in a **single response**:

   **Agent 1 — Orphan Check**: find pages with zero inbound links; suggest backlinks from related pages  
   **Agent 2 — Missing Pages**: find `[[concepts]]` referenced but without a `.md` file; rank by reference count  
   **Agent 3 — Contradictions**: compare definitions across pages; identify conflicting claims and their sources  
   **Agent 4 — Stale Claims**: find pages relying solely on older sources when newer papers exist in the wiki

3. Wait for all four agents. Apply confident fixes (backlinks, stub pages, index updates). Flag contradictions and stale claims for manual review.

---

## Phase 4: Sync Docs

Update all doc surfaces changed during this run. Read current state of each surface, then apply targeted edits:

| Surface | Path |
|---------|------|
| Root README | `README.md` |
| GitHub Pages | `docs/index.html` |
| Copilot workspace | `copilot-instructions.md` |

See `/sync-docs` for the change-to-surface mapping and update rules.

---

## Verification Steps

1. `wiki/log.md` — new source rows appear with today's date
2. `wiki/index.md` — all new concepts listed under appropriate categories
3. `reports/` — no new maintenance report needed (run `/run-maintenance` separately for health checks)
4. Flagged items — at least one `## Contradictions` section or stale-claim note exists where issues were found

---

## Results Summary

Output this exact block when complete:

```
✅ Orchestrate Wiki — complete  YYYY-MM-DD

Phase 1 — State:    <empty wiki | wiki had N pages>
Phase 2 — Sources:  <compiled N files | synced N new files | up to date>
   Entity pages created:  N
   Entity pages updated:  N
Phase 3 — Audit:
   Orphans resolved:       N
   Stubs created:          N
   Contradictions flagged: N
   Stale claims flagged:   N
Phase 4 — Docs:     <N surfaces updated | no changes>

⚠️  Manual review needed: N items
   <list each flagged contradiction or stale claim>

➡️  Next step: review flagged items, then commit with
    git add wiki/ docs/ README.md copilot-instructions.md
    git commit -m "Wiki refresh: <summary>"
```
