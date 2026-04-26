---
name: llm-wiki-commands
description: "LLM Wiki compilation and sync commands. Available prompts for managing wiki content."
---

# LLM Wiki Commands

This workspace includes ten prompts for managing wiki content and keeping documentation in sync.

## Supported Source Formats

Drop files into `/raw/` — skills will scan and process them automatically.

| Format | Support | Limitations |
|--------|---------|-------------|
| `.pdf` | ✅ Full | Images/diagrams not extracted; PDFs >20 pages read in chunks |
| `.txt` | ✅ Full | None |
| `.html` | ✅ Full | Inline JS/CSS may add noise; complex layouts may lose structure |
| `.pptx` | ✅ Text only | Charts, images, diagrams, and speaker notes are not extracted |
| `.docx` | ✅ Text only | Tables, images, headers/footers, and text boxes not extracted |
| `.xlsx` | ✅ Cell values only | Formulas shown as last-computed result; charts, images, and formatting lost |
| `.ppt`, other | ❌ Unsupported | Will be skipped with a warning |

## Available Prompts

### `Orchestrate Wiki`
Full pipeline in one command — detects wiki state and runs compile or sync, then audit, then sync-docs.
- Detects whether wiki is empty (compile path) or has content (sync path)
- Spawns parallel extraction agents (one per source file) for compile and sync phases
- Runs four parallel audit agents: orphan check, missing pages, contradictions, stale claims
- Updates all doc surfaces (README, GitHub Pages, copilot-instructions) after wiki changes
- Emits a phase-by-phase summary report with manual review items

**Use when**: Adding multiple papers to `/raw`, or as a periodic full wiki refresh

### `Reset Wiki`
Prepare the wiki before any other operation.
- Detects current wiki state (empty vs. has content)
- If empty: scaffolds `index.md` and `log.md`, confirms ready
- If content exists: summarizes pages and offers sync or reset options
- With `reset` argument: wipes all entity pages and resets to clean templates

**Use when**: Starting a session, unsure of wiki state, or want to start over

### `Compile Papers to Wiki`
Initial compilation prompt — scans `/raw` automatically, no filenames needed.
- Pre-flight check: blocks if wiki already has content, offers redirect
- Scans `/raw` and lists all supported files before reading
- Reads each file using the appropriate method for its format
- Creates markdown entity pages with summaries and cross-links
- Documents contradictions between sources
- Updates `wiki/index.md` and `wiki/log.md`

**Use when**: Wiki is empty and `/raw` has files to compile

### `Sync Wiki from Raw`
Incremental update — auto-detects new files in `/raw` not yet in `log.md`.
- Compares `/raw` contents against `wiki/log.md` Source column
- Only processes files not already logged
- Updates existing entity pages where new source overlaps
- Creates new pages for novel concepts
- Updates `index.md` and `log.md`

**Use when**: New files have been added to `/raw` and wiki already has content

### `Audit Wiki`
Quality assurance prompt for comprehensive wiki maintenance.
- Finds orphan pages (no inbound links)
- Identifies missing pages (referenced but not created)
- Detects contradictions across pages
- Flags stale claims superseded by newer sources

**Use when**: Wiki reaches ~20-30 pages (recommend monthly)

### `Launch Wiki UI`
Launch the browser-based wiki query interface.
- Checks Python 3 and Streamlit dependencies
- Reports wiki entity page count and readiness
- Starts Streamlit app and guides model/API key configuration

**Use when**: You want to query the wiki interactively through a browser

### `Stop Wiki UI`
Stop the running wiki query UI.
- Checks whether the Streamlit process is active
- Kills it if running; reports if already stopped
- Confirms the process is no longer running

**Use when**: You want to shut down the wiki UI started by `Launch Wiki UI`

## Recommended Workflow

```
Drop files into /raw/
    │
    ├─ Want full refresh? ───→ Orchestrate Wiki  (all-in-one pipeline)
    │
    ├─ Wiki empty? ──────────→ Reset Wiki → Compile Papers to Wiki
    │
    └─ Wiki has content? ───→ Sync Wiki from Raw
                                    │
                                    └─ 20+ pages? → Audit Wiki
```

| Situation | Start with |
|---|---|
| Full pipeline refresh | `Orchestrate Wiki` |
| First time, fresh wiki | `Reset Wiki` then `Compile Papers to Wiki` |
| Added new file to `/raw` | `Sync Wiki from Raw` |
| Wiki feels messy/stale | `Reset Wiki reset` then `Compile Papers to Wiki` |
| Quality check | `Audit Wiki` |

## Prompt Files

Prompts live in `.github/prompts/` and are available in GitHub Copilot and VS Code:

| Prompt file | Claude equivalent |
|---|---|
| `.github/prompts/orchestrate-wiki.prompt.md` | `/orchestrate-wiki` |
| `.github/prompts/reset-wiki.prompt.md` | `/reset-wiki` |
| `.github/prompts/compile-papers.prompt.md` | `/compile-papers` |
| `.github/prompts/sync-wiki.prompt.md` | `/sync-wiki` |
| `.github/prompts/audit-wiki.prompt.md` | `/audit-wiki` |
| `.github/prompts/launch-wiki-ui.prompt.md` | `/launch-wiki-ui` |
| `.github/prompts/stop-wiki-ui.prompt.md` | `/stop-wiki-ui` |
| `.github/prompts/sync-docs.prompt.md` | `/sync-docs` |
| `.github/prompts/run-maintenance.prompt.md` | `/run-maintenance` |
| `.github/prompts/regenerate-presentation.prompt.md` | `/regenerate-presentation` |

## Resources

**Orchestrate Wiki**:
- Skill: `skills/orchestrate-wiki/SKILL.md`
- Claude command: `.claude/commands/orchestrate-wiki.md`
- Copilot prompt: `.github/prompts/orchestrate-wiki.prompt.md`

**Wiki Reset**:
- Skill: `skills/wiki-reset/SKILL.md`
- Templates: `skills/wiki-reset/assets/`
- Checklist: `skills/wiki-reset/references/reset-checklist.md`

**Wiki Compilation**:
- Skill: `skills/wiki-compilation/SKILL.md`
- Template: `skills/wiki-compilation/assets/entity-template.md`
- Format Guide: `skills/wiki-compilation/references/wiki-format.md`

**Wiki Sync**:
- Skill: `skills/wiki-sync/SKILL.md`
- Update Checklist: `skills/wiki-sync/references/update-checklist.md`
- Log Format: `skills/wiki-sync/references/log-format.md`
- Entity Template: `skills/wiki-sync/assets/entity-template.md`

**Wiki Audit**:
- Skill: `skills/wiki-audit/SKILL.md`
- Audit Checklist: `skills/wiki-audit/references/audit-checklist.md`
- Report Template: `skills/wiki-audit/assets/audit-report.md`

**Stop Wiki UI**:
- Skill: `skills/stop-wiki-ui/SKILL.md`
- Claude command: `.claude/commands/stop-wiki-ui.md`
- Copilot prompt: `.github/prompts/stop-wiki-ui.prompt.md`

---

## Repo Maintenance

Tools for keeping the repo's own documentation and health in check — not part of the LLM-wiki workflow.

### `Sync Docs`

Keeps all repo documentation surfaces in sync after code changes — no argument needed.
- Detects changed files via `git diff` and `git status` automatically
- Maps changes to affected surfaces: `README.md`, `docs/index.html`, `copilot-instructions.md`, sub-READMEs
- Applies targeted edits only — never rewrites entire doc files
- Reports a summary of what was updated vs. already up-to-date
- Flags deletions for manual confirmation before removing doc entries

**Use when**: After adding/modifying/removing a skill, command, or project structure change

| Tool | Command |
|------|---------|
| Claude Code | `/sync-docs` |
| GitHub Copilot | `Sync Docs` |

**Resources**:
- Skill: `skills/repo-maintenance/SKILL.md`
- Doc Surface Map: `skills/repo-maintenance/assets/doc-surface-map.md`
- Doc Update Checklist: `skills/repo-maintenance/references/doc-checklist.md`

### `Run Maintenance`

Full repo health check — runs all tests, verifies every skill is properly registered, inspects wiki and git state, and saves a dated report.
- Runs `pytest --tb=short -v` across the full test suite and records pass/fail/skip/error counts
- Verifies every skill has its Claude command file, Copilot prompt file, and a `copilot-instructions.md` entry
- Checks wiki health: entity page count, index and log population, unsynced `raw/` sources
- Inspects git status and recent commit history
- Saves `reports/maintenance-YYYY-MM-DD.md` with overall health: ✅ Healthy / ⚠️ Needs Attention / ❌ Action Required

**Use when**: Before commits, after significant changes, or on a monthly cadence

| Tool | Command |
|------|---------|
| Claude Code | `/run-maintenance` |
| GitHub Copilot | `Run Maintenance` |

**Resources**:
- Claude command: `.claude/commands/run-maintenance.md`
- Copilot prompt: `.github/prompts/run-maintenance.prompt.md`
- Report template: `skills/repo-maintenance/assets/maintenance-report-template.md`
- Checklist: `skills/repo-maintenance/references/maintenance-checklist.md`

### `Regenerate Presentation`

Rebuilds demo videos and the PPTX deck when code, skills, or the wiki query UI has changed.
- Detects changed paths via `git diff` and `git status` — no argument needed
- Rebuilds only what's stale: videos first, then deck (deck embeds them)
- Verifies both videos are embedded in `presentation/llm-wiki-deck.pptx`
- Prints manual steps for Keynote and Google Slides formats

**Use when**: After modifying `generate_presentation.py`, `generate_demo_videos.py`, `wiki_query.py`, or any skill/command file

| Tool | Command |
|------|---------|
| Claude Code | `/regenerate-presentation` |
| GitHub Copilot | `Regenerate Presentation` |

**Arguments:** none (auto-detects via git) · `videos` · `deck` · `all`

**Resources**:
- Skill: `skills/repo-maintenance/regenerate-presentation/SKILL.md`
- Rebuild checklist: `skills/repo-maintenance/regenerate-presentation/references/rebuild-checklist.md`

