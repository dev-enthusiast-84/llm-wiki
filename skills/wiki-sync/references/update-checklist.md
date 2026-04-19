# Wiki Sync Update Checklist

Use this checklist when syncing a new source to the wiki.

## Pre-Sync Review

- [ ] Read new source from `/raw`
- [ ] List all key concepts mentioned
- [ ] Identify which concepts already have wiki pages
- [ ] Note which concepts are entirely new
- [ ] Read relevant existing wiki pages before making changes

## Update Existing Pages

For each concept that exists in both source and wiki:

| Concept | Page | Update Needed? | Type | Notes |
|---------|------|---|---|---|
| | | [ ] Yes [ ] No | [ ] Revision [ ] Link [ ] Contradiction | |
| | | [ ] Yes [ ] No | [ ] Revision [ ] Link [ ] Contradiction | |

**Changes made**:
- [ ] Explanations updated
- [ ] Related concepts added
- [ ] Sources section updated
- [ ] Contradictions documented

## Create New Pages

Concepts only in new source (no existing page):

- [ ] `concept-name-1.md` — Created
- [ ] `concept-name-2.md` — Created
- [ ] All new pages include:
  - [ ] Clear summary (2-3 sentences)
  - [ ] Detailed explanation
  - [ ] Related concepts linked with `[[brackets]]`
  - [ ] Sources cited

**Pages created**: __________ (count)

## Maintain Wiki Index

- [ ] Added all new concepts to `wiki/index.md`
- [ ] Verified alphabetical sorting
- [ ] All entries have one-line descriptions
- [ ] Categories are accurate

## Update Log

**For wikis with 30+ pages**:

- [ ] Updated `wiki/log.md` with entry:
  - [ ] Date
  - [ ] Source filename/title
  - [ ] Count of new entities
  - [ ] Count of updated entities
  - [ ] Special notes (contradictions found, stale info, etc.)

**Suggested log entry**:
```
| [DATE] | "[SOURCE TITLE]" ([YEAR]) | [NEW COUNT] | [UPDATE COUNT] | [NOTES] |
```

## Quality Check

- [ ] No orphan pages created (all new pages are linked from somewhere)
- [ ] No duplicate concepts (same idea in multiple pages)
- [ ] Sources section on every page cites which papers
- [ ] Contradictions section added where applicable
- [ ] All `[[references]]` have matching pages OR are marked as "TODO"

## Commit

- [ ] Changes staged
- [ ] Commit message: "Sync wiki: Add [X] new concepts, update [Y] pages from [SOURCE]"
- [ ] Example: `Sync wiki: Add masked-language-model, add-on-concepts from BERT paper`

---

**Status**: In progress / Complete  
**Source synced**: _________________  
**Date**: _________________  
**Entities added**: _________ | **Entities updated**: _________
