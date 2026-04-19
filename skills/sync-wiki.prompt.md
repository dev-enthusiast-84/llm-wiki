---
description: "Sync new sources from /raw to wiki. Update existing entities, create new pages, maintain index and log for 30+ entities. Use when adding new papers or research to the raw folder."
name: "Sync Wiki from Raw"
argument-hint: "New source in /raw folder"
---

A new source has been added to the `/raw` folder. Sync it with the existing wiki:

## Workflow

1. **Read the new source** alongside existing wiki pages in `wiki/`
2. **Update existing entity pages** affected by this new source:
   - Revise explanations if new information is more accurate or comprehensive
   - Add new related concepts section if relevant
   - Update sources to include the new paper
   - Flag contradictions if the new source conflicts with previous understanding
3. **Create new entity pages** for concepts introduced only in the new source:
   - Follow the format in [Entity Template](./skills/wiki-sync/assets/entity-template.md)
   - Use kebab-case filenames
   - Link to related existing entities using `[[brackets]]`
   - Always cite the source
4. **Maintain wiki structure**:
   - Update `wiki/index.md` with any new entities
   - If wiki now has 30+ pages: create/update `wiki/log.md` tracking:
     - What was compiled
     - When it was added
     - Which source(s) it came from

## Key Guidelines

- **One concept per file**: Keep pages focused and reusable
- **Cross-link**: Use `[[concept]]` to connect related ideas
- **Cite sources**: Always trace concepts back to papers
- **Document contradictions**: Note when sources define things differently
- **Incremental updates**: Don't recreate existing pages unless needed

## Log Format (30+ entities)

```markdown
| Date | Source | Entities Added | Entities Updated | Notes |
|------|--------|---|---|---|
| 2026-04-19 | "Paper Title" (Year) | concept1, concept2 | existing-concept | Noted contradiction with Paper X |
```

See [Wiki Sync Skill](./skills/wiki-sync/SKILL.md) and [Update Checklist](./skills/wiki-sync/references/update-checklist.md) for detailed guidance.

Provide the filename or description of the new source in `/raw` to begin syncing.
