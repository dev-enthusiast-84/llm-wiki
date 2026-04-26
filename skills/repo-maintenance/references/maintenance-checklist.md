# Run Maintenance Checklist

Step-by-step verification for `/run-maintenance`.

---

## Pre-run

- [ ] Running from the repo root directory (check: `ls wiki/ raw/ tests/`)
- [ ] `pytest` is available: `python3 -m pytest --version`
- [ ] `reports/` directory exists (or will be created by the skill)

---

## Step 1 — Tests

- [ ] `pytest --tb=short -v` executed successfully (no import errors)
- [ ] Total test count is ≥ 40 (if it drops unexpectedly, a test file may be missing)
- [ ] **Zero failures** — any failure must be investigated before committing
- [ ] **Zero errors** — errors indicate broken imports or missing fixtures, not just bad logic
- [ ] Skipped tests are intentional (e.g. marked `@pytest.mark.skip` with a reason)

**If tests fail**: Run `pytest tests/<failing_file>.py -v` to isolate. Common causes:
- Missing dependency (run `pip install -r requirements.txt` if it exists)
- Broken mock in `tests/conftest.py`
- Changed function signature not reflected in test

---

## Step 2 — Skill Registration

Check each row in the registration table:

**Capabilities skills** (Claude Code: `capabilities/` subdir, Copilot: flat `.github/prompts/`):
- [ ] `.claude/commands/compile-papers.md` exists with `description:` frontmatter
- [ ] `.github/prompts/compile-papers.prompt.md` exists with `mode: agent` frontmatter
- [ ] `.claude/commands/sync-wiki.md` exists
- [ ] `.github/prompts/sync-wiki.prompt.md` exists
- [ ] `.claude/commands/audit-wiki.md` exists
- [ ] `.github/prompts/audit-wiki.prompt.md` exists
- [ ] `.claude/commands/reset-wiki.md` exists
- [ ] `.github/prompts/reset-wiki.prompt.md` exists
- [ ] `.claude/commands/launch-wiki-ui.md` exists (Claude Code only — no Copilot equivalent)

**Repo maintenance skills** (Claude Code: `.claude/commands/`, Copilot: `.github/prompts/`):
- [ ] `.claude/commands/sync-docs.md` exists
- [ ] `.github/prompts/sync-docs.prompt.md` exists
- [ ] `.claude/commands/run-maintenance.md` exists
- [ ] `.github/prompts/run-maintenance.prompt.md` exists
- [ ] `.claude/commands/regenerate-presentation.md` exists
- [ ] `.github/prompts/regenerate-presentation.prompt.md` exists

**copilot-instructions.md registration**:
- [ ] `Compile Papers to Wiki` prompt listed under `## Available Prompts`
- [ ] `Sync Wiki from Raw` prompt listed
- [ ] `Audit Wiki` prompt listed
- [ ] `Reset Wiki` prompt listed
- [ ] `Sync Docs` prompt listed under `## Repo Maintenance`
- [ ] `Run Maintenance` prompt listed under `## Repo Maintenance`
- [ ] `Regenerate Presentation` prompt listed under `## Repo Maintenance`
- [ ] Prompt file table (under `## Prompt Files`) includes all `.github/prompts/*.prompt.md` entries

---

## Step 3 — Wiki Health

- [ ] `wiki/index.md` is populated (not the empty template — check for actual entity entries)
- [ ] `wiki/log.md` has at least one source row in the table
- [ ] Every file in `raw/` with a supported extension is accounted for in `wiki/log.md`
  - Supported: `.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`
  - Any unlogged file → run `/sync-wiki` after this report

---

## Step 4 — Git Status

- [ ] No unexpected staged changes (confirm each is intentional)
- [ ] No large untracked files accidentally left out of `.gitignore`
- [ ] Most recent commit message is meaningful (not "WIP" or blank)

---

## Step 5 — Report

- [ ] `reports/maintenance-YYYY-MM-DD.md` was created with today's date
- [ ] All five sections are populated (no empty dashes remaining)
- [ ] Overall health status is one of: ✅ Healthy / ⚠️ Needs Attention / ❌ Action Required
- [ ] Recommendations section lists specific, actionable items (or says "No issues found")

---

## Post-run Actions

| Issue | Action |
|-------|--------|
| Test failures | Fix before next commit; run `pytest -x` to stop at first failure |
| Missing skill file | Create using the established naming pattern for that skill type |
| Unsynced raw file | Run `/sync-wiki` |
| Missing Copilot registration | Add to `copilot-instructions.md` + create `.github/prompts/` file |
| Stale doc surface | Run `/sync-docs` |
