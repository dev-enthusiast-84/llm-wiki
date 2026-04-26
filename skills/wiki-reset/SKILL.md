---
name: wiki-reset
description: 'Prepare the wiki for a fresh start or smart update. Detects current wiki state and routes to the right workflow: clean start for empty wikis, sync for existing content, or forced reset when explicitly requested.'
argument-hint: 'reset or --force (optional: wipe all pages)'
---

# Wiki Reset

Guard-rail and entry point for all wiki workflows. Inspects the wiki state before any compilation or sync begins, and routes the user to the correct path.

## When to Use

- **Before your first compile-papers run**: Ensure `wiki/` is clean and scaffolded
- **Before adding a new paper**: Check if sync or reset is the right move
- **When wiki feels stale or broken**: Force-reset to start over without manual cleanup
- **Any time you're unsure of wiki state**: Use this as a diagnostic first step

## Procedure

### 1. Detect State

List all `.md` files in `wiki/`. Classify them:
- **Structural files**: `index.md`, `log.md` (always kept)
- **Entity pages**: everything else

If no entity pages exist → **Path A (Clean)**
If entity pages exist + no `reset`/`--force` argument → **Path B (Redirect)**
If entity pages exist + `reset` or `--force` argument → **Path C (Force Reset)**

### 2a. Path A — Clean Start

1. Create `wiki/index.md` from [empty-index-template.md](./assets/empty-index-template.md) if missing
2. Create `wiki/log.md` from [empty-log-template.md](./assets/empty-log-template.md) if missing
3. Confirm ready state to user

### 2b. Path B — Redirect to Correct Skill

1. Summarize current wiki: page count, categories
2. Tell the user clearly:
   - **New paper to add** → `/sync-wiki`
   - **Want to wipe everything** → `/reset-wiki reset`
3. Do not modify any files

### 2c. Path C — Force Reset

1. Delete all entity pages (every `.md` in `wiki/` except `index.md` and `log.md`)
2. Overwrite `wiki/index.md` with the empty index template
3. Overwrite `wiki/log.md` with the empty log template
4. Confirm to user how many pages were removed

## Argument

| Value | Effect |
|-------|--------|
| *(none)* | Detect state, redirect if content exists |
| `reset` | Force-wipe all entity pages |
| `--force` | Same as `reset` |

## Reference Files

- [Empty Index Template](./assets/empty-index-template.md)
- [Empty Log Template](./assets/empty-log-template.md)
- [Reset Checklist](./references/reset-checklist.md)

## Skill Flow Diagram

```
/reset-wiki
    │
    ├─ wiki/ empty? ──── Yes ──→ Path A: scaffold + confirm ready
    │
    └─ wiki/ has pages?
           │
           ├─ no "reset" arg ──→ Path B: summarize + offer /sync-wiki or /reset-wiki reset
           │
           └─ "reset" arg ────→ Path C: delete pages, reset templates, confirm
```

## Relation to Other Skills

| Skill | When to Use |
|-------|-------------|
| `/reset-wiki` | Always run first to understand wiki state |
| `/compile-papers` | After reset or on an empty wiki |
| `/sync-wiki` | When wiki has content and you want incremental updates |
| `/audit-wiki` | After 20+ pages to check quality |
