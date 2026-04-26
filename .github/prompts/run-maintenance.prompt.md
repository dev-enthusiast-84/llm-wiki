---
mode: agent
description: Run all pytest tests, verify every skill is registered in both Claude Code and Copilot, check wiki and git health, then save a dated report to reports/.
---

## Step 1: Spawn Parallel Health-Check Agents

Call the Agent tool four times in a **single response** — all run simultaneously. Do not wait for one to finish before sending the others.

**Agent 1 — Tests** (`subagent_type: "Explore"`): Run `pytest --tb=short -v 2>&1` (or `python3 -m pytest` if needed). Return: total discovered, passed, failed, errors, skipped, and full name + traceback for every failure.

**Agent 2 — Skill Registration** (`subagent_type: "Explore"`): Verify these files exist with valid frontmatter (Claude commands need `description:`, Copilot prompts need `mode: agent`): `.claude/commands/compile-papers.md`, `.claude/commands/sync-wiki.md`, `.claude/commands/audit-wiki.md`, `.claude/commands/reset-wiki.md`, `.claude/commands/launch-wiki-ui.md`, `.claude/commands/sync-docs.md`, `.claude/commands/run-maintenance.md`, `.claude/commands/regenerate-presentation.md`, `.claude/commands/orchestrate-wiki.md`, and all matching `.github/prompts/*.prompt.md` counterparts. Also confirm every Copilot skill is listed in `copilot-instructions.md`. Return: verified count, missing files, malformed frontmatter.

**Agent 3 — Wiki Health** (`subagent_type: "Explore"`): (1) Count entity pages in `wiki/` (exclude `index.md`, `log.md`); (2) check if `wiki/index.md` is populated; (3) count source rows in `wiki/log.md`; (4) list files in `raw/` with supported extensions; (5) cross-reference `raw/` against `wiki/log.md` Source column to find unsynced files. Return all five findings.

**Agent 4 — Git Status** (`subagent_type: "Explore"`): Run `git status --short` and `git log --oneline -5`. Return: staged, unstaged, untracked file counts and the last 5 commit messages.

## Step 2: Generate Report

Wait for all four agents to complete, then:
1. Create `reports/` directory if it does not exist
2. Create `reports/maintenance-YYYY-MM-DD.md` from the template at `skills/repo-maintenance/assets/maintenance-report-template.md`
3. Populate all sections with data from the four agents
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
