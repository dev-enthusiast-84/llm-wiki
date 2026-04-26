---
description: Audit entire wiki for quality issues. Check for orphan pages, missing linked concepts, contradictions, and stale claims. Run when wiki reaches ~20 pages.
---

## Usage

**Invoke:** type `/audit-wiki` in the Claude Code CLI  
**When to run:** every ~20–30 new pages, after a large sync batch, or before publishing/sharing  
**Prerequisites:** `wiki/` must contain entity pages (`/compile-papers` has been run at least once)  
**Arguments:** optionally pass a category or page name to scope the audit  
**Example:** `/audit-wiki contradictions` — only run the contradictions check  

---

## Step 1: Scan all entity pages

List every `.md` file in `wiki/` except `index.md` and `log.md`.  
Build an index of:
- All `[[bracket]]` outbound links per page
- All pages that link to each page (inbound links)
- All source citations and their publication years

## Step 2: Orphan pages

Pages that **no other page links to**:
- List them by filename
- Determine whether they are genuinely standalone or should be linked
- Suggest specific backlinks from the most related pages

## Step 3: Missing pages

Concepts referenced with `[[brackets]]` that **have no corresponding file**:
- Find all `[[concept]]` references across every page
- List concepts where `wiki/<concept>.md` does not exist
- Prioritize by number of pages that reference the missing concept
- Create stub pages for the top-priority missing concepts

## Step 4: Contradictions

Claims that **conflict across pages**:
- Compare definitions of the same concept in different pages
- Note when different sources define things differently
- Add or update the `## Contradictions` section in affected pages

## Step 5: Stale claims

Information that **may have been superseded**:
- Check publication dates of sources in `## Sources` sections
- Cross-reference against newer papers already in `wiki/log.md`
- Flag pages whose core claim relies only on older sources when newer ones exist

## Step 6: Apply fixes

- **Apply confidently** where the fix is clear (add backlink, create a stub page, update a source reference)
- **Flag for review** where the fix requires subject-matter judgment (contradictions, stale claims)

Use the [Audit Checklist](../skills/wiki-audit/references/audit-checklist.md) and [Report Template](../skills/wiki-audit/assets/audit-report.md) for guidance.

---

## Verification Steps

After the skill completes, confirm success by checking:

1. **Orphans resolved**: open each formerly-orphan page and confirm at least one other page now links to it
2. **Missing pages addressed**: `ls wiki/*.md` — stub pages should now exist for high-priority missing concepts
3. **Contradictions documented**: open affected pages and confirm a `## Contradictions` section exists with both viewpoints cited
4. **Index consistent**: `wiki/index.md` should list every entity page including any new stubs
5. **No new broken links**: confirm any new stubs have at least a `## Summary` and `## Sources` section

---

## Results Summary

Once all steps are complete, output this exact block:

```
✅ Audit Wiki — complete  YYYY-MM-DD

🔍 Findings:
   Orphan pages:        N  (list filenames, or "none")
   Missing pages:       N  (list concept names, or "none")
   Contradictions:      N  (list affected pages, or "none")
   Stale claims:        N  (list affected pages, or "none")

🔧 Auto-fixed: N issues
   ✓ Added backlink X → Y
   ✓ Created stub wiki/missing-concept.md
   ...

📌 Needs manual review: N issues
   ! wiki/concept.md — contradiction between "Source A" and "Source B" on definition of Z
   ! wiki/old-claim.md — relies solely on 2018 paper; check against newer sources in /raw
   ...

📋 wiki/index.md  — updated (stubs added) / no changes
📋 wiki/log.md    — unchanged (audit does not add log rows)

🔍 Verification: open each flagged page and confirm the Contradictions section is populated.
➡️  Next step: resolve manual-review items, then commit with
    git add wiki/ && git commit -m "Wiki audit: fix orphans, contradictions, stale claims"
```

$ARGUMENTS
