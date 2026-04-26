---
mode: agent
description: Scan /raw for all supported source files and compile them into entity wiki pages. Extracts key concepts, creates markdown files with summaries and cross-references, notes contradictions.
---

## Pre-flight Check

Before doing anything else, list all `.md` files in `wiki/` (excluding `index.md` and `log.md`).

- **If entity pages already exist**: Stop. Tell the user the wiki has existing content and offer:
  - `Sync Wiki from Raw` — to add new files from `/raw` incrementally (keeps existing pages)
  - `Reset Wiki` with argument `reset` — to wipe everything and start fresh, then re-run this prompt
  - Do NOT create or overwrite any files. Wait for the user to decide.
- **If wiki is empty**: Proceed below.

---

## Step 1: Scan /raw for sources

List all files in `raw/`. Classify each by extension:

| Format | Read method | Limitations |
|--------|-------------|-------------|
| `.pdf` | Read tool (native) | Images/diagrams not extracted; PDFs >20 pages require reading in page-range chunks |
| `.txt` | Read tool (native) | None |
| `.html` | Read tool, then strip tags with Python if output is noisy | Inline JS/CSS may add noise; complex layouts may lose structure |
| `.pptx` | Extract text via python-pptx bash command | Only text extracted; charts, images, diagrams, and speaker notes are lost |
| `.docx` | Extract text via python-docx bash command | Tables, images, headers/footers, and text boxes not extracted |
| `.xlsx` | Extract cell values via openpyxl bash command | Only cell values extracted; formulas shown as last-computed result; charts, images, and formatting lost |
| other | **Skip** — report filename and extension as unsupported |

Announce the list of files found and their formats before reading any of them.

## Step 2: Spawn Parallel Extraction Agents

For each supported source file from Step 1, call the Agent tool once — send **all agents in a single response** so they run in parallel. Use `subagent_type: "Explore"` for each.

Each agent prompt should name the specific file, specify its read method (Read tool for PDF/TXT/HTML; bash command for PPTX/DOCX/XLSX), and request extraction of: primary concepts, definitions, relationships between concepts, and any conflicting definitions. Each agent returns a structured list: concept name, 2–3 sentence definition, related concepts, source file.

For PDFs >20 pages, instruct the agent to read in page-range chunks (1–20, 21–40, …).

If only one source file exists, read it directly without spawning a sub-agent.

## Step 3: Collect Extraction Results

Wait for all agents to complete. Consolidate concept lists:
- Merge definitions for concepts appearing in multiple sources
- Flag conflicting definitions (record both)
- Identify cross-source relationships

## Step 4: Create entity pages

For each concept, create `wiki/<concept-name>.md` following the [Entity Template](../../skills/wiki-compilation/assets/entity-template.md):
- **Filename**: kebab-case (e.g., `self-attention.md`)
- **Summary**: 2-3 sentences, plain language
- **Links**: `[[concept-name]]` for all related concepts
- **Sources**: cite by paper title and year
- **Contradictions**: document if sources define the concept differently

## Step 5: Update wiki/index.md

Add every new entity under the appropriate category.

## Step 6: Update wiki/log.md

Add a row to the Compilation History table for each source processed.

## Output

After all steps, emit this results block:

```
✅ Compile Papers — complete  YYYY-MM-DD

📥 Sources processed: N
   ✓ file1.pdf
   ✓ file2.txt
   ⊘ file3.xyz  (unsupported — skipped)

📄 Entity pages created: N
📋 wiki/index.md  — updated (N new entries)
📋 wiki/log.md    — updated (N new rows)

⚠️  Issues: <none | list contradictions or parse errors>

➡️  Next step: commit with  git add wiki/ && git commit -m "Compile wiki: <summary>"
    When wiki reaches 20+ pages, run Audit Wiki for a quality check.
```
