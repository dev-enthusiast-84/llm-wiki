---
name: sync-docs
description: 'Sync all repo documentation surfaces after code changes. Uses git diff to detect what changed, maps changes to affected doc surfaces (README, GitHub Pages, copilot-instructions, sub-READMEs), and applies targeted updates. Run after adding/modifying skills, commands, or project structure.'
argument-hint: 'No argument needed — changes are detected automatically via git'
---

# Sync Docs

Keep all repo documentation surfaces in sync after code changes, without manual cross-editing.

## When to Use

- After adding or modifying a skill or slash command
- After adding support for a new file format in compile/sync
- After changing the presentation or extension docs
- After any structural repo change (new folder, renamed file, removed command)
- As a final step before committing to ensure no doc surface is stale

## Doc Surfaces Managed

| Surface | Path | What it documents |
|---------|------|-------------------|
| Root README | `README.md` | Quick start, commands table, folder structure, workflow |
| GitHub Pages | `docs/index.html` | Public-facing landing page; tool cards, stats, features |
| Copilot workspace | `copilot-instructions.md` | Prompt list, workflow table, resource links |
| Presentation docs | `presentation/README.md` | Slide content, generation instructions, file list |
| Extension docs | `extensions/README.md` | Obsidian Web Clipper setup, other tool integrations |

## Change-to-Surface Mapping

| Changed path pattern | Surfaces to update |
|----------------------|-------------------|
| `.claude/commands/*.md` | `copilot-instructions.md`, `README.md`, `docs/index.html` |
| `.github/prompts/*.prompt.md` | `copilot-instructions.md` |
| `skills/**` | `copilot-instructions.md`, `README.md` (folder structure) |
| `presentation/generate_presentation.py`, `presentation/generate_demo_videos.py` | Remind user to run `/regenerate-presentation`; update `README.md` → `## Presentation` |
| `presentation/**` (other) | `README.md` → `## Presentation` |
| `extensions/**` | `extensions/README.md` |
| `wiki/**` | Only if structural (new index categories) → `README.md` |
| `raw/**` | Remind user to run `/sync-wiki` |
| `README.md` | Check cascade to `docs/index.html` |
| `docs/index.html` | Check cascade to `README.md` |

## Procedure

### 1. Detect Changes

```bash
git diff --name-only HEAD   # staged + unstaged changes vs last commit
git status --short          # catches untracked new files
```

Combine both outputs. Group by category using the mapping table above.

### 2. Update Each Surface

Work surface by surface. For each:
1. Read the current content
2. Read the changed source files
3. Apply the minimum edit that makes the surface accurate

See [Doc Surface Map](./assets/doc-surface-map.md) for the exact elements to check per surface.
See [Update Checklist](./references/doc-checklist.md) for step-by-step verification per surface.

### 3. docs/index.html Tool Cards

The `#tools` section contains `.tool-card` divs. Each card follows this pattern:
```html
<div class="tool-card">
  <div class="tool-badge">keyword</div>
  <h3>/command-name</h3>
  <div class="tool-cmd">Claude Code &amp; Copilot</div>
  <p>One-sentence description.</p>
</div>
```

Match this structure exactly when adding new cards. Update the stat `<div class="stat-val">N</div>` for "AI-powered skill commands" in the stats bar when the skill count changes.

### 4. README Commands Table

The README commands table uses this format:
```markdown
| Tool | Command |
|------|---------|
| Claude Code | `/command-name` |
| GitHub Copilot | `Command Name` |
```

### 5. copilot-instructions.md Prompts Section

Each prompt entry follows:
```markdown
### `Prompt Name`
One-line description.
- Bullet of what it does

**Use when**: Situation description
```

### 6. Report

After updating, produce a summary table. Flag anything that required a deletion (to confirm intentional removal).

## Safety Rules

| Rule | Reason |
|------|--------|
| Never delete a skill entry without user confirmation | The change might be a mistake |
| Never rewrite full doc surfaces | Preserves context not visible in git diff |
| Never touch `wiki/*.md` entity pages | Those belong to `/sync-wiki` and `/compile-papers` |
| Always read before writing | Avoids overwriting content that isn't stale |

## Relation to Other Skills

| Skill | When to Use |
|-------|-------------|
| `/sync-wiki` | Sync wiki entity pages when new files are added to `/raw` |
| `/compile-papers` | Compile all sources in `/raw` into wiki pages |
| `/audit-wiki` | Quality check: orphans, missing links, contradictions |
| `/sync-docs` | **This skill** — sync all doc surfaces after code changes |

## Reference Files

- [Doc Surface Map](./assets/doc-surface-map.md) - What to check in each doc surface
- [Doc Update Checklist](./references/doc-checklist.md) - Step-by-step per surface
