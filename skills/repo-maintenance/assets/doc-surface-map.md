# Doc Surface Map

For each documentation surface, this file lists the exact elements that `sync-docs` must check and potentially update.

---

## `README.md`

| Element | Location | What to check |
|---------|----------|----------------|
| Tool choice banner | `> **Choose your tool:**` block | Slash command names match `.claude/commands/*.md` |
| Commands table | `### Step 1/2/3` sections | Command names and descriptions current |
| Folder structure | `## Folder Structure` code block | New skill folders listed; removed ones removed |
| Three-Step Workflow | `## Three-Step Workflow` | Step commands match current command names |

---

## `docs/index.html`

| Element | Selector / Location | What to check |
|---------|---------------------|----------------|
| Stats bar — skill count | `.stat-val` (3rd stat) | Number equals count of `.claude/commands/*.md` files |
| Feature cards | `#features .feature-grid` | Features still accurate; new major features added |
| Tool cards | `#tools .tools-grid` | One `.tool-card` per skill; names, badges, descriptions match |
| Workflow steps | `#how-it-works .workflow` | Step commands match current command names |
| Getting started steps | `#get-started .steps-list` | `<code>` command references are current |

**Tool card template:**
```html
<div class="tool-card">
  <div class="tool-badge">badge-keyword</div>
  <h3>/command-name</h3>
  <div class="tool-cmd">Claude Code &amp; Copilot</div>
  <p>One-sentence description.</p>
</div>
```

---

## `copilot-instructions.md`

| Element | Section | What to check |
|---------|---------|----------------|
| Format support table | `## Supported Source Formats` | Formats match `compile-papers` and `sync-wiki` commands |
| Prompt entries | `## Available Prompts` | One `###` block per `.github/prompts/*.prompt.md`; descriptions current |
| Workflow decision tree | `## Recommended Workflow` code block | Skill names current |
| Situation table | `| Situation | Start with |` table | Commands current |
| Prompt-file mapping | `## Prompt Files` table | Each `.github/prompts/*.prompt.md` listed with its Claude equivalent |
| Resources | `## Resources` | Each skill folder and its assets/references listed |

---

## `README.md` → `## Presentation`

| Element | Section | What to check |
|---------|---------|----------------|
| Format instructions | `### PPTX`, `### Keynote`, `### Google Slides` | Script commands and manual steps current |
| Regenerating assets | `### Regenerating` | Script filenames and arguments match `generate_presentation.py` / `generate_demo_videos.py` |
| Output file names | Throughout section | `llm-wiki-deck.pptx`, `terminal-demo.mp4`, `ui-demo.mp4` match actual files in `presentation/` |

> Note: `presentation/README.md` was removed — the presentation section now lives in root `README.md`.

---

## `extensions/README.md`

| Element | Section | What to check |
|---------|---------|----------------|
| Browser list | `**Browsers**:` | Current supported browsers |
| Installation steps | `**Installation**:` | Steps still accurate |
| Clip template | `### Clip Template` | Template format still matches wiki entity format |
| Workflow steps | `### Workflow` | References correct skill names (`/Sync Wiki from Raw` etc.) |
| Other tools | `## Other Useful Tools` | Tools still relevant |
