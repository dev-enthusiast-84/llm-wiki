---
name: wiki-compilation
description: 'Scan /raw for all supported source files and compile them into entity wiki pages. Extracts key concepts, creates interconnected markdown pages with cross-references. Use when initializing the wiki from a batch of papers in /raw.'
argument-hint: 'No argument needed — sources are read automatically from /raw'
---

# Wiki Compilation

Scan the `/raw` folder and transform all supported source files into a structured wiki by extracting key concepts and creating interconnected entity pages.

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

- Initializing the wiki for the first time from files in `/raw`
- Batch-compiling a set of papers after `/reset-wiki reset`
- Extracting definitions and links between concepts from multiple sources at once

## Procedure

### 1. Pre-flight Check

List entity pages in `wiki/` (exclude `index.md`, `log.md`). If any exist, stop and redirect to `sync-wiki` or `reset-wiki`.

### 2. Scan /raw

List all files in `raw/`. Group by supported vs unsupported extension. Announce the list before reading.

### 3. Read Each Source

Process files one at a time. For PDFs >20 pages, read in page-range chunks and combine understanding before extracting concepts.

### 4. Extract Key Concepts

For each paper source:
- Identify primary concepts and terminology
- Note definitions and explanations
- Record relationships to other concepts
- Flag conflicting definitions or approaches across sources

### 5. Create Entity Pages

For each concept, create a new markdown file in `wiki/` following the [Wiki Format](./references/wiki-format.md):
- **Filename**: kebab-case concept name (e.g., `masked-language-model.md`)
- **Content**: Use the [Entity Template](./assets/entity-template.md)
- **Links**: Connect related concepts using `[[brackets]]` syntax
- **Sources**: Reference which papers introduced or defined this concept

### 6. Update Index

Add each new entity to [wiki/index.md](../../wiki/index.md) in the appropriate category.

### 7. Update Log

Add a row to `wiki/log.md` for each source file processed:
```
| 2026-04-25 | "Paper Title" (Author, Year) | concept1, concept2 | — | Notes |
```

### 8. Resolve Contradictions

When multiple sources define a concept differently:
- Note all interpretations in the page
- Cite which papers support each definition
- Use `## Contradictions` section (see template)

## Example Workflow

```
/raw/ contains: attention.pdf, bert.pdf
↓
Read attention.pdf → extract: self-attention, positional-encoding, transformer
Read bert.pdf → extract: masked-language-model, next-sentence-prediction
↓
Create: 5 entity pages in wiki/
↓
Update: wiki/index.md (5 entries), wiki/log.md (2 source rows)
```

## Relation to Other Skills

| Skill | When to Use |
|-------|-------------|
| `reset-wiki` | **Run first** — ensures wiki is empty before compiling. If wiki has content, stops and redirects here |
| `sync-wiki` | Use instead of this skill when wiki already has pages and you're adding another paper |
| `audit-wiki` | Run after 20+ pages to catch orphan pages, missing links, and contradictions |

## Reference Files

- [Wiki Format & Conventions](./references/wiki-format.md) - Structure and style guide
- [Entity Template](./assets/entity-template.md) - Copy-paste starting point

## Tips

- **One concept per file**: Keep pages focused and reusable
- **Cross-link liberally**: Use `[[concept]]` syntax to connect ideas
- **Be precise with links**: Match exact filenames, including hyphens
- **Document sources**: Always trace concepts back to papers
- **Iterative refinement**: Update pages as you find new information
