---
mode: agent
description: Prepare the wiki for a fresh start or redirect to sync-wiki if content exists. Pass "reset" to force-wipe all pages.
---

Prepare the wiki for use. Follow this decision tree exactly:

## Step 1: Inspect current wiki state

List all `.md` files in `wiki/`. Entity pages are any files other than `index.md` and `log.md`.

Count the entity pages and note the topics from `wiki/index.md` if it exists.

## Step 2: Choose the correct path

### Path A — Wiki is empty (no entity pages)

1. Ensure `wiki/index.md` exists with the clean index template (create if missing)
2. Ensure `wiki/log.md` exists with the clean log template (create if missing)
3. Report: "Wiki is clean and ready. Run `Compile Papers to Wiki` with your source material."

### Path B — Wiki has content, no reset argument given

1. Report a summary of current state:
   - Number of entity pages
   - Topics/categories present (from index.md)
2. Present the user with their options:
   - **To add new papers**: Run `Sync Wiki from Raw` — preserves existing pages and updates them incrementally
   - **To start over completely**: Re-run this prompt with `reset` in your message — removes all pages and resets to a blank state
3. Do NOT delete or modify any files. Stop and wait for the user to choose.

### Path C — Message contains "reset" or "--force"

1. Delete every `.md` file in `wiki/` except `index.md` and `log.md`
2. Overwrite `wiki/index.md` with the clean index template below
3. Overwrite `wiki/log.md` with the clean log template below
4. Report: "Wiki has been reset. All [N] pages removed. Run `Compile Papers to Wiki` to start fresh."

## Templates

### Clean index.md

```markdown
# LLM Wiki Index

A structured knowledge base of concepts in large language models, agentic AI, and related systems.

*No entities yet. Run `Compile Papers to Wiki` to get started.*

---

*Last updated: YYYY-MM-DD*
```

### Clean log.md

```markdown
# Wiki Compilation Log

Tracks which sources were compiled and what changed each time.

## Summary

- **Total pages**: 0
- **Last updated**: —
- **Last source**: —

## Compilation History

| Date | Source | New Entities | Updated Entities | Notes |
|------|--------|---|---|---|
```

See [Reset Skill](../../skills/wiki-reset/SKILL.md) and [Reset Checklist](../../skills/wiki-reset/references/reset-checklist.md) for detailed guidance.

## Output

After completing, emit the appropriate results block:

**Path A (already empty):**
```
✅ Reset Wiki — wiki is already clean  YYYY-MM-DD
📋 wiki/index.md — present and clean
📋 wiki/log.md   — present and clean
➡️  Next step: add source files to raw/ then run Compile Papers to Wiki
```

**Path B (content exists, no reset argument):**
```
ℹ️  Reset Wiki — wiki has content, no action taken
📄 Entity pages found: N  (list filenames)
   Options:
   • Sync Wiki from Raw    — add new sources, keep existing pages
   • Reset Wiki reset      — wipe all N pages and start fresh (irreversible)
```

**Path C (reset executed):**
```
✅ Reset Wiki — complete  YYYY-MM-DD
🗑️  Pages removed: N  (list filenames)
📋 wiki/index.md — reset to clean template
📋 wiki/log.md   — reset to clean template
➡️  Next step: add source files to raw/ then run Compile Papers to Wiki
```
