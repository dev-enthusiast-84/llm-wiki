---
description: Scan /raw for unsynced sources and incrementally update the wiki. Updates existing entities, creates new pages, maintains index and log.
---

## Usage

**Invoke:** type `/sync-wiki` in the Claude Code CLI  
**When to run:** any time new files are added to `raw/` after the initial compile  
**Prerequisites:**
- `wiki/` must already contain entity pages (i.e., `/compile-papers` has been run at least once)
- New source files must be present in `raw/` that are not yet listed in `wiki/log.md`

**Arguments:** none required  
**Tip:** run `git diff wiki/log.md` to see which sources are already logged before invoking.

---

## Step 1: Identify unsynced sources

1. List all files in `raw/` with supported extensions: `.pdf`, `.txt`, `.html`, `.pptx`, `.docx`, `.xlsx`
2. Read `wiki/log.md` — check the "Source" column for already-compiled filenames
3. Files to process = files in `raw/` **not yet present in log.md**

If all files are already logged: report **"Wiki is up to date — no new sources found in /raw."** and stop.

If new files exist: announce them before processing.

## Step 2: Read New Sources

**Single new file**: read it directly using the format table below, then proceed to Step 3.

**Two or more new files**: call the Agent tool once per file in a **single response** so all reads run in parallel. Use `subagent_type: "Explore"` for each. Each agent prompt should name the specific file, specify the read method for its format, and return: concepts introduced, existing wiki pages that need updating, proposed updates to those pages, and proposed new pages. Collect all agent results before proceeding to Step 3.

Format read methods:

| Format | Read method |
|--------|-------------|
| `.pdf` | `Read` tool — for PDFs >20 pages read in page-range chunks (1–20, 21–40, …) |
| `.txt` | `Read` tool |
| `.html` | `Read` tool, strip tags with Python if noisy |
| `.pptx` | `python3 -c "from pptx import Presentation; prs=Presentation('raw/FILE.pptx'); [print(s.text_frame.text) for slide in prs.slides for s in slide.shapes if s.has_text_frame]"` |
| `.docx` | `python3 -c "import docx; doc=docx.Document('raw/FILE.docx'); print('\n'.join(p.text for p in doc.paragraphs if p.text.strip()))"` |
| `.xlsx` | `python3 -c "import openpyxl; wb=openpyxl.load_workbook('raw/FILE.xlsx',read_only=True,data_only=True); [print(ws.title,[[str(c.value) for c in r] for r in ws.iter_rows()]) for ws in wb.worksheets]"` |
| other | **Skip** — report as unsupported |

## Step 3: Update existing entity pages

For each concept that appears in both the new source and existing wiki pages:
- **Revise explanations** if the new source is more accurate or comprehensive
- **Add related concepts** if the new source introduces fresh connections
- **Update Sources section** to include the new paper
- **Flag contradictions** — add to `## Contradictions` section if the new source conflicts

See [Update Checklist](../skills/wiki-sync/references/update-checklist.md) for detailed guidance.

## Step 4: Create new entity pages

For concepts introduced only in the new source:
- Create `wiki/<concept-name>.md` following [Entity Template](../skills/wiki-sync/assets/entity-template.md)
- Use kebab-case filenames
- Link to related existing entities with `[[brackets]]`
- Always cite the source

## Step 5: Maintain wiki structure

**Update `wiki/index.md`**: add new entities to appropriate categories.

**Update `wiki/log.md`**: add a row per new source processed:
```
| YYYY-MM-DD | "Paper Title" (Author, Year) | new-concept1, new-concept2 | updated-concept1 | Notes |
```
Update the Summary block (Total pages, Last updated, Last source).

---

## Verification Steps

After the skill completes, confirm success by checking:

1. **Log updated**: open `wiki/log.md` — each new source should have a row with today's date
2. **New pages created**: `ls wiki/*.md` — new concept files should appear for novel concepts
3. **Existing pages updated**: open a page that should have changed — verify the Sources section lists the new paper
4. **Index current**: open `wiki/index.md` — new concepts should appear under appropriate categories
5. **No orphan links**: new pages should use `[[brackets]]` that resolve to real filenames

---

## Results Summary

Once all steps are complete, output this exact block:

```
✅ Sync Wiki — complete  YYYY-MM-DD

📥 New sources processed: N
   ✓ new-paper.pdf
   ⊘ already-logged.pdf  (skipped — already in log.md)

📄 Entity pages created: N
   wiki/new-concept.md
   ...

📝 Entity pages updated: N
   wiki/existing-concept.md  (added source, revised explanation)
   ...

⚠️  Contradictions flagged: N
   wiki/concept-name.md — conflicts with "Other Paper (Year)" on definition of X

📋 wiki/index.md  — updated (N new entries)
📋 wiki/log.md    — updated (N new rows)

🔍 Verification: open wiki/log.md and confirm the new source row appears with today's date.
➡️  Next step: commit with  git add wiki/ && git commit -m "Sync wiki: <summary>"
    Run /audit-wiki if wiki has grown to 20+ pages.
```

$ARGUMENTS
