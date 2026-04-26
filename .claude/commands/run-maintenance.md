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

## Step 1: Run Pytest Suite

```bash
pytest --tb=short -v 2>&1
```

Record from the output:
- Total tests discovered
- Passed / Failed / Error / Skipped counts
- Full name + short traceback for every failure or error

If pytest is not found, try `python3 -m pytest --tb=short -v 2>&1`.

---

## Step 2: Verify Skill Registrations

Check that every skill has its command file, Copilot prompt file, and a `copilot-instructions.md` entry.

**Wiki skills:**

| Skill | Claude command | Copilot prompt |
|-------|---------------|----------------|
| compile-papers | `.claude/commands/compile-papers.md` | `.github/prompts/compile-papers.prompt.md` |
| sync-wiki | `.claude/commands/sync-wiki.md` | `.github/prompts/sync-wiki.prompt.md` |
| audit-wiki | `.claude/commands/audit-wiki.md` | `.github/prompts/audit-wiki.prompt.md` |
| reset-wiki | `.claude/commands/reset-wiki.md` | `.github/prompts/reset-wiki.prompt.md` |
| launch-wiki-ui | `.claude/commands/launch-wiki-ui.md` | `.github/prompts/launch-wiki-ui.prompt.md` |

**Repo maintenance skills:**

| Skill | Claude command | Copilot prompt |
|-------|---------------|----------------|
| sync-docs | `.claude/commands/sync-docs.md` | `.github/prompts/sync-docs.prompt.md` |
| run-maintenance | `.claude/commands/run-maintenance.md` | `.github/prompts/run-maintenance.prompt.md` |
| regenerate-presentation | `.claude/commands/regenerate-presentation.md` | `.github/prompts/regenerate-presentation.prompt.md` |

For each file: confirm it exists and has valid frontmatter (`description:` for Claude commands, `mode: agent` for Copilot prompts). Report any missing or malformed files.

Also scan `copilot-instructions.md` to confirm every Copilot-available skill is listed under `## Available Prompts` or `## Repo Maintenance`.

---

## Step 3: Check Wiki Health

1. List all `.md` files in `wiki/` excluding `index.md` and `log.md` — these are entity pages
2. Check `wiki/index.md`: is it populated with actual entries, or still the empty template?
3. Read `wiki/log.md`: count source rows
4. List all files in `raw/` with supported extensions (`.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`)
5. Cross-reference `raw/` files against the Source column in `wiki/log.md`
6. Identify any `raw/` files not yet logged (unsynced sources)

---

## Step 4: Check Git Status

```bash
git status --short
git log --oneline -5
```

Record: staged file count, unstaged file count, untracked file count, and the last 5 commit messages.

---

## Step 5: Generate Maintenance Report

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
