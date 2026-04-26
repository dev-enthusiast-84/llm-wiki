---
mode: agent
description: Run all pytest tests, verify every skill is registered in both Claude Code and Copilot, check wiki and git health, then save a dated report to reports/.
---

## Step 1: Run Tests

Run `pytest --tb=short -v` (or `python3 -m pytest --tb=short -v` if needed) and record: total, passed, failed, errors, skipped counts, and full name + short traceback for every failure.

## Step 2: Verify Skill Registrations

Confirm each file pair exists with valid frontmatter (`description:` for Claude commands, `mode: agent` for Copilot prompts):

**Capabilities** (Claude Code: `.claude/commands/`, Copilot: `.github/prompts/`):
- `compile-papers` — command + prompt
- `sync-wiki` — command + prompt
- `audit-wiki` — command + prompt
- `reset-wiki` — command + prompt
- `launch-wiki-ui` — command only (Claude Code only; no Copilot prompt)

**Repo Maintenance** (Claude Code: `.claude/commands/`, Copilot: `.github/prompts/`):
- `sync-docs` — command + prompt
- `run-maintenance` — command + prompt
- `regenerate-presentation` — command + prompt

Also confirm every Copilot-available skill is listed under `## Available Prompts` or `## Repo Maintenance` in `copilot-instructions.md`.

## Step 3: Check Wiki Health

List entity pages in `wiki/` (exclude `index.md`, `log.md`). Check whether `wiki/index.md` is populated. Count source rows in `wiki/log.md`. List all files in `raw/` with supported extensions and cross-reference against `wiki/log.md` to find unsynced sources.

## Step 4: Check Git Status

Run `git status --short` and `git log --oneline -5`. Record staged, unstaged, and untracked file counts plus the last 5 commit messages.

## Step 5: Generate Report

1. Create `reports/` directory if it does not exist
2. Create `reports/maintenance-YYYY-MM-DD.md` from the template at `skills/repo-maintenance/assets/maintenance-report-template.md`
3. Populate all five sections with data from Steps 1–4
4. Set Overall Health: ✅ Healthy (all pass, all registered, no unsynced) / ⚠️ Needs Attention (warnings/skips/unsynced) / ❌ Action Required (failures, missing files)
5. Fill Recommendations with specific action items; write "No issues found" if clean

## Output

Report the Results Summary:
- Test counts (passed/failed/errors/skipped)
- Skill registration status (N/N verified, list any issues)
- Wiki health (entity count, index status, unsynced raw count)
- Git status (uncommitted changes, last commit)
- Report path (`reports/maintenance-YYYY-MM-DD.md`)
- Overall health indicator

See [Maintenance Checklist](../skills/repo-maintenance/references/maintenance-checklist.md) for complete verification steps.
