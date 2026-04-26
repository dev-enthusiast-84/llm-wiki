---
name: wiki-sync
description: 'Scan /raw for files not yet in log.md and incrementally update the wiki. Updates affected entities, creates new pages, maintains index and log. Use when adding new files to /raw.'
argument-hint: 'No argument needed — new sources are detected automatically from /raw vs log.md'
---

# Wiki Sync

Scan `/raw` for source files not yet compiled into the wiki, then incrementally update entity pages and create new ones.

## Supported Source Formats

| Format | Read method | Limitations |
|--------|-------------|-------------|
| `.pdf` | Read tool (native) | Images/diagrams not extracted; PDFs >20 pages require reading in page-range chunks |
| `.txt` | Read tool (native) | None |
| `.html` | Read tool, then strip tags with Python if output is noisy | Inline JS/CSS may add noise; complex layouts may lose structure |
| `.pptx` | `python3 -c "from pptx import Presentation; prs=Presentation('raw/FILE.pptx'); [print(s.text_frame.text) for slide in prs.slides for s in slide.shapes if s.has_text_frame]"` | Only text extracted; charts, images, diagrams, and speaker notes are lost |
| `.docx` | `python3 -c "import docx; doc=docx.Document('raw/FILE.docx'); print('\n'.join(p.text for p in doc.paragraphs if p.text.strip()))"` | Tables, images, headers/footers, and text boxes not extracted |
| `.xlsx` | `python3 -c "import openpyxl; wb=openpyxl.load_workbook('raw/FILE.xlsx',read_only=True,data_only=True); [print(ws.title,[[str(c.value) for c in r] for r in ws.iter_rows()]) for ws in wb.worksheets]"` | Only cell values extracted; formulas shown as last-computed result; charts, images, and formatting lost |
| other | Skip — report filename and extension as unsupported | — |

## When to Use

- A new file has been dropped into `/raw` and the wiki already has content
- Running a batch catch-up after several files were added at once
- Before an audit — ensure everything in `/raw` is reflected in the wiki

## Procedure

### 1. Detect New Sources

List all files in `raw/` with supported extensions. Cross-reference against the "Source" column in `wiki/log.md`. Files not yet logged are the ones to process.

If nothing is new: report "Wiki is up to date." and stop.

### 2. Read New Sources

**Single new file**: read it directly using the format table above, then proceed to Step 3.

**Two or more new files**: call the Agent tool once per file in a **single response** so all reads run in parallel. Use `subagent_type: "Explore"` for each agent. Each agent prompt should name its specific file, specify the read method for its format, and return: concepts introduced, existing wiki pages that need updating, proposed page updates, and proposed new pages. Collect all agent results before proceeding to Step 3.

### 3. Update Existing Entity Pages

For each concept that appears in both new source and existing wiki:
- **Revise explanations** if new source provides more accurate or comprehensive understanding
- **Add new related concepts** if the new source introduces fresh connections
- **Update sources section** to include the new paper
- **Flag contradictions** if the new source conflicts with previous information (add to "Contradictions" section)

See [Update Checklist](./references/update-checklist.md) for detailed guidance.

### 4. Create New Entity Pages

For concepts introduced only in the new source:
- Create new markdown files in `wiki/` following [Entity Template](./assets/entity-template.md)
- Use kebab-case filenames matching the concept name
- Link to related existing entities using `[[brackets]]`
- Always cite the new source in the Sources section

### 5. Maintain Wiki Structure

**Update `wiki/index.md`**:
- Add any new entities to appropriate categories
- Re-sort alphabetically if needed

**Update `wiki/log.md`**:
- Add a row per source file processed
- Update the Summary block (Total pages, Last updated, Last source)

See [Log Format Reference](./references/log-format.md).

## Example Workflow

```
/raw/ now contains: attention.pdf (logged), new-survey.pdf (NOT logged)
↓
Detect: new-survey.pdf is new
↓
Read new-survey.pdf
↓
Update: transformer.md (new variants), bert.md (contradiction noted)
↓
Create: new-concept1.md, new-concept2.md
↓
Add to: wiki/index.md, wiki/log.md
```

## Relation to Other Skills

| Skill | When to Use |
|-------|-------------|
| `reset-wiki` | Use instead of this skill when you want to start over entirely — wipes all pages before a fresh compile |
| `compile-papers` | Use instead of this skill when wiki is empty — bulk-compiles the first batch of papers |
| `audit-wiki` | Run after 20+ pages to check for orphans, missing links, and stale claims introduced by incremental syncs |

## Best Practices

- **One concept per file**: Keep pages focused and reusable
- **Link thoroughly**: Use `[[concept]]` to create a web of related ideas
- **Source attribution**: Always trace back to specific papers
- **Contradiction handling**: Document when sources disagree; don't assume one is "correct"
- **Iterative**: You may need to create missing pages as you discover new connections

## Reference Files

- [Update Checklist](./references/update-checklist.md) - Step-by-step verification
- [Log Format](./references/log-format.md) - How to track changes
- [Entity Template](./assets/entity-template.md) - Copy-paste structure for new pages

## Tips

- **Review existing first**: Skim all related wiki pages before creating new ones (avoid duplication)
- **Contradictions are insights**: Different sources may define concepts differently; this nuance is valuable
- **Lazy links**: If a referenced concept doesn't have a page yet, create a stub and return to it later
- **Source signal**: Pages with multiple sources are more reliable; papers cited by many sources are likely central concepts
