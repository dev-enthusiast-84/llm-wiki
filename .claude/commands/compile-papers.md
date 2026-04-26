---
description: Scan /raw for all supported source files and compile them into entity wiki pages. Extracts key concepts, creates markdown files with summaries and cross-references, notes contradictions.
---

## Usage

**Invoke:** type `/compile-papers` in the Claude Code CLI  
**When to run:** first time setting up the wiki, or when starting a fresh batch after a reset  
**Prerequisites:**
- At least one source file inside `raw/` (`.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`)
- `wiki/` directory must be empty (no entity pages other than `index.md` / `log.md`); if pages exist, use `/sync-wiki` instead  

**Arguments:** none required  
**Do not run** if entity pages already exist — use `/sync-wiki` to add new sources incrementally.

---

## Pre-flight Check

Before doing anything else, list all `.md` files in `wiki/` (excluding `index.md` and `log.md`).

- **If entity pages already exist**: Stop immediately. Tell the user the wiki has existing content and offer:
  - `/sync-wiki` — add new files from `/raw` incrementally (keeps existing pages)
  - `/reset-wiki reset` — wipe everything and start fresh, then re-run `/compile-papers`
  - Do NOT create or overwrite any files. Wait for the user to decide.
- **If wiki is empty**: Proceed below.

---

## Step 1: Scan /raw for sources

List all files in `raw/`. Classify each by extension:

| Format | Read method | Limitations |
|--------|-------------|-------------|
| `.pdf` | `Read` tool (native) | Images/diagrams not extracted; PDFs >20 pages require reading in page-range chunks |
| `.txt` | `Read` tool (native) | None |
| `.html` | `Read` tool, then strip tags with Python if output is noisy | Inline JS/CSS may add noise; complex layouts may lose structure |
| `.pptx` | `python3 -c "from pptx import Presentation; prs=Presentation('raw/FILE.pptx'); [print(s.text_frame.text) for slide in prs.slides for s in slide.shapes if s.has_text_frame]"` | Only text extracted; charts, images, diagrams, and speaker notes are lost |
| `.docx` | `python3 -c "import docx; doc=docx.Document('raw/FILE.docx'); print('\n'.join(p.text for p in doc.paragraphs if p.text.strip()))"` | Tables, images, headers/footers, text boxes not extracted |
| `.xlsx` | `python3 -c "import openpyxl; wb=openpyxl.load_workbook('raw/FILE.xlsx',read_only=True,data_only=True); [print(ws.title,[[str(c.value) for c in r] for r in ws.iter_rows()]) for ws in wb.worksheets]"` | Only cell values; formulas shown as last result; charts and images lost |
| other | **Skip** — report filename and extension as unsupported |

Announce the list of files found and their formats before reading any of them.

## Step 2: Spawn Parallel Extraction Agents

For each supported source file from Step 1, call the Agent tool once — send **all file agents in a single response** so they run in parallel. Do not process files sequentially.

Use `subagent_type: "Explore"` for each agent. Tailor the prompt to the file's format:

- **PDF**: "Read `raw/<filename>` using the Read tool. For PDFs longer than 20 pages, read in page-range chunks (pages 1–20, 21–40, …) until complete. Extract all key concepts: for each, return its name, a 2–3 sentence plain-language definition, related concepts mentioned, and any conflicting definitions across sections."
- **TXT / HTML**: "Read `raw/<filename>` using the Read tool (strip HTML tags with Python if the output is noisy). Extract all key concepts as above."
- **PPTX**: "Run `python3 -c \"from pptx import Presentation; prs=Presentation('raw/<filename>'); [print(s.text_frame.text) for slide in prs.slides for s in slide.shapes if s.has_text_frame]\"`. Extract all key concepts from the text output."
- **DOCX**: "Run `python3 -c \"import docx; doc=docx.Document('raw/<filename>'); print('\\n'.join(p.text for p in doc.paragraphs if p.text.strip()))\"`. Extract all key concepts from the output."
- **XLSX**: "Run `python3 -c \"import openpyxl; wb=openpyxl.load_workbook('raw/<filename>',read_only=True,data_only=True); [print(ws.title,[[str(c.value) for c in r] for r in ws.iter_rows()]) for ws in wb.worksheets]\"`. Extract all key concepts from the cell data."

Each agent should return a structured list: concept name, definition, related concepts, source file.

If only one source file exists, you may read it directly rather than spawning a sub-agent.

## Step 3: Collect Extraction Results

Wait for all extraction agents to complete. Consolidate their concept lists:
- Merge definitions for concepts that appear in multiple sources
- Flag conflicting definitions between sources (record both)
- Identify cross-source concept relationships

## Step 4: Create entity pages

For each concept, create `wiki/<concept-name>.md` following the [Entity Template](../skills/wiki-compilation/assets/entity-template.md):
- **Filename**: kebab-case (e.g., `self-attention.md`)
- **Summary**: 2–3 sentences, plain language
- **Links**: `[[concept-name]]` for all related concepts
- **Sources**: cite by paper title and year
- **Contradictions**: document if sources define the concept differently

## Step 5: Update wiki/index.md

Add every new entity under the appropriate category.

## Step 6: Update wiki/log.md

Add a row to the Compilation History table for each source processed:
```
| YYYY-MM-DD | "Paper Title" (Author, Year) | concept1, concept2 | — | Notes |
```
Update the Summary block (Total pages, Last updated, Last source).

---

## Verification Steps

After the skill completes, confirm success by checking:

1. **Entity pages exist**: `ls wiki/*.md` — should list new concept files (not just `index.md` / `log.md`)
2. **Index updated**: open `wiki/index.md` — all new concepts should appear under a category
3. **Log updated**: open `wiki/log.md` — a new row should appear for each source processed, with today's date
4. **Page structure**: open any entity page — verify it has `## Summary`, `## Related Concepts`, and `## Sources` sections
5. **Cross-links work**: confirm `[[bracket]]` references in one page match actual filenames of other pages

---

## Results Summary

Once all steps are complete, output this exact block:

```
✅ Compile Papers — complete  YYYY-MM-DD

📥 Sources processed: N
   ✓ file1.pdf
   ✓ file2.txt
   ⊘ file3.xyz  (unsupported — skipped)

📄 Entity pages created: N
   wiki/concept-a.md
   wiki/concept-b.md
   ...

📋 wiki/index.md  — updated (N new entries)
📋 wiki/log.md    — updated (N new rows)

⚠️  Issues: <none | list any contradictions flagged or parse errors>

🔍 Verification: open wiki/index.md and confirm all new concepts appear.
➡️  Next step: commit with  git add wiki/ && git commit -m "Compile wiki: <summary>"
    When wiki reaches 20+ pages, run /audit-wiki for a quality check.
```

$ARGUMENTS
