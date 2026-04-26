---
mode: agent
description: Run the full wiki pipeline in one command — detect wiki state, compile or sync all sources with parallel agents, audit quality with parallel agents, then sync docs.
---

Run the complete wiki maintenance pipeline end-to-end.

## Phase 1: Detect Wiki State

```bash
ls wiki/*.md 2>/dev/null | grep -v -e index.md -e log.md | wc -l
```

- **0 entity pages** → compile (Phase 2a)
- **1+ entity pages** → sync (Phase 2b)

## Phase 2a: Compile

List all supported files in `raw/`. Spawn one `Explore` sub-agent per file in a **single response** (all parallel). Each agent reads its file (Read tool for PDF/TXT/HTML; bash for PPTX/DOCX/XLSX) and returns structured concept extractions. Wait for all agents, merge results, write entity pages, update `wiki/index.md` and `wiki/log.md`.

## Phase 2b: Sync

Find files in `raw/` not yet in `wiki/log.md`. If none: report up to date and skip to Phase 3. If new files exist, spawn one `Explore` sub-agent per new file in a **single response** (all parallel). Collect results, update existing pages, create new ones, update index and log.

## Phase 3: Audit

Spawn four `Explore` sub-agents in a **single response**:
- **Orphans**: find pages with zero inbound links; suggest backlinks
- **Missing pages**: find `[[concepts]]` with no file; rank by reference count
- **Contradictions**: compare definitions across pages; identify conflicts
- **Stale claims**: find pages relying only on older sources when newer ones exist

Apply confident fixes; flag uncertain issues for review.

## Phase 4: Sync Docs

Update `README.md`, `docs/index.html`, and `copilot-instructions.md` to reflect any structural changes from this run. Read each surface before editing; make targeted updates only.

## Output

```
✅ Orchestrate Wiki — complete  YYYY-MM-DD

Phase 1 — State:    <empty wiki | wiki had N pages>
Phase 2 — Sources:  <compiled N | synced N new | up to date>
   Entity pages created: N  |  updated: N
Phase 3 — Audit:    orphans N  missing N  contradictions N  stale N
Phase 4 — Docs:     <N surfaces updated | no changes>

⚠️  Manual review: N items  (list each)

➡️  Next: commit with  git add wiki/ docs/ README.md copilot-instructions.md
```
