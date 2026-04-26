# Doc Update Checklist

Run this checklist for each doc surface that `sync-docs` identifies as affected.

---

## Before any edits

- [ ] Run `git diff --name-only HEAD` and `git status --short` — have a full list of changed files
- [ ] Read each changed source file (commands, prompts, skill SKILL.md) before touching any doc surface
- [ ] Identify: additions (new skills), modifications (renamed/redescribed), deletions (removed skills)

---

## README.md

- [ ] Check tool choice banner — do slash command names match actual command filenames?
- [ ] Check the workflow sections — do step commands match current `.claude/commands/*.md` names?
- [ ] Check Folder Structure code block — new skill folders listed? Removed ones gone?
- [ ] Verify no skill is referenced by an old name

---

## docs/index.html

- [ ] Count `.claude/commands/*.md` files — does the stats bar "skill commands" number match?
- [ ] Check `#tools .tools-grid` — one card per skill?
  - [ ] New skills have a new `.tool-card`
  - [ ] Removed skills have their card deleted (confirm deletion is intentional)
  - [ ] Modified skills have updated badge, h3, and description text
- [ ] Check `#how-it-works .workflow` — workflow step `div.step-cmd` values are current
- [ ] Check `#get-started` `<code>` references — command names still match
- [ ] Verify HTML is valid: every opened tag is closed, no broken quotes in attributes

---

## copilot-instructions.md

- [ ] `## Supported Source Formats` table — matches formats in compile-papers/sync-wiki commands?
- [ ] `## Available Prompts` — one `###` block per `.github/prompts/*.prompt.md`?
  - [ ] New prompts added
  - [ ] Removed prompts deleted (confirm intentional)
  - [ ] Modified prompts have updated descriptions and use-when
- [ ] Workflow code block — skill names current?
- [ ] Situation table — all four situations still accurate?
- [ ] `## Prompt Files` mapping table — all four prompt files listed with correct Claude equivalents?
- [ ] `## Resources` section — all skill folders and files listed?

---

## presentation/README.md

- [ ] Quick start script filename matches actual file in `presentation/`
- [ ] Slide count in heading matches actual slide count
- [ ] `## Files Included` list matches files actually present in `presentation/`
- [ ] Any new scripts or outputs mentioned

---

## extensions/README.md

- [ ] Skill names in `### Workflow` section match current Copilot prompt names
- [ ] Installation steps still accurate
- [ ] No references to removed skills or old command names

---

## After all edits

- [ ] Re-read each updated surface — does it accurately describe the current state of the repo?
- [ ] No old command names remain in any surface
- [ ] No undocumented new commands exist in `.claude/commands/` or `.github/prompts/`
- [ ] Produce the summary report table
