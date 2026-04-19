---
description: "Audit entire wiki for quality issues. Check for orphan pages, missing linked concepts, contradictions, and stale claims. Run when wiki reaches ~20 pages."
name: "Audit Wiki"
argument-hint: "Optional: specific areas to audit"
---

Audit the entire `wiki/` folder. Identify and fix:

1. **Orphan pages** — pages that no other page links to
   - Are they truly standalone, or should they be linked?
   - Suggest backlinks from related pages

2. **Missing pages** — concepts referenced with `[[brackets]]` that don't have their own page
   - Find all `[[concept]]` references across pages
   - List concepts that need new pages
   - Suggest which to prioritize

3. **Contradictions** — claims that conflict across pages
   - Compare definitions of same concepts in different pages
   - Check if different sources define things differently
   - Document conflicts in "Contradictions" sections

4. **Stale claims** — things that may have been superseded by newer sources in `/raw`
   - Check publication dates of sources
   - Cross-reference against newer papers
   - Flag outdated understanding

## Output

Generate a comprehensive report showing:
- Count of each issue type
- Specific pages and locations affected
- Recommended fixes

Apply fixes where confident; flag uncertain ones for review.

Use the [Audit Checklist](./skills/wiki-audit/references/audit-checklist.md) and [Report Template](./skills/wiki-audit/assets/audit-report.md) for guidance.

**Recommended**: Run this every ~20-30 new pages or monthly.
