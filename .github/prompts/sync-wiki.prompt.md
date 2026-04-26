---
mode: agent
description: Scan /raw for unsynced sources and incrementally update the wiki. Updates existing entities, creates new pages, maintains index and log.
---

## Step 1: Identify unsynced sources

1. List all files in `raw/` with supported extensions: `.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`
2. Read `wiki/log.md` — check the "Source" column for already-compiled filenames
3. Files to process = files in `raw/` **not yet present in log.md**

If all files are already logged: report **"Wiki is up to date — no new sources found in /raw."** and stop.

If new files exist: announce them before processing.

## Step 2: Read New Sources

**Single new file**: read it directly using the appropriate format method (Read tool for PDF/TXT/HTML; bash command for PPTX/DOCX/XLSX), then proceed to Step 3.

**Two or more new files**: call the Agent tool once per file in a **single response** so all reads run in parallel. Use `subagent_type: "Explore"` for each. Each agent prompt names its file, specifies the read method, and returns: concepts introduced, existing wiki pages to update, proposed updates, and proposed new pages. Collect all agent results before proceeding.

| Format | Read method |
|--------|-------------|
| `.pdf` | Read tool — for >20 pages read in chunks (1–20, 21–40, …) |
| `.txt` | Read tool |
| `.html` | Read tool, strip tags with Python if noisy |
| `.pptx` | python-pptx bash command |
| `.docx` | python-docx bash command |
| `.xlsx` | openpyxl bash command |
| other | **Skip** — report as unsupported |

## Step 3: Update existing entity pages

For each concept in the new source that overlaps with existing wiki pages:
- Revise explanations if the new source is more accurate or comprehensive
- Add related concepts if fresh connections are introduced
- Update the Sources section to include the new paper
- Flag contradictions in the `## Contradictions` section

See [Wiki Sync Skill](../../skills/wiki-sync/SKILL.md) and [Update Checklist](../../skills/wiki-sync/references/update-checklist.md) for guidance.

## Step 4: Create new entity pages

For concepts introduced only in the new source:
- Create `wiki/<concept-name>.md` following the [Entity Template](../../skills/wiki-sync/assets/entity-template.md)
- Use kebab-case filenames
- Link to related existing entities with `[[brackets]]`
- Always cite the source

## Step 5: Maintain wiki structure

- **Update `wiki/index.md`**: add new entities to appropriate categories
- **Update `wiki/log.md`**: add a row per source processed; update the Summary block

## Output

After all steps, emit this results block:

```
✅ Sync Wiki — complete  YYYY-MM-DD

📥 New sources processed: N
   ✓ new-paper.pdf
   ⊘ already-logged.pdf  (skipped — already in log.md)

📄 Entity pages created: N
📝 Entity pages updated: N
⚠️  Contradictions flagged: N

📋 wiki/index.md  — updated (N new entries)
📋 wiki/log.md    — updated (N new rows)

➡️  Next step: commit with  git add wiki/ && git commit -m "Sync wiki: <summary>"
    Run Audit Wiki if wiki has grown to 20+ pages.
```
