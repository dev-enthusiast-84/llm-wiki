---
name: wiki-sync
description: 'Sync new sources from /raw folder with existing wiki pages. Update affected entities, create new pages, maintain index and log. Use when adding new papers to /raw.'
argument-hint: 'Source filename or description from /raw folder'
---

# Wiki Sync

Incremental wiki updates by syncing new sources from the `/raw` folder with existing entity pages.

## When to Use

- **New paper added**: A new source appears in `/raw` that needs to be integrated
- **New research**: Updating wiki with recent findings or alternative viewpoints
- **Ongoing compilation**: Regularly processing batches of papers
- **Before audit**: Sync everything before running quality checks

## Procedure

### 1. Read New Source

- Identify the new source file in `/raw`
- Read it alongside relevant existing `wiki/` pages
- Take note of:
  - Key concepts introduced
  - Definitions and explanations
  - Relationships to existing concepts
  - Any contradictions with previous understanding

### 2. Update Existing Entity Pages

For each concept that appears in both new source and existing wiki:
- **Revise explanations** if new source provides more accurate or comprehensive understanding
- **Add new related concepts** if the new source introduces fresh connections
- **Update sources section** to include the new paper
- **Flag contradictions** if the new source conflicts with previous information (add to "Contradictions" section)

See [Update Checklist](./references/update-checklist.md) for detailed guidance.

### 3. Create New Entity Pages

For concepts introduced only in the new source:
- Create new markdown files in `wiki/` following [Entity Template](./assets/entity-template.md)
- Use kebab-case filenames matching the concept name
- Link to related existing entities using `[[brackets]]`
- Always cite the new source in the Sources section

### 4. Maintain Wiki Structure

Update organizational files:

**Update `wiki/index.md`**:
- Add any new entities to appropriate categories
- Re-sort alphabetically if needed

**Update/Create `wiki/log.md`** (when wiki reaches 30+ pages):
```markdown
| Date | Source | Entities Added | Entities Updated | Notes |
|------|--------|---|---|---|
| 2026-04-20 | "Paper Title" (2024) | concept1, concept2 | existing-concept | Noted contradiction with earlier definition |
```

See [Log Format Reference](./references/log-format.md).

## Example Workflow

```
New source: "Latest LLM Survey 2026" added to /raw/
↓
Read alongside: transformer.md, bert.md, gpt-3.md
↓
Update: transformer.md (new variants), add contradictions to bert.md
↓
Create: new-concept1.md, new-concept2.md
↓
Add to: wiki/index.md categories
↓
Log: Added 2 new concepts, updated 2 existing pages
```

## Best Practices

- **One concept per file**: Keep pages focused and reusable
- **Link thoroughly**: Use `[[concept]]` to create a web of related ideas
- **Source attribution**: Always trace back to specific papers
- **Contradiction handling**: Document when sources disagree; don't assume one is "correct"
- **Iterative**: You may need to create missing pages as you discover new connections
- **Commit frequently**: Commit after syncing each source

## Reference Files

- [Update Checklist](./references/update-checklist.md) - Step-by-step verification
- [Log Format](./references/log-format.md) - How to track changes
- [Entity Template](./assets/entity-template.md) - Copy-paste structure for new pages

## Tips

- **Review existing first**: Skim all related wiki pages before creating new ones (avoid duplication)
- **Contradictions are insights**: Different sources may define concepts differently; this nuance is valuable
- **Lazy links**: If a referenced concept doesn't have a page yet, create a stub and return to it later
- **Source signal**: Pages with multiple sources are more reliable; papers cited by many sources are likely central concepts
