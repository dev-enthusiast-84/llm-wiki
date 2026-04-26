---
name: orchestrate-wiki
description: 'Run the full wiki pipeline in one command: detect wiki state, compile or sync all sources using parallel agents, audit quality with parallel agents, and sync docs. One command to refresh everything.'
argument-hint: 'No argument needed — wiki state is detected automatically'
---

# Orchestrate Wiki

Run the complete wiki maintenance pipeline from a single command. Detects current wiki state, processes all uncompiled sources, audits quality, and updates all doc surfaces. Each phase uses parallel agents internally.

## When to Use

- After dropping several new papers into `/raw` and wanting a full refresh
- As a scheduled weekly or monthly maintenance routine
- When you want a single command to bring the wiki and docs fully up to date

## Phase 1: Detect Wiki State

```bash
ls wiki/*.md 2>/dev/null | grep -v -e index.md -e log.md | wc -l
```

- **0 entity pages** → wiki is empty; run the compile-papers pipeline (Phase 2a)
- **1+ entity pages** → wiki has content; run the sync-wiki pipeline (Phase 2b)

Announce the detected state before proceeding.

## Phase 2a: Compile (empty wiki)

Follow the `/compile-papers` procedure:
1. Pre-flight check confirms wiki is empty
2. Scan `/raw` for all supported source files
3. Spawn one `Explore` sub-agent per source file in a single response (parallel extraction)
4. Collect results, merge concept lists, flag cross-source contradictions
5. Write entity pages, update `wiki/index.md` and `wiki/log.md`

Wait for Phase 2a to complete before proceeding to Phase 3.

## Phase 2b: Sync (existing wiki)

Follow the `/sync-wiki` procedure:
1. Detect unsynced files (in `raw/` but not in `wiki/log.md`)
2. If no new files: report "Wiki is up to date" and skip to Phase 3
3. If multiple new files: spawn one `Explore` sub-agent per file in a single response (parallel extraction)
4. Collect results, update existing pages, create new pages, update index and log

Wait for Phase 2b to complete before proceeding to Phase 3.

## Phase 3: Audit Quality

Follow the `/audit-wiki` procedure:
1. Build link graph from all entity pages
2. Spawn four `Explore` sub-agents in a single response (parallel audit):
   - Orphan check
   - Missing pages
   - Contradictions
   - Stale claims
3. Wait for all four agents, then apply confident fixes and flag items for manual review

Wait for Phase 3 to complete before proceeding to Phase 4.

## Phase 4: Sync Docs

Follow the `/sync-docs` procedure to update all doc surfaces that changed during this run:
- `README.md`
- `docs/index.html`
- `copilot-instructions.md`
- Any sub-READMEs affected by structural changes

## Results Summary

Output a combined report:

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

## Relation to Other Skills

| Skill | Role in this pipeline |
|-------|-----------------------|
| `compile-papers` | Phase 2a — used when wiki is empty |
| `sync-wiki` | Phase 2b — used when wiki has existing content |
| `audit-wiki` | Phase 3 — quality check after source processing |
| `sync-docs` | Phase 4 — keeps README, GitHub Pages, and Copilot instructions current |
