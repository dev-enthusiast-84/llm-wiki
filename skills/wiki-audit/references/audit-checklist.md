# Wiki Audit Checklist

Use this checklist to systematically audit the wiki.

## Orphan Pages Report

- [ ] List all files in `wiki/` 
- [ ] Extract all `[[references]]` from every page
- [ ] Mark each file as "linked" if it appears in references
- [ ] Identify files with zero inbound links
- [ ] Decide: Add backlinks, or remove if not useful?

**Orphans found**: _______________

## Missing Pages Report

- [ ] Search for all `[[...]]` patterns across `wiki/*.md`
- [ ] Extract unique concept names referenced
- [ ] Check each against filenames in `wiki/`
- [ ] List concepts with no corresponding file
- [ ] Prioritize: Which are most critical to add?

**Missing pages found**: _______________

## Contradictions Report

| Concept | Page A (Source) | Page B (Source) | Conflict | Resolution |
|---------|---|---|---|---|
| | | | | |
| | | | | |

**Contradictions found**: _______________

## Stale Claims Report

- [ ] Review dates of all Sources sections
- [ ] Check `/raw` for newer papers on same topics
- [ ] Read commit log/audit log for when pages were last updated
- [ ] Identify papers older than 2+ years without recent updates
- [ ] Cross-check against misconceptions that evolved

| Page | Claim | Last Source Date | Newer Source in `/raw`? | Action |
|------|-------|---|---|---|
| | | | | |

**Stale claims found**: _______________

## Fixes Applied

- [ ] Added missing page links (list: ______________)
- [ ] Created backlinks for orphans (list: ______________)
- [ ] Updated contradictions sections (count: __)
- [ ] Refreshed stale information (count: __)
- [ ] Updated `wiki/log.md` with audit results
- [ ] Committed changes with message: "Wiki audit: [summary]"

## Quality Metrics (Before & After)

| Metric | Before | After |
|--------|--------|-------|
| Total pages | | |
| Orphan pages | | |
| Missing references | | |
| Contradictions documented | | |
| Stale claims updated | | |
