---
mode: agent
description: Sync all repo documentation after code changes. Detects changed files via git, maps them to affected doc surfaces, and updates README, GitHub Pages, copilot-instructions, and sub-READMEs automatically.
---

## Step 1: Detect what changed

Run these two commands:
```
git diff --name-only HEAD
git status --short
```

Combine both outputs (diff shows staged/unstaged changes; status catches new untracked files).

Group changed files into these categories:

| Category | Paths |
|----------|-------|
| **skills-commands** | `.claude/commands/**`, `.github/prompts/**`, `skills/**` |
| **presentation** | `presentation/**` |
| **extensions** | `extensions/**` |
| **wiki** | `wiki/**` |
| **raw** | `raw/**` |
| **core-docs** | `README.md`, `docs/index.html`, `copilot-instructions.md` |

Announce the grouped change list before making any edits.

If no relevant changes are detected: report "No documentation-affecting changes found." and stop.

---

## Step 2: Update affected doc surfaces

Work through each affected category. Read the current doc, compare to reality, apply minimum necessary edits.

### Category: skills-commands

**Affected surfaces**: `copilot-instructions.md`, `README.md`, `docs/index.html`

1. Read all `.claude/commands/*.md` — collect name and description of each
2. Update `copilot-instructions.md`:
   - Add/update/remove entries in `## Available Prompts`
   - Update the workflow table if commands changed
   - Update the prompt-file ↔ Claude command mapping table
3. Update `README.md`:
   - Update the commands table
   - Update folder structure if new skill folders were added
4. Update `docs/index.html`:
   - Add/update/remove `.tool-card` blocks in the `#tools` section
   - Update the stat for skill count in the stats bar if it changed
   - Preserve existing HTML class names and card structure

### Category: presentation

Read changed `presentation/**` files, then update `README.md` → `## Presentation` section — slide structure, file list, quick-start instructions.

If `presentation/generate_presentation.py` or `presentation/generate_demo_videos.py` changed, remind the user to run `Regenerate Presentation` to rebuild stale video or deck assets.

### Category: extensions

Read changed `extensions/**` files, then update `extensions/README.md` — setup instructions, tool list.

### Category: wiki

Only update `README.md` or `docs/index.html` if structural wiki changes (e.g., new index categories) should be reflected there. Entity page changes belong to `Sync Wiki from Raw`.

### Category: raw

If new files were added to `raw/`, remind the user to run `Sync Wiki from Raw` to incorporate them.

### Category: core-docs

If `README.md`, `docs/index.html`, or `copilot-instructions.md` changed, check whether those changes should cascade to the other surfaces.

---

## Step 3: Report

After all updates, produce a summary table:

| Doc surface | Status | Changes made |
|-------------|--------|--------------|
| `copilot-instructions.md` | Updated / Already up to date | … |
| `README.md` | Updated / Already up to date | … |
| `docs/index.html` | Updated / Already up to date | … |
| `presentation/README.md` | Updated / Skipped | … |
| `extensions/README.md` | Updated / Skipped | … |

Flag anything requiring manual review.

---

## Safety rules

- Never delete a doc entry without confirming the underlying skill was intentionally removed
- Never rewrite entire doc surfaces — targeted edits only
- Never touch `wiki/index.md`, `wiki/log.md`, or entity pages — those belong to other skills
