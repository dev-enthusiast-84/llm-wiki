---
description: Sync all repo documentation after code changes. Detects changed files via git, maps them to affected doc surfaces, and updates README, GitHub Pages, copilot-instructions, and sub-READMEs automatically.
---

## Usage

**Invoke:** type `/sync-docs` in the Claude Code CLI  
**When to run:** after adding, modifying, or removing a skill, command, configuration file, or any change that should be reflected in the project's documentation  
**Prerequisites:** git must be initialised and the working tree must have staged or unstaged changes (or use `--all` to force a full scan)  
**Arguments:**
- *(none)* — detect changes via `git diff` and update only affected surfaces
- `--all` — scan every doc surface regardless of git diff (use after a large reorganisation)

**Tip:** run `/sync-docs` as the final step before every commit that touches `.claude/commands/`, `skills/`, `presentation/`, or `wiki_query.py`.

---

## Step 1: Detect what changed

Run these two commands:
```bash
git diff --name-only HEAD
git status --short
```

Combine both outputs (diff shows staged/unstaged changes; status catches new untracked files).

Group changed files into these categories:

| Category | Paths |
|----------|-------|
| **skills-commands** | `.claude/commands/**`, `skills/**` |
| **ui** | `wiki_query.py`, `tests/**` |
| **presentation** | `presentation/**` |
| **extensions** | `extensions/**` |
| **wiki** | `wiki/**` |
| **raw** | `raw/**` |
| **core-docs** | `README.md`, `copilot-instructions.md` |

Announce the grouped change list before making any edits.

If no relevant changes are detected: report **"No documentation-affecting changes found."** and stop.

---

## Step 2: Update affected doc surfaces

Work through each affected category. For each one, read the current doc surface, compare to reality, and apply the **minimum necessary edits**.

### Category: skills-commands

**Affected surfaces**: `copilot-instructions.md`, `README.md`

1. Read all `.claude/commands/**/*.md` — collect name and `description` frontmatter of each
2. Read `copilot-instructions.md`:
   - Add/update/remove entries in `## Available Prompts` for any changed skill
   - Update the workflow table if skill names or behaviour changed
   - Update the prompt-file ↔ Claude command mapping table
3. Read `README.md`:
   - Update the commands table (Claude Code / Copilot columns)
   - Update `## Three-Step Workflow` if commands were renamed or added
   - Update `## Folder Structure` if new skill folders were added

### Category: ui

**Affected surfaces**: `README.md`

1. If `wiki_query.py` changed: update the "Query the Wiki" section in `README.md`
2. If `tests/` changed: update the "Testing" section in `README.md` with current test count

### Category: presentation

**Affected surfaces**: `README.md` (presentation sub-section if it exists)

Review whether slide content or video output changed; update any referenced file names or counts.

If `presentation/generate_presentation.py` or `presentation/generate_demo_videos.py` changed, also remind the user to run `/regenerate-presentation` to rebuild stale video or deck assets.

### Category: wiki

Wiki structure changes are handled by `/sync-wiki` and `/compile-papers`. Only update here if a structural change (e.g., a new index category) should be reflected in `README.md`.

### Category: raw

Do NOT compile here. If new files were added to `raw/`, remind the user to run `/sync-wiki` to incorporate them.

### Category: core-docs

If `README.md` or `copilot-instructions.md` themselves changed, check whether those changes should cascade to the other surface.

---

## Safety rules

- **Never delete** a doc entry without confirming the underlying skill/command was intentionally removed
- **Never rewrite** an entire doc surface — make targeted edits only
- **Never touch** `wiki/index.md` or `wiki/log.md` — those belong to `/sync-wiki`
- **Never touch** `wiki/` entity pages — those belong to `/compile-papers` or `/sync-wiki`

See [Sync Docs Skill](../../skills/repo-maintenance/SKILL.md) for detailed guidance.

---

## Verification Steps

After the skill completes, confirm success by:

1. **Diff is clean**: run `git diff README.md copilot-instructions.md` — changes should be minimal and targeted (no wholesale rewrites)
2. **Commands table current**: open `README.md` → Commands section — every file in `.claude/commands/` should have a matching row
3. **Folder structure accurate**: open `README.md` → Folder Structure — no missing or ghost entries
4. **copilot-instructions current**: open `copilot-instructions.md` → Available Prompts — every file in `skills/*.prompt.md` should be listed
5. **No broken references**: all file paths mentioned in docs should resolve to real files

---

## Results Summary

Once all steps are complete, output this exact block:

```
✅ Sync Docs — complete  YYYY-MM-DD

📄 Doc surfaces reviewed: N
   README.md              — updated (N targeted edits) / no changes needed
   copilot-instructions.md — updated (N targeted edits) / no changes needed

📝 Changes made:
   ✓ README.md: added /launch-wiki-ui to commands table
   ✓ README.md: updated folder structure (added wiki_query.py)
   ✓ copilot-instructions.md: added "Launch Wiki UI" prompt entry
   ...

⚠️  Manual review needed: N items  (or "none")
   ! A skill was removed — verify deletion from docs was intentional
   ...

🔍 Verification: run  git diff README.md copilot-instructions.md  to review all changes.
➡️  Next step: review diff, then  git add README.md copilot-instructions.md && git commit -m "docs: sync after <change>"
```

$ARGUMENTS
