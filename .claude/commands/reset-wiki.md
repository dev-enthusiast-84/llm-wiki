---
description: Prepare the wiki for a fresh start or redirect to sync-wiki if content exists. Pass "reset" to force-wipe all pages.
---

## Usage

**Invoke:** type `/reset-wiki` in the Claude Code CLI  
**When to run:** when you want to wipe everything and start over, or to confirm the wiki is in a clean initial state  
**Prerequisites:** none — safe to run on an empty or populated wiki  
**Arguments:**
- *(none)* — inspect state, report options, do not delete anything
- `reset` or `--force` — delete all entity pages and reset index/log to blank templates

**Example:** `/reset-wiki reset`  
⚠️ The `reset` argument is irreversible — all entity pages will be permanently deleted.

---

## Step 1: Inspect current wiki state

List all `.md` files in `wiki/`. Entity pages are any files other than `index.md` and `log.md`.

Count the entity pages and note the topics from `wiki/index.md` if it exists.

## Step 2: Choose the correct path

### Path A — Wiki is empty (no entity pages)

1. Ensure `wiki/index.md` exists with the clean index template (create if missing)
2. Ensure `wiki/log.md` exists with the clean log template (create if missing)
3. Report: "Wiki is clean and ready. Run `/compile-papers` with your source material."

### Path B — Wiki has content, no reset argument given

1. Report a summary of current state:
   - Number of entity pages
   - Topics/categories present (from index.md)
2. Present the user with their options:
   - **To add new papers**: run `/sync-wiki` — preserves existing pages and updates them incrementally
   - **To start over completely**: run `/reset-wiki reset` — removes all pages and resets to a blank state
3. Do NOT delete or modify any files. Stop and wait for the user to choose.

### Path C — Argument is `reset` or `--force`

1. Delete every `.md` file in `wiki/` except `index.md` and `log.md`
2. Overwrite `wiki/index.md` with the clean index template below
3. Overwrite `wiki/log.md` with the clean log template below
4. Report the Results Summary

## Templates

### Clean index.md

```markdown
# LLM Wiki Index

A structured knowledge base of concepts in large language models, agentic AI, and related systems.

*No entities yet. Run `/compile-papers` to get started.*

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

---

## Verification Steps

After Path C (reset) completes, confirm success by:

1. **Only two files remain**: `ls wiki/*.md` should return only `wiki/index.md` and `wiki/log.md`
2. **Index is clean**: open `wiki/index.md` and confirm it shows the "No entities yet" placeholder
3. **Log is clean**: open `wiki/log.md` and confirm Total pages is 0 and the history table is empty
4. **No entity files**: `ls wiki/ | grep -v "index.md\|log.md"` should return nothing

---

## Results Summary

Once all steps are complete, output this exact block:

**Path A (already empty):**
```
✅ Reset Wiki — wiki is already clean  YYYY-MM-DD

📋 wiki/index.md  — present and clean
📋 wiki/log.md    — present and clean

🔍 Verification: run  ls wiki/*.md  — should show only index.md and log.md
➡️  Next step: add source files to raw/ then run /compile-papers
```

**Path B (content exists, no reset argument):**
```
ℹ️  Reset Wiki — wiki has content, no action taken

📄 Entity pages found: N
   wiki/concept-a.md
   wiki/concept-b.md
   ...

   Options:
   • /sync-wiki          — add new sources, keep existing pages
   • /reset-wiki reset   — wipe all N pages and start fresh (irreversible)
```

**Path C (reset executed):**
```
✅ Reset Wiki — complete  YYYY-MM-DD

🗑️  Pages removed: N
   wiki/concept-a.md
   wiki/concept-b.md
   ...

📋 wiki/index.md  — reset to clean template
📋 wiki/log.md    — reset to clean template

🔍 Verification: run  ls wiki/*.md  — should show only index.md and log.md
➡️  Next step: add source files to raw/ then run /compile-papers
```

$ARGUMENTS
