# LLM Wiki — Personal Knowledge Base

A structured system for building and maintaining a personal wiki of LLM/AI concepts from research papers. Extract key concepts from sources, create interconnected entity pages, and keep your knowledge base organized and up-to-date.

**[Live docs →](https://dev-enthusiast-84.github.io/llm-wiki/)** · **[GitHub →](https://github.com/dev-enthusiast-84/llm-wiki)**

## Quick Start

1. **Add papers** to the `raw/` folder
2. **Run compile** to extract concepts and create entity pages
3. **Add new papers?** Run sync for incremental updates
4. **Reach 20+ pages?** Run audit for quality checks
5. **Query the wiki?** Launch the browser UI

> **Choose your tool:**
>
> | Step | Claude Code CLI | GitHub Copilot Chat |
> |------|----------------|---------------------|
> | Full pipeline | `/orchestrate-wiki` | `Orchestrate Wiki` |
> | Compile | `/compile-papers` | `Compile Papers to Wiki` |
> | Sync | `/sync-wiki` | `Sync Wiki from Raw` |
> | Audit | `/audit-wiki` | `Audit Wiki` |
> | Reset | `/reset-wiki` | `Reset Wiki` |
> | Query UI | `/launch-wiki-ui` | `Launch Wiki UI` |
> | Stop UI | `/stop-wiki-ui` | `Stop Wiki UI` |
> | Sync docs | `/sync-docs` | `Sync Docs` |
> | Run maintenance | `/run-maintenance` | `Run Maintenance` |
> | Regen presentation | `/regenerate-presentation` | `Regenerate Presentation` |

---

## Folder Structure

```
llm-wiki/
├── raw/                              # Source materials (papers, articles, docs)
├── wiki/                             # Your knowledge base
│   ├── index.md                      # (Auto-generated) Directory of all entities
│   ├── log.md                        # (Auto-generated) Compilation history
│   └── <concept>.md                  # Entity pages — one per concept
├── wiki_query.py                     # Browser UI for querying the wiki with LLMs
├── start-wiki-ui.sh                  # Start script to launch Browser UI
├── stop-wiki-ui.sh                   # Terminator script for Browser UI
├── tests/                            # Automated tests (63 tests)
│   ├── conftest.py                   # Streamlit mock, shared fixtures
│   └── test_wiki_query.py            # Validation, file loading, prompt, API
├── .github/
│   └── prompts/                      # GitHub Copilot prompt files (auto-discovered)
│       ├── orchestrate-wiki.prompt.md        # Copilot: Orchestrate Wiki
│       ├── compile-papers.prompt.md          # Copilot: Compile Papers to Wiki
│       ├── sync-wiki.prompt.md               # Copilot: Sync Wiki from Raw
│       ├── audit-wiki.prompt.md              # Copilot: Audit Wiki
│       ├── reset-wiki.prompt.md              # Copilot: Reset Wiki
│       ├── launch-wiki-ui.prompt.md          # Copilot: Launch Wiki UI
│       ├── stop-wiki-ui.prompt.md            # Copilot: Stop Wiki UI
│       ├── sync-docs.prompt.md               # Copilot: Sync Docs
│       ├── run-maintenance.prompt.md         # Copilot: Run Maintenance
│       └── regenerate-presentation.prompt.md # Copilot: Regenerate Presentation
├── skills/                           # Skill assets & references (flat)
│   ├── orchestrate-wiki/             # Full pipeline orchestration skill
│   ├── wiki-compilation/             # Compile skill assets & references
│   ├── wiki-sync/                    # Sync skill assets & references
│   ├── wiki-audit/                   # Audit skill assets & references
│   ├── wiki-reset/                   # Reset skill assets & references
│   ├── stop-wiki-ui/                 # Stop Wiki UI skill
│   └── repo-maintenance/             # Repo maintenance skill assets
├── .claude/
│   └── commands/                     # Claude Code slash commands (auto-discovered)
│       ├── orchestrate-wiki.md            # Claude: /orchestrate-wiki
│       ├── compile-papers.md              # Claude: /compile-papers
│       ├── sync-wiki.md                   # Claude: /sync-wiki
│       ├── audit-wiki.md                  # Claude: /audit-wiki
│       ├── reset-wiki.md                  # Claude: /reset-wiki
│       ├── launch-wiki-ui.md              # Claude: /launch-wiki-ui
│       ├── stop-wiki-ui.md                # Claude: /stop-wiki-ui
│       ├── sync-docs.md                   # Claude: /sync-docs
│       ├── run-maintenance.md             # Claude: /run-maintenance
│       └── regenerate-presentation.md     # Claude: /regenerate-presentation
├── presentation/                     # Slide deck and demo videos
├── extensions/                       # Browser & tool integrations
│   └── README.md                     # Obsidian Web Clipper setup
├── copilot-instructions.md           # Copilot workspace configuration
├── pytest.ini                        # Test runner configuration
└── .gitignore                        # Excludes .env, secrets, generated binaries
```

---

## Workflows

### Step 1: Compile Initial Wiki

**Use when:** starting the wiki for the first time, or after a reset.

| Tool | Command | Prerequisite |
|------|---------|-------------|
| Claude Code | `/compile-papers` | Files in `raw/`, empty `wiki/` |
| GitHub Copilot | `Compile Papers to Wiki` | Files in `raw/`, empty `wiki/` |

**What it does:**
- Reads every supported file in `raw/` (PDF, TXT, HTML, PPTX, DOCX, XLSX)
- Extracts key concepts, definitions, and relationships
- Creates `wiki/<concept>.md` for each concept (summary, links, sources)
- Updates `wiki/index.md` and `wiki/log.md`

**Example flow:**
```
raw/transformer-2017.pdf + raw/bert-2019.pdf
         ↓ compile
wiki/transformer.md, wiki/self-attention.md, wiki/bert.md, wiki/masked-lm.md
         ↓
wiki/index.md ← 4 new entries    wiki/log.md ← 2 new rows
```

**Verify the result:**
1. `ls wiki/*.md` — entity pages appear (not just `index.md` / `log.md`)
2. Open `wiki/index.md` — all concepts listed under categories
3. Open any entity page — has `## Summary`, `## Related Concepts`, `## Sources`
4. Open `wiki/log.md` — new row with today's date per source

**Results summary (emitted by the skill):**
```
✅ Compile Papers — complete  YYYY-MM-DD
📥 Sources processed: N   📄 Pages created: N   📋 index + log updated
⚠️  Issues: none / <list>
```

---

### Step 2: Sync New Sources

**Use when:** new files have been added to `raw/` after the initial compile.

| Tool | Command | Prerequisite |
|------|---------|-------------|
| Claude Code | `/sync-wiki` | Existing wiki pages + new files in `raw/` |
| GitHub Copilot | `Sync Wiki from Raw` | Existing wiki pages + new files in `raw/` |

**What it does:**
- Compares `raw/` against `wiki/log.md` to find unprocessed sources
- Updates existing entity pages (new sources, revised explanations, contradiction flags)
- Creates new entity pages for novel concepts
- Updates `wiki/index.md` and `wiki/log.md`

**When to sync:**
- After adding any new paper to `raw/`
- After using Obsidian Web Clipper to clip articles
- On a regular schedule (weekly/monthly)

**Verify the result:**
1. Open `wiki/log.md` — new row with today's date
2. `ls wiki/*.md` — new concept files present
3. Open an updated page — Sources section lists the new paper
4. Open `wiki/index.md` — new concepts under appropriate categories

**Results summary (emitted by the skill):**
```
✅ Sync Wiki — complete  YYYY-MM-DD
📥 New sources: N   📄 Created: N   📝 Updated: N
⚠️  Contradictions flagged: N   📋 index + log updated
```

---

### Step 3: Audit for Quality

**Use when:** wiki reaches ~20–30 pages, after a large sync, or before sharing.

| Tool | Command | Prerequisite |
|------|---------|-------------|
| Claude Code | `/audit-wiki` | Existing wiki pages |
| GitHub Copilot | `Audit Wiki` | Existing wiki pages |

**Scoped audit:** add `orphans`, `missing`, `contradictions`, or `stale` as an argument to run only one check.

**What it checks:**

| Check | What it finds |
|-------|--------------|
| Orphan pages | Entity pages no other page links to |
| Missing pages | `[[brackets]]` referencing non-existent pages |
| Contradictions | Conflicting definitions across pages |
| Stale claims | Information only supported by old sources |

**Verify the result:**
1. Each formerly-orphan page now has at least one inbound link
2. Stub pages created for top-priority missing concepts
3. Affected pages have a populated `## Contradictions` section
4. Items needing manual review are listed with specific page+issue details

**Results summary (emitted by the skill):**
```
✅ Audit Wiki — complete  YYYY-MM-DD
🔍 Orphans: N   Missing: N   Contradictions: N   Stale: N
🔧 Auto-fixed: N   📌 Needs review: N (list)
```

---

### Step 4: Query the Wiki

**Use when:** you want to ask questions about your wiki through a browser interface.

| Tool | Command | Prerequisite |
|------|---------|-------------|
| Claude Code | `/launch-wiki-ui` | `wiki_query.py`, Python 3, API key from any major LLM provider |
| GitHub Copilot | `Launch Wiki UI` | `wiki_query.py`, Python 3, API key from any major LLM provider |

**Or launch directly:**

1. Install dependencies:
   ```bash
   pip install streamlit litellm
   ```

2. (Optional) Pre-fill your API key via environment variable so the Settings screen auto-populates it:
   ```bash
   export LLM_API_KEY="your-provider-api-key"
   ```

3. Run from the project root (where `wiki_query.py` lives):
   ```bash
   streamlit run wiki_query.py
   ```

   or run the start script

    ```bash
   sh ./start-wiki-ui.sh
   ```

   The app opens at **http://localhost:8501**.

4. (Optional) To stop the UI (if force stop required), run from the project root

 ```bash
   sh ./stop-wiki-ui.sh
   ```

**Three-screen flow:**

| Screen | What happens |
|--------|-------------|
| **1. Settings** | Enter a model ID and API key from any major LLM provider — both validated before proceeding |
| **2. Wiki confirmation** | Review which entity pages are loaded; blocks querying if wiki is empty |
| **3. Chat** | Ask questions — answers grounded strictly in the wiki (no hallucination) |

**Supported providers** (enter the model ID exactly as shown):

| Provider | Example model IDs |
|----------|-------------------|
| Anthropic | `claude-opus-4-7` · `claude-sonnet-4-6` · `claude-haiku-4-5` |
| OpenAI | `gpt-4o` · `gpt-4o-mini` · `o3` |
| Google | `gemini/gemini-2.0-flash` · `gemini/gemini-1.5-pro` |
| Mistral | `mistral/mistral-large-latest` |
| Cohere | `cohere/command-r-plus` |

**Security controls (OWASP):**
- Model ID validated against allowlist regex — injection characters rejected (A03)
- API key validated for safe characters before any network call (A07)
- Key held in browser session memory only — never written to disk or git (A02/A04)

**When the wiki doesn't have an answer:**
```
No information found in the wiki for this query.
Add relevant source files to raw/ and run /sync-wiki to update the knowledge base.
```

**Verify the UI:**
1. Navigate to http://localhost:8501 — Settings screen appears
2. Type `INVALID MODEL` — validation error appears immediately
3. Enter valid credentials — Wiki Confirmation screen shows page count
4. Ask a question — response cites the source page filename

**Results summary (emitted by the skill):**
```
✅ Wiki UI launched — http://localhost:8501
📋 Entity pages: N   🔒 OWASP controls active
🖥️  Enter model ID + API key on the Settings screen to begin
```

---

### Reset (Start Over)

**Use when:** you want to wipe the wiki and start fresh.

| Tool | Command | Effect |
|------|---------|--------|
| Claude Code | `/reset-wiki` | Reports state only — no changes |
| Claude Code | `/reset-wiki reset` | ⚠️ Wipes all entity pages |
| GitHub Copilot | `Reset Wiki` | Reports state only — no changes |
| GitHub Copilot | `Reset Wiki reset` | ⚠️ Wipes all entity pages |

⚠️ **Irreversible** — all entity pages are permanently deleted. Commit or back up first.

**Verify the result:**
1. `ls wiki/*.md` — only `index.md` and `log.md` remain
2. `wiki/index.md` shows the "No entities yet" placeholder
3. `wiki/log.md` shows Total pages: 0

---

## Entity Pages Format

```markdown
# Concept Name

One-line definition.

## Summary

2-3 sentence overview of what this is and why it matters.

## Explanation

Detailed breakdown, components, examples, formulas if applicable.

## Related Concepts

- [[concept1]] - How it relates
- [[concept2]] - Connection or distinction

## Sources

- Author(s) - "Paper Title" (Year) - Section/page reference

## Contradictions

(Optional) Note if different sources define this differently

---
**Status**: New / Updated   **Last Updated**: YYYY-MM-DD
```

---

## Available Commands

### Claude Code
Type `/` in Claude Code CLI:

**Wiki skills** — build and maintain the knowledge base:

| Command | When to use | Results summary emitted |
|---------|-------------|------------------------|
| `/orchestrate-wiki` | Full pipeline refresh — compile or sync + audit + sync-docs in one command | Phase-by-phase report: sources, audit findings, doc surfaces updated |
| `/compile-papers` | Initial setup or batch processing | Sources processed, pages created, index/log updated |
| `/sync-wiki` | Adding new sources incrementally | Sources synced, pages created/updated, contradictions |
| `/audit-wiki` | Every ~20–30 pages | Findings by category, auto-fixes, manual review list |
| `/reset-wiki` | Inspect state or wipe and restart | State report or pages-removed count |
| `/launch-wiki-ui` | Query wiki via browser | UI URL, page count, OWASP security status |
| `/stop-wiki-ui` | Stop the running wiki UI | Confirmation the Streamlit process was killed |

**Repo maintenance skills** — keep the repo healthy:

| Command | When to use | Results summary emitted |
|---------|-------------|------------------------|
| `/sync-docs` | After any skill/command/structure change | Doc surfaces updated, manual review items |
| `/run-maintenance` | Before commits, monthly health check | Test results, skill registration, wiki health |
| `/regenerate-presentation` | After changing generator scripts, skills, or UI | Rebuilt assets (MP4 + PPTX), embedded media verified |

### GitHub Copilot
Type in Copilot Chat:

**Wiki skills:**

| Command | When to use | Results summary emitted |
|---------|-------------|------------------------|
| `Orchestrate Wiki` | Full pipeline refresh — compile or sync + audit + sync-docs in one command | Phase-by-phase report: sources, audit findings, doc surfaces updated |
| `Compile Papers to Wiki` | Initial setup or batch processing | Sources processed, pages created, index/log updated |
| `Sync Wiki from Raw` | Adding new sources incrementally | Sources synced, pages created/updated, contradictions |
| `Audit Wiki` | Every ~20–30 pages | Findings by category, auto-fixes, manual review list |
| `Reset Wiki` | Inspect state or wipe and restart | State report or pages-removed count |
| `Launch Wiki UI` | Query wiki via browser | UI URL, page count, OWASP security status |
| `Stop Wiki UI` | Stop the running wiki UI | Confirmation the Streamlit process was killed |

**Repo maintenance skills:**

| Command | When to use | Results summary emitted |
|---------|-------------|------------------------|
| `Sync Docs` | After any skill/command/structure change | Doc surfaces updated, manual review items |
| `Run Maintenance` | Before commits, monthly health check | Test results, skill registration, wiki health |
| `Regenerate Presentation` | After changing generator scripts, skills, or UI | Rebuilt assets (MP4 + PPTX), embedded media verified |

---

## Testing

```bash
python3 -m pytest         # run all 63 tests
python3 -m pytest -v      # verbose output
python3 -m pytest tests/test_wiki_query.py   # single file
```

| Test file | What it covers |
|-----------|---------------|
| `test_wiki_query.py` | Input validation (OWASP A03/A07), file loading, system prompt, API query mocking |

---

## Best Practices

**Commit after every operation:**
```bash
git add wiki/ && git commit -m "Compile wiki: <summary>"
git add wiki/ && git commit -m "Sync wiki: add <concept>"
git add wiki/ && git commit -m "Wiki audit: fix orphans, contradictions"
```

**Run Sync Docs after structural changes:**
```bash
# After adding a new skill or command:
# Claude Code:  /sync-docs
# Copilot:      Sync Docs
```

**Audit cadence:** every ~20–30 new pages or after a large sync batch.

---

## Repo Maintenance

### Sync Docs

Keeps `README.md` and `copilot-instructions.md` in sync after any change to skills, commands, or `wiki_query.py`.

| Tool | Command |
|------|---------|
| Claude Code | `/sync-docs` |
| GitHub Copilot | `Sync Docs` |

- Detects changed files via `git diff`
- Makes targeted edits only — never rewrites entire doc surfaces
- Never touches `wiki/` entity pages
- Emits a results summary listing every doc surface updated

Skill files: `.claude/commands/sync-docs.md` · `.github/prompts/sync-docs.prompt.md`

---

### Run Maintenance

Full repo health check — runs all tests, verifies every skill is registered, checks wiki health and git state, and saves a dated report.

| Tool | Command |
|------|---------|
| Claude Code | `/run-maintenance` |
| GitHub Copilot | `Run Maintenance` |

- Runs `pytest --tb=short -v` across the full test suite
- Verifies every skill has a Claude command file, Copilot prompt file, and a `copilot-instructions.md` entry
- Checks wiki health: entity page count, index/log population, unsynced `raw/` sources
- Saves `reports/maintenance-YYYY-MM-DD.md` with overall health status

Skill files: `.claude/commands/run-maintenance.md` · `.github/prompts/run-maintenance.prompt.md`

---

### Regenerate Presentation

Rebuilds demo videos and the PPTX deck when code, skills, or the wiki query UI has changed.

| Tool | Command |
|------|---------|
| Claude Code | `/regenerate-presentation` |
| GitHub Copilot | `Regenerate Presentation` |

**Arguments:** none (auto-detects via git) · `videos` · `deck` · `all`

- Detects which generator scripts or source files changed
- Rebuilds only what's stale — videos before deck (deck embeds them)
- Verifies both videos are embedded in `llm-wiki-deck.pptx`
- Prints manual steps for Keynote and Google Slides formats

**When to run:** after modifying `generate_presentation.py`, `generate_demo_videos.py`, `wiki_query.py`, or any skill/command file. Run `/sync-docs` afterwards.

Skill file: `skills/repo-maintenance/regenerate-presentation/SKILL.md`  
Rebuild checklist: `skills/repo-maintenance/regenerate-presentation/references/rebuild-checklist.md`

---

## Troubleshooting

**Q: I added a paper to `/raw` but nothing changed**  
A: Run `/sync-wiki` or `Sync Wiki from Raw` — the skill compares `raw/` against `wiki/log.md` to find unprocessed files.

**Q: The wiki query UI says "No information found"**  
A: The wiki either is empty or doesn't cover the topic. Add relevant source files to `raw/` and run `/sync-wiki`.

**Q: How do I fix a broken `[[bracket]]` link?**  
A: Run `/audit-wiki` — it finds all missing pages and either creates stubs or lists them for manual creation.

**Q: The UI rejected my model ID or API key**  
A: Model IDs must be lowercase alphanumeric + hyphens/dots/slashes only (e.g. `gpt-4o` or `gemini/gemini-1.5-pro`). API keys must contain only letters, digits, hyphens, underscores, and dots (min 8 characters). Check for typos or extra whitespace.

**Q: Tests fail after changes to wiki_query.py**  
A: Run `python3 -m pytest tests/test_wiki_query.py -v` to identify failures. If you change the validation regexes (`_MODEL_RE`, `_KEY_RE`), update the corresponding test cases.

**Q: Documentation is out of sync after I added a skill**  
A: Run `/sync-docs` or `Sync Docs` — it detects changed skill files and updates `README.md` and `copilot-instructions.md` automatically.

---

## Resources

**Skill assets & references:**
- Entity template: `skills/wiki-compilation/assets/entity-template.md`
- Format guide: `skills/wiki-compilation/references/wiki-format.md`
- Update checklist: `skills/wiki-sync/references/update-checklist.md`
- Audit checklist: `skills/wiki-audit/references/audit-checklist.md`
- Doc surface map: `skills/repo-maintenance/assets/doc-surface-map.md`

**Optional: Browser Integration**

Use **Obsidian Web Clipper** to save web articles directly:
1. Install the browser extension (see `extensions/README.md`)
2. Clip relevant articles while browsing
3. Run `Sync Wiki from Raw` to extract concepts from clipped content

---

## Presentation

The `presentation/` folder contains a professional 5-slide deck (16:9, dark theme) and two embedded demo videos.

### Output files

| File | Description |
|------|-------------|
| `llm-wiki-deck.pptx` | 5-slide deck with both demo videos embedded (click-to-play in PowerPoint) |
| `terminal-demo.mp4` | Claude Code CLI skills demo: compile-papers, sync-wiki, audit-wiki, Copilot Chat |
| `ui-demo.mp4` | Streamlit query UI demo: settings, happy-path query, empty-wiki error, not-found error |

### Formats

**PPTX — generated and ready:**
```bash
cd presentation
python generate_presentation.py --pptx
```

**Keynote** — launched in Keynote Creator Studio; use `File → Export To → Keynote` for the `.key` file.

> macOS Sequoia 15.x blocks programmatic PPTX import via AppleScript, so one manual step is required in Keynote.

```bash
python generate_presentation.py --keynote
# Opens Keynote with the deck — then in Keynote: File → Export To → Keynote
# Save as: presentation/llm-wiki-deck.key
```

**Google Slides** — upload via Drive API or import manually:

```bash
pip install google-api-python-client google-auth-oauthlib
# Place your OAuth 2.0 client secret at: ~/.llm-wiki-google-credentials.json
# (Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID)
# Enable: Google Drive API + Google Slides API
python generate_presentation.py --slides
```

Or manually: `slides.google.com → File → Import slides → Upload → select llm-wiki-deck.pptx`  
Google auto-converts the PPTX to Google Slides format.

### Regenerating after code changes

```bash
cd presentation
python generate_demo_videos.py     # rebuild terminal-demo.mp4 and ui-demo.mp4
python generate_presentation.py    # rebuild PPTX with videos re-embedded
```

---

## Next Steps

1. Add your first batch of papers to `raw/`
2. Run `Compile Papers to Wiki` (or `/compile-papers`) to initialize `wiki/`
3. Review created pages and familiarise yourself with the format
4. Add more papers as you find them, syncing with `Sync Wiki from Raw`
5. When wiki reaches ~20 pages, run `Audit Wiki` for quality checks
6. Use `streamlit run wiki_query.py` to query the knowledge base interactively
7. Commit progress regularly

---

*Inspired by [Andrej Karpathy's LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)*

---

**Created**: 2026-04-19 · **Commands**: 10 (orchestrate, compile, sync, audit, reset, launch-ui, stop-ui, sync-docs, run-maintenance, regenerate-presentation) · **Tests**: 63
