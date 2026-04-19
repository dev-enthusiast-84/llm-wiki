---
name: llm-wiki-commands
description: "LLM Wiki compilation and sync commands. Available prompts for managing wiki content."
---

# LLM Wiki Commands

This workspace includes two main commands for managing wiki content:

## Available Prompts

### `/Compile Papers to Wiki`
Initial setup prompt for building the wiki from research papers.
- Extract key concepts from new sources
- Create markdown entity pages with summaries
- Cross-link related concepts using `[[brackets]]`
- Document contradictions between papers

**Use when**: Setting up the wiki or processing a batch of papers

### `/Sync Wiki from Raw`
Incremental update prompt for syncing new sources from `/raw` folder.
- Read new sources alongside existing wiki pages
- Update affected entity pages
- Create new pages for novel concepts
- Maintain `index.md` and `log.md` (30+ entities)

**Use when**: Adding new papers or research to `/raw` folder

### `/Audit Wiki`
Quality assurance prompt for comprehensive wiki maintenance.
- Find orphan pages (no inbound links)
- Identify missing pages (referenced but not created)
- Detect contradictions across pages
- Flag stale claims superseded by newer sources

**Use when**: Wiki reaches ~20-30 pages (recommend monthly)

## Workflow

1. **New paper?** Add to `/raw` folder
2. **Initial setup?** Use `/Compile Papers to Wiki`
3. **Incremental update?** Use `/Sync Wiki from Raw`
4. **Reaching 20+ pages?** Use `/Audit Wiki` for quality checks
5. **Need guidance?** Check skill docs in `skills/` folder for detailed procedures

## Resources

**Wiki Compilation**:
- Skill: `skills/wiki-compilation/SKILL.md`
- Template: `skills/wiki-compilation/assets/entity-template.md`
- Format Guide: `skills/wiki-compilation/references/wiki-format.md`

**Wiki Sync**:
- Skill: `skills/wiki-sync/SKILL.md`
- Update Checklist: `skills/wiki-sync/references/update-checklist.md`
- Log Format: `skills/wiki-sync/references/log-format.md`
- Entity Template: `skills/wiki-sync/assets/entity-template.md`

**Wiki Audit**:
- Skill: `skills/wiki-audit/SKILL.md`
- Audit Checklist: `skills/wiki-audit/references/audit-checklist.md`
- Report Template: `skills/wiki-audit/assets/audit-report.md`
