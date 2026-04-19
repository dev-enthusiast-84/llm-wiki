# Wiki Audit Report Template

Copy this template to document audit results.

```markdown
# Wiki Audit Report — [DATE]

## Summary

- **Pages audited**: XX
- **Orphan pages**: X
- **Missing pages**: X
- **Contradictions found**: X
- **Stale claims**: X

## Orphan Pages

Pages with no inbound links:
- `page-name.md` — Suggestion: [link from X or remove]
- `page-name.md` — Suggestion: [link from X or remove]

## Missing Pages

Concepts referenced but without a page:
- `[[concept-name]]` — Referenced in: page1.md, page2.md
- `[[concept-name]]` — Referenced in: page1.md

**Action**: Create pages for these concepts

## Contradictions

| Concept | Location 1 | Location 2 | Issue | Resolution |
|---------|---|---|---|---|
| concept | page1.md | page2.md | Different definitions | Added Contradictions section to both |

## Stale Claims

| Page | Claim | Last Source | Issue | Update |
|------|-------|---|---|---|
| page-name.md | Claim text | 2020 Paper | Newer source in /raw | Updated with 2024 findings |

## Fixes Applied

✓ Added 3 missing pages  
✓ Consolidated 2 orphan pages into related entries  
✓ Updated 5 contradictions sections  
✓ Refreshed 2 stale claims with newer sources  
✓ Updated wiki/log.md  

## Next Steps

- [ ] Review suggested links before publishing
- [ ] Prioritize creating missing pages in next sync
- [ ] Schedule next audit for [date] when wiki reaches [30-40] pages

---

**Auditor**: [name]  
**Date**: [date]  
**Commit**: [commit hash]
```

## Key Metrics to Track

Over time, use these metrics to measure wiki health:

```
Audit History

| Date | Pages | Orphans | Missing | Contradictions | Stale Claims |
|------|-------|---------|---------|---|---|
| 2026-04-20 | 20 | 2 | 5 | 1 | 3 |
| (next) | | | | | |
```

Good wiki hygiene targets:
- Orphan pages < 5% of total
- Missing references < 10% of found links
- All contradictions explicitly documented
- Sources updated at least quarterly
