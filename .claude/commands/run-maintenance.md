---
description: Run all pytest tests, verify every skill is registered in both Claude Code and Copilot, check wiki and git health, then save a dated report to reports/.
---

## Usage

**Invoke:** type `/run-maintenance` in Claude Code CLI
**When to run:** Before commits, after significant changes, or on a monthly cadence
**Prerequisites:** Python 3 + pytest installed; run from repo root
**Arguments:** None required
**Tip:** Run `/sync-docs` first to ensure docs are current, then run this to confirm overall health.

---

## Step 1: Spawn Parallel Health-Check Agents

Call the Agent tool four times in a **single response** — send all four calls together without waiting for any to complete first.

**Agent 1 — Tests**
`subagent_type: "Explore"` — prompt: "Run `pytest --tb=short -v 2>&1` in the repo root (try `python3 -m pytest --tb=short -v 2>&1` if pytest is not found). Return: total tests discovered, passed count, failed count, error count, skipped count, and the full name plus short traceback for every failure or error."

**Agent 2 — Skill Registration**
`subagent_type: "Explore"` — prompt: "Check that each file below exists and has valid frontmatter. Claude commands (`.claude/commands/*.md`) must have a `description:` field. Copilot prompts (`.github/prompts/*.prompt.md`) must have `mode: agent`. Files to verify: `.claude/commands/compile-papers.md`, `.claude/commands/sync-wiki.md`, `.claude/commands/audit-wiki.md`, `.claude/commands/reset-wiki.md`, `.claude/commands/launch-wiki-ui.md`, `.claude/commands/sync-docs.md`, `.claude/commands/run-maintenance.md`, `.claude/commands/regenerate-presentation.md`, `.claude/commands/orchestrate-wiki.md`, `.github/prompts/compile-papers.prompt.md`, `.github/prompts/sync-wiki.prompt.md`, `.github/prompts/audit-wiki.prompt.md`, `.github/prompts/reset-wiki.prompt.md`, `.github/prompts/sync-docs.prompt.md`, `.github/prompts/run-maintenance.prompt.md`, `.github/prompts/regenerate-presentation.prompt.md`, `.github/prompts/orchestrate-wiki.prompt.md`. Also scan `copilot-instructions.md` to confirm every Copilot-available skill is listed under `## Available Prompts` or `## Repo Maintenance`. Return: verified count, missing files, malformed frontmatter."

**Agent 3 — Wiki Health**
`subagent_type: "Explore"` — prompt: "In this repo: (1) list all `.md` files in `wiki/` excluding `index.md` and `log.md` — count them as entity pages; (2) read the first few lines of `wiki/index.md` — is it populated with actual entries or still an empty template? (3) read `wiki/log.md` and count source rows in the table; (4) list all files in `raw/` with extensions `.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`; (5) cross-reference `raw/` filenames against the Source column in `wiki/log.md` and list any raw files not yet logged as unsynced sources. Return all five findings."

**Agent 4 — Git Status**
`subagent_type: "Explore"` — prompt: "Run `git status --short` and `git log --oneline -5`. Return: staged file count, unstaged file count, untracked file count, and the text of the last 5 commit messages."

---

## Step 2: Collect Results

Wait for all four agents to complete. Gather their outputs before proceeding to the report.

---

## Step 3: Generate Maintenance Report

1. Create the `reports/` directory if it does not exist:
   ```bash
   mkdir -p reports
   ```

2. Create `reports/maintenance-YYYY-MM-DD.md` (use today's date) from the template at:
   `skills/repo-maintenance/assets/maintenance-report-template.md`

3. Populate every section with data collected in Steps 1–4.

4. Set the Overall Health status at the top:
   - **✅ Healthy** — all tests pass, all skills registered, no unsynced sources, zero unexpected git changes
   - **⚠️ Needs Attention** — skipped tests, warnings, or unsynced raw files present (but no failures)
   - **❌ Action Required** — any test failures or errors, missing skill files, or unregistered skills

5. Fill the Recommendations section with specific action items for any issues found. If no issues: write "No issues found."

See [Maintenance Checklist](../../skills/repo-maintenance/references/maintenance-checklist.md) for full verification steps.

---

## Verification Steps

After the skill completes, confirm:
1. `reports/maintenance-YYYY-MM-DD.md` exists and all five sections are populated
2. No section still contains placeholder dashes (`—`)
3. Overall health status is clearly set

---

## Results Summary

Once all steps complete, output this exact block:

```
✅ Run Maintenance — complete  YYYY-MM-DD

🧪 Tests
   ✓ Passed:  N
   ✗ Failed:  N
   ⚠ Errors:  N
   ⏭ Skipped: N

🛠  Skill Registration
   ✓ Verified: N/N files present
   ⚠  Issues:  <none | list missing files>

📚 Wiki
   Entity pages:    N
   Index populated: Yes / No
   Unsynced raw:    N file(s)

🗂  Git
   Uncommitted changes: N files
   Last commit: <message>

📄 Report saved: reports/maintenance-YYYY-MM-DD.md
🏥 Overall health: ✅ Healthy | ⚠️ Needs Attention | ❌ Action Required

➡️  Next step: <none | fix failing tests | run /sync-wiki | fix missing registrations>
```
